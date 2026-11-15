import type { ClimateResponse } from "../../types/api";

export function ClimateSummary({ climate }: { climate: ClimateResponse }) {
  return (
    <section className="card climate-summary">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Site conditions</p>
          <h3>Climate {climate.period}</h3>
        </div>
        {climate.is_mock && <span className="status-pill">Demo data</span>}
      </div>
      <div className="metric-grid">
        <div className="metric"><span>Average temperature</span><strong>{climate.temperature_avg_c}°C</strong></div>
        <div className="metric"><span>Average precipitation</span><strong>{climate.precipitation_avg_mm_day} <small>mm/day</small></strong></div>
        <div className="metric"><span>Location</span><strong>{climate.location.latitude.toFixed(2)}°, {climate.location.longitude.toFixed(2)}°</strong></div>
      </div>
      <p className="source-note">Source: {climate.source}. Averages provide context for the conversation with the grower.</p>
    </section>
  );
}
