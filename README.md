# LLM Eval Toolkit

A practical, PM-driven toolkit for evaluating the quality of LLM-generated outputs — built from real experience defining evaluation criteria, scoring rubrics, and confidence thresholds for production AI systems.

This repo documents both the **thinking** (frameworks, PRDs, risk registers) and the **doing** (working tools you can run).

---

## Current Tool — Search Ad Copy Evaluator

> **LLMs can generate search ad copy at scale. They cannot tell you if it will actually work.**

The Search Ad Copy Evaluator is a Streamlit web app that evaluates LLM-generated search ads against a structured, intent-aware rubric — before a single rupee of budget is spent.

**How it works:**
1. Paste a product description
2. Paste an LLM-generated search ad (headline + description)
3. Get a dimensional scorecard + verdict in seconds

**What it evaluates:**

| Dimension | What it checks |
|-----------|---------------|
| Relevance | Does the ad accurately reflect the product? |
| Intent Alignment | Does the CTA match where the searcher is in their journey? |
| Differentiation | Is there a clear, compelling reason to click over competitors? |
| CTA Strength | Is the call to action specific, urgent, and funnel-appropriate? |
| Character Efficiency | Is every character earning its place? |

**Verdict output:** `✅ READY TO SERVE` · `⚠️ NEEDS REVISION` · `❌ REJECT`

**Status:** 🔨 Actively building — follow along via the [build log](./docs/09_build_log.md)

**Live demo:** *(link added at launch)*

---

## Why This Exists

Bad search ads don't fail because they're wrong. They fail because they're irrelevant — written without imagining the searcher for even five seconds.

LLMs make this worse at scale. They optimise for sounding right, not for working right. The result is copy that passes every surface-level check and quietly bleeds ad spend — generic headlines, mismatched CTAs, wasted characters.

This tool is the missing pre-serve quality layer: structured, consistent, and fast enough to run before every launch.

Full problem framing: [docs/01_problem_statement.md](./docs/01_problem_statement.md)

---

## Repo Structure

```
llm-eval-toolkit/
├── README.md
├── app/                        # Streamlit application (coming Stage 8)
│   └── main.py
├── docs/                       # Full PM documentation — built stage by stage
│   ├── 01_problem_statement.md ✅
│   ├── 02_prd.md
│   ├── 03_ux_flow_wireframe.md
│   ├── 04_tech_stack_decisions.md
│   ├── 05_risk_register.md
│   ├── 06_cost_plan.md
│   ├── 07_roadmap.md
│   ├── 08_setup_guide.md
│   ├── 09_build_log.md
│   ├── 10_launch_checklist.md
│   └── 11_retrospective.md
└── requirements.txt            # Python dependencies (coming Stage 8)
```

---

## The PM Documentation

One thing that separates a side project from a portfolio piece is the thinking behind it. Every stage of this build is documented the way a PM would approach it at work — problem framing, requirements, UX flows, risk registers, cost plans, and retrospectives.

| Doc | Stage | Status |
|-----|-------|--------|
| [Problem Statement](./docs/01_problem_statement.md) | Why this exists | ✅ Done |
| PRD | What we're building and why | 🔨 In progress |
| UX Flow & Wireframe | How the user moves through the app | ⏳ Upcoming |
| Tech Stack Decisions | Tools evaluated and chosen | ⏳ Upcoming |
| Risk Register | What could go wrong and how we handle it | ⏳ Upcoming |
| Cost Plan | API costs, monthly burn, spend controls | ⏳ Upcoming |
| Roadmap | Milestone plan from 0 to live | ⏳ Upcoming |
| Setup Guide | How to run this locally | ⏳ Upcoming |
| Build Log | Weekly journal of what was built and learned | ⏳ Upcoming |
| Launch Checklist | Pre-launch QA and go-live steps | ⏳ Upcoming |
| Retrospective | What worked, what didn't, what's next | ⏳ Upcoming |

---

## Who This Is For

**If you use LLMs to generate ad copy** — this tool gives you a consistent pre-serve quality check that doesn't rely on gut feel or post-spend regret.

**If you're a PM or TPM building AI products** — the docs folder is a worked example of how to frame, spec, and ship an LLM-powered tool from scratch.

**If you're evaluating LLM output quality** — the rubric and scoring design are directly transferable to other domains beyond ad copy.

---

## About This Project

Built by [Saurabh Das](https://linkedin.com/in/saurabhdas7) — Senior TPM and Designated PM at Microsoft AI, documenting an AI learning journey in public.

Background: I've spent the last few years defining LLM evaluation frameworks, model-human parity benchmarks, and scoring rubrics for production AI systems in Ad Tech. This project applies those same principles to a problem anyone working with LLMs in marketing will recognise.

Related reading: [LLM Evaluation — Problem Landscape for PMs](https://github.com/saurabh-das7/pm-tpm-playbooks/blob/main/ai-learning/llm_eval_problem_landscape.md)
