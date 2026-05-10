"""
SENSITIVITY ANALYSIS — Flux-Conservative Version
Same parameter sweeps as original, using fixed top boundary.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time as timer
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

# Import constants from flux-conservative module
from sim_3d_fluxcons import (
    k_Si, rho_Si, cp_Si, k_TIM, rho_TIM, cp_TIM,
    k_PCM, rho_PCM, cp_PCM, L_PCM, T_melt, dT_melt,
    k_Cu, rho_Cu, cp_Cu, epsilon, rho_MM, cp_MM, L_MM,
    h_top, T_sink, T_init,
    W, Ly, t_Si, t_TIM, t_PCM_layer,
    Nx, Ny, dx, dy, X, Y,
    build_grid, build_props, spatial_pattern,
    Q_peak_areal, Q_base_areal, t_active, Q_peak_vol, Q_base_vol,
    liquid_fraction, c_effective
)

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures_output")


def f_ai_custom(t, T_per, tau_r, tau_d):
    tl = t % T_per
    return (1.0 - np.exp(-tl/tau_r)) * np.exp(-tl/tau_d)


def run_sens_FC(case, label, params, t_total=40e-3, k_MM_override=None):
    """
    Flux-conservative sensitivity run.
    """
    z_arr, layer_id, dz, Nz_Si = build_grid(case)
    Nz = len(z_arr)
    k_z, rho_z, cp_z, pcm_mask_z, L_z = build_props(case, layer_id)
    
    # k_MM override
    if case == 'B' and k_MM_override is not None:
        for i in range(Nz):
            if pcm_mask_z[i]:
                k_z[i] = k_MM_override

    alpha_z = k_z / (rho_z * cp_z)
    dt_cfl_z = 0.5 * dz.min()**2 / alpha_z.max()
    alpha_max_xy = alpha_z.max()
    dt_cfl_xy = 0.5 / (alpha_max_xy * (1/dx**2 + 1/dy**2))
    dt = 0.3 * min(dt_cfl_z, dt_cfl_xy)
    n_steps = int(np.ceil(t_total/dt))

    dz_cell = np.zeros(Nz)
    dz_cell[0] = dz[0]*0.5
    dz_cell[-1] = dz[-1]*0.5
    dz_cell[1:-1] = 0.5*(dz[:-1] + dz[1:])

    T = np.full((Nz, Ny, Nx), T_init, dtype=np.float64)
    spatial = spatial_pattern()
    active_iz = list(range(max(0, Nz_Si-2), Nz_Si))

    inv_dx2 = 1.0/dx**2; inv_dy2 = 1.0/dy**2
    
    k_face = np.zeros(Nz - 1)
    for i in range(Nz - 1):
        if layer_id[i] == layer_id[i+1]:
            k_face[i] = 0.5*(k_z[i] + k_z[i+1])
        else:
            k_face[i] = 2*k_z[i]*k_z[i+1] / (k_z[i] + k_z[i+1])

    print(f"  [SENS-FC] {label} (params={params})", end=' ', flush=True)
    t0 = timer.time()
    t = 0.0
    Tpeak_max = 0.0

    for n in range(n_steps + 1):
        f_t = f_ai_custom(t, params['T_per'], params['tau_r'], params['tau_d'])
        q_t = Q_base_vol + (Q_peak_vol - Q_base_vol)*f_t
        q_xy = q_t*spatial
        q_3d = np.zeros_like(T)
        for iz in active_iz:
            q_3d[iz] = q_xy

        c_eff = c_effective(T, cp_z, pcm_mask_z, L_z)

        dT_dz = np.diff(T, axis=0)/dz[:, None, None]
        flux_z = k_face[:, None, None]*dT_dz
        dqz = np.zeros_like(T)
        dz_avg = 0.5*(dz[:-1] + dz[1:])
        dqz[1:-1] = (flux_z[1:] - flux_z[:-1])/dz_avg[:, None, None]
        dqz[0] = flux_z[0, :, :] / dz_cell[0]

        L_xy = np.zeros_like(T)
        L_xy[:, 1:-1, 1:-1] = (
            (T[:, 1:-1, 2:] - 2*T[:, 1:-1, 1:-1] + T[:, 1:-1, :-2])*inv_dx2
            + (T[:, 2:, 1:-1] - 2*T[:, 1:-1, 1:-1] + T[:, :-2, 1:-1])*inv_dy2
        )
        lap_xy = k_z[:, None, None] * L_xy

        dTdt = (dqz + lap_xy + q_3d) / (rho_z[:, None, None] * c_eff)
        T_new = T + dt * dTdt

        # Flux-conservative top BC
        T_top_v = T[-1, :, :]; T_below = T[-2, :, :]
        dz_face_top = dz[-1]; dz_cell_top = dz_cell[-1]
        rho_top = rho_z[-1]; c_eff_top = c_eff[-1, :, :]
        k_face_top = k_face[-1]
        q_in_from_below = k_face_top * (T_below - T_top_v) / dz_face_top
        q_out_to_sink = h_top * (T_top_v - T_sink)
        dTdt_z_top = (q_in_from_below - q_out_to_sink) / (dz_cell_top * rho_top * c_eff_top)
        T_new[-1, :, :] = T_new[-1, :, :] + dt * dTdt_z_top

        T_new[:, 0, :] = T_new[:, 1, :]
        T_new[:, -1, :] = T_new[:, -2, :]
        T_new[:, :, 0] = T_new[:, :, 1]
        T_new[:, :, -1] = T_new[:, :, -2]

        T = T_new
        t += dt

        T_si_top = T[Nz_Si - 1, :, :]
        Tp = T_si_top.max()
        if Tp > Tpeak_max:
            Tpeak_max = Tp

    elapsed = timer.time() - t0
    print(f"-> Peak T = {Tpeak_max:.2f}°C ({elapsed:.0f}s)")
    return Tpeak_max


if __name__ == "__main__":
    # Reference parameters
    params_ref = {'tau_r': 0.5e-3, 'tau_d': 5e-3, 'T_per': 10e-3}
    
    print("="*75)
    print("  SENSITIVITY ANALYSIS — Flux-Conservative")
    print("="*75)
    
    results = {}
    
    # Sweep tau_r
    print("\n--- τ_r sweep ---")
    tau_r_vals = [0.1e-3, 0.5e-3, 1.0e-3, 2.0e-3]
    Tpeaks_tau_r = []
    for tr in tau_r_vals:
        p = dict(params_ref); p['tau_r'] = tr
        T_peak = run_sens_FC('B', f'tau_r={tr*1000}ms', p)
        Tpeaks_tau_r.append(T_peak)
    results['tau_r'] = (tau_r_vals, Tpeaks_tau_r)
    
    # Sweep tau_d
    print("\n--- τ_d sweep ---")
    tau_d_vals = [2e-3, 5e-3, 10e-3, 20e-3]
    Tpeaks_tau_d = []
    for td in tau_d_vals:
        p = dict(params_ref); p['tau_d'] = td
        T_peak = run_sens_FC('B', f'tau_d={td*1000}ms', p)
        Tpeaks_tau_d.append(T_peak)
    results['tau_d'] = (tau_d_vals, Tpeaks_tau_d)
    
    # Sweep k_eff
    print("\n--- k_eff sweep ---")
    k_eff_vals = [5.0, 10.0, 15.0, 20.0]
    Tpeaks_k = []
    for k in k_eff_vals:
        T_peak = run_sens_FC('B', f'k_eff={k}', params_ref, k_MM_override=k)
        Tpeaks_k.append(T_peak)
    results['k_eff'] = (k_eff_vals, Tpeaks_k)
    
    # Save & summarize
    import pickle
    with open(f'{OUTDIR}/sensitivity_FC.pkl', 'wb') as f:
        pickle.dump(results, f)
    
    print("\n" + "="*75)
    print("  SENSITIVITY SUMMARY")
    print("="*75)
    
    print(f"\nτ_r (ms) -> Peak T (°C):")
    for tr, Tp in zip(tau_r_vals, Tpeaks_tau_r):
        print(f"  {tr*1000:.2f}  ->  {Tp:.2f}")
    
    print(f"\nτ_d (ms) -> Peak T (°C):")
    for td, Tp in zip(tau_d_vals, Tpeaks_tau_d):
        print(f"  {td*1000:.2f}  ->  {Tp:.2f}")
    
    print(f"\nk_eff (W/m·K) -> Peak T (°C):")
    for k, Tp in zip(k_eff_vals, Tpeaks_k):
        print(f"  {k:.1f}  ->  {Tp:.2f}")
