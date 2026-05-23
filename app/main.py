import random
import streamlit as st
from engine import evaluate_ad_copy
from samples import ALL_SAMPLES

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Search Ad Copy Evaluator",
    page_icon="🎯",
    layout="wide",
)

# ── Header ─────────────────────────────────────────────────────────────────
st.title("Search Ad Copy Evaluator")
st.caption(
    "Evaluate LLM-generated search ads before you spend a rupee "
    "finding out the hard way"
)

# ── Tabs ───────────────────────────────────────────────────────────────────
tab_evaluate, tab_compare, tab_batch = st.tabs(
    ["Evaluate", "Compare", "Batch"]
)

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — EVALUATE
# ══════════════════════════════════════════════════════════════════════════
with tab_evaluate:
    st.subheader("Single ad evaluation")
    st.write(
        "Paste your own copy or load a sample. "
        "Get a dimensional scorecard in seconds."
    )

    # ── Load random sample ─────────────────────────────────────────────
    if st.button("🎲 Load random sample", key="load_sample"):
        sample = random.choice(ALL_SAMPLES)
        st.session_state["ev_product"] = sample["product_desc"]
        st.session_state["ev_keyword"] = sample["keyword"]
        st.session_state["ev_headline"] = sample["headline"]
        st.session_state["ev_description"] = sample["description"]
        st.session_state["ev_result"] = None

    # ── Inputs ─────────────────────────────────────────────────────────
    product = st.text_area(
        "Product description",
        value=st.session_state.get("ev_product", ""),
        placeholder="Describe your product in 1–5 sentences. Include key features, pricing, and what makes it different.",
        height=100,
        key="ev_product",
    )

    col_kw, col_intent = st.columns([2, 1])
    with col_kw:
        keyword = st.text_input(
            "Target search keyword",
            value=st.session_state.get("ev_keyword", ""),
            placeholder="e.g. buy nike running shoes online",
            key="ev_keyword",
        )
    with col_intent:
        if keyword:
            from engine import infer_intent
            intent_label = infer_intent(keyword)
            st.markdown(f"**Inferred intent**")
            st.markdown(f"`{intent_label}`")

    col_hl, col_desc = st.columns(2)
    with col_hl:
        headline = st.text_input(
            "Ad headline",
            value=st.session_state.get("ev_headline", ""),
            placeholder="Max 30 characters",
            max_chars=30,
            key="ev_headline",
        )
        hl_len = len(headline)
        hl_color = "red" if hl_len > 30 else "gray"
        st.markdown(
            f"<p style='color:{hl_color}; font-size:12px'>{hl_len} / 30</p>",
            unsafe_allow_html=True,
        )

    with col_desc:
        description = st.text_input(
            "Ad description",
            value=st.session_state.get("ev_description", ""),
            placeholder="Max 90 characters",
            max_chars=90,
            key="ev_description",
        )
        desc_len = len(description)
        desc_color = "red" if desc_len > 90 else "gray"
        st.markdown(
            f"<p style='color:{desc_color}; font-size:12px'>{desc_len} / 90</p>",
            unsafe_allow_html=True,
        )

    # ── Live ad preview ────────────────────────────────────────────────
    if headline or description:
        st.markdown("**Ad preview**")
        st.markdown(
            f"""
            <div style='border:1px solid #ddd; border-radius:8px;
                        padding:12px 16px; max-width:600px;
                        background:#fff; color:#000;'>
                <span style='font-size:11px; border:1px solid #888;
                             border-radius:3px; padding:1px 5px;
                             color:#555;'>Sponsored</span><br>
                <span style='font-size:12px; color:#555;'>yoursite.com</span><br>
                <span style='font-size:18px; color:#1a0dab;
                             font-weight:400;'>{headline}</span><br>
                <span style='font-size:13px; color:#444;'>{description}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")

    # ── Evaluate button ────────────────────────────────────────────────
    if st.button("Evaluate", type="primary", key="ev_submit"):
        if not product or not keyword or not headline or not description:
            st.warning("Please fill in all four fields before evaluating.")
        else:
            with st.spinner("Evaluating..."):
                result = evaluate_ad_copy(product, keyword, headline, description)
            st.session_state["ev_result"] = result

    # ── Scorecard output ───────────────────────────────────────────────
    result = st.session_state.get("ev_result")
    if result:
        st.divider()

        # Intent badge
        if result.get("intent"):
            st.markdown(
                f"<span style='background:#e8f0fe; color:#1a73e8; "
                f"padding:4px 10px; border-radius:12px; font-size:13px;'>"
                f"🔍 {result['intent']} intent detected</span>",
                unsafe_allow_html=True,
            )
            st.markdown("")

        # Verdict
        verdict = result["verdict"]
        verdict_map = {
            "READY_TO_SERVE":  ("✅ READY TO SERVE",  "success"),
            "NEEDS_REVISION":  ("⚠️ NEEDS REVISION",  "warning"),
            "REJECT":          ("❌ REJECT",           "error"),
            "NOT_EVALUABLE":   ("🟡 NOT EVALUABLE",   "warning"),
        }
        verdict_label, verdict_type = verdict_map.get(
            verdict, (verdict, "info")
        )

        if verdict_type == "success":
            st.success(f"**{verdict_label}**")
        elif verdict_type == "error":
            st.error(f"**{verdict_label}**")
        else:
            st.warning(f"**{verdict_label}**")

        # Dimension scores
        if result.get("dimensions"):
            st.markdown("**Scorecard**")
            dim_labels = {
                "relevance": "Relevance",
                "intent_alignment": "Intent Alignment",
                "differentiation": "Differentiation",
                "cta_strength": "CTA Strength",
                "character_efficiency": "Character Efficiency",
            }
            for dim_key, dim_label in dim_labels.items():
                dim = result["dimensions"].get(dim_key)
                if dim:
                    score = dim["score"]
                    reasoning = dim["reasoning"]
                    col_name, col_bar, col_score = st.columns([2, 4, 1])
                    with col_name:
                        st.markdown(
                            f"<p style='font-size:13px; margin:4px 0;'>"
                            f"{dim_label}</p>",
                            unsafe_allow_html=True,
                        )
                    with col_bar:
                        st.progress(score / 5)
                    with col_score:
                        st.markdown(
                            f"<p style='font-size:13px; font-weight:600; "
                            f"margin:4px 0;'>{score}/5</p>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f"<p style='font-size:12px; color:#666; "
                        f"margin:-8px 0 8px 0;'>{reasoning}</p>",
                        unsafe_allow_html=True,
                    )

        # Overall score
        if result.get("overall_score") is not None:
            st.markdown(
                f"**Overall score: {result['overall_score']} / 5**"
            )

        # Evaluator note
        if result.get("evaluator_note"):
            st.info(f"💡 {result['evaluator_note']}")

        # Char warnings
        if result.get("char_warnings"):
            for w in result["char_warnings"]:
                st.warning(f"⚠️ {w}")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — COMPARE (placeholder)
# ══════════════════════════════════════════════════════════════════════════
with tab_compare:
    st.subheader("Side-by-side comparison")
    st.info("Coming soon — Milestone 3")

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — BATCH (placeholder)
# ══════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.subheader("Batch evaluation")
    st.info("Coming soon — Milestone 4")