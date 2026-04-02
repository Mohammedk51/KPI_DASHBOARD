# KPI Dashboard (Streamlit + CI/CD)

A minimal Streamlit starter project for your semester dashboard with GitHub-based CI and Streamlit Cloud auto-deploy.

## 1) Run locally

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## 2) Git branching flow

Use this simple model:
- `develop`: client/developer pushes changes here first.
- `main`: production-ready branch only.

Recommended flow:
1. Push code to `develop`
2. GitHub Actions runs lint + tests
3. Create PR `develop` -> `main`
4. Merge only when CI is green
5. Streamlit Cloud auto-deploys from `main`

## 3) CI (GitHub Actions)

Workflow file: `.github/workflows/ci.yml`

It runs on push and PR for both `develop` and `main`, and executes:
- `flake8 .`
- `pytest -q`

## 4) CD (Streamlit Cloud)

Streamlit Community Cloud lets you choose the Python version from the deploy UI (Advanced settings).

1. Push this project to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select repo, branch `main`, file path `app.py`
5. Deploy

After that, every successful merge to `main` updates production automatically.

## 5) Will client push work later?

Yes. If your client pushes future code:
- CI checks run automatically on GitHub.
- On merge to `main`, Streamlit Cloud redeploys automatically.

So the same pipeline keeps working without manual deploy each time.
