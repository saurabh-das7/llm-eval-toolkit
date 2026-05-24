# 04 — Tech Stack Decisions v2 (Browser-Based)
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 4 of 8*
*Author: Saurabh Das | Last updated: April 2026*
*Status: v2.0 — browser-based development approach*
*See also: [04_tech_stack_decisions.md](./04_tech_stack_decisions.md) — original local development approach (fallback)*

---

## Purpose of This Document

This document re-evaluates the tech stack from the perspective of a single constraint: **the entire build must happen in a browser — no local machine setup required.**

Every other constraint from v1 remains unchanged:
- Solo build, ~8 hours/week
- ₹0 API and hosting cost
- Python + Streamlit stack (not React)
- Public URL as the end deliverable
- Gemini free tier as the evaluation engine

The decisions that did not change from v1 are noted briefly. Only decisions that changed have full re-evaluation sections.

---

## What Changed vs v1

| Decision | v1 (Local) | v2 (Browser) |
|----------|-----------|-------------|
| Development environment | Local machine, VS Code installed | GitHub Codespaces — browser VS Code |
| Code execution | Local Python runtime | Codespaces cloud container |
| AI coding assistant | None specified | GitHub Copilot (free tier in Codespaces) |
| Git workflow | Local git commands | Codespaces built-in source control |
| Everything else | Unchanged | Unchanged |

---

## Decision 1 — Development Environment

**The question:** Where is the code written and tested?

### Why a browser-based IDE

The original plan assumed a local machine with Python installed. Browser-based development eliminates:
- Python version management
- Virtual environment setup
- Package installation on a local machine
- Risk of work laptop being used accidentally

### Options evaluated

**GitHub Codespaces**
A cloud-hosted development environment that opens directly from a GitHub repo. Runs a full Linux container in the cloud — accessible via browser-based VS Code. Full terminal access, full Python runtime, full package installation. No local setup required.

**Replit**
A browser-based IDE with built-in AI coding agent. Has native Streamlit template support. Charges compute credits for AI agent usage — free tier gives $10/month in credits which can deplete quickly on complex tasks. Vendor lock-in risk: deployment configuration is Replit-specific, making migration harder.

**Google Cloud Shell**
Google's free browser-based terminal. 5GB persistent storage, pre-installed Python. No integrated VS Code editor — terminal only. Less ergonomic for a multi-file Streamlit project.

**GitHub browser editor (github.dev)**
The lightweight editor accessed by pressing `.` on any GitHub repo. Good for markdown and small edits. Cannot run code — no terminal, no Python runtime. Already using this for documentation. Not suitable for the build phase.

**Bolt.new / Lovable**
Browser-based AI app builders. Generate React/JavaScript apps — incompatible with the Python/Streamlit stack without a full rewrite. Evaluated and excluded. See the Python vs React explainer in the project context document.

### Decision: GitHub Codespaces

| Factor | Rationale |
|--------|-----------|
| Zero local setup | Opens directly from the GitHub repo — one click, full IDE in browser |
| Free tier | 60 core-hours/month free (2-core machine = 30 hours of active use). More than sufficient for ~8 hours/week. |
| Stack compatibility | Full Python runtime, full pip, full Streamlit support — identical to local development |
| Zero lock-in | Code lives in GitHub. Closing Codespaces changes nothing — same files, same repo. |
| GitHub integration | Built-in source control — commit and push without touching the terminal |
| Existing repo | Opens directly into `llm-eval-toolkit` — no import or migration needed |
| Copilot integration | GitHub Copilot available inside Codespaces on free tier |

**Why not Replit:** The $10/month compute credit model is opaque and can deplete unexpectedly. Replit's deployment is also Replit-specific — exporting to Streamlit Community Cloud requires extra steps. Codespaces produces identical output to local development with zero additional configuration.

**Why not Google Cloud Shell:** Terminal-only interface is less ergonomic for a multi-tab Streamlit project with several Python files. No integrated file browser or extension support.

---

## How to Open a Codespace

