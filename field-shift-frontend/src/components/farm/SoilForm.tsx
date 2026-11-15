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
      <legend>Soil and water</legend>
      <div className="form-grid">
        <label>
          Soil type
          <select value={soilType} onChange={(event) => onSoilTypeChange(event.target.value as SoilType)}>
            <option value="clay">Clay</option>
            <option value="sandy">Sandy</option>
            <option value="loam">Loam</option>
            <option value="silt">Silt</option>
          </select>
        </label>
        <label className="checkbox-label">
          <input type="checkbox" checked={irrigation} onChange={(event) => onIrrigationChange(event.target.checked)} />
          <span><strong>Irrigation available</strong><small>The engine uses this when assessing water risk.</small></span>
        </label>
      </div>
    </fieldset>
  );
}
