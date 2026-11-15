import type { Recommendation } from "../../types/api";

export function RotationComparison({ recommendations }: { recommendations: Recommendation[] }) {
  return (
    <section className="card comparison-card">
      <p className="eyebrow">Comparativo</p>
      <h3>Ranking das estratégias</h3>
      <div className="comparison-list">
        {recommendations.map((recommendation, index) => (
          <div className="comparison-row" key={recommendation.strategy}>
            <span className="rank">{index + 1}</span>
            <strong>{recommendation.strategy}</strong>
            <span className="score-meter"><i style={{ width: `${recommendation.score}%` }} /></span>
            <b>{recommendation.score}</b>
          </div>
        ))}
      </div>
    </section>
  );
}
