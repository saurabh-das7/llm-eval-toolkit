# 04 — Tech Stack Decisions
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 4 of 8*
*Author: Saurabh Das | Last updated: April 2026*

---

## Purpose of This Document

Every technology choice in a product involves a trade-off. This document records what was evaluated, what was chosen, and — more importantly — why. It is not a list of tools. It is a set of decisions with reasoning.

The guiding constraints for all decisions in this project:

- **Solo build:** no engineering team, no DevOps support
- **Time budget:** MVP in 2 weeks, ~8 hours per week
- **Cost ceiling:** personal API spend capped at $10/month
- **Skill level:** Python with AI assistance; no prior Streamlit or deployment experience
- **Audience:** the app must run at a public URL — shareable with anyone, no local setup required

---

## Decision 1 — Frontend Framework

**The question:** What do I use to build the UI?

### Options evaluated

**Streamlit**
A Python-native framework for building data and ML apps. Renders UI components from Python script — no HTML, CSS, or JavaScript required. Widely used in the data science and AI community.

**Gradio**
Similar to Streamlit — Python-native, designed for ML demos. More opinionated about input/output layout (better suited to model inference demos than multi-tab apps).

**Flask + HTML**
Full control over UI. Requires writing HTML templates, CSS, and JavaScript separately from the Python backend. Significantly higher engineering overhead for a solo builder.

**v0 by Vercel (React)**
AI-generated React components. High-quality output but requires a JavaScript/TypeScript runtime, separate backend API, and deployment pipeline — significant overhead beyond the Python-only stack.

### Decision: Streamlit

| Factor | Rationale |
|--------|-----------|
| Python-only | No context switching between languages. One file runs the entire app. |
| Tab support | Streamlit's `st.tabs()` maps directly to the three-tab design (Compare / Evaluate / Batch) |
| Deployment | Streamlit Community Cloud deploys directly from GitHub — one-click, free tier, public URL |
| Community | Large ecosystem of examples for Anthropic API + Streamlit integrations |
| Speed | Estimated time to working UI: days, not weeks |

**Why not Gradio:** Gradio's interface model is built around single input-output pairs. The three-tab layout — especially the Compare tab with dual panels, source toggles, and linked dropdowns — requires more flexibility than Gradio's opinionated structure comfortably supports.

**Why not Flask or React:** Engineering overhead is disproportionate to project scope. Both require managing a separate frontend/backend split, which adds deployment complexity and debugging surface area — none of which adds product value for this MVP.

---

## Decision 2 — Evaluation Engine (LLM)

**The question:** Which LLM powers the evaluation, and how do I access it?

### Options evaluated

**Claude API (Anthropic) — claude-sonnet-4**
Pay-per-use API. Accessed via `anthropic` Python SDK. Requires a separate Anthropic Console account and API key — distinct from Claude Pro subscription.

**OpenAI API — GPT-4o / GPT-5**
Industry-standard. Requires credit card even for the small free credit. No persistent free tier for API access.

**Google Gemini API — Gemini 2.5 Flash-Lite (free tier)**
No credit card required. 1,000 requests/day free on Flash-Lite, 250/day on Flash. OpenAI-compatible API — minimal code change to integrate. Strong reasoning quality at this model tier for structured tasks.

**Local model (Ollama + open-source)**
Zero API cost. Runs on personal machine. Cannot be called from Streamlit Community Cloud (a remote server) without exposing the local server via ngrok — which produces an unreliable, non-persistent URL. Only viable if the app is also run locally, which eliminates the public demo URL entirely.

**Hardcoded rubric scoring (no LLM)**
Rule-based scoring using character counts, keyword matching, and regex. Fast and free but cannot reason about intent alignment or differentiation — the two most important dimensions.

**Claude API (Anthropic)**
Excellent quality and consistency. Requires separate paid API account — distinct from Claude Pro subscription. ~$3/M input tokens. Cannot be reused across future projects without ongoing cost.

