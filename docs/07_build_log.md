# 07 — Build Log
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 7 of 8*
*Author: Saurabh Das | Last updated: May 2026*

---

## How to Use This Log

This is a running journal of the build — updated at the end of each working session. It is not a polished document. It is an honest record of what was built, what was harder than expected, what changed from the plan, and what was learned.

Entries are in reverse chronological order — most recent at the top.

---

## Entries

---

### Entry 07 — M6 Complete — App Live
**Date:** May 2026
**Milestone:** M6 — Deploy to Streamlit Community Cloud
**Hours this session:** ~1 hour

---

**What was accomplished:**

App deployed and publicly accessible.

**Live URL:** https://llm-eval-toolkit-uwvrvxbgvcgwmk9rpbpjun.streamlit.app/

- Streamlit Community Cloud account created via GitHub sign-in
- App connected to `saurabh-das7/llm-eval-toolkit`, branch `main`, entry point `app/main.py`
- Python version set to 3.12
- Gemini API key added to Streamlit secrets manager
- All three tabs confirmed working on public URL

**What was harder than expected:**

A git divergence caused the first deployment to show an older version. The Codespace and GitHub had different commit histories — editing files directly on GitHub browser during the docs phase created commits the Codespace didn't have. When new Codespace commits were added, git rejected the push. Resolved with `git push --force`. Lesson: once a Codespace is active, never edit files directly on GitHub browser.

**What changed from the plan:**

No deviations. Deployed exactly as specified in `04b_tech_stack_decisions_v2.md`.

**What's next:**

Update README with live URL. Complete `08_launch_and_retro.md`. Fill in WIP playbooks with real build experience.

---

### Entry 06 — M5 Complete — Polish and Pre-Launch
**Date:** May 2026
**Milestone:** M5 — Polish and pre-launch validation
**Hours this session:** ~3 hours

---

**What was accomplished:**

- Full UI overhaul: clean header with personal branding and links, subtle left-border section accents, two-section scorecard layout (dimensions → summary), color-coded score badges (green/amber/red)
- Tab order changed to Compare → Evaluate → Batch (most impressive flow first)
- Evaluate tab: dual mode buttons (Load sample / Enter manually) with active state; Enter manually clears all fields
- Batch summary upgraded to metric tiles: avg score, best ad, weakest ad, top failure dimension, strongest dimension
- Sample bank validation: found and fixed two Variant A descriptions exceeding 90-char limit (Nike: 95 chars, Trello: 99 chars)
- Rate limit error handling: 429 returns a distinct RATE_LIMIT verdict with user-friendly message
- 4-second delay between batch API calls to stay within 15 RPM free tier limit
- Hard cap of 10 ads enforced in batch evaluation loop

**What was harder than expected:**

UI styling in Streamlit is genuinely limited. CSS injected via `st.markdown()` works but fights Streamlit's opinionated defaults. The final result is clean and functional but not pixel-perfect. For a portfolio project this is acceptable; for a production product it would warrant a React frontend.

**What changed from the plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| gemini-2.5-flash-lite | Switched to gemini-3.1-flash-lite | Free tier cap is 20 RPD not 1,000 as documented — switched to model with 500 RPD |

---

### Entry 05 — M4 Complete — Batch Tab
**Date:** May 2026
**Milestone:** M4 — Batch tab
**Hours this session:** ~3 hours

---

**What was accomplished:**

- Batch tab with dynamic form rows — add up to 10, remove any except row 1
- "Load sample scenario" dropdown pre-fills product, keyword, and all rows in one action
- Session state architecture corrected — Streamlit widget `value=` parameter is ignored after first render when a `key=` is set; fixed by driving all inputs through session state keys
- .txt upload secondary option with pipe-separator format and sample download link
- Results table with all five dimension scores, overall score, and verdict per ad
- Batch summary: avg score, best performer, most common failure dimension

**What was harder than expected:**

Streamlit session state for pre-populated form rows was the hardest engineering problem of the whole build. The `value=` parameter on `st.text_input` is silently ignored after first render — only the `key=` value persists. Getting scenario pre-fill to work required abandoning `value=` entirely and using widget keys that change when the underlying data changes to force a re-render.

**What changed from the plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| .txt upload as primary bulk input | Dynamic form rows as primary | Eliminates format parsing errors for first-time users |

---

### Entry 04 — M3 Complete — Compare Tab
**Date:** May 2026
**Milestone:** M3 — Compare tab
**Hours this session:** ~3 hours

---

**What was accomplished:**

- Linked cascading dropdowns — changing product filters keyword options, changing keyword updates variant options and ad previews
- Source toggle (Use samples / Enter manually) — when manual, both panels switch to text inputs and panel toggles are hidden
- Panel-level toggle per panel in sample mode — allows benchmarking a known sample against user's own copy
- Ad preview cards in both panels, live on every selection or keystroke
- Two parallel Gemini API calls with 503 retry logic
- Side-by-side scorecards with head-to-head winner summary identifying which dimensions each panel won

**What was harder than expected:**

