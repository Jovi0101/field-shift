import type { FormEvent } from "react";
import type { FarmCreate, SoilType } from "../../types/api";
import { CropHistoryForm } from "./CropHistoryForm";
import { FarmLocationMap } from "./FarmLocationMap";
import { SoilForm } from "./SoilForm";

interface Props {
  form: FarmCreate;
  cropsText: string;
  loading: boolean;
  error: string | null;
  onFieldChange: <K extends keyof FarmCreate>(key: K, value: FarmCreate[K]) => void;
  onCropsChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}

export function FarmForm({ form, cropsText, loading, error, onFieldChange, onCropsChange, onSubmit }: Props) {
  return (
    <form className="farm-form card" onSubmit={onSubmit}>
      <p className="eyebrow">Etapa 1 de 2</p>
      <h2>Conheça a propriedade</h2>
      <p className="muted">Em poucos campos, o Field Shift prepara cenários iniciais de rotação para a conversa de safra.</p>

      <fieldset className="form-section">
        <legend>Informações gerais</legend>
        <div className="form-grid">
          <label>
            Nome da propriedade
            <input value={form.name} onChange={(event) => onFieldChange("name", event.target.value)} required />
          </label>
          <label>
            Área (ha)
            <input type="number" min="0.1" step="any" value={form.area_hectares} onChange={(event) => onFieldChange("area_hectares", Number(event.target.value))} required />
          </label>
        </div>
      </fieldset>

      <FarmLocationMap
        latitude={form.latitude}
        longitude={form.longitude}
        onLatitudeChange={(value) => onFieldChange("latitude", value)}
        onLongitudeChange={(value) => onFieldChange("longitude", value)}
      />
      <SoilForm
        soilType={form.soil_type}
        irrigation={form.irrigation}
        onSoilTypeChange={(value: SoilType) => onFieldChange("soil_type", value)}
        onIrrigationChange={(value) => onFieldChange("irrigation", value)}
      />
      <CropHistoryForm value={cropsText} onChange={onCropsChange} />
      {error && <p className="error">{error}</p>}
      <button className="primary-action" type="submit" disabled={loading}>{loading ? "Preparando análise..." : "Ver análise da propriedade"}</button>
    </form>
  );
}
