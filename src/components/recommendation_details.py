import streamlit as st

from src.models.dashboard import Strategy


def render_recommendation_details(strategy: Strategy) -> None:
    st.subheader("Recomendação e riscos")
    st.markdown(f"### Estratégia recomendada: {strategy.name}")
    st.write(strategy.justification)

    with st.expander("Ver riscos e pontos de atenção"):
        for risk in strategy.risks:
            st.markdown(f"- {risk}")

    st.caption(
        "Esta recomendação usa dados fictícios e não deve orientar decisões de plantio."
    )
