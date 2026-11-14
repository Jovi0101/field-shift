// Dono: Integrante 04 — dashboard de resultados.
// TODO: gráficos de climate.monthly (ex.: npm i recharts), comparador e ranking visual.
import { useEffect, useState } from "react";
import { api } from "../services/api";
import type { ClimateResponse, Farm, RotationAnalyzeResponse } from "../types/api";

const DEFAULT_PRIORITIES = {
  soil_health: 30,
  water_efficiency: 25,
  climate_resilience: 25,
  diversification: 20,
};

export default function DashboardPage({ farm, onBack }: { farm: Farm; onBack: () => void }) {
  const [climate, setClimate] = useState<ClimateResponse | null>(null);
  const [rotation, setRotation] = useState<RotationAnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.getClimate(farm.latitude, farm.longitude),
      api.analyzeRotation({ farm_id: farm.id, priorities: DEFAULT_PRIORITIES }),
    ])
      .then(([c, r]) => {
        setClimate(c);
        setRotation(r);
      })
      .catch((err) => setError(err instanceof Error ? err.message : String(err)));
  }, [farm]);

  return (
    <div>
      <button onClick={onBack}>← Voltar</button>
      <h2>{farm.name}</h2>
      {error && <p className="error">{error}</p>}

      {climate && (
        <section className="card">
          <h3>Clima ({climate.period}) {climate.is_mock && <small>(mock)</small>}</h3>
          <p>Temperatura média: {climate.temperature_avg_c} °C</p>
          <p>Precipitação média: {climate.precipitation_avg_mm_day} mm/dia</p>
          <small>Fonte: {climate.source}</small>
        </section>
      )}

      {rotation?.recommendations.map((rec) => (
        <section className="card" key={rec.strategy}>
          <h3>{rec.strategy} — {rec.score}/100</h3>
          <p>{rec.crops.join(" → ")}</p>
          <strong>Benefícios</strong>
          <ul>{rec.benefits.map((b) => <li key={b}>{b}</li>)}</ul>
          <strong>Riscos</strong>
          <ul>{rec.risks.map((r) => <li key={r}>{r}</li>)}</ul>
        </section>
      ))}
    </div>
  );
}
