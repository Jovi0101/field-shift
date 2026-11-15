import { useEffect, useState } from "react";
import { api } from "../services/api";
import { ClimateHistoryChart } from "../components/dashboard/ClimateHistoryChart";
import { ClimateSummary } from "../components/dashboard/ClimateSummary";
import { PrioritySelector } from "../components/dashboard/PrioritySelector";
import { RecommendationCard } from "../components/dashboard/RecommendationCard";
import { RotationComparison } from "../components/dashboard/RotationComparison";
import { SoilIndicators } from "../components/dashboard/SoilIndicators";
import type { ClimateResponse, Farm, Priorities, RotationAnalyzeResponse } from "../types/api";

const DEFAULT_PRIORITIES = {
  soil_health: 30,
  water_efficiency: 25,
  climate_resilience: 25,
  diversification: 20,
};

export default function DashboardPage({ farm, onBack }: { farm: Farm; onBack: () => void }) {
  const [climate, setClimate] = useState<ClimateResponse | null>(null);
  const [rotation, setRotation] = useState<RotationAnalyzeResponse | null>(null);
  const [priorities, setPriorities] = useState<Priorities>(DEFAULT_PRIORITIES);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const prioritiesAreValid = Object.values(priorities).reduce((sum, value) => sum + value, 0) === 100;

  async function updateRotation(nextPriorities: Priorities) {
    if (!prioritiesAreValid) return;
    setLoading(true);
    setError(null);
    try {
      setRotation(await api.analyzeRotation({ farm_id: farm.id, priorities: nextPriorities }));
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let active = true;
    setLoading(true);
    Promise.allSettled([
      api.getClimate(farm.latitude, farm.longitude),
      api.analyzeRotation({ farm_id: farm.id, priorities: DEFAULT_PRIORITIES }),
    ])
      .then(([climateResult, rotationResult]) => {
        if (!active) return;
        if (climateResult.status === "fulfilled") setClimate(climateResult.value);
        if (rotationResult.status === "fulfilled") setRotation(rotationResult.value);
        const failed = [climateResult, rotationResult].filter((result) => result.status === "rejected");
        if (failed.length) setError("Não foi possível carregar todos os dados. Você ainda pode explorar o resultado disponível.");
      })
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [farm]);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <button className="back-button" onClick={onBack}>← Nova propriedade</button>
        <div>
          <p className="eyebrow">Diagnóstico da safra</p>
          <h2>{farm.name}</h2>
          <p className="muted">Compare cenários de rotação e encontre um ponto de partida para a conversa técnica.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}

      <div className="dashboard-overview">
        {climate && <ClimateSummary climate={climate} />}
        <SoilIndicators farm={farm} />
      </div>
      {climate && <ClimateHistoryChart climate={climate} />}
      <PrioritySelector value={priorities} onChange={setPriorities} />
      <button className="primary-action" onClick={() => updateRotation(priorities)} disabled={!prioritiesAreValid || loading}>
        {loading ? "Atualizando análise..." : "Atualizar recomendações"}
      </button>

      {rotation && <RotationComparison recommendations={rotation.recommendations} />}
      <section className="recommendations-section">
        <div className="section-heading"><div><p className="eyebrow">Resultado</p><h3>Estratégias recomendadas</h3></div></div>
        <div className="recommendations-grid">
          {rotation?.recommendations.map((recommendation, index) => (
            <RecommendationCard key={recommendation.strategy} recommendation={recommendation} rank={index + 1} />
          ))}
        </div>
      </section>
    </div>
  );
}
