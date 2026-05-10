"""
Main runner — reproduces the principal headline numbers reported
in Tables 2 and 3 of the paper.

Runs the three principal cases (baseline, pure RT60, RT60+Cu foam composite)
at the baseline 50x50 grid for the full 40 ms simulation window, and
reports peak silicon-surface temperature, energy decomposition, and
energy-balance closure.

Expected runtime: approximately 50 seconds on a modern workstation
(Intel Core i7 / equivalent, 16 GB RAM).
"""

import os
import sys
import pickle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main_simulation as sim


def main():
    print("=" * 78)
    print("  Reproducing Tables 2 and 3 of the paper")
    print("  Flux-conservative 3D thermal simulation")
    print("=" * 78)

    cases = [('0', 'Baseline (no PCM)'),
              ('A', 'Pure RT60 Paraffin'),
              ('B', 'RT60 + Cu Foam Composite')]
    results = {}
    for case, label in cases:
        results[case] = sim.run_3D_FC(case, label, t_total=40e-3)

    # Headline temperatures (Table 2)
    T0 = results['0']['Tpeak_hist'].max()
    TA = results['A']['Tpeak_hist'].max()
    TB = results['B']['Tpeak_hist'].max()

    print("\n" + "=" * 78)
    print("  TABLE 2: Peak silicon temperatures")
    print("=" * 78)
    print(f"  {'Configuration':<32} {'Peak T (°C)':<14} {'ΔT vs base (°C)':<16}")
    print("-" * 78)
    print(f"  {'Case 0: Baseline (no PCM)':<32} {T0:<14.2f} {'---':<16}")
    print(f"  {'Case A: Pure RT60 Paraffin':<32} {TA:<14.2f} {-(T0-TA):<+16.2f}")
    print(f"  {'Case B: RT60 + Cu Foam':<32} {TB:<14.2f} {-(T0-TB):<+16.2f}")
    print(f"\n  Matrix benefit (composite vs pure PCM): {TA-TB:+.2f} °C")

    # Energy decomposition (Table 3)
    print("\n" + "=" * 78)
    print("  TABLE 3: Energy decomposition at t = 40 ms")
    print("=" * 78)
    print(f"  {'Quantity':<40} {'Pure RT60':<14} {'Composite':<14}")
    print("-" * 78)
    Q_in = results['A']['Q_in_cum']
    print(f"  {'Total Q_in (J)':<40} {Q_in:<14.4f} {Q_in:<14.4f}")
    for c in ['A', 'B']:
        pass
    print(f"  {'Sensible energy in PCM (J)':<40} {results['A']['E_sensible']:<14.4f} {results['B']['E_sensible']:<14.4f}")
    print(f"  {'Latent energy in PCM (J)':<40} {results['A']['E_latent']:<14.4f} {results['B']['E_latent']:<14.4f}")

    # Closure verification
    print("\n  Energy balance closure error (per case):")
    for c, label in cases:
        print(f"    {label:<32}: {results[c]['closure_pct']:.3f}%")

    # Save for figure generation
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_results.pkl')
    with open(out, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved: {out}")


if __name__ == "__main__":
    main()
