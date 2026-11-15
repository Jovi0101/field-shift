import type { ClimateResponse } from "../../types/api";

export function ClimateHistoryChart({ climate }: { climate: ClimateResponse }) {
  const months = climate.monthly.slice(-12);
  const maxRain = Math.max(...months.map((month) => month.precipitation_mm_day), 1);
  const maxTemp = Math.max(...months.map((month) => month.temperature_c), 1);

  return (
    <section className="card climate-chart">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Recent history</p>
          <h3>Temperature and rainfall</h3>
        </div>
        <span className="chart-legend"><i className="legend-temp" /> temperature <i className="legend-rain" /> rainfall</span>
      </div>
      <div className="chart-bars" aria-label="Climate history for the last 12 available months">
        {months.map((month) => (
          <div className="chart-column" key={month.month} title={`${month.month}: ${month.temperature_c}°C and ${month.precipitation_mm_day} mm/day`}>
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
