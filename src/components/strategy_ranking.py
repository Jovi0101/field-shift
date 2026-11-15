import streamlit as st

from src.models.dashboard import Strategy


def render_strategy_ranking(strategies: list[Strategy]) -> None:
    st.subheader("Ranking de estratégias")
    ranked = sorted(strategies, key=lambda item: item.score, reverse=True)

    for position, strategy in enumerate(ranked, start=1):
        with st.container(border=True):
            first, second = st.columns([4, 1])
            with first:
                st.markdown(f"**{position}. {strategy.name}**")
                st.caption(f"Rotação: {strategy.rotation}")
            with second:
                st.metric("Pontuação", f"{strategy.score:.0f}/100")
