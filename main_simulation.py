"""
3D simulation module — FLUX-CONSERVATIVE VERSION
Resolves the 7-8% energy balance closure error from the post-update Robin BC.

Key change: top boundary cell treated as a control volume with its own
energy balance (incoming conduction flux from below minus outgoing convection
to sink), rather than overwriting after the time step.

This integrates the boundary into the conservation system rather than
imposing it as an external constraint.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import time as timer

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures_output")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# PROPERTIES (locked)
# ============================================================
k_Si, rho_Si, cp_Si = 130.0, 2329.0, 700.0
k_TIM, rho_TIM, cp_TIM = 8.5, 2500.0, 800.0
k_PCM, rho_PCM, cp_PCM = 0.2, 880.0, 2000.0
L_PCM = 214000.0; T_melt = 58.0; dT_melt = 6.0
k_Cu, rho_Cu, cp_Cu = 400.0, 8960.0, 385.0
epsilon = 0.97
rho_MM = epsilon*rho_PCM + (1-epsilon)*rho_Cu
cp_MM = epsilon*cp_PCM + (1-epsilon)*cp_Cu
L_MM = epsilon*L_PCM
k_MM = 10.0
h_top = 5000.0
T_sink = 40.0
T_init = 40.0

W, Ly = 28e-3, 28e-3
t_Si, t_TIM, t_PCM_layer = 0.5e-3, 0.08e-3, 2.0e-3
Nx, Ny = 50, 50
dx = W/(Nx-1); dy = Ly/(Ny-1)
x_arr = np.linspace(0, W, Nx); y_arr = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x_arr, y_arr, indexing='xy')


def build_grid(case):
    Nz_Si, Nz_TIM, Nz_PCM = 4, 2, 12
    z, lid = [], []
    z.extend(np.linspace(0, t_Si, Nz_Si+1)[:-1]); lid.extend([0]*Nz_Si)
    if case == '0':
        z.extend(np.linspace(t_Si, t_Si+t_TIM, Nz_TIM+1)); lid.extend([1]*(Nz_TIM+1))
    else:
        z.extend(np.linspace(t_Si, t_Si+t_TIM, Nz_TIM+1)[:-1]); lid.extend([1]*Nz_TIM)
        z.extend(np.linspace(t_Si+t_TIM, t_Si+t_TIM+t_PCM_layer, Nz_PCM+1)[1:])
        lid.extend([2]*Nz_PCM)
    z = np.array(z); lid = np.array(lid)
    return z, lid, np.diff(z), Nz_Si


def build_props(case, layer_id):
    Nz = len(layer_id)
    k_z = np.zeros(Nz); rho_z = np.zeros(Nz); cp_z = np.zeros(Nz); L_z = np.zeros(Nz)
    pcm_mask = np.zeros(Nz, dtype=bool)
    for i in range(Nz):
        lid = layer_id[i]
        if lid == 0: k_z[i], rho_z[i], cp_z[i] = k_Si, rho_Si, cp_Si
        elif lid == 1: k_z[i], rho_z[i], cp_z[i] = k_TIM, rho_TIM, cp_TIM
        elif lid == 2:
            if case == 'A':
                k_z[i], rho_z[i], cp_z[i] = k_PCM, rho_PCM, cp_PCM
                pcm_mask[i] = True; L_z[i] = L_PCM
            elif case == 'B':
                k_z[i], rho_z[i], cp_z[i] = k_MM, rho_MM, cp_MM
                pcm_mask[i] = True; L_z[i] = L_MM
    return k_z, rho_z, cp_z, pcm_mask, L_z


def spatial_pattern(center=(14e-3, 14e-3), sigma=3e-3):
    xc, yc = center
    return np.exp(-((X-xc)**2 + (Y-yc)**2)/(2*sigma**2))


def f_ai(t, T_per=10e-3, tau_r=0.5e-3, tau_d=5e-3):
    tl = t % T_per
    return (1.0 - np.exp(-tl/tau_r)) * np.exp(-tl/tau_d)


Q_peak_areal = 5.0e6; Q_base_areal = 1.0e6; t_active = 0.25e-3
Q_peak_vol = Q_peak_areal/t_active; Q_base_vol = Q_base_areal/t_active


def liquid_fraction(T, pcm_mask_z):
    T_low = T_melt - 0.5*dT_melt; T_high = T_melt + 0.5*dT_melt
    f = np.zeros_like(T)
    is_pcm = pcm_mask_z[:, None, None] & np.ones_like(T, dtype=bool)
    above = is_pcm & (T >= T_high); band = is_pcm & (T > T_low) & (T < T_high)
    f[above] = 1.0
    f[band] = (T[band] - T_low)/dT_melt
    return f


def c_effective(T, cp_z, pcm_mask_z, L_z):
    c = cp_z[:, None, None] * np.ones_like(T)
    in_band = (T >= T_melt - 0.5*dT_melt) & (T <= T_melt + 0.5*dT_melt)
    pcm3d = pcm_mask_z[:, None, None] & in_band
    L3d = L_z[:, None, None] * np.ones_like(T)
    c[pcm3d] += L3d[pcm3d]/dT_melt
    return c


def run_3D_FC(case, label, t_total=40e-3, save_field=False):
    """
    Flux-conservative 3D simulation.
    
    The key modification vs. the original sim_3d_all.py is in the TOP boundary
    treatment. Instead of overwriting T[-1] after the time-step update with
    the steady-state Robin form, we treat the top boundary cell as a control
    volume and compute its temperature update from the local energy balance:
    
        dE/dt|_top = (q_in_from_below) - (q_out_to_sink)
                  = -k_face*(T[-1] - T[-2])/dz_face - h*(T[-1] - T_sink)
    
    Then T_new[-1] = T[-1] + dt * dE/dt / (rho_top * c_eff_top * dz_cell_top)
    
    This integrates the boundary into the conservation system, eliminating
    the closure error from the post-update overwrite.
    """
    z_arr, layer_id, dz, Nz_Si = build_grid(case)
    Nz = len(z_arr)
    k_z, rho_z, cp_z, pcm_mask_z, L_z = build_props(case, layer_id)

    alpha_z = k_z / (rho_z * cp_z)
    dt_cfl_z = 0.5 * dz.min()**2 / alpha_z.max()
    alpha_max_xy = alpha_z.max()
    dt_cfl_xy = 0.5 / (alpha_max_xy * (1/dx**2 + 1/dy**2))
    dt = 0.3 * min(dt_cfl_z, dt_cfl_xy)
    n_steps = int(np.ceil(t_total/dt))

    # Cell sizes (for finite-volume)
    dz_cell = np.zeros(Nz)
    dz_cell[0] = dz[0]*0.5
    dz_cell[-1] = dz[-1]*0.5
    dz_cell[1:-1] = 0.5*(dz[:-1] + dz[1:])
    
    # XY cell area
    A_xy = dx*dy

    T = np.full((Nz, Ny, Nx), T_init, dtype=np.float64)
    spatial = spatial_pattern()
    active_iz = list(range(max(0, Nz_Si-2), Nz_Si))

    inv_dx2 = 1.0/dx**2; inv_dy2 = 1.0/dy**2
    
    # Face conductivities (harmonic mean for inter-layer faces)
    k_face = np.zeros(Nz - 1)
    for i in range(Nz - 1):
        if layer_id[i] == layer_id[i+1]:
            k_face[i] = 0.5*(k_z[i] + k_z[i+1])
        else:
            k_face[i] = 2*k_z[i]*k_z[i+1] / (k_z[i] + k_z[i+1])

    print(f"\n  [3D-FC] Case {case} — {label}, dt={dt*1e6:.2f}us, n_steps={n_steps}")

    t0 = timer.time()
    t = 0.0
    t_hist, Tpeak_hist, melt_hist = [], [], []
    Q_in_cumulative_hist = []
    Q_out_cumulative_hist = []
    Q_in_cum = 0.0
    Q_out_cum = 0.0
    snapshots = {}

    for n in range(n_steps + 1):
        f_t = f_ai(t)
        q_t = Q_base_vol + (Q_peak_vol - Q_base_vol)*f_t
        q_xy = q_t*spatial
        q_3d = np.zeros_like(T)
        for iz in active_iz:
            q_3d[iz] = q_xy

        c_eff = c_effective(T, cp_z, pcm_mask_z, L_z)

        # Z-direction conduction (interior + bottom)
        dT_dz = np.diff(T, axis=0)/dz[:, None, None]
        flux_z = k_face[:, None, None]*dT_dz  # heat flux at each face (upward positive)
        
        dqz = np.zeros_like(T)
        dz_avg = 0.5*(dz[:-1] + dz[1:])
        # Interior cells: standard divergence
        dqz[1:-1] = (flux_z[1:] - flux_z[:-1])/dz_avg[:, None, None]
        
        # Bottom cell: adiabatic (no flux from below)
        # dE/dt for bottom = +flux_z[0] (heat going UP, leaving cell)
        # Wait — sign convention: flux_z[i] = -k * dT/dz at face i (positive = heat flowing UP)
        # Actually: dT_dz = (T[i+1] - T[i])/dz, flux_z = k*dT_dz
        # If T[i+1] > T[i], dT_dz > 0, flux_z > 0 means heat flows from i+1 down to i
        # Wait, that's wrong — Fourier law: q = -k*dT/dz, so heat flows from hot to cold
        # If T[i+1] > T[i], q points DOWN (toward lower z), into cell i
        # So heat INTO cell i from face i = +k*(T[i+1]-T[i])/dz = +flux_z[i]
        # Heat OUT of cell i to face i-1 = +k*(T[i]-T[i-1])/dz = +flux_z[i-1]
        # Net: dE/cell_i = (flux_z[i] - flux_z[i-1])/dz_avg[i-1]
        # That's what dqz computes for interior cells
        
        # Bottom (i=0): no face below, so heat in = flux_z[0] only
        dqz[0] = flux_z[0, :, :] / dz_cell[0]
        
        # XY conduction (Laplacian, interior nodes only with adiabatic side BCs)
        L_xy = np.zeros_like(T)
        L_xy[:, 1:-1, 1:-1] = (
            (T[:, 1:-1, 2:] - 2*T[:, 1:-1, 1:-1] + T[:, 1:-1, :-2])*inv_dx2
            + (T[:, 2:, 1:-1] - 2*T[:, 1:-1, 1:-1] + T[:, :-2, 1:-1])*inv_dy2
        )
        lap_xy = k_z[:, None, None] * L_xy

        # === Standard interior update ===
        dTdt = (dqz + lap_xy + q_3d) / (rho_z[:, None, None] * c_eff)
        T_new = T + dt * dTdt

        # === FLUX-CONSERVATIVE TOP BOUNDARY ===
        # Top cell energy balance includes:
        #   (a) Heat in from below (z-conduction)
        #   (b) Heat out via Robin BC to sink
        #   (c) Lateral xy-conduction within the top layer (already in lap_xy)
        # The standard T_new[-1] from interior update has (c) but MISSING (a) and (b).
        # We add (a) + (b) and re-update.
        T_top = T[-1, :, :]
        T_below = T[-2, :, :]
        dz_face_top = dz[-1]
        dz_cell_top = dz_cell[-1]
        rho_top = rho_z[-1]
        c_eff_top = c_eff[-1, :, :]
        k_face_top = k_face[-1]
        
        # Heat flux into top cell from below (Fourier — heat from hot to cold)
        # Positive when T_below > T_top (heat flows up into top cell)
        q_in_from_below = k_face_top * (T_below - T_top) / dz_face_top
        
        # Heat flux out via Robin BC (positive when T_top > T_sink)
        q_out_to_sink = h_top * (T_top - T_sink)
        
        # Net rate of change for top cell (per unit volume)
        # Already included in T_new[-1]: lateral xy-conduction (lap_xy term)
        # Missing: z-flux balance from (a) and (b)
        # Add the missing z-flux contribution:
        dTdt_z_top = (q_in_from_below - q_out_to_sink) / (dz_cell_top * rho_top * c_eff_top)
        T_new[-1, :, :] = T_new[-1, :, :] + dt * dTdt_z_top
        
        # === Bottom: adiabatic (already handled via dqz[0]=flux_z[0]/dz_cell[0]) ===
        # Actually need to fix: bottom is adiabatic so no heat exits below
        # dqz[0] formula above gives just the flux from above (positive when -1 is colder, into cell 0)
        # This is actually correct: dE/cell_0 = -flux_z[0] (out the top, since flux_z[0] is downward into 0)
        # Wait no — I redo:
        # cell 0 has only ONE face (with cell 1, which is face 0)
        # flux_z[0] = k*(T[1]-T[0])/dz[0] — by our convention, when T[1]>T[0], flux_z[0]>0 = heat going DOWN from 1 to 0
        # So heat INTO cell 0 = flux_z[0] (when T[1]>T[0])
        # Per unit volume: dE/dt = flux_z[0] / dz_cell[0]
        # That's what dqz[0] computes — CORRECT.
        
        # === Side adiabatic BCs (mirror) ===
        T_new[:, 0, :] = T_new[:, 1, :]
        T_new[:, -1, :] = T_new[:, -2, :]
        T_new[:, :, 0] = T_new[:, :, 1]
        T_new[:, :, -1] = T_new[:, :, -2]

        # Cumulative heat tracking (do it ONCE per step)
        if n == 0:
            Q_in_cum = 0.0
            Q_out_cum = 0.0
        Q_in_step = 0.0
        for iz in active_iz:
            Q_in_step += np.sum(q_3d[iz, :, :]) * A_xy * dz_cell[iz]
        Q_in_cum += Q_in_step * dt
        Q_out_step = np.sum(h_top * (T[-1, :, :] - T_sink)) * A_xy
        Q_out_cum += Q_out_step * dt

        T = T_new
        t += dt

        if n % max(1, n_steps//200) == 0:
            t_hist.append(t)
            T_si_top = T[Nz_Si - 1, :, :]
            Tpeak_hist.append(T_si_top.max())
            f_liq = liquid_fraction(T, pcm_mask_z)
            if pcm_mask_z.any():
                pcm_volumes = []
                for iz in range(Nz):
                    if pcm_mask_z[iz]:
                        pcm_volumes.append(dz_cell[iz])
                if pcm_volumes:
                    melt_avg = np.average(
                        [f_liq[iz, :, :].mean() for iz in range(Nz) if pcm_mask_z[iz]],
                        weights=pcm_volumes
                    )
                else:
                    melt_avg = 0.0
            else:
                melt_avg = 0.0
            melt_hist.append(melt_avg)
            Q_in_cumulative_hist.append(Q_in_cum)
            Q_out_cumulative_hist.append(Q_out_cum)

        # Snapshots
        for ts_target_ms in [5, 10, 20, 40]:
            ts_target = ts_target_ms * 1e-3
            if abs(t - ts_target) < dt * 0.6 and ts_target_ms not in snapshots:
                snapshots[ts_target_ms] = T.copy()

    elapsed = timer.time() - t0
    print(f"  Done in {elapsed:.1f}s. Peak Si T at end = {Tpeak_hist[-1]-273.15+273.15:.2f}°C")
    
    # Final energy balance check
    # Energy stored = sum over all cells of rho*c_p*(T-T_init)*V + latent
    f_liq_final = liquid_fraction(T, pcm_mask_z)
    E_sensible_total = 0.0
    E_latent_total = 0.0
    for iz in range(Nz):
        V_iz = A_xy * dz_cell[iz] * Nx * Ny  # Total volume at this z
        # But we need cell-by-cell because T varies
        cell_sensible = rho_z[iz] * cp_z[iz] * (T[iz, :, :] - T_init) * A_xy * dz_cell[iz]
        E_sensible_total += np.sum(cell_sensible)
        if pcm_mask_z[iz]:
            cell_latent = rho_z[iz] * L_z[iz] * f_liq_final[iz, :, :] * A_xy * dz_cell[iz]
            E_latent_total += np.sum(cell_latent)
    
    E_stored_total = E_sensible_total + E_latent_total
    closure = (Q_in_cum - Q_out_cum - E_stored_total) / Q_in_cum * 100 if Q_in_cum > 0 else 0
    
    print(f"  Q_in: {Q_in_cum:.4f} J | Q_out: {Q_out_cum:.4f} J | E_stored: {E_stored_total:.4f} J")
    print(f"  Closure error: {closure:.2f}%")
    print(f"  Sensible: {E_sensible_total:.4f} J ({E_sensible_total/Q_in_cum*100:.1f}% of Q_in)")
    print(f"  Latent:   {E_latent_total:.4f} J ({E_latent_total/Q_in_cum*100:.1f}% of Q_in)")
    
    result = {
        'case': case, 'label': label,
        't_hist': np.array(t_hist),
        'Tpeak_hist': np.array(Tpeak_hist),
        'melt_hist': np.array(melt_hist),
        'snapshots': snapshots,
        'Q_in_cum': Q_in_cum,
        'Q_out_cum': Q_out_cum,
        'E_sensible': E_sensible_total,
        'E_latent': E_latent_total,
        'closure_pct': closure,
        'T_final': T,
        'Nz_Si': Nz_Si,
        'pcm_mask_z': pcm_mask_z,
        'dz_cell': dz_cell,
        'rho_z': rho_z, 'cp_z': cp_z, 'L_z': L_z,
    }
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("  FLUX-CONSERVATIVE 3D SIMULATION — Energy Balance Fix")
    print("=" * 70)
    
    results = {}
    for case, label in [('0', 'Baseline (no PCM)'),
                         ('A', 'Pure RT60 Paraffin'),
                         ('B', 'RT60 + Cu Foam Composite')]:
        results[case] = run_3D_FC(case, label, t_total=40e-3)
    
    print("\n" + "=" * 70)
    print("  SUMMARY — Closure Error Comparison")
    print("=" * 70)
    print(f"  {'Case':<5} {'Label':<25} {'Peak T (°C)':<12} {'Closure':<10}")
    print("-" * 60)
    for case in ['0', 'A', 'B']:
        r = results[case]
        peak_T = r['Tpeak_hist'][-1]
        print(f"  {case:<5} {r['label']:<25} {peak_T:<12.2f} {r['closure_pct']:<10.2f}%")
