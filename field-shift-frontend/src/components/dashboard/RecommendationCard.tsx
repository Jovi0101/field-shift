import type { Recommendation } from "../../types/api";

const CROP_NAMES: Record<string, string> = {
  soybean: "Soybean",
  corn: "Corn",
  oats: "Oats",
  wheat: "Wheat",
  bean: "Bean",
};

const CRITERIA_NAMES: Record<string, string> = {
  soil_health: "Soil",
  water_efficiency: "Water",
  climate_resilience: "Climate",
  diversification: "Diversity",
};

export function RecommendationCard({ recommendation, rank }: { recommendation: Recommendation; rank: number }) {
  return (
    <article className={`recommendation-card ${rank === 1 ? "recommendation-top" : ""}`}>
      <div className="recommendation-head">
        <div>
          <span className="rank-label">{rank === 1 ? "Best fit" : `Option ${rank}`}</span>
          <h3>{recommendation.strategy}</h3>
        </div>
        <div className="score-badge"><strong>{recommendation.score}</strong><span>/100</span></div>
      </div>
      <p className="crop-sequence">{recommendation.crops.map((crop) => CROP_NAMES[crop] ?? crop).join("  →  ")}</p>
      <div className="criteria-chips">
        {Object.entries(recommendation.criteria).map(([criterion, score]) => (
          <span key={criterion}>{CRITERIA_NAMES[criterion] ?? criterion}: <b>{score}</b></span>
        ))}
      </div>
      <div className="recommendation-details">
        <div><strong>Benefits</strong><ul>{recommendation.benefits.map((item) => <li key={item}>{item}</li>)}</ul></div>
        <div><strong>Watch points</strong><ul>{recommendation.risks.map((item) => <li key={item}>{item}</li>)}</ul></div>
      </div>
      <details>
        <summary>Why this option?</summary>
        <ul>{recommendation.rationale.map((item) => <li key={item}>{item}</li>)}</ul>
      </details>
    </article>
  );
}
