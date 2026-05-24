# 02a — Product Requirements Document (PRD)
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 2 of 8*
*Author: Saurabh Das | Last updated: April 2026*
*Status: Draft v1.2 — updated to reflect UX decisions from Stage 3 (tab names, Compare source toggle, panel-level toggles, Batch form rows)*

---

## Document Purpose

This PRD defines what the Search Ad Copy Evaluator does, who it is for, how success is measured, and what is explicitly out of scope for the v1 MVP. It is the source of truth for all downstream design, technical, and build decisions.

For the full problem framing that informs this document, see [01_problem_statement.md](./01_problem_statement.md).
For sample ad copies used in Flow 1, see [02b_sample_ad_copy_bank.md](./02b_sample_ad_copy_bank.md).

---

## 1. Product Overview

### 1.1 What It Is

The Search Ad Copy Evaluator is a Streamlit web application that evaluates LLM-generated search ad copy against a structured, intent-aware rubric — before a single unit of budget is spent.

The tool has three tabs — **Compare**, **Evaluate**, and **Batch** — all scored against the same rubric with dynamically allocated dimension weights based on the inferred search intent of the keyword. Every tab is zero-friction: a first-time user can experience the full output without typing a single character.

### 1.2 The Core Job To Be Done

> Give a performance marketer or growth PM a fast, consistent, expert-level quality check on LLM-generated search ad copy — before it enters a launch workflow.

### 1.3 Primary User

> A performance marketer or growth PM who uses LLMs to generate search ads at scale, but currently relies on gut feel, spreadsheets, and post-spend A/B tests to catch copy that is technically correct yet quietly ineffective.

**Their context:**
- Generates dozens to hundreds of ad variants via LLM to meet velocity targets
- Ads are not obviously wrong — just quietly underperforming
- When metrics dip, attribution is unclear: copy, targeting, or timing?
- Review today happens in Google Docs with comments like "too generic" or "fix CTA"
- A/B testing is their primary validation — reactive, slow, and expensive
- They get blamed for outcome metrics, not just creative quality

---

## 2. Goals and Non-Goals

### 2.1 Goals (v1)

- Provide structured, rubric-based quality evaluation of LLM-generated search ad copy across three distinct usage flows
- Dynamically allocate rubric dimension weights based on inferred search intent from the keyword
- Surface specific, actionable feedback per dimension — not just an overall score
- Deliver a clear, unambiguous verdict: `READY TO SERVE`, `NEEDS REVISION`, or `REJECT`
- Support side-by-side comparison of two ad copies for the same product + keyword combination
- Support bulk evaluation of up to 10 ad copies against a single product + keyword combination
- Handle malformed, incomplete, or edge-case inputs gracefully without forcing a false verdict
- Be fast enough to use before every launch (target: single verdict within 10 seconds)
- Be fully usable without any platform integration, account access, or historical data

### 2.2 Non-Goals (v1 — explicitly out of scope)

| Out of Scope | Why |
|---|---|
| Ad copy generation or rewriting | Mixing generation + evaluation collapses the separation between creation and critique — which is exactly the gap this tool exists to fill |
| CTR / CVR / CPA prediction | Performance prediction requires auction context, audience signals, and historical data unavailable in a copy-only evaluation |
| Landing page message match | LP analysis introduces URL ingestion and crawl latency — breaks the intended fast, text-in → verdict-out loop |
| Platform policy / compliance checks | Policy safety is a distinct problem from effectiveness — this tool evaluates whether an ad will win attention, not whether it will be approved |
| Audience segment inference | Targeting strategy sits upstream of copy evaluation — expanding into this risks drifting from quality control into campaign planning |
| A/B test management or variant orchestration | Post-serve optimisation is out of scope — this product addresses the moment before the ad serves |
| Ad platform API integration | MVP is designed for standalone, pre-workflow QA — demoable without enterprise permissions |
| Brand voice or creative guidelines learning | Brand-specific tuning requires persistent memory and feedback loops — roadmap items beyond v1 |
| Bulk evaluation beyond 10 ads | Keeps API costs bounded and output readable in v1 |

---

## 3. The Three Tabs

### Tab 1 — Compare (Side-by-Side Comparison)

The primary onboarding experience. Designed for first-time users and for anyone who wants to see the evaluator reason through a judgment call between two ad copy variants.

**Input source toggle (top of tab):**

The user first decides where their product and keyword come from:

