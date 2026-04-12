# 06 — Roadmap
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 6 of 8*
*Author: Saurabh Das | Last updated: April 2026*

---

## Constraints

- **Time budget:** ~8 hours/week, primarily evenings and weekends
- **Build window:** 4 weeks from environment setup to live URL
- **Solo build:** no pair programming, no code review, no DevOps support
- **Skill level:** Python with AI assistance; learning Streamlit and Gemini API during the build
- **Definition of done:** a public URL that works reliably, demonstrates all three tabs, and returns real evaluations powered by the Gemini API

---

## Milestone Plan

### Milestone 0 — Environment Setup
**Target: Week 1, Days 1–2 | ~2 hours**

The goal of this milestone is a working local development environment where the first line of application code can be written.

Deliverables:
- Python 3.11 installed and verified on personal machine
- Virtual environment created and activated
- `streamlit`, `google-generativeai`, `python-dotenv` installed
- Google AI Studio account created, API key generated
- `.env` file configured with API key, `.gitignore` confirmed
- GitHub repo `llm-eval-toolkit` cloned locally
- `app/` folder created with empty `main.py`
- `streamlit run app/main.py` returns a blank Streamlit page in the browser
- Setup steps documented in `07_build_log.md` (first entry)

**Done when:** `streamlit run app/main.py` opens in browser with no errors.

---

### Milestone 1 — Evaluation Engine
**Target: Week 1, Days 3–5 | ~3 hours**

The goal of this milestone is a working Gemini API call that returns a structured scorecard for a hardcoded test input.

Deliverables:
- System prompt written covering all five dimensions with scoring anchors
- API call to Gemini 2.5 Flash-Lite with hardcoded product description + keyword + ad copy
- Response parsed and printed as structured JSON
- All five dimension scores + reasoning + overall score + verdict returned correctly
- Evaluation tested against 3 sample bank entries (one per expected verdict)
- Results match expected verdicts for all three

**Done when:** Hardcoded evaluation returns the correct verdict for Variant A (Ready), B (Revision), and C (Reject) from the Nike sample set.

---

### Milestone 2 — Evaluate Tab (Single Ad)
**Target: Week 2, Days 1–3 | ~4 hours**

The goal of this milestone is a working, usable Evaluate tab — the simplest of the three flows and the best starting point.

Deliverables:
- Streamlit app with single tab (Evaluate)
- Input fields: product description, keyword, headline (with char counter), description (with char counter)
- "Load random sample" button pre-fills all fields from sample bank
- Ad preview card renders live as user types
- Inferred intent label displayed from keyword
- "Evaluate" button triggers Gemini API call
- Scorecard output renders: dimension scores with progress bars and reasoning, overall score, verdict badge, evaluator note
- Loading state shown while API call is in progress
- Error handling for empty inputs and API failures

**Done when:** A complete end-to-end evaluation runs — from blank fields, load sample, hit Evaluate, see scorecard — with no errors.

---

### Milestone 3 — Compare Tab (Side-by-Side)
**Target: Week 2, Days 4–5 + Week 3, Day 1 | ~5 hours**

The goal of this milestone is the Compare tab with both sample and manual modes working.

Deliverables:
- Tab structure added (Compare / Evaluate / Batch)
- Compare tab: source toggle (Use samples / Enter manually)
- Use samples mode: product dropdown → keyword dropdown (linked, cascading) → variant dropdowns per panel
- Manual mode: product description textarea + keyword input → both panels switch to headline/description inputs
- Panel-level toggle (Use sample / Enter manually) visible in sample source mode
- Ad preview cards in both panels, updating live on selection or typing
- Inferred intent label and weight profile badge displayed
- "Compare" button triggers two parallel Gemini API calls
- Side-by-side scorecard output with head-to-head winner summary
- Results hidden/reset when inputs change

**Done when:** Full Compare flow works in both sample mode and manual mode, producing two scorecards and a winner summary.

---

### Milestone 4 — Batch Tab
**Target: Week 3, Days 2–4 | ~4 hours**

The goal of this milestone is the Batch tab with dynamic form rows and results table.

