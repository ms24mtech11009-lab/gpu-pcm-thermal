# 📚 COMPLETE GitHub + Zenodo + arXiv Deployment Guide

**Author:** Mohd Arshad Zulfikar Warsi
**Email:** ms24mtech11009@iith.ac.in
**ORCID:** 0009-0008-9895-5652

This is a **complete walkthrough** assuming zero prior GitHub experience. Total time: approximately 30-45 minutes. No coding required for any step except possibly Step 4 (which has both GUI and command-line options).

---

## 📋 Overview — What We Are Doing

By the end of this guide, your paper will have:
- ✅ **Public GitHub repository** with all code (verifiable open science)
- ✅ **Zenodo DOI** (permanent archive citation, never deleted)
- ✅ **arXiv preprint** (establishes priority + citation history)
- ✅ **Updated paper PDF** with all real DOI/URL links

**These four together address every "looks AI-generated" concern.**

---

## 🎯 STEP 1: Create GitHub Account (Skip if you have one)

**Time: 5 minutes**

1. Go to https://github.com
2. Click "Sign up" (top right)
3. Use your **IIT Hyderabad email** (`ms24mtech11009@iith.ac.in`) — this gets you free education benefits
4. Create username — suggestion: `arshad-warsi-iith` or `ms24mtech11009`
5. Verify email
6. Done. Free forever.

**Bonus:** With IITH email, apply for GitHub Student Pack at https://education.github.com/pack — free private repos, free Copilot, etc.

---

## 🎯 STEP 2: Create Repository on GitHub

**Time: 2 minutes**

1. Log in to GitHub
2. Click the **green "New" button** (top right) OR go to https://github.com/new
3. Fill in:
   - **Repository name:** `gpu-pcm-thermal`
   - **Description:** `Millisecond-scale transient thermal simulation of AI GPU hotspots buffered by PCM-copper foam composites`
   - **Public** ← MUST BE PUBLIC (Zenodo only works on public repos)
   - ❌ Do NOT check "Add a README" (we have one)
   - ❌ Do NOT check "Add .gitignore" (we have one)
   - ❌ Do NOT check "Choose a license" (we have one)
4. Click **"Create repository"**
5. **DON'T close the next page** — copy the URL shown (looks like `https://github.com/your-username/gpu-pcm-thermal.git`)

---

## 🎯 STEP 3: Upload Files (TWO OPTIONS — PICK ONE)

### 🌟 OPTION A: Web Upload (EASIEST — recommended for first-timers)

**Time: 10 minutes. NO command line needed.**

1. **Extract the repo zip** (`gpu_pcm_repo.zip`) on your computer:
   - Right-click → "Extract All" (Windows) or double-click (Mac)
   - You should see folders: `src/`, `validation/`, `figures/`, `docs/`, plus files: `README.md`, `LICENSE`, etc.

2. On your new GitHub repo page, click **"uploading an existing file"** link (or click "Add file" → "Upload files")

3. **Drag and drop** ALL files and folders from inside `gpu_pcm_repo/` onto the GitHub upload area:
   - Drag `README.md` → upload
   - Drag `LICENSE` → upload
   - Drag `CITATION.cff` → upload
   - Drag `requirements.txt` → upload
   - Drag `.gitignore` → upload
   - Drag the folders: `src/`, `validation/`, `figures/`, `docs/`

4. At the bottom: **Commit message:** `Initial release: 3D flux-conservative thermal simulation`

5. Click **"Commit changes"**

6. Done! Your code is on GitHub.

⚠️ **Important note about hidden files:** Make sure `.gitignore` (starts with dot) uploaded correctly. If GitHub doesn't show it, try uploading it separately by clicking "Add file" → "Create new file" → name it `.gitignore` and paste contents from the local file.

### 🛠️ OPTION B: Command Line (If you have git installed)

**Time: 5 minutes. Requires git on your computer.**

