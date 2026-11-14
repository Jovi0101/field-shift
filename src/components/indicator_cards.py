import streamlit as st

from src.models.dashboard import Indicator


def render_indicator_cards(indicators: list[Indicator]) -> None:
    columns = st.columns(len(indicators))

    for column, indicator in zip(columns, indicators):
        with column:
            st.metric(
                label=indicator.name,
                value=f"{indicator.value} {indicator.unit}".strip(),
                help=indicator.help_text,
            )
