import pandas as pd
import streamlit as st

from src.models.dashboard import RotationStrategy

CRITERIA_LABELS = {
    "soil_health": "Soil health",
    "water_efficiency": "Water efficiency",
    "climate_resilience": "Climate resilience",
    "diversification": "Diversification",
}


def render_rotation_comparison(strategies: list[RotationStrategy]) -> None:
    st.subheader("Rotation comparison")
    st.caption("Scores from 0 to 100 per criterion; the final score weights the criteria by the selected priorities.")

    comparison = pd.DataFrame(
        [
            {
                "Strategy": strategy.name,
                "Score": f"{strategy.score:.0f}/100",
                "Rotation": strategy.rotation,
                **{label: strategy.criteria.get(key) for key, label in CRITERIA_LABELS.items() if strategy.criteria},
            }
            for strategy in strategies
        ]
    )
    st.dataframe(comparison, hide_index=True, width="stretch")