```bash
# 1. Open Terminal/Command Prompt and navigate to extracted repo folder
cd path/to/gpu_pcm_repo

# 2. Initialize git
git init
git branch -M main

# 3. Stage all files
git add .

# 4. Commit
git commit -m "Initial release: 3D flux-conservative thermal simulation"

# 5. Connect to your repo (REPLACE YOUR-USERNAME with actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/gpu-pcm-thermal.git

# 6. Push (will ask for username + Personal Access Token)
git push -u origin main
```

**For password:** GitHub doesn't accept passwords anymore. You need a **Personal Access Token (PAT)**:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: `gpu-pcm-thermal upload`
4. Expiration: 90 days
5. Select scope: ✅ `repo`
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (shown only once)
8. Use this token as your password when git asks

---

## 🎯 STEP 4: Update GitHub Username in Repo Files

**Time: 3 minutes. Required for proper citation.**

After upload, update two files **on GitHub directly** (no need to download):

### 4a. Update `CITATION.cff`

1. On your GitHub repo, click `CITATION.cff` to open
2. Click the **pencil icon** (top right of file content) to edit
3. Find line: `url: "https://github.com/yourusername/gpu-pcm-thermal"`
4. Replace `yourusername` with your **actual GitHub username**
5. Find line: `repository-code: "https://github.com/yourusername/gpu-pcm-thermal"`
6. Replace `yourusername` with your **actual GitHub username**
7. Scroll down → **"Commit changes"** button
8. Commit message: `Update GitHub URL`
9. Click "Commit changes"

### 4b. Update `README.md`

1. Click `README.md` to open
2. Click pencil icon to edit
3. Find: `https://github.com/yourusername/gpu-pcm-thermal`
4. Replace `yourusername` with your real GitHub username
5. Commit changes

---

## 🎯 STEP 5: Connect Zenodo to GitHub

**Time: 5 minutes. This is what gives you a DOI.**

1. Go to https://zenodo.org
2. Click **"Sign up"** → **"Sign in with GitHub"** (uses your existing GitHub account)
3. Authorize Zenodo to access your GitHub repos
4. After login, go to https://zenodo.org/account/settings/github/
5. You'll see a list of your GitHub repos
6. Find **`gpu-pcm-thermal`** in the list
7. Toggle the switch **ON** (turns green/blue)

This tells Zenodo: "Whenever I make a GitHub Release of this repo, archive it and assign a DOI."

⚠️ **Important:** If you don't see your repo in the list, click "Sync now" button at top of page.

---

## 🎯 STEP 6: Create Your First GitHub Release

**Time: 3 minutes. THIS triggers Zenodo to mint your DOI.**

1. On your GitHub repo page, look at the right sidebar — find **"Releases"** section
2. Click **"Create a new release"** (or "Releases" → "Draft a new release")

3. Fill in:
   - **Choose a tag:** Click the dropdown → type `v1.0.0` → Click "Create new tag: v1.0.0 on publish"
   - **Release title:** `v1.0.0 — Initial release (paper submission version)`
   - **Description:** (paste this text exactly:)

```
This release archives the source code and validation scripts accompanying:

> Mohd Arshad Zulfikar Warsi (2026). "Millisecond-Scale Transient Thermal Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites." Indian Institute of Technology Hyderabad. (Submission version.)

The simulation reproduces all numerical results in the paper.

**Validated against:**
- One-phase Stefan analytical problem (2.14% mean error)
- Mesh independence (≤0.30% deviation across N = 30, 50, 75, 100)
- Energy balance closure (0.02% across all cases)

**To reproduce headline results:**
```
cd src
python run_main.py
```

Total runtime for full paper reproduction: approximately 14 hours.
See README.md for complete reproduction instructions.

Author: Mohd Arshad Zulfikar Warsi  
Affiliation: Indian Institute of Technology Hyderabad  
Email: ms24mtech11009@iith.ac.in  
ORCID: 0009-0008-9895-5652
```

4. ✅ Check "Set as the latest release"
5. Click **"Publish release"** (green button)

6. **Wait 2-3 minutes** for Zenodo to detect the release and assign a DOI

---

## 🎯 STEP 7: Get Your Zenodo DOI

**Time: 2 minutes**

