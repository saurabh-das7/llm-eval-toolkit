# LLM Eval Toolkit

A practical, PM-driven toolkit for evaluating the quality of LLM-generated outputs — built from real experience defining evaluation criteria, scoring rubrics, and confidence thresholds for production AI systems.

This repo documents both the **thinking** (frameworks, PRDs, risk registers) and the **doing** (working tools you can run).

---

## Current Tool — Search Ad Copy Evaluator

> **LLMs can generate search ad copy at scale. They cannot tell you if it will actually work.**

The Search Ad Copy Evaluator is a Streamlit web application that evaluates LLM-generated search ads against a structured, intent-aware rubric — before a single rupee of budget is spent.

### Three Ways to Use It

**Flow 1 — Side-by-Side Sample Comparison**
Pick a product, pick a keyword, select two ad copy variants from the built-in sample bank. Hit Compare. See both ads scored across five dimensions with a winner declared and a plain-English reason for every score.

**Flow 2 — Manual Single Input**
Paste your own product description, target keyword, and LLM-generated ad copy. Get a full dimensional scorecard and verdict in under 10 seconds.

**Flow 3 — Bulk Evaluation**
Enter a product and keyword, upload a .txt file with up to 10 ad copy variants. Get a comparison table — all scored on the same rubric, same keyword, same dynamic weight profile.

### What It Evaluates

| Dimension | What it checks |
|-----------|---------------|
| Relevance | Does the ad accurately reflect the product? |
| Intent Alignment | Does the CTA match where the searcher is in their journey? |
| Differentiation | Is there a clear, compelling reason to click over competitors? |
| CTA Strength | Is the call to action specific, urgent, and funnel-appropriate? |
| Character Efficiency | Is every character earning its place? |

Dimension weights shift dynamically based on inferred search intent from the keyword — a purchase-intent keyword weights CTA Strength higher; a consideration keyword weights Differentiation higher.

**Verdict output:** `✅ READY TO SERVE` · `⚠️ NEEDS REVISION` · `❌ REJECT`

**Status:** 🔨 Actively building — follow along via the [build log](./docs/07_build_log.md)

**Live demo:** *(link added at launch)*

---

## Why This Exists

Bad search ads don't fail because they're wrong. They fail because they're irrelevant — written without imagining the searcher for even five seconds.

LLMs make this worse at scale. They optimise for sounding right, not for working right. The result is copy that passes every surface-level check and quietly bleeds ad spend — generic headlines, mismatched CTAs, wasted characters.

This tool is the missing pre-serve quality layer: structured, consistent, and fast enough to use before every launch.

Full problem framing: [docs/01_problem_statement.md](./docs/01_problem_statement.md)

---

## How to Run This Locally

**Requirements:** Python 3.9+, an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

```bash
# Clone the repo
git clone https://github.com/saurabh-das7/llm-eval-toolkit.git
cd llm-eval-toolkit

# Install dependencies
pip install -r requirements.txt

# Add your API key
export ANTHROPIC_API_KEY=your_key_here

# Run the app
streamlit run app/main.py
```

*Full setup walkthrough and environment notes will be added here as the build progresses.*

---

## Repo Structure

```
llm-eval-toolkit/
├── README.md
├── app/                               # Streamlit application (coming Stage 7+)
│   └── main.py
├── docs/                              # PM documentation — built stage by stage
│   ├── 01_problem_statement.md   ✅
│   ├── 02a_prd.md                ✅
│   ├── 02b_sample_ad_copy_bank.md ✅
│   ├── 03_ux_flow_wireframe.md
│   ├── 04_tech_stack_decisions.md
│   ├── 05_risk_and_cost.md
│   ├── 06_roadmap.md
│   ├── 07_build_log.md
│   └── 08_launch_and_retro.md
└── requirements.txt                   # Python dependencies (coming Stage 7+)
```

---

## The PM Documentation

Every stage of this build is documented the way a PM would approach it at work — problem framing, requirements, UX flows, risk registers, cost plans, and retrospectives.

| Doc | What it covers | Status |
|-----|---------------|--------|
| [01 — Problem Statement](./docs/01_problem_statement.md) | Why this exists, who it's for, cost of the problem | ✅ Done |
| [02a — PRD](./docs/02a_prd.md) | Three flows, rubric design, dynamic weights, success metrics | ✅ Done |
| [02b — Sample Ad Copy Bank](./docs/02b_sample_ad_copy_bank.md) | 18 curated ad copies across 6 keywords, 3 products | ✅ Done |
| 03 — UX Flow & Wireframe | User journeys and lo-fi interface design | 🔨 In progress |
| 04 — Tech Stack Decisions | Tools evaluated and chosen, with rationale | ⏳ Upcoming |
| 05 — Risk & Cost Plan | What could go wrong, API cost breakdown, spend controls | ⏳ Upcoming |
| 06 — Roadmap | Milestone plan from 0 to live | ⏳ Upcoming |
| 07 — Build Log | Running journal of what was built and learned each week | ⏳ Upcoming |
| 08 — Launch & Retrospective | Pre-launch QA checklist, post-launch reflection | ⏳ Upcoming |

---

## Who This Is For

**If you use LLMs to generate ad copy** — this tool gives you a consistent pre-serve quality check that doesn't rely on gut feel or post-spend regret.

**If you're a PM or TPM building AI products** — the docs folder is a worked example of how to frame, spec, and ship an LLM-powered tool from scratch, including the thinking behind every product decision.

**If you're evaluating LLM output quality** — the rubric and dynamic weight design are directly transferable to other domains beyond ad copy.

---

## About This Project

Built by [Saurabh Das](https://linkedin.com/in/saurabhdas7) — Senior TPM and Designated PM at Microsoft AI, documenting an AI learning journey in public.

Background: I've spent the last few years defining LLM evaluation frameworks, model-human parity benchmarks, and scoring rubrics for production AI systems in Ad Tech. This project applies those same principles to a problem anyone working with LLMs in marketing will recognise.

Related reading: [LLM Evaluation — Problem Landscape for PMs](https://github.com/saurabh-das7/pm-tpm-playbooks/blob/main/ai-learning/llm_eval_problem_landscape.md)
