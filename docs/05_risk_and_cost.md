# 05 — Risk & Cost Plan
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 5 of 8*
*Author: Saurabh Das | Last updated: April 2026*

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

**Description:** Google reduced free tier quotas by 50–80% in December 2025. A further reduction could drop the 1,000 req/day limit to a level that makes the demo unreliable for external visitors.

**Probability:** Medium — Google has a demonstrated pattern of tightening free tiers as adoption grows.

**Impact:** Medium — the app continues to work but rate limit errors would appear under moderate traffic.

**Mitigation:**
- Primary: Monitor the Gemini API pricing page and Google AI Studio dashboard monthly
- Fallback: Switch to Gemini 2.5 Flash-Lite paid tier — estimated cost at current volume is $0.10/M input tokens, well under ₹100/month
- Code design: Use the OpenAI-compatible endpoint format so switching from free to paid tier requires changing only the API key configuration, not the code

**Escalation trigger:** More than 3 rate limit errors in a single day on the live app.

---

### R2 — Gemini Free Tier Discontinued Entirely

**Category:** API / External dependency

**Description:** Google could shut down the free tier entirely for API access, as they have done for other products. This would require a new evaluation engine decision.

**Probability:** Low — the free tier is a deliberate developer acquisition strategy; full discontinuation is unlikely in the near term but not impossible.

**Impact:** High — requires switching evaluation engine, which touches the core of the application.

**Mitigation:**
- Code design: Abstract the evaluation call behind a single function (`evaluate_ad_copy()`). Swapping providers requires changing one function, not rewriting the app.
- Fallback options in priority order:
  1. Groq free tier (Llama 4) — zero cost, higher volume, lower reasoning quality
  2. Gemini paid tier — minimal cost, no code change
  3. Claude Haiku 4.5 — ~₹0.01/evaluation, requires Anthropic Console account

**Escalation trigger:** Official Google announcement of free tier deprecation.

---

### R3 — Evaluation Quality is Inconsistent

**Category:** Product / LLM behaviour

**Description:** The Gemini model may score the same ad differently across runs, or may not follow the rubric reliably on edge case inputs. This would undermine user trust in the evaluator.

**Probability:** Medium — LLM output variance is inherent; structured prompting reduces but does not eliminate it.

**Impact:** High — inconsistent scoring directly contradicts the core value proposition of a "repeatable, consistent quality standard."

**Mitigation:**
- Use low temperature setting (0.1–0.2) in API calls to reduce output variance
- Require JSON-only output in the system prompt — structured output reduces hallucination
- Add a consistency validation layer: if the same input scores >1 point differently on two runs, flag it
- Validate against the sample bank before launch — all 18 samples must produce the expected verdict

**Escalation trigger:** Any sample bank ad producing a verdict different from its expected verdict during pre-launch testing.

---

### R4 — Streamlit Community Cloud Reliability

**Category:** Hosting / Infrastructure

**Description:** Streamlit Community Cloud free tier apps go to sleep after periods of inactivity and have occasional downtime. A recruiter or hiring manager landing on the app during a cold start may see a loading delay or error.

**Probability:** High — sleep mode is documented behaviour for free tier Streamlit apps.

**Impact:** Low — the app recovers within 30–60 seconds; it's a friction point, not a failure.

**Mitigation:**
- Add a clear loading message so users understand the app is waking up, not broken
- Document the cold start behaviour in the README so it's not mistaken for a bug
- If the app is being actively shared (e.g. during a job application process), manually visit it first to wake it up

**Escalation trigger:** Downtime lasting more than 10 minutes, which would indicate a platform issue rather than sleep mode.

---

### R5 — Scope Creep During Build

**Category:** Execution / Solo builder

**Description:** The feature set is well-defined but the temptation to add features during build is real — especially when something "small" seems easy to add. Each addition extends the timeline and risks the 2-week MVP target.

**Probability:** High — this is a known failure mode for solo builders.

**Impact:** Medium — delays launch, reduces time available for later stages.

**Mitigation:**
- The PRD non-goals list (Section 2.2 of `02a_prd.md`) is the gate — any feature not in the PRD requires a conscious decision to update the PRD before building
- New ideas go into a "post-MVP" backlog in `08_launch_and_retro.md`, not into the current build
- The build log (`07_build_log.md`) tracks scope changes explicitly — if something is added, it must be documented

**Escalation trigger:** Any feature being built that isn't in the PRD without a corresponding PRD update.

---

### R6 — API Key Exposure

**Category:** Security

**Description:** The Gemini API key could be accidentally committed to the GitHub repo, exposing it publicly.

**Probability:** Low — Streamlit secrets management and `.gitignore` configuration prevent this if set up correctly.

**Impact:** Medium — a compromised key on a free tier account has limited financial impact (no billing attached) but requires key rotation and could exhaust the daily quota before rotation.

**Mitigation:**
- API key stored only in Streamlit secrets manager (production) and `.env` file (local dev)
- `.gitignore` excludes `.env` and `.streamlit/secrets.toml` from day one — verified before first commit
- If accidental exposure occurs: revoke key immediately in Google AI Studio, generate new key, update Streamlit secrets

