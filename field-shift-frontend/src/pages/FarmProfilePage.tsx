// Dono: Integrante 03 — formulário da propriedade.
// TODO: trocar latitude/longitude por seleção no mapa (Leaflet: npm i leaflet react-leaflet).
import { useState, type FormEvent } from "react";
import { api } from "../services/api";
import type { Farm, FarmCreate, SoilType } from "../types/api";

const INITIAL: FarmCreate = {
  name: "Farm Demo",
  latitude: -29.717,
  longitude: -52.425,
  area_hectares: 120,
  soil_type: "clay",
  irrigation: false,
  previous_crops: ["soybean", "corn"],
};

export default function FarmProfilePage({ onCreated }: { onCreated: (farm: Farm) => void }) {
  const [form, setForm] = useState<FarmCreate>(INITIAL);
  const [cropsText, setCropsText] = useState(INITIAL.previous_crops.join(", "));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const set = <K extends keyof FarmCreate>(key: K, value: FarmCreate[K]) =>
    setForm((f) => ({ ...f, [key]: value }));

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const previous_crops = cropsText.split(",").map((s) => s.trim()).filter(Boolean);
      onCreated(await api.createFarm({ ...form, previous_crops }));
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Cadastro da propriedade</h2>
      <label>
        Nome
        <input value={form.name} onChange={(e) => set("name", e.target.value)} required />
      </label>
      <label>
        Latitude
        <input type="number" step="any" value={form.latitude}
          onChange={(e) => set("latitude", Number(e.target.value))} required />
      </label>
      <label>
        Longitude
        <input type="number" step="any" value={form.longitude}
          onChange={(e) => set("longitude", Number(e.target.value))} required />
      </label>
      <label>
        Área (ha)
        <input type="number" min="0" step="any" value={form.area_hectares}
          onChange={(e) => set("area_hectares", Number(e.target.value))} required />
      </label>
      <label>
        Tipo de solo
        <select value={form.soil_type} onChange={(e) => set("soil_type", e.target.value as SoilType)}>
          <option value="clay">Argiloso</option>
          <option value="sandy">Arenoso</option>
          <option value="loam">Franco</option>
          <option value="silt">Siltoso</option>
        </select>
      </label>
      <label>
        <input type="checkbox" checked={form.irrigation} style={{ display: "inline", width: "auto" }}
          onChange={(e) => set("irrigation", e.target.checked)} /> Possui irrigação
      </label>
      <label>
        Culturas anteriores (separadas por vírgula)
        <input value={cropsText} onChange={(e) => setCropsText(e.target.value)} />
      </label>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>{loading ? "Enviando..." : "Analisar propriedade"}</button>
    </form>
  );
}
