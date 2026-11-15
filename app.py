"""Dashboard Streamlit do Field Shift.

Consome o backend FastAPI (clima NASA POWER + motor de rotação). Se o backend
estiver fora do ar, mostra os dados fictícios de src/data/sample_data.py com aviso.

Rodar a partir da raiz do repositório:  streamlit run app.py
Backend esperado em FIELD_SHIFT_API_URL (padrão http://localhost:8000/api/v1).
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.components.geolocation import current_location
from src.components.historical_charts import render_historical_charts
from src.components.indicator_cards import render_indicator_cards
from src.components.recommendation_details import render_recommendation_details
from src.components.rotation_comparison import render_rotation_comparison
from src.components.strategy_ranking import render_strategy_ranking
from src.data import api_client
from src.data.dashboard_data import load_real_dashboard, load_sample_dashboard
from src.models.dashboard import DashboardData

NEW_FARM = "__new__"
SOIL_LABELS = {"clay": "Clay", "sandy": "Sandy", "loam": "Loam", "silt": "Silt"}
CROP_ALIASES = {
    "soja": "soybean", "milho": "corn", "aveia": "oats", "trigo": "wheat", "feijão": "bean", "feijao": "bean",
}
PRIORITY_LABELS = {
    "soil_health": "Soil health",
    "water_efficiency": "Water efficiency",
    "climate_resilience": "Climate resilience",
    "diversification": "Diversification",
}


st.set_page_config(page_title="Field Shift | Decision Dashboard", page_icon="🌱", layout="wide")

css_path = Path(__file__).parent / "src" / "styles" / "dashboard.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.title("Field Shift")
st.caption("Decision-support dashboard to compare crop rotation strategies.")


def normalize_priorities(weights: dict[str, int]) -> dict[str, int]:
    """Converte os pesos dos sliders em porcentagens inteiras que somam 100 (exigência do backend)."""
    total = sum(weights.values())
    if total == 0:
        weights, total = {key: 1 for key in weights}, len(weights)
    raw = {key: value * 100 / total for key, value in weights.items()}
    result = {key: int(value) for key, value in raw.items()}
    remainder = 100 - sum(result.values())
    for key in sorted(raw, key=lambda k: raw[k] - result[k], reverse=True)[:remainder]:
        result[key] += 1
    return result


def render_dashboard(data: DashboardData) -> None:
    if data.is_demo:
        st.warning(data.source_note, icon="⚠️")
    for message in data.warnings:
        st.warning(message)

    st.subheader("Site conditions")
    if data.indicators:
        render_indicator_cards(data.indicators)
    else:
        st.info("No climate data is available for this farm right now.")

    if data.historical is not None and not data.historical.empty:
        st.divider()
        render_historical_charts(data.historical, data.history_caption)

    st.divider()
    render_rotation_comparison(data.strategies)

    left, right = st.columns([1, 1])
    with left:
        render_strategy_ranking(data.strategies)
    with right:
        render_recommendation_details(
            max(data.strategies, key=lambda item: item.score),
            "A starting point for the technical discussion; it does not replace advice from an agronomist.",
        )

    st.divider()
    st.caption(data.source_note)


def render_sample_fallback(reason: str) -> None:
    st.error(
        f"{reason}\n\nShowing **fictional demo data**. To see real data, start the backend:\n\n"
        "`cd field-shift-backend; .\\.venv\\Scripts\\Activate.ps1; uvicorn main:app --reload`",
        icon="🔌",
    )
    render_dashboard(load_sample_dashboard())


def render_new_farm_form() -> None:
    st.subheader("Register a farm")
    st.caption("The location is filled in with the device's current position (the browser asks for permission).")

    st.session_state.setdefault("new_lat", None)
    st.session_state.setdefault("new_lon", None)

    # Pede a posição automaticamente só na primeira vez que o formulário aparece; depois, pelo botão.
    location = current_location(auto=not st.session_state.get("geo_requested", False))
    st.session_state["geo_requested"] = True
    if location:
        if "error" in location:
            st.session_state["geo_message"] = ("error", location["error"])
        else:
            st.session_state["new_lat"] = location["latitude"]
            st.session_state["new_lon"] = location["longitude"]
            st.session_state["geo_message"] = ("ok", location["accuracy"])

    kind, value = st.session_state.get("geo_message", (None, None))
    if kind == "ok":
        st.success(f"Current location found (accuracy ±{value:.0f} m).")
    elif kind == "error":
        st.warning(f"{value} Allow location access in the browser or enter the coordinates.")

    left, right = st.columns(2)
    with left:
        name = st.text_input("Farm name", placeholder="Double K Ranch")
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%.6f", key="new_lat")
        soil = st.selectbox("Soil type", list(SOIL_LABELS), format_func=SOIL_LABELS.get)
        irrigation = st.checkbox("Irrigation available")
    with right:
        area = st.number_input("Area (ha)", min_value=0.1, value=120.0, step=1.0)
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%.6f", key="new_lon")
        crops_text = st.text_input("Previous crops (comma-separated)", value="soybean, corn")

    has_location = latitude is not None and longitude is not None
    if has_location:
        st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}), zoom=13, height=260)

    if st.button("Register and analyze", type="primary", disabled=not has_location or not name.strip()):
        previous = [CROP_ALIASES.get(c.strip().lower(), c.strip().lower()) for c in crops_text.split(",") if c.strip()]
        try:
            farm = api_client.create_farm(
                {
                    "name": name.strip(),
                    "latitude": latitude,
                    "longitude": longitude,
                    "area_hectares": area,
                    "soil_type": soil,
                    "irrigation": irrigation,
                    "previous_crops": previous,
                }
            )
        except api_client.BackendUnavailable as exc:
            st.error(str(exc))
            return
        except api_client.BackendError as exc:
            st.error(f"The backend rejected the farm: {exc.detail}")
            return
        st.session_state["selected_farm_id"] = farm["id"]
        for key in ("new_lat", "new_lon", "geo_requested", "geo_message"):
            st.session_state.pop(key, None)
        st.rerun()


# --- Fluxo principal --------------------------------------------------------

if not api_client.health():
    render_sample_fallback(f"Backend unavailable at {api_client.API_URL}.")
    st.stop()

try:
    farms = {farm["id"]: farm for farm in api_client.list_farms()}
except (api_client.BackendUnavailable, api_client.BackendError) as exc:
    render_sample_fallback(f"Failed to list farms: {exc}")
    st.stop()

with st.sidebar:
    st.header("Farm")
    choices = [*farms, NEW_FARM]
    selected = st.session_state.get("selected_farm_id")
    default_index = choices.index(selected) if selected in choices else 0
    choice = st.selectbox(
        "Farm",
        choices,
        index=default_index,
        format_func=lambda c: "➕ Register a new farm" if c == NEW_FARM else f"{farms[c]['name']} ({c})",
        label_visibility="collapsed",
    )
    st.session_state["selected_farm_id"] = choice

if choice == NEW_FARM:
    render_new_farm_form()
    st.stop()

farm = farms[choice]
with st.sidebar:
    st.caption(
        f"📍 {farm['latitude']:.5f}, {farm['longitude']:.5f} · {farm['area_hectares']:.0f} ha · "
        f"{SOIL_LABELS.get(farm['soil_type'], farm['soil_type']).lower()} soil · "
        f"{'with' if farm['irrigation'] else 'no'} irrigation"
    )
    st.header("Priorities")
    weights = {key: st.slider(label, 0, 100, 25, step=5, key=f"w_{key}") for key, label in PRIORITY_LABELS.items()}
    priorities = normalize_priorities(weights)
    st.caption("Normalized weights: " + " · ".join(f"{PRIORITY_LABELS[k]} {v}%" for k, v in priorities.items()))

st.markdown(f"#### {farm['name']}")
try:
    with st.spinner("Fetching NASA POWER climate data and computing the rotation..."):
        dashboard = load_real_dashboard(farm, priorities)
except api_client.BackendUnavailable as exc:
    render_sample_fallback(f"The backend went down during the analysis ({exc}).")
    st.stop()
except api_client.BackendError as exc:
    st.error(f"The backend returned an error: {exc.detail}")
    st.stop()

render_dashboard(dashboard)