**Escalation trigger:** Any commit that contains a string matching `AIza` (Google API key prefix).

---

### R7 — Evaluation Prompt Injection via User Input

**Category:** Security / LLM behaviour

**Description:** A malicious user could craft a product description or ad copy designed to manipulate the evaluation prompt — for example, instructing the model to always return READY TO SERVE regardless of actual quality.

**Probability:** Low — the app is a portfolio demo, not a production product with adversarial users.

**Impact:** Low — the consequence is a skewed scorecard, not data loss or financial harm.

**Mitigation:**
- System prompt clearly separates the rubric instructions from user-supplied content
- User input is passed as data (within quotes in the prompt), not as instructions
- Input length limits (150 words for product description, 30/90 chars for ad copy) reduce the attack surface

**Escalation trigger:** Not applicable at portfolio demo scale — document for awareness only.

---

### Risk Summary

| Risk | Probability | Impact | Priority | Status |
|------|-------------|--------|----------|--------|
| R1 — Free tier restrictions tighten | Medium | Medium | Medium | Mitigated — paid fallback documented |
| R2 — Free tier discontinued | Low | High | Medium | Mitigated — provider abstraction planned |
| R3 — Inconsistent evaluation quality | Medium | High | High | Mitigated — low temp + JSON output + pre-launch validation |
| R4 — Streamlit cold start | High | Low | Low | Accepted — documented in README |
| R5 — Scope creep | High | Medium | High | Mitigated — PRD non-goals as gate |
| R6 — API key exposure | Low | Medium | Low | Mitigated — secrets management + .gitignore |
| R7 — Prompt injection | Low | Low | Low | Accepted — portfolio demo scale |

---

## Section B — Cost Plan

### B1 — Cost Philosophy

The target for this project is ₹0 in API and hosting costs, consolidated under existing free-tier accounts. The only acceptable cost is the Claude Pro subscription already in use for building — which covers this conversation and all future iterations on docs and code.

This constraint is intentional: it forces API decisions that are replicable across future portfolio projects without accumulating per-project costs.

---

### B2 — Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| Gemini API (evaluation engine) | ₹0 | Free tier — 1,000 req/day, no credit card |
| Streamlit Community Cloud (hosting) | ₹0 | Free tier for public apps |
| GitHub (version control) | ₹0 | Free for public repos |
| Google AI Studio (API key management) | ₹0 | Free |
| Python, VS Code, Streamlit framework | ₹0 | All open source |
| Claude Pro subscription (building tool) | Already paying | Not a project cost — pre-existing |
| **Total monthly project cost** | **₹0** | |

---

### B3 — Cost Scenarios

**Scenario 1 — Free tier holds, low traffic (expected)**

The app is shared with recruiters and hiring managers — a small, targeted audience. At 50–100 evaluations/day, the free tier comfortably handles all traffic. Monthly cost: ₹0.

**Scenario 2 — Free tier tightened, paid fallback required**

If Google reduces Flash-Lite free limits below 100 req/day, the paid tier becomes necessary.

Cost estimate at 100 evaluations/day on Gemini 2.5 Flash-Lite paid tier:
- Average tokens per evaluation: ~1,500 input + ~500 output = 2,000 tokens
- 100 evaluations/day × 30 days = 3,000 evaluations/month
- Input: 3,000 × 1,500 = 4.5M tokens × $0.10/M = $0.45
- Output: 3,000 × 500 = 1.5M tokens × $0.40/M = $0.60
- **Total: ~$1.05/month (~₹88/month)**

This is the absolute worst-case cost scenario at the expected traffic level. It is acceptable if the project value warrants it.

**Scenario 3 — Provider switch to Groq free tier**

If Gemini free tier is discontinued, Groq offers 14,400 req/day free on open-source models. No billing required. Quality may be lower for nuanced rubric scoring — requires validation against the sample bank before switching.

Monthly cost: ₹0.

---

### B4 — Spend Controls

Since the primary evaluation engine (Gemini free tier) has no billing attached, there is no risk of unexpected charges from the API. The free tier's daily request cap is enforced by Google's infrastructure — not by application logic.

If a paid tier is ever enabled:
- Set a Google Cloud budget alert at $2/month — triggers an email notification
- Set a hard spend cap at $5/month in Google Cloud Console
- Review monthly usage in Google AI Studio dashboard

No automatic billing escalation is possible on the free tier. This is the primary spend control.

---

### B5 — Cost Comparison — What Was Considered

| Option | Monthly cost at 100 eval/day | Why not chosen |
|--------|------------------------------|----------------|
| Gemini 2.5 Flash-Lite (free) | ₹0 | ✅ Chosen |
| Gemini 2.5 Flash-Lite (paid) | ~₹88 | Fallback only |
| Claude Haiku 4.5 | ~₹30 | Requires separate paid account |
| Claude Sonnet 4.6 | ~₹370 | Not justified at this scale |
| Groq + Llama 4 (free) | ₹0 | Fallback only — quality validation needed |
| Local Ollama | ₹0 | Incompatible with public URL deployment |

---

*Previous: [04 — Tech Stack Decisions](./04_tech_stack_decisions.md)*
*Next: [06 — Roadmap](./06_roadmap.md)*
