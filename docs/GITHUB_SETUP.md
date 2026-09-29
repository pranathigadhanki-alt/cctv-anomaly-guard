# GitHub setup (no Cursor as collaborator)

This repo is meant to live on **your** GitHub account. Commits should be authored by **you**, not an AI bot account.

## Create the empty repo

1. GitHub → **New repository** → name: `cctv-anomaly-guard`  
2. **Do not** add README (this project already has one)  
3. Create repository  

## Push from your machine

```bash
cd cctv-anomaly-guard
git remote add origin https://github.com/YOUR_USERNAME/cctv-anomaly-guard.git
git push -u origin main
```

Use **your** GitHub credentials or SSH key.

## Cursor / AI tools

- Using Cursor locally does **not** automatically add Cursor as a GitHub collaborator.  
- In GitHub → **Settings → Collaborators**, only invite real teammates.  
- If you want clean commit history without `Co-authored-by` trailers, commit from your terminal with your name/email:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

(Use `--global` only if you intend to set that for all repos on this machine.)

## Colab link after push

```text
https://colab.research.google.com/github/YOUR_USERNAME/cctv-anomaly-guard/blob/main/notebooks/01_environment_and_stream.ipynb
```

Update `docs/COLAB_SETUP.md` and `scripts/build_notebooks.py` clone URL if your username differs.