Deliverables:
- Batch tab added
- "Load sample scenario" dropdown pre-fills product, keyword, and all ad copy rows
- Dynamic form rows: add row (up to 10), remove row, character counters per field
- .txt file upload option with format instructions and sample file download link
- "Evaluate All" button triggers sequential Gemini API calls for all rows
- Progress indicator shown while batch is evaluating
- Results table: one row per ad, all five dimension scores, overall score, verdict
- Summary row: best performer, most common failure dimension
- Error handling for malformed rows and API failures

**Done when:** Loading the Nike batch scenario, hitting Evaluate All, and receiving a correctly populated results table with all three variants scored.

---

### Milestone 5 — Polish and Pre-Launch
**Target: Week 3, Day 5 + Week 4, Days 1–2 | ~4 hours**

The goal of this milestone is an app that is reliable, readable, and ready to share with strangers.

Deliverables:
- App title and subtitle visible on all tabs
- Tab highlighting works correctly (active tab visually distinct)
- All edge cases from PRD Section 5.3 tested and handled gracefully
- All 18 sample bank entries validated — correct verdicts returned for all
- Consistency check: three sample ads re-evaluated 3 times each — no verdict variance
- Cold start behaviour documented in README
- `requirements.txt` finalised and verified
- `.gitignore` verified — no credentials in repo
- README updated with live demo URL placeholder
- Launch checklist (`08_launch_and_retro.md`) reviewed and all items confirmed

**Done when:** All items in the launch checklist are checked.

---

### Milestone 6 — Deploy to Streamlit Community Cloud
**Target: Week 4, Days 3–4 | ~2 hours**

The goal of this milestone is a live, public URL.

Deliverables:
- Streamlit Community Cloud account created (if not already)
- App connected to `llm-eval-toolkit` GitHub repo
- Gemini API key added to Streamlit secrets manager
- App deployed successfully — public URL confirmed working
- All three tabs tested on the live URL (not just local)
- README updated with live demo URL
- Live URL shared in `07_build_log.md` (final entry)

**Done when:** The public URL loads all three tabs and returns real Gemini API evaluations.

---

### Post-MVP Backlog (v2 candidates)

These features are explicitly deferred. They are listed here in priority order for reference, not as commitments.

| Feature | Why deferred | Priority for v2 |
|---------|-------------|----------------|
| CSV export of batch results | Useful but not core to the demo | High |
| Side-by-side view of a sample vs user's own copy (mixed mode) | Requires UX refinement | High |
| Consistency score shown to user | Requires multiple API calls per evaluation | Medium |
| Additional sample products (beyond Nike, Trello, MMT) | Content work, not engineering | Medium |
| Custom rubric builder | Significant scope increase | Low |
| Brand voice learning | Requires persistent memory | Low |
| Platform API integration (Google Ads, Bing) | Enterprise feature | Post-portfolio |

---

## Timeline Summary

| Milestone | Focus | Hours | Target |
|-----------|-------|-------|--------|
| M0 — Environment setup | Setup | 2h | Week 1, Days 1–2 |
| M1 — Evaluation engine | Core API | 3h | Week 1, Days 3–5 |
| M2 — Evaluate tab | First working tab | 4h | Week 2, Days 1–3 |
| M3 — Compare tab | Main tab | 5h | Week 2–3 |
| M4 — Batch tab | Third tab | 4h | Week 3, Days 2–4 |
| M5 — Polish + pre-launch | Quality | 4h | Week 3–4 |
| M6 — Deploy | Live URL | 2h | Week 4, Days 3–4 |
| **Total** | | **24h** | **4 weeks** |

At 8 hours/week this is a tight but achievable 3–4 week build. The milestone order is deliberate — each milestone produces something testable before moving to the next. If a milestone runs over, the next one absorbs the delay without blocking the critical path.

---

## The Critical Path

The one dependency chain that determines when the project launches:

```
M0 (env setup) → M1 (eval engine) → M2 (Evaluate tab) → M6 (deploy)
```

M3 (Compare) and M4 (Batch) are on a parallel path — they are additive to M2, not prerequisites for deployment. If time is short, a working Evaluate tab is the minimum deployable product. The other two tabs enhance the demo but are not required for a shareable URL.

---

*Previous: [05 — Risk & Cost Plan](./05_risk_and_cost.md)*
*Next: [07 — Build Log](./07_build_log.md)*