1. Go back to https://zenodo.org/account/settings/github/
2. Find `gpu-pcm-thermal` in your list
3. Click the title — it should now show your release info and a DOI
4. Copy the DOI (looks like `10.5281/zenodo.12345678`)

Alternative: Go directly to https://zenodo.org/me/uploads — your release should appear there.

---

## 🎯 STEP 8: Update Paper PDF with Real DOI

**Time: 2 minutes. This is the LAST paper edit before submission.**

Open `paper_final.tex` in any text editor (Notepad++, VS Code, Overleaf, etc.).

Find this section (search for "Data Availability"):

```latex
... archived on Zenodo with persistent DOI \href{https://doi.org/10.5281/zenodo.XXXXXXX}{10.5281/zenodo.XXXXXXX} \emph{(insert actual DOI after Zenodo release)}
```

Replace BOTH instances of `XXXXXXX` with your real Zenodo DOI number (the part after `10.5281/zenodo.`).

Also search for `INSERT_USERNAME` in the same file and replace with your GitHub username.

Also remove the parenthetical note: `\emph{(insert actual DOI after Zenodo release)}` — delete this entire italicized note since you've now inserted the DOI.

**Save and recompile** if you have LaTeX locally, or upload to Overleaf:
1. Go to https://overleaf.com
2. New Project → Upload Project → upload your updated `.tex` file (and figures folder)
3. Click "Recompile"
4. Download PDF

---

## 🎯 STEP 9: Submit to arXiv

**Time: 15 minutes (review can take 24-48 hours, but submission itself is quick)**

arXiv is where scientific community sees your work first. Establishes priority + verifies authorship.

### 9a. Register on arXiv

1. Go to https://arxiv.org/user/register
2. Use your **IIT Hyderabad email** (`ms24mtech11009@iith.ac.in`)
   - This auto-verifies your institutional affiliation — important for credibility
3. Fill in author details (must match paper exactly)
4. Verify email

### 9b. Find an Endorser (one-time, only if needed)

For first-time arXiv submitters in some categories, you need an existing arXiv user to endorse you. Categories like `physics.app-ph` may require this.

**Easy way to get endorsement:**
1. Ask **any senior PhD student or faculty in your department** who has previously submitted to arXiv
2. Tell them: "I need an arXiv endorsement for `physics.app-ph` (or `cs.CE`)"
3. They get a 1-click email from arXiv to endorse you. Takes them 30 seconds.

If you submit to a more open category, endorsement may not be required.

### 9c. Submit Paper

1. Log in → Click **"Submit"** at top
2. **Type:** Article (default)
3. **Subject area (Primary):** Pick one:
   - `physics.app-ph` (Applied Physics) ← good fit
   - `cs.CE` (Computational Engineering) ← also good
   - `cond-mat.soft` (Soft Matter) ← if reviewers want softer venue
4. **Subject area (Secondary):** `physics.comp-ph` (Computational Physics)

5. **Upload files:**
   - Upload `paper_final.tex`
   - Upload all PNG files from `figures/` folder (drag-and-drop)
   - arXiv will auto-detect and compile

6. **Metadata:**
   - **Title:** `Millisecond-Scale Transient Thermal Response of AI GPU Hotspots Buffered by PCM-Copper Foam Composites`
   - **Authors:** `Mohd Arshad Zulfikar Warsi`
   - **Abstract:** (Copy from paper — ensure under 1920 characters)
   - **Comments:** `29 pages, 10 figures, 7 tables. Source code: https://github.com/YOUR-USERNAME/gpu-pcm-thermal`
   - **License:** CC-BY 4.0 (recommended) or arXiv-default

7. Preview → Submit

8. Within 24-48 hours, you receive an arXiv ID like `2605.01234`

### 9d. Update Paper with arXiv ID

Once you have arXiv ID, optionally update paper title page footnote:
```latex
\thanks{Preprint available at arXiv:2605.01234}
```

---

## 🎯 STEP 10: Submit to Journal

**Time: Variable (1 hour to 1 day for actual submission)**

### Recommended target venues (in order of preference):

