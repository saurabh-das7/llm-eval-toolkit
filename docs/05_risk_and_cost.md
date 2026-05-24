# 05 — Risk & Cost Plan
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 5 of 8*
*Author: Saurabh Das | Last updated: May 2026*

---

## Section A — Risk Register

### Risk Rating Scale

| Probability | Impact | Rating |
|-------------|--------|--------|
| Low = unlikely in this project's lifetime | Low = minor inconvenience | P×I = Priority |
| Medium = plausible given known constraints | Medium = delays or rework | |
| High = likely given how this is built | High = blocks launch or breaks the demo | |

---

### R1 — Gemini Free Tier Restrictions Tighten Further

**Category:** API / External dependency

**Status: MATERIALISED AND RESOLVED**

**What happened:** During development, `gemini-2.5-flash-lite` (the originally planned model) was found to have a free tier cap of 20 requests per day — far below the advertised 1,000 RPD. This was discovered during M4 batch testing when the quota was exhausted within a single build session. The error was `429 RESOURCE_EXHAUSTED` with quota metric `GenerateRequestsPerDayPerProjectPerModel-FreeTier`.

**Resolution:** Switched evaluation engine to `gemini-3.1-flash-lite`, which provides 500 RPD on the free tier — sufficient for a portfolio demo tool at expected traffic levels. Confirmed via Google AI Studio rate limits dashboard.

**Residual risk:** Google has a demonstrated pattern of tightening free tier quotas. A further reduction on `gemini-3.1-flash-lite` is possible.

**Mitigation:**
- Monitor Google AI Studio dashboard monthly for quota changes
- Fallback: switch to `gemini-3.1-flash-lite` paid tier at $0.10/M input tokens — estimated ₹50/month at current volume
- Code design: evaluation engine abstracted behind `evaluate_ad_copy()` — swapping models requires changing one line

**Escalation trigger:** More than 3 rate limit errors in a single day on the live app.

---

### R2 — Gemini Free Tier Discontinued Entirely

**Category:** API / External dependency

**Description:** Google could shut down the free tier entirely for API access.

**Probability:** Low — the free tier is a deliberate developer acquisition strategy.

**Impact:** High — requires switching evaluation engine.

**Mitigation:**
- Evaluation call abstracted behind `evaluate_ad_copy()` — provider swap is a one-line change
- Fallback options in priority order:
  1. Gemini paid tier — minimal cost (~₹50/month), zero code change
  2. Groq free tier (Llama 4) — zero cost, higher volume, lower reasoning quality
  3. Claude Haiku — ~₹0.01/evaluation, requires separate Anthropic API account

**Escalation trigger:** Official Google announcement of free tier deprecation.

---

### R3 — Evaluation Quality is Inconsistent

**Category:** Product / LLM behaviour

**Description:** The model may score the same ad differently across runs, or may not follow the rubric reliably on edge case inputs.

**Probability:** Medium — LLM output variance is inherent; structured prompting reduces but does not eliminate it.

**Impact:** High — inconsistent scoring undermines the core value proposition.

**Mitigation:**
- Temperature set to 0.1 — near-deterministic output
- JSON-only output enforced in system prompt
- Overall score calculated in Python, not trusted from model (model arithmetic found to be off by ~0.2 during testing)
- Downgrade rule catches catastrophic failures regardless of weighted average
- All 18 sample bank entries validated pre-launch

**Escalation trigger:** Any sample bank ad producing a verdict different from its expected verdict.

---

### R4 — Streamlit Community Cloud Reliability

**Category:** Hosting / Infrastructure

**Description:** Free tier apps go to sleep after inactivity. First visitor after a sleep period waits 30–60 seconds.

**Probability:** High — documented behaviour for free tier apps.

**Impact:** Low — app recovers; it's friction, not failure.

**Mitigation:**
- Loading state visible to user — not mistaken for a broken app
- Cold start behaviour documented in README
- Visit URL before sharing with important visitors to pre-warm

**Escalation trigger:** Downtime exceeding 10 minutes — indicates platform issue, not sleep mode.

---

### R5 — Scope Creep During Build

**Category:** Execution / Solo builder

**Status: MANAGED**

**What happened:** Several features were proposed during the build that were not in the PRD — additional sample products, export functionality, a consistency scoring feature. All were logged in the post-MVP backlog and not built.

