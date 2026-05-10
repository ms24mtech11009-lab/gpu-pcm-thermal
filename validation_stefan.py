"""
ANALYTICAL VALIDATION: One-Phase Stefan Problem
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from scipy.optimize import brentq
import os
import time as timer

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures_output")
os.makedirs(OUTDIR, exist_ok=True)

# Properties
k_pcm = 0.21
rho_pcm = 800.0
cp_pcm = 2890.0
L_pcm = 173400.0
T_m_C = 55.0
T_m = T_m_C + 273.15
dT_m_band = 2.0  # narrow band

T_wall = T_m + 30.0
T_init = T_m - dT_m_band  # slightly below melt band so front is detectable

alpha = k_pcm / (rho_pcm * cp_pcm)
Ste = cp_pcm * (T_wall - T_m) / L_pcm

print(f"alpha = {alpha:.3e} m²/s, Ste = {Ste:.4f}")

# Lambda
def stefan_eq(lam):
    return lam * np.exp(lam**2) * erf(lam) - Ste/np.sqrt(np.pi)

lam = brentq(stefan_eq, 1e-6, 5.0)
print(f"lambda = {lam:.6f}")

s_analytical = lambda t: 2*lam*np.sqrt(alpha*t)

# Numerical setup
L_domain = 0.020
N = 400
dx = L_domain/(N-1)
x_arr = np.linspace(0, L_domain, N)

dt = 0.1 * dx**2 / (2 * alpha)
t_total = 600.0
n_steps = int(np.ceil(t_total/dt))
print(f"Grid: N={N}, dx={dx*1e6:.1f}um, dt={dt*1e3:.2f}ms, n_steps={n_steps:,}")

T = np.full(N, T_init)

def c_eff_fn(T):
    c = np.full_like(T, cp_pcm)
    in_band = (T >= T_m - 0.5*dT_m_band) & (T <= T_m + 0.5*dT_m_band)
    c[in_band] += L_pcm / dT_m_band
    return c

def liq_frac_fn(T):
    f = np.zeros_like(T)
    f[T >= T_m + 0.5*dT_m_band] = 1.0
    band_mask = (T > T_m - 0.5*dT_m_band) & (T < T_m + 0.5*dT_m_band)
    f[band_mask] = (T[band_mask] - (T_m - 0.5*dT_m_band)) / dT_m_band
    return f

t = 0.0
sample_times = [10, 60, 120, 300, 600]
sample_taken = {}
melt_front_hist = []
t_hist = []

t0 = timer.time()
print("Running...", end=" ", flush=True)
for n in range(n_steps + 1):
    c = c_eff_fn(T)
    dTdt = np.zeros(N)
    dTdt[1:-1] = (k_pcm / (rho_pcm * c[1:-1])) * (T[:-2] - 2*T[1:-1] + T[2:]) / dx**2
    T_new = T + dt * dTdt
    T_new[0] = T_wall
    T_new[-1] = T_init
    T = T_new
    t += dt
    
    if n % 50 == 0:
        f_liq = liq_frac_fn(T)
        below = np.where(f_liq < 0.5)[0]
        if len(below) > 0 and below[0] > 0:
            i = below[0]
            f_left = f_liq[i-1]
            f_right = f_liq[i]
            if f_left > f_right:
                frac = (f_left - 0.5) / (f_left - f_right)
                s_num = x_arr[i-1] + frac * dx
            else:
                s_num = x_arr[i]
            melt_front_hist.append(s_num)
            t_hist.append(t)
    
    for ts in sample_times:
        if ts not in sample_taken and t >= ts:
            sample_taken[ts] = T.copy()

elapsed = timer.time() - t0
print(f"done in {elapsed:.1f}s")

t_hist = np.array(t_hist)
melt_front_hist = np.array(melt_front_hist)
melt_front_ana = np.array([s_analytical(t) for t in t_hist])

mask = t_hist > 5
err_rel = 100 * np.abs(melt_front_hist[mask] - melt_front_ana[mask]) / melt_front_ana[mask]
mean_err = err_rel.mean()
max_err = err_rel.max()

print(f"\nMELT FRONT COMPARISON (t > 5s):")
print(f"  Mean relative error: {mean_err:.3f}%")
print(f"  Max relative error:  {max_err:.3f}%")
print(f"  At t=600s: num={melt_front_hist[-1]*1000:.4f}mm, ana={melt_front_ana[-1]*1000:.4f}mm")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

ax = axes[0]
ax.plot(t_hist, melt_front_ana*1000, '-', color='black', lw=2.5,
        label='Analytical Stefan solution')
ax.plot(t_hist, melt_front_hist*1000, 'o', color='tab:red', ms=4, alpha=0.7,
        label=f'FD simulation\n(mean err = {mean_err:.2f}%)')
ax.set_xlabel('Time (s)', fontsize=11)
ax.set_ylabel('Melt front position s(t) (mm)', fontsize=11)
ax.set_title(f'(a) Stefan melt front (Ste = {Ste:.3f})', fontsize=12)
ax.grid(alpha=0.3)
ax.legend(loc='lower right', fontsize=10)

ax = axes[1]
colors = ['tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:purple']
for i, ts in enumerate(sample_times):
    if ts in sample_taken:
        T_num = sample_taken[ts]
        s_t = s_analytical(ts)
        T_ana = np.zeros(N)
        for j in range(N):
            if x_arr[j] < s_t:
                eta = x_arr[j] / (2*np.sqrt(alpha * ts))
                T_ana[j] = T_wall + (T_m - T_wall)*erf(eta)/erf(lam)
            else:
                T_ana[j] = T_m
        ax.plot(x_arr*1000, T_num - 273.15, '-', color=colors[i], lw=2,
                label=f't={ts}s')
        ax.plot(x_arr*1000, T_ana - 273.15, '--', color=colors[i], lw=1.5, alpha=0.5)

ax.axhline(T_m_C, color='black', ls='-.', lw=1, alpha=0.5,
           label=f'T_m = {T_m_C}°C')
ax.set_xlabel('Position x (mm)', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('(b) T(x,t): solid=FD, dashed=analytical', fontsize=12)
ax.grid(alpha=0.3)
ax.legend(loc='upper right', fontsize=8, ncol=2)
ax.set_xlim(0, 12)
ax.set_ylim(T_m_C - 5, T_wall - 273.15 + 5)

plt.suptitle('Stefan Problem Analytical Validation (one-phase, paraffin properties)',
             fontsize=12.5, y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{OUTDIR}/validation_stefan.png", dpi=200, bbox_inches='tight')
plt.savefig(f"{OUTDIR}/validation_stefan.pdf", bbox_inches='tight')
print(f"\nSaved: {OUTDIR}/validation_stefan.png")

with open(f"{OUTDIR}/validation_stefan_data.txt", 'w') as f:
    f.write("STEFAN PROBLEM VALIDATION\n" + "="*60 + "\n\n")
    f.write(f"Ste = {Ste:.4f}, lambda = {lam:.6f}\n\n")
    f.write(f"{'t (s)':<8} {'s_num (mm)':<14} {'s_ana (mm)':<14} {'err (%)':<10}\n")
    for i in range(0, len(t_hist), max(1, len(t_hist)//20)):
        if t_hist[i] > 5:
            err = 100*abs(melt_front_hist[i] - melt_front_ana[i])/melt_front_ana[i]
            f.write(f"{t_hist[i]:<8.1f} {melt_front_hist[i]*1000:<14.4f} "
                    f"{melt_front_ana[i]*1000:<14.4f} {err:<10.4f}\n")
    f.write(f"\nMean rel error (t>5s): {mean_err:.3f}%\n")
    f.write(f"Max rel error: {max_err:.3f}%\n")

print(f"CONCLUSION: PCM melting validated to within {mean_err:.2f}% (mean error)")
