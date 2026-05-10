# Millisecond-Scale Transient Thermal Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

This repository contains the complete simulation source code, validation scripts, and figure-generation tools for the paper:

> **Mohd Arshad Zulfikar Warsi.** *Millisecond-Scale Transient Thermal Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites.* Indian Institute of Technology Hyderabad. (2026).

## Overview

Sustained millisecond-scale heat spikes during large language model inference produce transient junction-temperature excursions in modern AI accelerator GPUs that conventional active cooling cannot follow on the timescale of the spike itself. This work develops a fully three-dimensional transient finite-difference model of an AI GPU thermal stack (silicon die, Arctic MX-4 thermal interface material, Rubitherm RT60 paraffin embedded in a copper foam matrix at porosity ε = 0.97, lumped Robin convective heat-sink boundary), driven by a Gaussian-localized bi-exponential heat-spike profile.

**Principal findings:**

- The PCM--copper foam composite reduces peak silicon-surface temperature by 18.5 °C relative to a no-PCM baseline; pure paraffin alone produces only a 3.1 °C reduction at this timescale.
- At millisecond timescales, the buffer functions principally as a **sensible-heat capacitor**, not a latent-heat absorber. Sensible-to-latent energy ratio in the composite is approximately 44:1; pure paraffin shows no measurable melting in the 40 ms window.
- The dominant performance lever is the effective thermal conductivity of the buffer, not the latent capacity — inverting the conventional design priority for second-to-minute applications.

## Reproducibility

All numerical results in the paper can be reproduced from this repository. The simulation uses an explicit three-dimensional finite-difference scheme with a flux-conservative Robin boundary condition; energy balance closes to within 0.02% across all reported cases.

### Requirements

- Python 3.10 or later
- NumPy ≥ 1.24
- Matplotlib ≥ 3.6
- SciPy ≥ 1.10 (for analytical Stefan validation only)

Install via:
```bash
pip install -r requirements.txt
```

### Quick reproduction

To reproduce the headline numbers (Tables 2 and 3 of the paper):
```bash
cd src
python run_main.py
```

Expected runtime: approximately 50 seconds on a modern workstation. Output should match the paper to within 0.05 °C on peak temperatures.

### Full reproduction of the paper

```bash
# 1. Main simulation results (Tables 2-3, Figures 4-7)
cd src && python run_main.py

# 2. Sensitivity sweeps (Table 4, Figure 8) — approximately 10 minutes
python sensitivity_analysis.py

# 3. Mesh independence (Table 1, Figure 3) — approximately 12-15 minutes
cd ../validation && python mesh_independence.py

# 4. Stefan analytical validation (Section 4.2, Figure 2)
python validation_stefan.py

# 5. Heat-source parameter consistency (Section 4.4, Figure 9)
python heat_source_validation.py

# 6. Kandasamy 2008 qualitative comparison (Section 4.3)
python validation_kandasamy.py
```

### Hardware used in the paper

All simulations in the paper were executed on a workstation with:
- Intel Core i7 processor
- 16 GB RAM
- Ubuntu Linux 22.04
- Python 3.12 with NumPy 1.26 and Matplotlib 3.8

Total wall-clock time for full study: approximately 14 hours (dominated by the 100x100 mesh-independence and the four-parameter sensitivity sweep).

## Repository structure

```
.
├── README.md                         This file
├── LICENSE                           MIT License
├── CITATION.cff                      Machine-readable citation metadata
├── requirements.txt                  Python dependencies
├── src/
│   ├── main_simulation.py            Core 3D FDM solver (flux-conservative)
│   ├── run_main.py                   Reproduces Tables 2-3 (50 s runtime)
│   └── sensitivity_analysis.py       Reproduces Table 4 (~10 min runtime)
├── validation/
│   ├── mesh_independence.py          Reproduces Table 1
│   ├── validation_stefan.py          Reproduces Figure 2 (Stefan analytical)
│   ├── validation_kandasamy.py       Reproduces Figure 10 (Kandasamy qualitative)
│   └── heat_source_validation.py     Reproduces Figure 9 (apples-to-apples flux)
├── figures/                          Pre-generated figures used in the paper
└── docs/                             Supplementary documentation
```

## Numerical method

The transient three-dimensional heat equation is solved using:

- Explicit Euler time integration
- Second-order centered finite differences for conduction in all three directions
- Harmonic-mean conductivity at material interfaces
- Effective heat capacity formulation for PCM phase change (Voller & Prakash, 1987)
- **Flux-conservative finite-volume Robin boundary condition** at the upper surface (energy balance closure: 0.02%)
- Adiabatic boundaries on all other surfaces
- CFL time step with safety factor 0.3

The flux-conservative Robin treatment is the principal numerical contribution of this code. The top boundary cell is incorporated into the conservation system as a control volume with explicit incoming-conduction and outgoing-convection energy balance, rather than imposed as an external constraint through post-update overwrite. This eliminates the residual closure error characteristic of post-update Robin implementations.

## Validation

Three independent validation layers:

1. **Mesh independence:** ≤0.30% deviation from 100×100 reference grid
2. **Stefan analytical problem:** 2.14% mean relative error in melt-front position over 600 s simulation
3. **Energy balance:** 0.02% closure error across all three cases (essentially machine precision)

Comparison with the experimental measurements of Kandasamy et al. (2008) reproduces the qualitative three-stage temperature evolution under transient heating; quantitative agreement is limited by the geometric simplification of the 1D replication.

## Key parameters

| Parameter | Value | Source |
|---|---|---|
| Domain | 28 × 28 × 2.58 mm³ | Approximate A100 die footprint |
| Hotspot Gaussian σ | 3 mm | SM cluster scale |
| Spike rise time τ_r | 0.5 ms | Power-management transient |
| Spike decay time τ_d | 5 ms | Kernel relaxation |
| Period T_per | 10 ms | LLM token cadence |
| Peak areal flux | 5×10⁶ W/m² | Worst-case prefill load |
| Heat sink h | 5000 W/m²·K | Forced-convection finned |
| Sink temperature | 40 °C | Data-center reference |
| Foam porosity | 0.97 | Xiao et al. (2013) |
| Composite k_eff | 10 W/m·K | Mid-range experimental |

## Citation

If you use this code in your research, please cite:

```bibtex
@article{warsi2026millisecond,
  author       = {Warsi, Mohd Arshad Zulfikar},
  title        = {Millisecond-Scale Transient Thermal Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites},
  year         = {2026},
  institution  = {Indian Institute of Technology Hyderabad},
  note         = {Preprint}
}
```

The exact code release used in the paper is archived on Zenodo with persistent DOI `10.5281/zenodo.XXXXXXX` (replace with actual DOI after Zenodo release).

## License

This software is released under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

**Author:** Mohd Arshad Zulfikar Warsi
**Affiliation:** Indian Institute of Technology Hyderabad, Sangareddy, Telangana 502285, India
**ORCID:** [0009-0008-9895-5652](https://orcid.org/0009-0008-9895-5652)
**Email:** [ms24mtech11009@iith.ac.in](mailto:ms24mtech11009@iith.ac.in)

For questions about the code or paper, please open an issue on GitHub or contact the author at the email above.

## Acknowledgments

Author gratefully acknowledges discussions with the IIT Hyderabad Department of Mechanical and Aerospace Engineering thermal sciences group during the development of this work.
