import pandas as pd
import streamlit as st

from src.models.dashboard import Strategy


def render_rotation_comparison(strategies: list[Strategy]) -> None:
    st.subheader("Comparador de rotações")
    st.caption("Compare os resultados estimados das estratégias.")

    comparison = pd.DataFrame(
        [
            {
                "Estratégia": strategy.name,
                "Pontuação": f"{strategy.score:.0f}/100",
                "Produtividade estimada (t/ha)": strategy.estimated_yield,
                "Uso de água estimado (mm)": strategy.water_use,
                "Saúde do solo": strategy.soil_health,
            }
            for strategy in strategies
        ]
    )
    st.dataframe(comparison, hide_index=True, use_container_width=True)
