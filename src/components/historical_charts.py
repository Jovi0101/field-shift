import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render_historical_charts(data: pd.DataFrame) -> None:
    st.subheader("Histórico climático")
    st.caption("Série demonstrativa. Substitua por dados validados da propriedade.")

    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(
        go.Scatter(
            x=data["Mês"],
            y=data["Temperatura (°C)"],
            name="Temperatura",
            mode="lines+markers",
            line={"color": "#d97706", "width": 3},
        ),
        secondary_y=False,
    )
    figure.add_trace(
        go.Bar(
            x=data["Mês"],
            y=data["Precipitação (mm)"],
            name="Precipitação",
            marker_color="#3b82f6",
            opacity=0.55,
        ),
        secondary_y=True,
    )

    figure.update_layout(
        height=380,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        legend={"orientation": "h", "y": 1.12, "x": 0},
        hovermode="x unified",
    )
    figure.update_yaxes(title_text="Temperatura (°C)", secondary_y=False)
    figure.update_yaxes(title_text="Precipitação (mm)", secondary_y=True)
    st.plotly_chart(figure, use_container_width=True)
