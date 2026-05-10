"""
Mesh Independence Study — Flux-Conservative Solver

Reproduces the grid-refinement table reported in Section 4.1 of the paper.
Tests in-plane resolution N×N for N = 30, 50, 75, 100 across all three
configurations (baseline, pure RT60, composite). Through-thickness
resolution held fixed at 18 vertical nodes.

Expected runtime: approximately 12-15 minutes on a modern workstation
(varies primarily with the 100x100 case).

Output: console table matching Table 1 of the paper, plus pickle file
for downstream plotting.
"""

import sys
import os
import pickle
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main_simulation as sim


def run_grid(Nx_test):
    """Reconfigure the simulation module for a given in-plane grid size."""
    sim.Nx = Nx_test
    sim.Ny = Nx_test
    sim.dx = sim.W / (Nx_test - 1)
    sim.dy = sim.Ly / (Nx_test - 1)
    sim.x_arr = np.linspace(0, sim.W, Nx_test)
    sim.y_arr = np.linspace(0, sim.Ly, Nx_test)
    sim.X, sim.Y = np.meshgrid(sim.x_arr, sim.y_arr, indexing='xy')

    print(f"\n=== Grid {Nx_test}x{Nx_test} ===")
    Tpeaks = {}
    for case, lbl in [('0', 'Baseline'),
                       ('A', 'Pure RT60'),
                       ('B', 'Composite')]:
        result = sim.run_3D_FC(case, lbl, t_total=40e-3)
        Tpeaks[case] = result['Tpeak_hist'].max()
    return Tpeaks


def main():
    grids = [30, 50, 75, 100]
    results = {}

    for N in grids:
        results[N] = run_grid(N)

    # Save results
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'mesh_results.pkl')
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)

    # Report table matching paper format
    print("\n" + "=" * 78)
    print("  MESH INDEPENDENCE — FLUX-CONSERVATIVE")
    print("=" * 78)
    print(f"  {'Grid':<14} {'Baseline (°C)':<18} {'Pure RT60 (°C)':<18} {'Composite (°C)':<16}")
    print("-" * 78)
    for N in grids:
        T = results[N]
        print(f"  {N}x{N:<11} {T['0']:<18.2f} {T['A']:<18.2f} {T['B']:<16.2f}")

    # Convergence check
    ref = results[100]
    print("\nDeviation of N=50 from N=100 reference:")
    for c in ['0', 'A', 'B']:
        diff = results[50][c] - ref[c]
        rel = 100 * diff / ref[c]
        print(f"  Case {c}: dT = {diff:+.2f} °C ({rel:+.3f}%)")

    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
