import type { Farm } from "../../types/api";

const SOIL_NAMES: Record<Farm["soil_type"], string> = {
  clay: "Clay",
  sandy: "Sandy",
  loam: "Loam",
  silt: "Silt",
};

export function SoilIndicators({ farm }: { farm: Farm }) {
  return (
    <section className="card indicators-card">
      <p className="eyebrow">Registered profile</p>
      <h3>Farm indicators</h3>
      <dl className="indicator-list">
        <div><dt>Area</dt><dd>{farm.area_hectares} ha</dd></div>
        <div><dt>Soil</dt><dd>{SOIL_NAMES[farm.soil_type]}</dd></div>
        <div><dt>Irrigation</dt><dd>{farm.irrigation ? "Available" : "Not provided"}</dd></div>
        <div><dt>Crop history</dt><dd>{farm.previous_crops.length ? farm.previous_crops.join(" → ") : "Not provided"}</dd></div>
      </dl>
    </section>
  );
}