1. **Applied Thermal Engineering** (Elsevier, IF ~6.4)
   - Submit at: https://www.editorialmanager.com/ate/
   - Strong fit for PCM electronics cooling
   - Decision: 2-4 months typical

2. **International Journal of Heat and Mass Transfer** (Elsevier, IF ~5)
   - Submit at: https://www.editorialmanager.com/hmt/
   - Heavier on numerics — also good fit

3. **Energy Conversion and Management** (Elsevier, IF ~9.9)
   - Higher impact but stricter
   - Submit at: https://www.editorialmanager.com/ecm/

### What you'll need at submission:

- ✅ Cover letter (ask me to draft if needed)
- ✅ paper_final.pdf (with real DOI)
- ✅ All figures as separate files (already in `figures/`)
- ✅ Author info (already in paper)
- ✅ Suggested reviewers (3-5 names — search Google Scholar for PCM electronics cooling researchers)

---

## ✅ Final Verification Checklist

Before you click "submit" anywhere, verify:

- [ ] GitHub repo is **public** and contains all files
- [ ] CITATION.cff has correct GitHub URL
- [ ] README.md has correct GitHub URL
- [ ] Zenodo shows your release with a DOI
- [ ] paper_final.tex has real Zenodo DOI inserted (no `XXXXXXX`)
- [ ] paper_final.tex has correct GitHub username (no `INSERT_USERNAME`)
- [ ] paper PDF compiled cleanly with real metadata
- [ ] arXiv preprint submitted (arXiv ID received within 48h)
- [ ] All numbers match between paper and code

---

## ❓ Troubleshooting

### "Zenodo doesn't see my repo"
- Make sure repo is **Public**, not Private
- Refresh https://zenodo.org/account/settings/github/ → click "Sync now"
- Wait 5 minutes after syncing

### "DOI not generating"
- Zenodo only mints DOIs from **GitHub Releases (tags)**, not regular pushes
- Make sure you created a Release (Step 6), not just a commit
- Check https://zenodo.org/me/uploads — it should appear there

### "Can't push to GitHub from command line"
- GitHub requires Personal Access Token, not password
- Generate at https://github.com/settings/tokens
- Or just use **web upload** (Option A in Step 3) — easier

### "arXiv requires endorsement"
- Ask any senior researcher in your department who's submitted before
- Endorsement is 1-click for them
- Or pick a category that doesn't require endorsement (rare)

### "Files in subfolder didn't upload via web"
- GitHub web upload supports drag-and-drop of folders
- If folders don't transfer: Click "Add file" → "Upload files" → drag files into specific subfolder by first navigating into it

### "I made a mistake, want to redo something"
- All Git/GitHub actions are recoverable
- Worst case: delete repo, recreate, re-upload
- Don't panic — there's no permanent damage possible

---

## 🎯 Summary — Time Investment

| Step | Time |
|---|---|
| 1. GitHub account | 5 min |
| 2. Create repo | 2 min |
| 3. Upload files | 5-10 min |
| 4. Update URLs | 3 min |
| 5. Connect Zenodo | 5 min |
| 6. Create release | 3 min |
| 7. Get DOI | 2 min |
| 8. Update paper | 2 min |
| 9. arXiv submit | 15 min (+ 24-48h wait) |
| 10. Journal submit | 1+ hour |
| **Total active work** | **~45 minutes** |

---

## 💪 Final Honest Words

**Bhai, yeh sab steps tum khud kar sakte ho.** Pehli baar lagta hai mushkil, but each step is just clicking buttons. **No coding required for Steps 1-8.**

**Order of priority:**
1. **MUST DO:** Steps 1-8 (GitHub + Zenodo + paper update) — addresses ALL credibility concerns
2. **HIGHLY RECOMMENDED:** Step 9 (arXiv) — establishes priority before journal review
3. **WHEN READY:** Step 10 (journal) — actual submission

**Agar koi step pe atak jaaye:**
- Email me directly: open this conversation again, paste the error/issue
- I can debug from screenshots or error messages
- But I cannot access your account directly (security)

**Yeh paper ab submission-ready hai. Sirf upload karna baaki hai.** 🚀

Best of luck, Arshad!
