import type { ClimateResponse } from "../../types/api";

export function ClimateHistoryChart({ climate }: { climate: ClimateResponse }) {
  const months = climate.monthly.slice(-12);
  const maxRain = Math.max(...months.map((month) => month.precipitation_mm_day), 1);
  const maxTemp = Math.max(...months.map((month) => month.temperature_c), 1);

  return (
    <section className="card climate-chart">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Histórico recente</p>
          <h3>Temperatura e chuva</h3>
        </div>
        <span className="chart-legend"><i className="legend-temp" /> temperatura <i className="legend-rain" /> chuva</span>
      </div>
      <div className="chart-bars" aria-label="Histórico climático dos últimos 12 meses disponíveis">
        {months.map((month) => (
          <div className="chart-column" key={month.month} title={`${month.month}: ${month.temperature_c}°C e ${month.precipitation_mm_day} mm/dia`}>
            <div className="bars">
              <span className="bar temp" style={{ height: `${Math.max(12, (month.temperature_c / maxTemp) * 100)}%` }} />
              <span className="bar rain" style={{ height: `${Math.max(12, (month.precipitation_mm_day / maxRain) * 100)}%` }} />
            </div>
            <small>{month.month.slice(5)}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