### Decision: Google Gemini API — Gemini 2.5 Flash-Lite (free tier)

The core constraint is clear: keep API cost at ₹0 across all portfolio projects, consolidated under one free-tier account. This changes the decision from the original Claude API plan.

| Factor | Rationale |
|--------|-----------|
| Cost | Completely free — no credit card, no monthly charge, no per-token cost within free limits |
| Requests/day | 1,000 requests/day on Flash-Lite — sufficient for a portfolio demo tool |
| Consolidation | One Google account, one API key, reusable across all future projects in this portfolio |
| OpenAI-compatible API | Minimal code change — swap base URL and key, same request/response structure |
| Reasoning quality | Gemini 2.5 Flash-Lite handles structured rubric scoring well for this use case |
| No deployment conflict | Cloud-hosted API called from Streamlit Community Cloud — no local server issues |

**Why not local models (Ollama):** Streamlit Community Cloud cannot reach a local Ollama server running on a personal laptop. The only workarounds — ngrok tunnel or cloud-hosted Ollama — add infrastructure complexity and cost that eliminate the core benefit. Local LLM is useful for development testing only, not for the deployed public app.

**Why not Claude API:** Quality is excellent but requires a paid account separate from Claude Pro. At this project's scale the cost is minimal (~₹200/month) but the principle is to keep API spend at zero across the portfolio. Claude Pro subscription covers building and iterating; Gemini free tier covers the app's inference costs.

**Why not hardcoded scoring:** A rule-based evaluator cannot assess intent alignment or differentiation — the two dimensions that matter most and that require semantic reasoning.

**Acknowledged risk:** Google has tightened the free tier twice since 2024. If limits become too restrictive, the fallback is Gemini 2.5 Flash-Lite on the paid tier at $0.10/M input tokens — still among the cheapest options available and well under ₹100/month at this volume. This is documented in the risk register.

---

## Decision 3 — Deployment and Hosting

**The question:** Where does the app live so anyone can access it?

### Options evaluated

**Streamlit Community Cloud**
Free hosting for Streamlit apps deployed directly from a public GitHub repo. One-click deployment. Custom subdomain provided (e.g. `saurabh-das7-llm-eval.streamlit.app`). Secrets (API keys) managed via Streamlit's secrets manager — not exposed in code.

**Hugging Face Spaces**
Free hosting for ML demos. Supports Streamlit and Gradio apps. Slightly more configuration overhead than Streamlit Community Cloud for a pure Streamlit app.

**Railway / Render**
General-purpose app hosting. Free tiers available. More flexible than Streamlit Community Cloud but requires Dockerfile or build configuration — unnecessary overhead for a Streamlit app.

**Heroku**
Previously free tier discontinued. Paid plans start at $5/month — adds cost without meaningful benefit over Streamlit Community Cloud.

**Local only (ngrok tunnel)**
Temporary public URL via ngrok. Not persistent — URL changes on every restart. Not suitable as a shareable demo link.

### Decision: Streamlit Community Cloud

| Factor | Rationale |
|--------|-----------|
| Zero configuration | Connects directly to GitHub repo. Deployment is triggered by pushing to main branch. |
| Free tier | No cost for public apps. Fits within project constraints. |
| Secrets management | API key stored as a Streamlit secret — never committed to the repo |
| Persistence | App stays live at a fixed URL indefinitely (unlike ngrok) |
| GitHub integration | Every commit to main auto-deploys — clean continuous deployment workflow |

**API key safety:** The Google Gemini API key is stored in Streamlit's secrets manager, not in the codebase. The GitHub repo contains no credentials. The free tier's daily request cap (1,000 req/day) is enforced by Google's infrastructure — no additional spend controls needed since there is no billing attached.

---

## Decision 4 — Python Environment and Dependencies

**The question:** How do I manage the Python environment and dependencies?