**Mitigation that worked:** PRD non-goals list served as the gate. New ideas were added to `08_launch_and_retro.md` post-MVP backlog, not to the current build.

---

### R6 — API Key Exposure

**Category:** Security

**Description:** Gemini API key accidentally committed to the GitHub repo.

**Probability:** Low — Codespaces Secrets and Streamlit secrets management prevent this when followed correctly.

**Impact:** Medium — free tier has no billing attached, so financial exposure is zero. But key rotation is required and daily quota could be exhausted.

**Mitigation:**
- API key stored in GitHub Codespaces Secrets (dev) and Streamlit secrets manager (prod)
- `.gitignore` excludes `.env` and `.streamlit/secrets.toml`
- Key rotation: revoke in Google AI Studio, generate new, update Streamlit secrets

**Escalation trigger:** Any commit containing a string matching `AIza` (Google API key prefix).

---

### R7 — Git Divergence Between Codespace and GitHub

**Category:** Execution / Version control

**Status: MATERIALISED AND RESOLVED**

**What happened:** During the docs phase, files were edited directly on GitHub browser. This created commits that the Codespace didn't have. When M5 commits were pushed, git rejected the push with `non-fast-forward` error. Resolved with `git push --force`.

**Prevention going forward:** Once a Codespace is active, never edit files directly on GitHub browser. All changes go through the Codespace.

---

### Risk Summary

| Risk | Probability | Impact | Priority | Status |
|------|-------------|--------|----------|--------|
| R1 — Free tier restrictions | Medium | Medium | Medium | ✅ Resolved — switched to gemini-3.1-flash-lite (500 RPD) |
| R2 — Free tier discontinued | Low | High | Medium | Mitigated — provider abstraction in place |
| R3 — Inconsistent evaluation | Medium | High | High | Mitigated — low temp + Python scoring + pre-launch validation |
| R4 — Streamlit cold start | High | Low | Low | Accepted — documented in README |
| R5 — Scope creep | High | Medium | High | ✅ Managed — post-MVP backlog used throughout |
| R6 — API key exposure | Low | Medium | Low | Mitigated — secrets management + .gitignore |
| R7 — Git divergence | Medium | Medium | Medium | ✅ Resolved — force push; prevention documented |

---

## Section B — Cost Plan

### B1 — Cost Philosophy

Target: ₹0 in API and hosting costs across all portfolio projects, consolidated under existing free-tier accounts. The only cost is the Claude Pro subscription already in use for building — which covers chat-based iteration and code generation.

### B2 — Cost Breakdown (Actual at Launch)

| Item | Cost | Notes |
|------|------|-------|
| Gemini API (gemini-3.1-flash-lite) | ₹0 | Free tier — 500 req/day, no credit card |
| Streamlit Community Cloud | ₹0 | Free for public apps |
| GitHub | ₹0 | Free for public repos |
| GitHub Codespaces | ₹0 | 120 core-hours/month free; used ~3 hours/session |
| GitHub Copilot | ₹0 | Free tier — 2,000 completions/month |
| Claude Pro (building tool) | Already paying | Not a project cost |
| **Total monthly project cost** | **₹0** | |

### B3 — Cost Scenarios

**Scenario 1 — Free tier holds (expected)**

At 50–100 evaluations/day the free tier comfortably handles all traffic. Monthly cost: ₹0.

**Scenario 2 — Gemini free tier tightened again**

If `gemini-3.1-flash-lite` free tier drops below 100 RPD, switch to paid tier.

Estimated cost at 100 evaluations/day:
- Input: 100 × 1,500 tokens × 30 days = 4.5M tokens × $0.10/M = $0.45
- Output: 100 × 500 tokens × 30 days = 1.5M tokens × $0.40/M = $0.60
- **Total: ~$1.05/month (~₹88/month)**

**Scenario 3 — Provider switch to Groq**

If Gemini free tier discontinued entirely, Groq offers 14,400 req/day free on open-source models. Quality validation against sample bank required before switching. Monthly cost: ₹0.

### B4 — Spend Controls

No billing is attached to the Gemini free tier — Google's infrastructure enforces the daily cap. No risk of unexpected charges from the API. If a paid tier is ever enabled, set a Google Cloud budget alert at $2/month.

---

*Previous: [04b — Tech Stack Decisions v2](./04b_tech_stack_decisions_v2.md)*
*Next: [06 — Roadmap](./06_roadmap.md)*
