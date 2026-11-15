import type { FormEvent } from "react";
import type { FarmDraft, LocationStatus } from "../../hooks/useFarm";
import type { SoilType } from "../../types/api";
import { CropHistoryForm } from "./CropHistoryForm";
import { FarmLocationMap } from "./FarmLocationMap";
import { SoilForm } from "./SoilForm";

interface Props {
  form: FarmDraft;
  cropsText: string;
  loading: boolean;
  error: string | null;
  locationStatus: LocationStatus;
  onFieldChange: <K extends keyof FarmDraft>(key: K, value: FarmDraft[K]) => void;
  onCropsChange: (value: string) => void;
  onUseCurrentLocation: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}

export function FarmForm({
  form,
  cropsText,
  loading,
  error,
  locationStatus,
  onFieldChange,
  onCropsChange,
  onUseCurrentLocation,
  onSubmit,
}: Props) {
  const missingLocation = form.latitude === null || form.longitude === null;
  return (
    <form className="farm-form card" onSubmit={onSubmit}>
      <p className="eyebrow">Step 1 of 2</p>
      <h2>Tell us about the farm</h2>
      <p className="muted">With just a few fields, Field Shift prepares initial rotation scenarios for your season planning.</p>

      <fieldset className="form-section">
        <legend>General information</legend>
        <div className="form-grid">
          <label>
            Farm name
            <input value={form.name} onChange={(event) => onFieldChange("name", event.target.value)} required />
          </label>
          <label>
            Area (ha)
            <input type="number" min="0.1" step="any" value={form.area_hectares} onChange={(event) => onFieldChange("area_hectares", Number(event.target.value))} required />
          </label>
        </div>
      </fieldset>

      <FarmLocationMap
        latitude={form.latitude}
        longitude={form.longitude}
        status={locationStatus}
        onLatitudeChange={(value) => onFieldChange("latitude", value)}
        onLongitudeChange={(value) => onFieldChange("longitude", value)}
        onUseCurrentLocation={onUseCurrentLocation}
      />
      <SoilForm
        soilType={form.soil_type}
        irrigation={form.irrigation}
        onSoilTypeChange={(value: SoilType) => onFieldChange("soil_type", value)}
        onIrrigationChange={(value) => onFieldChange("irrigation", value)}
      />
      <CropHistoryForm value={cropsText} onChange={onCropsChange} />
      {error && <p className="error">{error}</p>}
      <button className="primary-action" type="submit" disabled={loading || missingLocation}>{loading ? "Preparing analysis..." : "See farm analysis"}</button>
    </form>
  );
}