```
1. Go to github.com/saurabh-das7/llm-eval-toolkit
2. Click the green "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"
5. Wait ~60 seconds — browser VS Code opens with the full repo
6. Open the terminal: Ctrl+` (backtick)
7. Run: pip install streamlit google-generativeai python-dotenv
8. Add Gemini API key: export GOOGLE_API_KEY=your_key_here
9. Run: streamlit run app/main.py
10. Click "Open in Browser" when Streamlit port forwards
```

The app runs inside the Codespace container and is accessible via a forwarded URL — visible only to you while developing. When ready to share publicly, push to GitHub and Streamlit Community Cloud auto-deploys.

---

## Decision 2 — AI Coding Assistant Inside the IDE

**The question:** What AI help is available while writing code in Codespaces?

### Options evaluated

**GitHub Copilot (free tier)**
Inline code completion and chat inside VS Code. Available in Codespaces. Free tier introduced in 2024 — limited to 2,000 completions/month and 50 chat messages/month on the free plan. Sufficient for a solo build at 8 hours/week.

**This chat (Claude)**
The primary tool for planning, architecture decisions, debugging strategy, and code review. Not inline — requires switching to browser tab, pasting code, getting response, pasting back. Slightly more friction than inline Copilot but better for complex reasoning and longer code generation.

**Claude Code (work setup)**
Available at work but must not be used for this personal project. IP ownership risk — same reasoning as the work laptop decision. Do not use.

**Replit Agent**
Only available inside Replit. Not applicable in Codespaces.

### Decision: GitHub Copilot (inline) + This Chat (strategy and complex code)

Two-tool setup with clear separation of roles:

| Tool | Use for |
|------|---------|
| GitHub Copilot | Inline completion — boilerplate, repetitive patterns, standard library calls |
| This chat (Claude) | Architecture decisions, complex logic, debugging, full function/component generation, prompt engineering |

**Workflow in practice:**
1. Plan the next code task in this chat — get a clear explanation and approach
2. Write the code in Codespaces with Copilot helping with completion
3. Paste specific problems or full functions back here when stuck
4. This chat reviews, debugs, or rewrites as needed

**Copilot free tier limits:** 2,000 completions and 50 chat messages per month. At ~8 hours/week of coding, this is sufficient — most complex decisions come here rather than to Copilot.

---

## Decision 3 — Secrets Management in Codespaces

**The question:** Where does the Gemini API key live in a Codespaces environment?

**The problem with Codespaces:** Unlike a local machine where you have a persistent `.env` file, each Codespace can be rebuilt or stopped. Environment variables set in the terminal are not persistent across Codespace restarts.

### Options evaluated

**Codespaces Secrets (Recommended)**
GitHub allows storing secrets at the account or repo level that are automatically injected into any Codespace as environment variables. Set once in GitHub settings — available every time a Codespace opens.

**`.env` file in Codespace**
Works but must be recreated if the Codespace is deleted. Falls back to the fallback problem.

**Streamlit `secrets.toml` in Codespace**
Works for running Streamlit locally inside Codespaces. Same persistence issue as `.env`.

### Decision: GitHub Codespaces Secrets

```
Setup (one time only):
1. Go to github.com → Settings → Codespaces → Secrets
2. Click "New secret"
3. Name: GOOGLE_API_KEY
4. Value: your Gemini API key
5. Select repository: llm-eval-toolkit
6. Save
```

From that point, every Codespace opened from `llm-eval-toolkit` automatically has `GOOGLE_API_KEY` available as an environment variable. Access in code:

```python
import os
api_key = os.environ.get("GOOGLE_API_KEY")
```

Or via Streamlit secrets for production consistency:

```python
import streamlit as st
import os
api_key = st.secrets.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY"))
```

This pattern works in both Codespaces (environment variable) and Streamlit Community Cloud (Streamlit secrets) with no code change.

---

## Decision 4 — Evaluation Engine (Unchanged from v1)

**Decision: Google Gemini 2.5 Flash-Lite (free tier)**

No change from v1. Full rationale in `04_tech_stack_decisions.md`.

Key facts:
- 1,000 requests/day free, no credit card required
- OpenAI-compatible API
- `google-generativeai` Python SDK
- Paid fallback: $0.10/M input tokens (~₹88/month at current volume)

---

## Decision 5 — Hosting and Deployment (Unchanged from v1)

**Decision: Streamlit Community Cloud**

No change from v1. Full rationale in `04_tech_stack_decisions.md`.

The deployment workflow from Codespaces:
```
Write code in Codespaces
    → Commit via Codespaces built-in source control (or terminal: git add, git commit, git push)
    → Push reaches GitHub main branch
    → Streamlit Community Cloud auto-deploys within 2-3 minutes
    → Public URL updates automatically
