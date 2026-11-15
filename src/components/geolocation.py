"""Localização atual do dispositivo via navigator.geolocation (st.components.v2, sem dependência extra).

O navegador pede permissão ao usuário. Funciona em http://localhost ou HTTPS (contexto seguro).
"""
import streamlit as st

_HTML = """
<div class="fs-geo">
  <button type="button">📍 Use my current location</button>
  <span class="fs-geo-status"></span>
</div>
"""

_CSS = """
.fs-geo { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; font-family: var(--st-font, sans-serif); }
.fs-geo button {
  padding: 6px 14px; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--st-border-color, #ccc);
  background: var(--st-secondary-background-color, #f0f2f6); color: var(--st-text-color, inherit);
}
.fs-geo button:disabled { opacity: .6; cursor: default; }
.fs-geo-status { font-size: .85rem; opacity: .8; }
"""

_JS = """
export default function (component) {
  const { data, setTriggerValue, parentElement } = component;
  const button = parentElement.querySelector("button");
  const status = parentElement.querySelector(".fs-geo-status");
  const MESSAGES = {
    1: "Location permission was denied in the browser.",
    2: "Location is unavailable on this device.",
    3: "Timed out while getting the location.",
  };

  function locate() {
    if (!("geolocation" in navigator)) {
      setTriggerValue("location", { error: "This browser does not support geolocation." });
      return;
    }
    button.disabled = true;
    status.textContent = "Getting the current location...";
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        button.disabled = false;
        status.textContent = "";
        setTriggerValue("location", {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
        });
      },
      (err) => {
        button.disabled = false;
        status.textContent = "";
        setTriggerValue("location", { error: MESSAGES[err.code] || err.message });
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 },
    );
  }

  button.onclick = locate;
  if (data && data.auto) locate();
}
"""

_geolocation = st.components.v2.component("field_shift_geolocation", html=_HTML, css=_CSS, js=_JS)


def current_location(auto: bool, key: str = "geolocation") -> dict | None:
    """Mostra o botão e devolve {latitude, longitude, accuracy} ou {error} quando o navegador responde.

    auto=True pede a localização assim que o componente aparece.
    Devolve None nas execuções em que o navegador não enviou nada novo.
    """
    result = _geolocation(key=key, data={"auto": auto}, on_location_change=lambda: None)
    return getattr(result, "location", None)
