# 07 — Build Log
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 7 of 8*
*Author: Saurabh Das | Last updated: April 2026*

---

## How to Use This Log

This is a running journal of the build — updated at the end of each working session or week. It is not a polished document. It is an honest record of what was built, what was harder than expected, what changed from the plan, and what was learned.

The format per entry is deliberately lightweight:
- **What was accomplished** — concrete outputs, not activities
- **What was harder than expected** — honest difficulty, not performance
- **What changed from the plan** — decisions that deviated from PRD or roadmap, with reasons
- **What's next** — the immediate next step, not a full plan

Entries are added in reverse chronological order — most recent at the top.

---

## Entries

---

### Entry 01 — Planning and Documentation Phase Complete
**Date:** April 2026
**Milestone:** Pre-build (Stages 1–6 complete)
**Hours this session:** ~20 hours across multiple sessions

---

**What was accomplished:**

The entire PM documentation phase is complete before a single line of application code has been written. This is intentional — the docs are the portfolio signal, not just scaffolding for the build.

Documents completed:

| Doc | What it contains |
|-----|-----------------|
| `01_problem_statement.md` | Problem framing, user archetype, cost of the problem, why now |
| `02a_prd.md` | Three-tab product spec, evaluation rubric, dynamic weights, success metrics |
| `02b_sample_ad_copy_bank.md` | 18 curated ad copies across 3 products × 2 keywords × 3 quality variants |
| `03_ux_flow_wireframe.md` | Full UX flows for all three tabs, interactive wireframe, 8 screenshots |
| `04_tech_stack_decisions.md` | Six evaluated decisions with alternatives and rationale |
| `05_risk_and_cost.md` | 7 risks with mitigations, cost scenarios, ₹0 monthly target confirmed |
| `06_roadmap.md` | 6 milestones across 4 weeks, critical path identified |

Five playbook documents also created in `pm-tpm-playbooks/ai-learning/` as reusable frameworks extracted from this project's research.

**What was harder than expected:**

The UX design took significantly longer than anticipated. What looked like a simple three-tab interface evolved through multiple iterations as real product decisions surfaced — the source toggle in Compare, the manual entry option for product and keyword, the batch pre-population via scenario dropdown, the consistency of empty manual fields across all three tabs. Each decision required reasoning through implications for other parts of the interface.

The tech stack decision was also more nuanced than expected. The original plan (Claude API) was revisited after clarifying the goal of ₹0 API costs across all portfolio projects. Switching to Gemini free tier required re-evaluating the local LLM option honestly — the deployment constraint (public URL requires cloud-hosted API) is not obvious until you think through the architecture.

**What changed from the original plan:**

| Original plan | What changed | Why |
|---------------|-------------|-----|
| Claude API as evaluation engine | Switched to Google Gemini 2.5 Flash-Lite (free tier) | Portfolio consolidation goal — ₹0 API costs across all projects |
| 11 documentation stages | Reduced to 8 stages | Merged risk + cost, merged launch + retro, moved setup guide into README |
| Audience + funnel stage as inputs | Replaced with target search keyword | Keyword naturally encodes both — closer to how marketers actually work |
| Single evaluation mode | Three tabs: Compare / Evaluate / Batch | Richer demo experience; bulk mode emerged as a natural extension |
| .txt file upload for bulk | Dynamic form rows as primary, .txt as secondary | Eliminates parsing ambiguity; better UX for first-time users |

**What's next:**

Milestone 0 — Environment setup. Personal machine, Python 3.11, virtual environment, Google AI Studio API key, first `streamlit run` with blank page.

---

*[New entries will be added above this line as the build progresses]*

---

## Entry Template

Copy and paste this for each new entry:

```
---

### Entry [N] — [Short title]
**Date:** [Month Year]
**Milestone:** [M0–M6]
**Hours this session:** [X hours]

---

**What was accomplished:**

**What was harder than expected:**

**What changed from the plan:**

**What's next:**

---
```

---

## Build Timeline Reference

| Milestone | Description | Target | Status |
|-----------|-------------|--------|--------|
| Docs | Planning and documentation | Apr 2026 | ✅ Complete |
| M0 | Environment setup | Week 1 | ⏳ |
| M1 | Evaluation engine (API call working) | Week 1 | ⏳ |
| M2 | Evaluate tab (single ad, full flow) | Week 2 | ⏳ |
| M3 | Compare tab (SBS, sample + manual) | Week 2–3 | ⏳ |
| M4 | Batch tab (dynamic rows + results table) | Week 3 | ⏳ |
| M5 | Polish and pre-launch validation | Week 3–4 | ⏳ |
| M6 | Deploy to Streamlit Community Cloud | Week 4 | ⏳ |

**Live URL:** *(added at M6)*

---

*Previous: [06 — Roadmap](./06_roadmap.md)*
*Next: [08 — Launch & Retrospective](./08_launch_and_retro.md)*