- **Use samples (default):** Product dropdown (Nike / Trello / MakeMyTrip) → Keyword dropdown (filtered dynamically to selected product) → inferred intent label displayed
- **Enter manually:** Product and keyword dropdowns are replaced with free text inputs. Both panels automatically switch to manual entry mode and their individual toggles are hidden.

**Panel-level toggles (when source is "Use samples"):**

Each panel has its own independent toggle — "Use sample / Enter manually" — allowing the user to mix modes. For example: a known-good sample variant in Panel A benchmarked against the user's own copy in Panel B.

**Input sequence (Use samples mode):**
1. Select Product (dropdown)
2. Select Keyword (filtered dropdown)
3. Panel A — select Ad Copy variant (dropdown) or switch to manual entry
4. Panel B — select a different Ad Copy variant (dropdown) or switch to manual entry
5. Click **Compare**

**Input sequence (Enter manually mode):**
1. Enter Product Description (textarea)
2. Enter Target Search Keyword (text input)
3. Panel A — enter Headline (≤30 chars) + Description (≤90 chars)
4. Panel B — enter Headline (≤30 chars) + Description (≤90 chars)
5. Click **Compare**

**Ad preview card:** Always visible in each panel. Updates live as variant is selected or copy is typed. Shows the ad as it would appear on a search results page — Sponsored label, display URL, headline, description.

**Output:**
- Intent badge (inferred from keyword, with weight profile shown)
- Scorecard for Panel A (all five dimensions, score + one-line reasoning each, overall score, verdict)
- Scorecard for Panel B (same structure)
- Head-to-head summary: which ad wins, on which dimensions, and the primary reason

---

### Tab 2 — Evaluate (Single Ad Evaluation)

For users who have their own copy ready and want a direct evaluation without using samples.

**Zero-friction entry point:** "Load random sample" button pre-fills all fields with a randomly selected sample from the 18 in the sample bank. Ad preview and intent hint appear immediately.

**Input:**
1. Paste or type **Product Description** (textarea, 10–150 words)
2. Paste or type **Target Search Keyword** (text input) — inferred intent shown alongside
3. Paste or type **Ad Headline** (≤30 characters — live character counter)
4. Paste or type **Ad Description** (≤90 characters — live character counter)
5. Ad preview card appears as soon as headline or description has content, updates live
6. Click **Evaluate**

**Output:**
- Intent badge with weight profile
- Scorecard (all five dimensions, score + one-line reasoning each)
- Overall weighted score
- Verdict: `READY TO SERVE` / `NEEDS REVISION` / `REJECT` / `NOT EVALUABLE`
- Plain-English evaluator note naming the single most important issue or strength

---

### Tab 3 — Batch (Batch Evaluation)

For users evaluating multiple LLM-generated variants for the same campaign.

**Zero-friction entry point:** "Load sample scenario" dropdown pre-fills product description, keyword, and all ad copy rows in one action. Three scenarios available — one per product.

**Primary input method — dynamic form rows:**
1. Enter **Product Description** (textarea)
2. Enter **Target Search Keyword** (text input) — inferred intent shown alongside
3. Ad copy rows — one row per ad, each with Headline (≤30 chars) and Description (≤90 chars) fields with live character counters
4. Minimum 1 row, maximum 10 rows. Rows can be added or removed individually. Row 1 cannot be removed.
5. Click **Evaluate All**

**Secondary input method — .txt file upload:**
Separated below the form rows. Format: `Headline | Description` one per line, max 10 lines. A sample .txt file is available to download so users understand the format before uploading.

**Constraints:**
- Maximum 10 ad copies per batch
- All ads evaluated against the same product + keyword (same dynamic weight profile)
- If .txt file contains more than 10 lines, app processes the first 10 and warns the user

**Output:**
- Intent badge with weight profile shown once for the batch
- Results table: one row per ad — headline, five dimension scores, overall score, verdict
- Summary row: best-performing ad and most common failure dimension across the batch

---

## 4. Evaluation Rubric

### 4.1 Dimensions

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | **Relevance** | Does the ad accurately reflect the product or offer described? |
| 2 | **Intent Alignment** | Does the CTA match where the searcher is in their decision journey? |
| 3 | **Differentiation** | Is there a clear, specific reason to click this ad over a competitor? |
| 4 | **CTA Strength** | Is the call to action specific, urgent, and action-oriented? |
| 5 | **Character Efficiency** | Is every character earning its place? No filler, no wasted space? |

Each dimension is scored 1–5 (integer) with a mandatory one-line reasoning statement.

### 4.2 Dynamic Weight Allocation

