import type { Priorities } from "../../types/api";

const FIELDS: Array<{ key: keyof Priorities; label: string; hint: string }> = [
  { key: "soil_health", label: "Soil health", hint: "soil cover and quality" },
  { key: "water_efficiency", label: "Water efficiency", hint: "water use and availability" },
  { key: "climate_resilience", label: "Climate resilience", hint: "adapting to climate variability" },
  { key: "diversification", label: "Diversification", hint: "alternating crops and families" },
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
          <p className="eyebrow">Your strategy</p>
          <h3>What matters most right now?</h3>
        </div>
        <strong className={total === 100 ? "total-valid" : "total-invalid"}>{total}% / 100%</strong>
      </div>
      <p className="muted">Adjust the weights to compare recommendations against your season goal.</p>
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
      {total !== 100 && <p className="validation-message">The four weights must add up to 100% to update the analysis.</p>}
    </section>
  );
}
