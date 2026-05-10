# 📦 REPOSITORY MANIFEST — Complete File Inventory

**Repository:** `gpu-pcm-thermal`
**Author:** Mohd Arshad Zulfikar Warsi (ms24mtech11009@iith.ac.in)
**ORCID:** 0009-0008-9895-5652
**Total files:** 19
**Total size:** ~4.5 MB

This document describes **every file** in the repository, what it does, and how it relates to the paper.

---

## 📂 Top-Level Files

### `README.md` (8.2 KB)
Public-facing documentation displayed automatically on GitHub repo homepage.
- Project description and headline findings
- Reproduction instructions
- Repository structure overview
- Hardware/software requirements
- Validation summary
- Citation information
- Contact details (your real ORCID + IITH email)

**On GitHub:** This is what visitors see first when they open your repo.

---

### `LICENSE` (1.1 KB)
MIT License — standard open-source license for academic code.
- Allows others to use, modify, distribute your code
- Requires attribution
- Industry-standard for scientific software

**Why MIT:** Most permissive while preserving authorship credit. Used by NumPy, SciPy, TensorFlow, etc.

---

### `CITATION.cff` (1.1 KB)
**Citation File Format** — machine-readable citation metadata.
- GitHub auto-detects this and shows "Cite this repository" button
- Allows tools like Zotero, Mendeley to import citation
- Contains your ORCID, name, affiliation, paper title

**Format:** YAML — human-readable, structured metadata.

---

### `requirements.txt` (40 bytes)
Python package dependencies for reproduction:
```
numpy>=1.24
matplotlib>=3.6
scipy>=1.10
```

**Usage:** Anyone reproducing your work runs `pip install -r requirements.txt` to get exact versions needed.

---

### `.gitignore` (260 bytes)
Tells Git which files to ignore:
- `__pycache__/` — Python compiled cache
- `*.pkl` — Generated data files
- `*.log` — LaTeX/Python logs
- `.DS_Store`, `Thumbs.db` — OS metadata

**Why important:** Keeps repo clean, avoids accidentally committing temp files.

---

## 📂 `src/` — Main Simulation Source Code

### `src/main_simulation.py` (14.5 KB) ⭐ CORE FILE
**The primary simulation solver.** Implements:
- 3D explicit finite-difference scheme
- Multilayer thermal stack (Si + TIM + PCM/composite)
- Bi-exponential heat-spike profile
- **Flux-conservative Robin boundary** (the key innovation that gave 0.02% energy balance)
- Effective heat capacity method for PCM phase change
- Composite homogenization for ε=0.97 paraffin/Cu foam

**Functions defined:**
- `build_grid(case)` — generates layered z-grid for each case
- `build_props(case, layer_id)` — assigns thermophysical properties per layer
- `spatial_pattern(center, sigma)` — Gaussian heat source spatial profile
- `f_ai(t, T_per, tau_r, tau_d)` — bi-exponential temporal spike
- `liquid_fraction(T, pcm_mask_z)` — liquid fraction for diagnostic
- `c_effective(T, cp_z, pcm_mask_z, L_z)` — effective heat capacity formulation
- `run_3D_FC(case, label, t_total)` — main simulation loop with FC top BC

**Cases supported:**
- `'0'` = Baseline (no PCM)
- `'A'` = Pure RT60 paraffin
- `'B'` = RT60 + Cu foam composite (ε=0.97)

---

### `src/run_main.py` (2.7 KB)
**Reproducer for paper Tables 2 and 3.** Runs all 3 cases and prints headline numbers.

**Output expected:**
```
Case 0: Baseline           115.92°C
Case A: Pure RT60          112.84°C  
Case B: Composite          97.42°C
Matrix benefit: +15.42°C
```

**Runtime:** ~50 seconds.

---

### `src/sensitivity_analysis.py` (6.1 KB)
**Reproducer for paper Table 4 (Sensitivity).** Sweeps:
- τ_r (rise time): 0.1, 0.5, 1.0, 2.0 ms
- τ_d (decay time): 2, 5, 10, 20 ms
- k_eff (composite conductivity): 5, 10, 15, 20 W/m·K

**Runtime:** ~10 minutes.

---

## 📂 `validation/` — Validation Scripts

### `validation/mesh_independence.py` (2.4 KB)
**Reproducer for paper Table 1 (Mesh Independence).** Tests grids:
- 30×30, 50×50 (baseline), 75×75, 100×100 (reference)

**Expected result:** ≤0.30% deviation between baseline and reference grid.
**Runtime:** ~12-15 minutes.

---

### `validation/validation_stefan.py` (5.9 KB) ⭐ KEY VALIDATION
**Reproducer for paper Figure 2 (Stefan Analytical Validation).** 

This is the **most important validation** — proves PCM phase-change implementation correctness against closed-form analytical solution.

**Setup:** One-phase Stefan problem
- Material: paraffin properties
- T_init = T_m, T_wall = T_m + 30 K
- Stefan number Ste = 0.5
- Lambda = 0.4648 (transcendental equation root)

**Expected:** 2.14% mean error in melt-front position over 600 s simulation.
**Runtime:** ~10 seconds.

---

### `validation/validation_kandasamy.py` (12.0 KB)
**Reproducer for paper Section 4.3 (Literature Comparison).** 

1D simplified replication of Kandasamy et al. (2008) HS1 + paraffin experiment at 4W input power.

