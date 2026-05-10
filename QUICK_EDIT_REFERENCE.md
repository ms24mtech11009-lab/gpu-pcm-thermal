# 🔧 QUICK REFERENCE — Exactly What You Need to Edit

This is a **cheat sheet** of every placeholder you need to replace. Open each file in any text editor (Notepad, VS Code, Overleaf, etc.) and find-and-replace.

---

## 🎯 BEFORE Pushing to GitHub — Edit These Files

### File 1: `README.md`

**Find:** `https://github.com/yourusername/gpu-pcm-thermal`
**Replace with:** `https://github.com/YOUR-ACTUAL-USERNAME/gpu-pcm-thermal`

**Find:** `https://github.com/INSERT_USERNAME/gpu-pcm-thermal`
**Replace with:** `https://github.com/YOUR-ACTUAL-USERNAME/gpu-pcm-thermal`

(There are 2 URL placeholders. Replace BOTH.)

---

### File 2: `CITATION.cff`

**Find (line 14):** `url: "https://github.com/yourusername/gpu-pcm-thermal"`
**Replace with:** `url: "https://github.com/YOUR-ACTUAL-USERNAME/gpu-pcm-thermal"`

**Find (line 15):** `repository-code: "https://github.com/yourusername/gpu-pcm-thermal"`
**Replace with:** `repository-code: "https://github.com/YOUR-ACTUAL-USERNAME/gpu-pcm-thermal"`

---

## 🎯 AFTER Getting Zenodo DOI — Edit These Files

### File 3: `paper_final.tex` (the LaTeX source)

**Find (around line 641):**
```latex
archived on Zenodo with persistent DOI \href{https://doi.org/10.5281/zenodo.XXXXXXX}{10.5281/zenodo.XXXXXXX} \emph{(insert actual DOI after Zenodo release)}
```

**Replace with:** (use your real Zenodo DOI number, e.g., 14123456)
```latex
archived on Zenodo with persistent DOI \href{https://doi.org/10.5281/zenodo.14123456}{10.5281/zenodo.14123456}
```

**Find:** `INSERT_USERNAME` (in the GitHub URL)
**Replace with:** Your actual GitHub username

(Note: also remove the italicized `\emph{(insert actual DOI after Zenodo release)}` text since DOI is now real.)

---

### File 4: `README.md` (UPDATE again with DOI)

**Find:** `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`
**Replace XXXXXXX with:** Your real Zenodo DOI number

**Find:** `archived on Zenodo with persistent DOI \`10.5281/zenodo.XXXXXXX\``
**Replace with:** Your real DOI

---

## 📝 ALREADY-DONE Items — DO NOT EDIT

These are already correct in the files I gave you:

- ✅ Author name: Mohd Arshad Zulfikar Warsi
- ✅ Affiliation: Indian Institute of Technology Hyderabad
- ✅ Email: ms24mtech11009@iith.ac.in
- ✅ ORCID: 0009-0008-9895-5652
- ✅ All paper numbers (115.92°C, 18.5°C, 15.4°C, 0.02% closure, etc.)
- ✅ All references and citations
- ✅ All figures and captions

**Don't change these unless you see a mistake.**

---

## 🔍 How to Find-and-Replace in Different Tools

### Notepad++ (Windows)
1. Open file
2. Ctrl+H (Replace dialog)
3. "Find what:" → paste the text to find
4. "Replace with:" → paste new text
5. Click "Replace All"

### VS Code (any OS)
1. Open file
2. Ctrl+H (Replace dialog)
3. Find what / Replace with
4. Click "Replace All"

### Overleaf (online LaTeX)
1. Upload paper_final.tex to Overleaf
2. Use Ctrl+F (find), type placeholder
3. Manually edit each one
4. Recompile when done

### Mac TextEdit
1. Open file (must be in plain text mode: Format → Make Plain Text)
2. Cmd+F → click "Replace"
3. Replace All

---

## ✅ Final Verification — Before You Submit Anywhere

Run through this checklist to make sure all placeholders are gone:

```
□ README.md has your real GitHub URL (no "yourusername", no "INSERT_USERNAME")
□ CITATION.cff has your real GitHub URL
□ paper_final.tex has real Zenodo DOI (no "XXXXXXX")
□ paper_final.tex has real GitHub URL (no "INSERT_USERNAME")
□ paper_final.pdf compiled without errors after these edits
□ All numbers in paper match what's in code (115.92°C, etc.)
□ ORCID 0009-0008-9895-5652 appears correctly in paper
□ Email ms24mtech11009@iith.ac.in appears correctly in paper
```

---

## 🚨 Common Mistakes to Avoid

1. **Forgetting to update README.md AGAIN after Zenodo DOI** — README has TWO placeholders for DOI (badge URL + text reference)

2. **Typos in GitHub username** — case-sensitive! Make sure URL EXACTLY matches your username

3. **Pushing to wrong branch** — make sure you're on `main` (default), not some other branch

4. **Submitting paper PDF before recompiling** — after editing `.tex`, you MUST recompile to update PDF

5. **Forgetting to recompile DOI badge** — README's DOI badge URL must point to your real Zenodo deposit

---

## 💡 Pro Tip: Use Search Multiple Files at Once

If you're using VS Code:
1. Open the entire `gpu_pcm_repo` folder
2. Press `Ctrl+Shift+H` (Find and Replace in Files)
3. "Search:" `XXXXXXX`
4. "Replace:" your real DOI number
5. Click "Replace All"

This catches all instances across all files at once.

---

## 📞 If Something Goes Wrong

**You can't break anything permanently.** GitHub keeps full version history. Worst case:
- Delete repo, recreate, re-upload — takes 10 minutes
- Or just create a new commit fixing the issue

**No file is sacred — edit freely. Git tracks everything.**

Best of luck, Arshad! 🚀