```

No additional steps compared to local development.

---

## Decision 6 — Python Environment in Codespaces

**The question:** How are dependencies managed inside a Codespace?

Unlike local development where you create a virtual environment, Codespaces runs in an isolated container — there is no risk of package conflicts with other projects. You can install directly without a virtual environment.

```bash
# Install all dependencies
pip install streamlit google-generativeai python-dotenv

# Or install from requirements.txt
pip install -r requirements.txt
```

**Persistence note:** Pip installations persist within a Codespace session but may need to be reinstalled if the Codespace is rebuilt. Solution: always use `pip install -r requirements.txt` at the start of each session. This takes ~30 seconds and ensures a consistent environment.

**requirements.txt:**
```
streamlit
google-generativeai
python-dotenv
```

---

## Decision 7 — Git Workflow in Codespaces

**The question:** How does version control work without local git?

Codespaces includes full git support in three ways:

**Option A — VS Code source control panel (no terminal needed)**
- Click the branch icon in the left sidebar
- Stage files, write commit message, click commit
- Push with one click
- Simplest option — no commands needed

**Option B — Terminal git commands (standard)**
```bash
git add .
git commit -m "[milestone] description of what was built"
git push origin main
```

**Option C — GitHub.dev (for small edits only)**
Press `.` on any GitHub repo page to open the lightweight browser editor. Good for fixing a typo in a markdown file — not suitable for Python development.

**Decision:** Use VS Code source control panel as primary. Terminal git as fallback. Commit at the end of each session with a descriptive message following the pattern: `[M1] evaluation engine — Gemini API call returning structured JSON`.

---

## Stack Summary v2

| Layer | Choice | Notes |
|-------|--------|-------|
| Development environment | GitHub Codespaces | Browser VS Code, full Python, 60 hrs/month free |
| AI coding assistant | GitHub Copilot (inline) + Claude chat | Copilot for completion, Claude for architecture |
| Evaluation engine | Google Gemini 2.5 Flash-Lite (free tier) | Unchanged from v1 |
| Hosting | Streamlit Community Cloud | Unchanged from v1 |
| UI framework | Streamlit | Unchanged from v1 |
| Language | Python 3.11 | Unchanged from v1 |
| Secrets (dev) | GitHub Codespaces Secrets | Auto-injected into every Codespace |
| Secrets (prod) | Streamlit secrets manager | Unchanged from v1 |
| Sample data | Python dictionary in `app/samples.py` | Unchanged from v1 |
| Version control | GitHub (built-in to Codespaces) | Commit/push via VS Code panel or terminal |

---

## Cost Summary v2

| Item | Cost | Notes |
|------|------|-------|
| GitHub Codespaces | ₹0 | 60 core-hours/month free |
| GitHub Copilot | ₹0 | Free tier: 2,000 completions + 50 chat/month |
| Gemini API | ₹0 | Free tier: 1,000 req/day |
| Streamlit Community Cloud | ₹0 | Free for public apps |
| Claude Pro (this chat) | Already paying | Not a project cost |
| **Total monthly project cost** | **₹0** | |

---

## Fallback Plan

If Codespaces free tier hours run out before the project is complete:

1. **Wait for monthly reset** — hours reset on the 1st of each month
2. **Switch to local development** — follow `04_tech_stack_decisions.md` (v1). All code written in Codespaces works identically on a local machine. No migration needed — just clone the repo and run.
3. **Replit** — import the GitHub repo, configure Secrets, continue building. Compute credit model kicks in for AI agent usage but basic coding is free.

The fallback to v1 (local development) is the lowest-risk path — identical stack, identical output, no code changes required.

---

## Claude Code Prompts for Each Milestone

These are the prompts to use in this chat (not Claude Code at work) to generate code for each milestone. Paste the relevant prompt at the start of each build session along with the project context.

**M0 — Environment Verification**
```
I am setting up a GitHub Codespace for the LLM Eval Toolkit.
The project is a Streamlit app with Google Gemini API. Python 3.11.
Help me verify the environment is working:
1. What should I run to confirm Python version?
2. What should I install from pip?
3. How do I test the Gemini API key is working before writing the app?
Give me the exact terminal commands step by step.
```

**M1 — Evaluation Engine**
```
I am building a Gemini API evaluation function for search ad copy.
Stack: Python 3.11, google-generativeai SDK, Gemini 2.5 Flash-Lite.
The function takes: product_description, keyword, inferred_intent,
headline, description.
It returns a JSON scorecard with 5 dimensions (Relevance, Intent Alignment,
Differentiation, CTA Strength, Character Efficiency), each scored 1-5
with one-line reasoning, plus overall_score and verdict.
Dynamic weights apply based on inferred_intent (Purchase/Consideration/Awareness).
Verdict logic: 4.0+ = READY_TO_SERVE, 2.5-3.9 = NEEDS_REVISION,
below 2.5 = REJECT, insufficient input = NOT_EVALUABLE.
Downgrade rule: any dimension scoring 1/5 caps verdict at NEEDS_REVISION.
Write the complete evaluate_ad_copy() function with system prompt included.
```

**M2 — Evaluate Tab**
```
I am building the Evaluate tab for a Streamlit search ad copy evaluator.
The evaluate_ad_copy() function already exists in app/engine.py.
This tab needs:
- "Load random sample" button (samples in app/samples.py)
- Product description textarea
- Keyword text input with inferred intent label
- Headline input with live 30-char counter
- Description input with live 90-char counter
- Ad preview card (Sponsored / URL / Headline in blue / Description)
  that updates live as user types
