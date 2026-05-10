# GitHub + Zenodo Deployment Guide

This file gives **step-by-step instructions** to publish this repository on GitHub and obtain a citable Zenodo DOI for the paper. Total time: approximately 30 minutes once you have GitHub and Zenodo accounts.

## Prerequisites

You need:
- A GitHub account (free at https://github.com)
- A Zenodo account linked to your GitHub (free at https://zenodo.org)
- An ORCID iD (free at https://orcid.org — register with your IIT Hyderabad email)
- Git installed locally

## Step 1: Create the GitHub repository

1. Log in to GitHub.
2. Click "New repository" (top-right green button).
3. Repository name: `gpu-pcm-thermal` (or your preferred name).
4. Description: "Millisecond-scale transient thermal modeling of AI GPU hotspots buffered by PCM-copper foam composites"
5. Make it **Public** (required for Zenodo integration).
6. Do **not** initialize with README/license/gitignore (we already have them).
7. Click "Create repository".

## Step 2: Push the code

Open a terminal in the directory containing this folder. Then run:

```bash
cd gpu_pcm_repo

# Initialize git (if not already)
git init
git branch -M main

# Stage all files
git add .

# Commit
git commit -m "Initial release: 3D flux-conservative thermal simulation"

# Connect to your GitHub repo (replace with YOUR username)
git remote add origin https://github.com/YOUR_USERNAME/gpu-pcm-thermal.git

# Push
git push -u origin main
```

If asked for credentials, use a GitHub Personal Access Token, not your password (GitHub no longer accepts passwords for git). Create one at https://github.com/settings/tokens — give it `repo` scope.

## Step 3: Update repository metadata (if needed)

The author's real metadata is already populated in the repository:
- ORCID: 0009-0008-9895-5652
- Email: ms24mtech11009@iith.ac.in

You only need to update the GitHub URL placeholders in `CITATION.cff` and `README.md` after creating your repo (Step 1):

### `CITATION.cff`
Replace `https://github.com/yourusername/...` with your actual repo URL.

### `README.md`
Replace `[your repo URL]` and `INSERT_USERNAME` placeholders with your GitHub username.

## Step 4: Connect Zenodo to GitHub

1. Go to https://zenodo.org/account/settings/github/
2. Sign in (use "Sign in with GitHub").
3. Authorize Zenodo to access your GitHub repos.
4. Find `gpu-pcm-thermal` in the repository list.
5. Toggle the switch to **ON**.

This tells Zenodo: every time you make a GitHub release, automatically archive it and assign a DOI.

## Step 5: Make a GitHub Release

This is what triggers Zenodo to mint a DOI.

1. On your GitHub repo page, click "Releases" (right sidebar).
2. Click "Create a new release".
3. Tag version: `v1.0.0`
4. Release title: `Initial release — paper submission version`
5. Description (paste this):

```
This release archives the source code accompanying:

> Mohd Arshad Zulfikar Warsi (2026). "Millisecond-Scale Transient Thermal
> Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites."
> Indian Institute of Technology Hyderabad. (Submission version.)

The simulation reproduces all numerical results in the paper. See README.md
for reproduction instructions.

Validated against:
- One-phase Stefan analytical problem (2.14% mean error)
- Mesh independence (≤0.30% deviation across N = 30, 50, 75, 100)
- Energy balance closure (0.02% across all cases)
```

6. Click "Publish release".

Within a few minutes, Zenodo will:
- Archive a snapshot of your repository
- Assign a permanent DOI
- Make it searchable in Zenodo

## Step 6: Get the DOI

1. Go to https://zenodo.org/account/settings/github/
2. Click on your repository.
3. The DOI badge will be visible — copy the DOI (looks like `10.5281/zenodo.XXXXXXX`).

## Step 7: Update the paper with the DOI

In `paper_final.tex`, find the "Data Availability" section and replace it with:

```latex
\section*{Data Availability}
The complete simulation source code, parameter files, and post-processing
scripts that support the findings of this study are openly available in a
public GitHub repository at \url{https://github.com/YOUR_USERNAME/gpu-pcm-thermal}
and archived on Zenodo with persistent DOI \href{https://doi.org/10.5281/zenodo.XXXXXXX}{10.5281/zenodo.XXXXXXX}.
```

In `README.md`, update the DOI badge URL with your real DOI.

## Step 8: Submit to arXiv (recommended before journal submission)

This establishes priority and verifies authorship publicly.

1. Go to https://arxiv.org/submit
2. Register if needed (use your IIT Hyderabad email — this auto-verifies institutional affiliation).
3. Subject area: "Computational Engineering, Finance, and Science (cs.CE)" or "Soft Condensed Matter (cond-mat.soft)" or "Applied Physics (physics.app-ph)" — any of these works for thermal engineering.
4. Upload `paper_final.tex` plus all PNG figures from the `figures/` folder.
5. Title, abstract, authors — copy from the paper.
6. Submit.

After arXiv processes the submission (typically 24-48 hours), you receive an arXiv ID like `2605.XXXXX`. Add this to the paper's title-page footnote or use as a citation.

## Verification checklist

After all steps, you should have:

- [ ] Public GitHub repo with all source code
- [ ] Real ORCID iD inserted in CITATION.cff and README.md
- [ ] Zenodo DOI for v1.0.0 release
- [ ] DOI inserted in paper_final.tex Data Availability section
- [ ] arXiv preprint with arXiv ID
- [ ] README.md badges showing DOI and license

This combination addresses all four credibility concerns:
1. **Code/data availability** → GitHub + Zenodo DOI
2. **Author verification** → ORCID + IIT Hyderabad email + arXiv
3. **Reproducibility** → README with step-by-step instructions, validated numbers
4. **Persistent archival** → Zenodo (institutional-grade, never deleted)

## Troubleshooting

**Zenodo not seeing my repo:** Make sure repo is Public (not Private). Refresh Zenodo's GitHub list.

**DOI not generating:** Zenodo only mints DOIs from GitHub Releases (tags), not regular pushes. Make sure you created a Release, not just a tag.

**Push rejected:** GitHub requires Personal Access Token instead of password. Create one at https://github.com/settings/tokens with `repo` scope.

**arXiv endorsement required:** First-time arXiv submitters in some categories need endorsement from an existing arXiv user. Ask any senior researcher in your department who has previously submitted to arXiv. Endorsement is one click for them.