Dimension weights are not fixed. They shift based on the search intent inferred from the keyword. The evaluator infers intent from keyword signals and applies the appropriate weight profile before scoring.

**Intent inference rules:**

| Keyword signals | Inferred Intent |
|----------------|----------------|
| "buy", "order", "book", "purchase", "shop", price terms (₹, $), "deal", "offer" | Purchase |
| "best", "compare", "top", "vs", "review", "which", "alternative" | Consideration |
| "what is", "how to", "guide", "tips", "learn", "explained" | Awareness |
| Ambiguous / no clear signal | Consideration (default) |

**Weight profiles by intent:**

| Dimension | Purchase | Consideration | Awareness |
|-----------|---------|--------------|----------|
| Relevance | 15% | 20% | 25% |
| Intent Alignment | 30% | 20% | 15% |
| Differentiation | 20% | 30% | 20% |
| CTA Strength | 25% | 15% | 10% |
| Character Efficiency | 10% | 15% | 30% |
| **Total** | **100%** | **100%** | **100%** |

**Rationale:**
- **Purchase intent:** CTA Strength and Intent Alignment matter most — user is ready to act, mismatch here costs the click
- **Consideration intent:** Differentiation and Relevance matter most — user is comparing, USP and accuracy drive the decision
- **Awareness intent:** Clarity (Character Efficiency) and Relevance matter most — user is learning, information quality and readability drive engagement

The applied weight profile is always displayed to the user so the scoring is transparent and auditable.

### 4.3 Verdict Logic

| Overall Score | Verdict |
|---------------|---------|
| 4.0 – 5.0 | ✅ READY TO SERVE |
| 2.5 – 3.9 | ⚠️ NEEDS REVISION |
| Below 2.5 | ❌ REJECT |
| Input invalid / insufficient | 🟡 NOT EVALUABLE — INSUFFICIENT INPUT |

**Verdict downgrade rule:** If any single dimension scores 1/5, the overall verdict cannot be higher than `NEEDS REVISION` — regardless of the weighted average. A catastrophic failure on one dimension disqualifies the ad even if others score well.

---

## 5. Input Specification

### 5.1 Required Inputs (all flows)

| Input | Format | Constraints |
|-------|--------|-------------|
| Product description | Free text | 10–150 words |
| Target search keyword | Free text | 2–10 words |
| Ad headline | Free text | ≤ 30 characters |
| Ad description | Free text | ≤ 90 characters |

### 5.2 Bulk-Specific Input

| Input | Format | Constraints |
|-------|--------|-------------|
| Ad copy batch | .txt file upload | Max 10 lines; format: `Headline \| Description` per line |

### 5.3 Edge Case Handling

| Edge Case | How v1 Handles It |
|-----------|------------------|
| Vague product description ("AI tool for teams") | Return `NOT EVALUABLE` + prompt for clearer offer |
| Keyword too short or generic ("shoes") | Warn: ambiguous intent, defaulting to Consideration weights |
| Headline over 30 characters | Hard fail Character Efficiency; flag before evaluation |
| Description over 90 characters | Hard fail Character Efficiency; flag before evaluation |
| Ad missing CTA | Explicitly penalise CTA Strength |
| RSA-style multi-headline input | Prompt user to select one headline |
| Dynamic keyword insertion ({KeyWord:Headphones}) | Evaluate static fallback text |
| Non-English input | Detect language; evaluate if supported, else warn |
| Emoji or ALL CAPS | Penalise Character Efficiency |
| URL or landing page pasted as ad copy | Reject input type with explanation |
| Placeholder text ("Insert USP here") | Reject with explanation |
| Bulk file with > 10 lines | Process first 10, warn user |
| Bulk file with wrong format | Return format error with example |
| Same variant selected in both SBS panels | Prevent submission; prompt user to select different variants |

---

## 6. Output Specification

### 6.1 Single Evaluation Output (Flows 1 and 2)

```
PRODUCT:         [product description summary]
KEYWORD:         [keyword]
INFERRED INTENT: [Purchase / Consideration / Awareness]
WEIGHT PROFILE:  [profile name + weights applied]

AD EVALUATED: [headline] | [description]

SCORECARD
──────────────────────────────────────────────────────
Relevance             [X/5]   [one-line reasoning]
Intent Alignment      [X/5]   [one-line reasoning]
Differentiation       [X/5]   [one-line reasoning]
CTA Strength          [X/5]   [one-line reasoning]
Character Efficiency  [X/5]   [one-line reasoning]
──────────────────────────────────────────────────────
Overall Score         [X.X / 5]

VERDICT: [READY TO SERVE / NEEDS REVISION / REJECT / NOT EVALUABLE]

EVALUATOR NOTE: [1–2 sentences naming the single most important issue or confirming strength]
```

