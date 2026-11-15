import { useState, type FormEvent } from "react";
import { farmService } from "../services/farmService";
import type { Farm, FarmCreate } from "../types/api";

const INITIAL_FORM: FarmCreate = {
  name: "Fazenda Demo",
  latitude: -29.717,
  longitude: -52.425,
  area_hectares: 120,
  soil_type: "clay",
  irrigation: false,
  previous_crops: ["soybean", "corn"],
};

const CROP_ALIASES: Record<string, string> = {
  soja: "soybean",
  soybean: "soybean",
  milho: "corn",
  corn: "corn",
  aveia: "oats",
  oats: "oats",
  trigo: "wheat",
  wheat: "wheat",
  feijão: "bean",
  feijao: "bean",
  bean: "bean",
};

export function useFarm(onCreated: (farm: Farm) => void) {
  const [form, setForm] = useState<FarmCreate>(INITIAL_FORM);
  const [cropsText, setCropsText] = useState(INITIAL_FORM.previous_crops.join(", "));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const setField = <K extends keyof FarmCreate>(key: K, value: FarmCreate[K]) =>
    setForm((current) => ({ ...current, [key]: value }));

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const previous_crops = cropsText
        .split(",")
        .map((crop) => crop.trim().toLowerCase())
        .filter(Boolean)
        .map((crop) => CROP_ALIASES[crop] ?? crop);
      onCreated(await farmService.create({ ...form, previous_crops }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setLoading(false);
    }
  }

  return { form, cropsText, loading, error, setField, setCropsText, submit };
}