503 errors from Gemini on the second parallel API call — model high demand. Added retry logic with 2-second wait. This became the foundation for the more comprehensive rate limit handling in M5.

---

### Entry 03 — M2 Complete — Evaluate Tab
**Date:** May 2026
**Milestone:** M2 — Evaluate tab
**Hours this session:** ~3 hours

---

**What was accomplished:**

- Full Evaluate tab: product description, keyword, headline, description with live character counters
- "Load random sample" pre-fills all four fields from sample bank
- Ad preview card renders live as user types
- Inferred intent label displayed next to keyword field
- Scorecard output: five dimensions with progress bars and one-line reasoning, overall score, verdict, evaluator note
- Module import error fixed — relative imports required when Streamlit runs from `app/` directory
- Intent inference expanded — added "cheap", "weekend", "today", "now" to purchase signals after misclassification

**What was harder than expected:**

`ModuleNotFoundError: No module named 'app'` was the first real debugging challenge. Streamlit runs the script from the `app/` folder context so absolute imports (`from app.engine import`) fail. Fixed with `touch app/__init__.py` and relative imports.

**What changed from the plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| Intent inference signal list from PRD | Expanded purchase signals | "cheap flights to Goa this weekend" was misclassified as Consideration — "cheap" and "weekend" not in original list |

---

### Entry 02 — M0 + M1 Complete — Environment and Evaluation Engine
**Date:** May 2026
**Milestone:** M0 + M1
**Hours this session:** ~3 hours

---

**What was accomplished:**

**M0 — Environment:**
- GitHub Codespaces as browser-based IDE — no local machine required
- `google-genai` SDK installed (replaced deprecated `google-generativeai`)
- Gemini API key stored as GitHub Codespaces Secret — auto-injected into every session
- App folder structure created with `__init__.py`
- `.devcontainer/devcontainer.json` — auto-installs dependencies on Codespace start

**M1 — Evaluation engine:**
- `evaluate_ad_copy()` function complete in `app/engine.py`
- Intent inference, dynamic weight profiles, system prompt with rubric
- Overall score calculated in Python — model arithmetic was off by ~0.2
- Downgrade rule: any dimension scoring 1/5 caps verdict at NEEDS_REVISION
- Retry logic for 503 errors
- Validated against all three Nike variants — correct verdicts returned

**What was harder than expected:**

`google-generativeai` SDK deprecation was the first unexpected blocker. The new `google-genai` SDK has a different import structure — required rewriting the engine before a single evaluation could run.

**What changed from the plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| Local machine | GitHub Codespaces | Avoids work laptop IP risk; zero local setup |
| `google-generativeai` | `google-genai` | Old SDK deprecated |

---

### Entry 01 — Documentation Phase Complete
**Date:** April 2026
**Milestone:** Pre-build (all 8 docs)
**Hours this session:** ~20 hours across multiple sessions

---

**What was accomplished:**

All PM documentation completed before any application code was written.

| Doc | What it contains |
|-----|-----------------|
| `01_problem_statement.md` | Problem framing, user archetype, cost of the problem, why now |
| `02a_prd.md` | Three-tab spec, rubric, dynamic weights, success metrics |
| `02b_sample_ad_copy_bank.md` | 18 curated ad copies across 3 products × 2 keywords × 3 variants |
| `03_ux_flow_wireframe.md` | UX flows, wireframe, 8 screenshots |
| `04_tech_stack_decisions.md` | Six decisions with alternatives and rationale |
| `04b_tech_stack_decisions_v2.md` | Browser-based approach via GitHub Codespaces |
| `05_risk_and_cost.md` | 7 risks, ₹0 cost confirmed |
| `06_roadmap.md` | 6 milestones, critical path |

Seven playbook documents also created in `pm-tpm-playbooks/ai-learning/`.

**What was harder than expected:**

UX design took far longer than expected. The three-tab interface evolved through many iterations as real product decisions surfaced — source toggle, manual entry, batch pre-population, consistency of empty fields. Each decision had implications across the other tabs.

**What changed from the plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| Claude API | Gemini free tier | ₹0 API cost across all portfolio projects |
| 11 documentation stages | 8 stages | Merged overlapping docs |
| Audience + funnel stage as inputs | Target keyword only | Keyword naturally encodes intent |
| Single evaluation mode | Three tabs | Richer demo experience |

---

## Build Timeline Reference

| Milestone | Description | Status |
|-----------|-------------|--------|
| Docs | All 8 PM docs | ✅ Complete |
| M0 | Environment setup | ✅ Complete |
| M1 | Evaluation engine | ✅ Complete |
| M2 | Evaluate tab | ✅ Complete |
| M3 | Compare tab | ✅ Complete |
| M4 | Batch tab | ✅ Complete |
| M5 | Polish and pre-launch | ✅ Complete |
| M6 | Deploy | ✅ Complete |

**Live URL:** https://llm-eval-toolkit-uwvrvxbgvcgwmk9rpbpjun.streamlit.app/

---

*Previous: [06 — Roadmap](./06_roadmap.md)*
*Next: [08 — Launch & Retrospective](./08_launch_and_retro.md)*
