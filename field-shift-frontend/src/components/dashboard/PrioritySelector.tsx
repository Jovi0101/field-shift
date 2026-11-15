import type { Priorities } from "../../types/api";

const FIELDS: Array<{ key: keyof Priorities; label: string; hint: string }> = [
  { key: "soil_health", label: "Saúde do solo", hint: "cobertura e qualidade do solo" },
  { key: "water_efficiency", label: "Eficiência hídrica", hint: "uso e disponibilidade de água" },
  { key: "climate_resilience", label: "Resiliência climática", hint: "adaptação a variações do clima" },
  { key: "diversification", label: "Diversificação", hint: "alternância de culturas e famílias" },
];

interface Props {
  value: Priorities;
  onChange: (priorities: Priorities) => void;
}

export function PrioritySelector({ value, onChange }: Props) {
  const total = Object.values(value).reduce((sum, item) => sum + item, 0);

  return (
    <section className="card priorities-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Sua estratégia</p>
          <h3>O que é mais importante agora?</h3>
        </div>
        <strong className={total === 100 ? "total-valid" : "total-invalid"}>{total}% / 100%</strong>
      </div>
      <p className="muted">Ajuste os pesos para comparar as recomendações com o objetivo da safra.</p>
      <div className="priority-grid">
        {FIELDS.map(({ key, label, hint }) => (
          <label className="priority-control" key={key}>
            <span><strong>{label}</strong><small>{hint}</small></span>
            <output>{value[key]}%</output>
            <input
              type="range"
              min="0"
              max="100"
              value={value[key]}
              onChange={(event) => onChange({ ...value, [key]: Number(event.target.value) })}
            />
          </label>
        ))}
      </div>
      {total !== 100 && <p className="validation-message">Os quatro pesos precisam somar 100% para atualizar a análise.</p>}
    </section>
  );
}