**Expected:** Qualitative three-stage temperature evolution reproduces; quantitative error ~22°C due to 1D vs their 3D finned geometry.
**Runtime:** ~5 seconds.

---

### `validation/heat_source_validation.py` (10.0 KB)
**Reproducer for paper Figure 9 (Heat Source Apples-to-Apples).** 

Computes the relationship between pointwise peak flux and area-averaged values, comparing to published GPU/CPU hotspot measurements (Hamann 2007, Mahajan 2006, Sheaffer 2005).

**Expected:** Time-averaged within 3σ = 42 W/cm² matches Hamann/Mahajan range.
**Runtime:** <1 second.

---

## 📂 `figures/` — Pre-Generated Figures

All figures are PNG format at 200 DPI, embedded directly in the paper PDF.

### `figures/figure1_geometry.png` (391 KB)
**Schematic** of the 4-layer thermal stack: Si die / TIM / PCM-foam composite / Robin BC heat sink.

### `figures/figure1_geometry_user.png` (293 KB)
Alternative geometry schematic (used in paper).

### `figures/figure3_transient_response.png` (204 KB)
**Figure 4 in paper.** Peak Si T evolution + melt fraction over 40 ms for 3 cases.

### `figures/section_6_2_contours.png` (307 KB)
**Figure 6 in paper.** 2D temperature contours at 4 time snapshots × 3 cases (12 panels).

### `figures/figure7_3d_headline.png` (895 KB)
**Figure 7 in paper.** 3D mountain visualization at t=40 ms for all 3 cases.

### `figures/figure7_3d_surfaces.png` (1.2 MB)
Extended 3D surfaces (additional views, supplementary material).

### `figures/section_6_3_energy_split.png` (138 KB)
**Figure 8 in paper.** Energy decomposition (sensible vs latent) for buffered cases.

### `figures/sensitivity_analysis.png` (191 KB)
**Figure 9 in paper.** τ_r, τ_d, k_eff sensitivity sweeps.

### `figures/mesh_independence.png` (228 KB)
**Figure 3 in paper.** Grid convergence study.

### `figures/validation_stefan.png` (277 KB)
**Figure 2 in paper.** Stefan analytical validation comparison.

### `figures/validation_heat_source.png` (289 KB)
**Figure 5 in paper.** Apples-to-apples flux comparison.

---

## 📂 `docs/` — Deployment Documentation

### `docs/DEPLOYMENT.md` (6.4 KB)
Brief deployment guide (older, abbreviated version).

### `docs/COMPLETE_DEPLOYMENT_GUIDE.md` (11+ KB) ⭐ READ THIS
**Complete step-by-step walkthrough** for deploying repo to GitHub + Zenodo + arXiv. Assumes zero prior experience. Includes troubleshooting.

---

## 🔗 File Dependencies Diagram

```
README.md (entry point — anyone arriving at repo reads this first)
    │
    ├──→ src/main_simulation.py (core solver)
    │       │
    │       ├──→ src/run_main.py (uses main_simulation)
    │       └──→ src/sensitivity_analysis.py (uses main_simulation)
    │
    ├──→ validation/ (5 standalone validation scripts)
    │
    ├──→ figures/ (paper figures, regenerated by scripts)
    │
    └──→ docs/COMPLETE_DEPLOYMENT_GUIDE.md (publishing instructions)
```

---

## 🎯 Reproduction Order (for someone trying to reproduce paper)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Reproduce headline numbers (50 sec)
cd src && python run_main.py

# 3. Reproduce sensitivity analysis (~10 min)
python sensitivity_analysis.py

# 4. Reproduce mesh independence (~12-15 min)
cd ../validation && python mesh_independence.py

# 5. Run all validations (~5 min)
python validation_stefan.py
python validation_kandasamy.py  
python heat_source_validation.py
```

**Total reproduction time:** approximately 30 minutes.

---

## 📊 What Each File Proves to Reviewers

| File | Reviewer Concern Addressed |
|---|---|
| `LICENSE` | Open-source, reproducible science |
| `CITATION.cff` | Machine-readable provenance |
| `README.md` | Clear documentation, professional presentation |
| `requirements.txt` | Exact dependency versions |
| `src/main_simulation.py` | All numerical methods transparent |
| `validation/validation_stefan.py` | Analytical validation rigor |
| `validation/mesh_independence.py` | Grid convergence proven |
| `figures/*.png` | All figures regeneratable |

**Everything in this repo together = "this is real, reproducible research."**

---

## ⚠️ What This Repo Does NOT Contain (and why)

- ❌ Actual paper PDF (separate from code repo — at arXiv/journal)
- ❌ Personal data/credentials (security)
- ❌ Generated `.pkl` files (regenerated by running scripts; ignored by `.gitignore`)
- ❌ Python compiled cache (`__pycache__/`)

These are intentional — kept clean per Git best practices.

---

## 📝 Customization Notes

If you want to extend this work:

### Add experimental data
Create `experimental_data/` folder with:
- CSV files of any thermal measurements
- Photos of test setup
- Calibration data

### Add multi-hotspot scenarios
Modify `src/main_simulation.py`:
- `spatial_pattern()` function
- Add multiple Gaussian peaks at different (x₀, y₀) coordinates

### Run on GPU/HPC
The current code is CPU-only NumPy. For GPU:
- Replace `numpy` with `cupy` (drop-in for most ops)
- Or rewrite kernels in CUDA/Triton

---

**This manifest itself should be in the repo as `docs/MANIFEST.md` for reference.**