### Key libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | Latest stable | UI framework |
| `google-generativeai` | Latest stable | Gemini API SDK |
| `python-dotenv` | Latest stable | Local environment variable management (API key in `.env` for local dev) |

### Environment approach

- **Local development:** Python 3.11 virtual environment (`venv`). API key stored in `.env` file, excluded from git via `.gitignore`.
- **Production:** Streamlit Community Cloud manages the runtime. Dependencies specified in `requirements.txt`. Secrets managed via Streamlit's secrets manager.
- **No Docker:** Unnecessary complexity for a single-file Streamlit app at this scale.

### requirements.txt (initial)

```
streamlit
google-generativeai
python-dotenv
```

Additional libraries will be added as needed during the build stage and documented in the build log.

---

## Decision 5 — Version Control and Code Workflow

**The question:** How is the code managed and what is the commit workflow?

### Decision: GitHub (existing repo)

The `llm-eval-toolkit` repo at `github.com/saurabh-das7/llm-eval-toolkit` already exists and contains all documentation. Application code will live in an `app/` subfolder.

**Branch strategy for a solo project:**
- All work on `main` branch directly — no feature branches for a solo MVP build
- Commits at logical checkpoints (end of each working session, after each working feature)
- Commit messages follow the pattern: `[stage] description` — e.g. `[build] add Compare tab with linked dropdowns`

**What goes in the repo:**
- All documentation (`docs/`)
- Application code (`app/`)
- `requirements.txt`
- `.gitignore` (excludes `.env`, `__pycache__`, `.streamlit/secrets.toml`)

**What never goes in the repo:**
- API keys
- Any `.env` file
- Any file containing credentials

---

## Decision 6 — Sample Data Storage

**The question:** How are the 18 sample ad copies stored and accessed in the app?

### Options evaluated

**Hardcoded Python dictionary in app code**
Sample data stored as a nested dictionary in `app/main.py` or a separate `data/samples.py` file.

**JSON file in repo**
Sample data stored in `data/samples.json`, loaded at app startup.

**Database (SQLite or external)**
Persistent storage for sample data. Significant overkill for 18 static records.

### Decision: Python dictionary in a separate data module

Stored in `app/samples.py` as a Python dictionary — imported by `main.py`. This keeps the main application file clean, makes the sample bank easy to read and extend, and requires no file I/O or database connections.

Structure mirrors `02b_sample_ad_copy_bank.md` exactly — same three products, same six keywords, same three variants per keyword. Adding a new sample means adding one entry to the dictionary.

---

## Stack Summary

| Layer | Choice | Reason |
|-------|--------|--------|
| UI framework | Streamlit | Python-native, tab support, one-click deployment |
| Evaluation engine | Google Gemini 2.5 Flash-Lite (free tier) | Zero cost, 1,000 req/day free, OpenAI-compatible API |
| Hosting | Streamlit Community Cloud | Free, persistent, GitHub-integrated |
| Language | Python 3.11 | Only language required across all layers |
| Environment | venv + requirements.txt | Simple, standard, no Docker overhead |
| Secrets | Streamlit secrets manager | API key never in codebase |
| Sample data | Python dictionary (samples.py) | Simple, readable, easily extensible |
| Version control | GitHub (existing repo) | Already set up, deploys to hosting automatically |

---

## What This Stack Does Not Include (and Why)

| Excluded | Why |
|----------|-----|
| Database | No persistent user data in v1 — stateless evaluations only |
| Authentication | Public tool, no user accounts in v1 |
| Analytics / logging | No usage tracking in v1 — added post-launch if needed |
| CI/CD pipeline | Streamlit Community Cloud auto-deploys on push — no pipeline needed |
| Testing framework | Unit tests added in a future iteration — not blocking MVP |
| Docker | Unnecessary for Streamlit Community Cloud deployment |

---

*Previous: [03 — UX Flow & Wireframe](./03_ux_flow_wireframe.md)*
*Next: [05 — Risk & Cost Plan](./05_risk_and_cost.md)*