### 6.2 SBS Head-to-Head Summary (Flow 1 only)

After both individual scorecards:

```
HEAD-TO-HEAD SUMMARY
──────────────────────────────────────────────────────
Ad A wins on:    [dimension(s)]
Ad B wins on:    [dimension(s)]
Overall winner:  Ad [A/B] — [one-line reason]
──────────────────────────────────────────────────────
```

### 6.3 Bulk Output Table (Flow 3)

Results displayed as a scrollable table with:
- One row per ad copy
- Score per dimension
- Overall weighted score
- Verdict with icon
- Summary row: best performer, most common failure dimension

### 6.4 Output Principles

- Every dimension score must have a one-line explanation specific enough to act on
- The evaluator note names one thing — not a summary of all five
- The weight profile applied is always visible — scoring is never a black box
- Verdicts are unambiguous — no hedging in the verdict label itself
- The tool never outputs a confident verdict on insufficient or malformed input

---

## 7. Success Metrics

### 7.1 Human Alignment
| Metric | Target |
|--------|--------|
| Evaluator ↔ expert reviewer verdict agreement rate | ≥ 75% |
| Mean dimension score delta vs human rubric | ≤ 0.5 per dimension |
| False negative rate (weak ads marked READY TO SERVE) | < 10% |

### 7.2 Decision Utility
| Metric | Target |
|--------|--------|
| Revision rate on NEEDS REVISION verdicts | ≥ 60% |
| Override rate on REJECT verdicts | < 20% |
| Feedback usefulness rating (post-eval) | ≥ 4.0 / 5 |

### 7.3 Pre-Serve Defect Detection
| Metric | Target |
|--------|--------|
| Pre-serve catch rate vs human QA baseline | ≥ 70% |
| Character efficiency violations caught | 100% |
| Intent-CTA mismatch detection rate | ≥ 75% |

### 7.4 Consistency and Robustness
| Metric | Target |
|--------|--------|
| Verdict consistency across paraphrased inputs | ≥ 85% same verdict |
| Dimension score variance for same semantic content | ≤ 0.5 score points |

### 7.5 Workflow Fit
| Metric | Target |
|--------|--------|
| Time-to-verdict, single eval (p95) | ≤ 10 seconds |
| Time-to-results, bulk 10 ads (p95) | ≤ 45 seconds |

---

## 8. Design Principles

1. **Verdict clarity over nuance.** The tool must tell the user what to do, not make them interpret a score.
2. **Reasoning over scores.** A score without explanation is noise. Every dimension score has a one-line reason specific enough to act on.
3. **Transparent weights.** The dynamic weight profile applied is always shown. Scoring is never a black box.
4. **Graceful failure over forced judgment.** When context is missing or input is malformed, the tool fails transparently — never hallucinating a verdict.
5. **Pre-serve speed.** If evaluation takes longer than the decision it informs, it gets skipped.
6. **Separation of creation and critique.** The evaluator diagnoses; it does not fix.

---

## 9. Open Questions

| Question | Resolution needed by |
|----------|---------------------|
| Should overall score be shown numerically or as a visual bar only? | Build stage |
| Should dynamic weight profile be shown as percentages or a named label (e.g. "Purchase mode")? | Build stage |
| How do we handle keywords with ambiguous intent signals in bulk mode? | Tech planning stage |
| Minimum viable test set size for human alignment validation? | Pre-launch |
| Should bulk output be downloadable as CSV in v1? | Tech planning stage |
| Should Compare tab remember the last selected product/keyword within a session? | Build stage |

---

## 10. Assumptions and Dependencies

**Assumptions:**
- Users have already generated their ad copy using an LLM before reaching this tool
- Users understand basic search ad anatomy (headline, description, CTA)
- The evaluation rubric is fixed in v1 — no custom rubric builder
- English is the primary supported language at launch
- All ads in a bulk batch share the same product + keyword combination

**Dependencies:**
- Google Gemini API (gemini-3.1-flash-lite, free tier, via Google AI Studio) — evaluation engine
- Streamlit — application framework
- Python 3.9+ — runtime

---

*Previous: [01 — Problem Statement](./01_problem_statement.md)*
*Supporting: [02b — Sample Ad Copy Bank](./02b_sample_ad_copy_bank.md)*
*Next: [03 — UX Flow and Wireframe](./03_ux_flow_wireframe.md)*