- Evaluate button that calls evaluate_ad_copy()
- Loading spinner during API call
- Scorecard output with progress bars per dimension and verdict badge
Write the complete Streamlit code for this tab.
```

**M3 — Compare Tab**
```
I am building the Compare tab for a Streamlit search ad copy evaluator.
The evaluate_ad_copy() function exists in app/engine.py.
Samples are in app/samples.py as a nested dict:
DATA[product][keyword][variant] = {hl, desc}.
This tab needs:
- Source toggle: "Use samples" / "Enter manually"
- Use samples mode: Product dropdown → Keyword dropdown (cascading)
  → Panel A variant dropdown + Panel B variant dropdown
- Enter manually mode: product textarea + keyword input,
  both panels show headline/description inputs, panel toggles hidden
- Panel-level toggle (Use sample / Enter manually) per panel
  when source is "Use samples"
- Ad preview card in each panel, updates live
- Inferred intent label + weight profile displayed
- Compare button → two parallel scorecards + head-to-head winner
Write the complete Streamlit code for this tab.
```

**M4 — Batch Tab**
```
I am building the Batch tab for a Streamlit search ad copy evaluator.
The evaluate_ad_copy() function exists in app/engine.py.
Samples in app/samples.py.
This tab needs:
- "Load sample scenario" dropdown (Nike / Trello / MakeMyTrip)
  that pre-fills product, keyword, and all ad rows
- Product description textarea
- Keyword text input with inferred intent label
- Dynamic form rows: headline + description fields per row,
  add row up to 10, remove row (row 1 cannot be removed),
  live char counters per field
- .txt file upload secondary option (format: Headline | Description)
- Sample .txt download link
- Evaluate All button → progress indicator → results table
  (one row per ad, all 5 dimension scores, overall score, verdict)
- Summary row at bottom
Write the complete Streamlit code for this tab.
```

---

## What Has Not Changed From v1

The following decisions were made in v1 and remain unchanged. Refer to
`04_tech_stack_decisions.md` for the full rationale on each.

- Evaluation engine: Google Gemini 2.5 Flash-Lite free tier
- UI framework: Streamlit
- Hosting: Streamlit Community Cloud
- Language: Python 3.11
- Sample data storage: Python dictionary in `app/samples.py`
- API key in production: Streamlit secrets manager

---

*Previous: [03 — UX Flow & Wireframe](./03_ux_flow_wireframe.md)*
*Fallback: [04 — Tech Stack Decisions v1](./04_tech_stack_decisions.md)*
*Next: [05 — Risk & Cost Plan](./05_risk_and_cost.md)*
