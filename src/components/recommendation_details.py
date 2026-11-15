import streamlit as st

from src.models.dashboard import RotationStrategy


def render_recommendation_details(strategy: RotationStrategy, caption: str) -> None:
    st.subheader("Recommendation and risks")
    st.markdown(f"### Recommended strategy: {strategy.name}")
    st.caption(f"Rotation: {strategy.rotation}")

    for line in strategy.rationale:
        st.markdown(f"- {line}")

    if strategy.benefits:
        with st.expander("Benefits"):
            for benefit in strategy.benefits:
                st.markdown(f"- {benefit}")

    with st.expander("Risks and watch points"):
        for risk in strategy.risks:
            st.markdown(f"- {risk}")

    st.caption(caption)
