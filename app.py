from pathlib import Path

import streamlit as st

from src.components.historical_charts import render_historical_charts
from src.components.indicator_cards import render_indicator_cards
from src.components.recommendation_details import render_recommendation_details
from src.components.rotation_comparison import render_rotation_comparison
from src.components.strategy_ranking import render_strategy_ranking
from src.data.sample_data import (
    get_historical_data,
    get_indicators,
    get_strategies,
)


st.set_page_config(
    page_title="Field Shift | Decision Dashboard",
    page_icon="🌱",
    layout="wide",
)

css_path = Path(__file__).parent / "src" / "styles" / "dashboard.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

st.title("Field Shift")
st.caption("Painel de apoio à decisão para comparar estratégias de rotação.")

with st.sidebar:
    st.header("Filtros")
    st.selectbox("Propriedade", ["Propriedade demonstrativa"])
    st.selectbox("Safra", ["2025/2026", "2024/2025"])

st.subheader("Indicadores ambientais")
render_indicator_cards(get_indicators())

st.divider()
render_historical_charts(get_historical_data())

st.divider()
strategies = get_strategies()
render_rotation_comparison(strategies)

left, right = st.columns([1, 1])
with left:
    render_strategy_ranking(strategies)
with right:
    recommended_strategy = max(strategies, key=lambda item: item.score)
    render_recommendation_details(recommended_strategy)

st.divider()
st.caption(
    "Protótipo com dados fictícios. Conecte fontes validadas antes de usar "
    "as informações em decisões de produção."
)
