import type { ClimateResponse } from "../../types/api";

export function ClimateSummary({ climate }: { climate: ClimateResponse }) {
  return (
    <section className="card climate-summary">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Condições da área</p>
          <h3>Clima em {climate.period}</h3>
        </div>
        {climate.is_mock && <span className="status-pill">Dados demonstrativos</span>}
      </div>
      <div className="metric-grid">
        <div className="metric"><span>Temperatura média</span><strong>{climate.temperature_avg_c}°C</strong></div>
        <div className="metric"><span>Precipitação média</span><strong>{climate.precipitation_avg_mm_day} <small>mm/dia</small></strong></div>
        <div className="metric"><span>Localização</span><strong>{climate.location.latitude.toFixed(2)}°, {climate.location.longitude.toFixed(2)}°</strong></div>
      </div>
      <p className="source-note">Fonte: {climate.source}. Médias usadas como contexto para a conversa com o produtor.</p>
    </section>
  );
}
