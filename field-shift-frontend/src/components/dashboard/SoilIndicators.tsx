import type { Farm } from "../../types/api";

const SOIL_NAMES: Record<Farm["soil_type"], string> = {
  clay: "Argiloso",
  sandy: "Arenoso",
  loam: "Franco",
  silt: "Siltoso",
};

export function SoilIndicators({ farm }: { farm: Farm }) {
  return (
    <section className="card indicators-card">
      <p className="eyebrow">Perfil cadastrado</p>
      <h3>Indicadores da propriedade</h3>
      <dl className="indicator-list">
        <div><dt>Área</dt><dd>{farm.area_hectares} ha</dd></div>
        <div><dt>Solo</dt><dd>{SOIL_NAMES[farm.soil_type]}</dd></div>
        <div><dt>Irrigação</dt><dd>{farm.irrigation ? "Disponível" : "Não informada"}</dd></div>
        <div><dt>Histórico</dt><dd>{farm.previous_crops.length ? farm.previous_crops.join(" → ") : "Não informado"}</dd></div>
      </dl>
    </section>
  );
}
