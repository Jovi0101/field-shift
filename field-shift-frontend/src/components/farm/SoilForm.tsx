import type { SoilType } from "../../types/api";

interface Props {
  soilType: SoilType;
  irrigation: boolean;
  onSoilTypeChange: (value: SoilType) => void;
  onIrrigationChange: (value: boolean) => void;
}

export function SoilForm({ soilType, irrigation, onSoilTypeChange, onIrrigationChange }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Solo e água</legend>
      <div className="form-grid">
        <label>
          Tipo de solo
          <select value={soilType} onChange={(event) => onSoilTypeChange(event.target.value as SoilType)}>
            <option value="clay">Argiloso</option>
            <option value="sandy">Arenoso</option>
            <option value="loam">Franco</option>
            <option value="silt">Siltoso</option>
          </select>
        </label>
        <label className="checkbox-label">
          <input type="checkbox" checked={irrigation} onChange={(event) => onIrrigationChange(event.target.checked)} />
          <span><strong>Irrigação disponível</strong><small>O motor considera essa informação ao avaliar o risco hídrico.</small></span>
        </label>
      </div>
    </fieldset>
  );
}
