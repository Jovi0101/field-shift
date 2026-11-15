import { useCallback, useEffect, useState, type FormEvent } from "react";
import { api } from "../services/api";
import type { Farm, FarmCreate } from "../types/api";

/** Form draft: the location starts empty until the browser reports the current position. */
export type FarmDraft = Omit<FarmCreate, "latitude" | "longitude"> & {
  latitude: number | null;
  longitude: number | null;
};

export type LocationStatus =
  | { state: "idle" }
  | { state: "locating" }
  | { state: "located"; accuracy: number }
  | { state: "manual" }
  | { state: "error"; message: string };

const INITIAL_FORM: FarmDraft = {
  name: "",
  latitude: null,
  longitude: null,
  area_hectares: 0,
  soil_type: "clay",
  irrigation: false,
  previous_crops: [],
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

const GEOLOCATION_ERRORS: Record<number, string> = {
  1: "Location permission was denied in the browser.",
  2: "Location is unavailable on this device.",
  3: "Timed out while getting the location.",
};

export function useFarm(onCreated: (farm: Farm) => void) {
  const [form, setForm] = useState<FarmDraft>(INITIAL_FORM);
  const [cropsText, setCropsText] = useState(INITIAL_FORM.previous_crops.join(", "));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [locationStatus, setLocationStatus] = useState<LocationStatus>({ state: "idle" });

  const setField = <K extends keyof FarmDraft>(key: K, value: FarmDraft[K]) => {
    if (key === "latitude" || key === "longitude") setLocationStatus({ state: "manual" });
    setForm((current) => ({ ...current, [key]: value }));
  };

  const locateCurrentPosition = useCallback(() => {
    if (!("geolocation" in navigator)) {
      setLocationStatus({ state: "error", message: "This browser does not support geolocation." });
      return;
    }
    setLocationStatus({ state: "locating" });
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setForm((current) => ({
          ...current,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }));
        setLocationStatus({ state: "located", accuracy: position.coords.accuracy });
      },
      (reason) => {
        setLocationStatus({
          state: "error",
          message: GEOLOCATION_ERRORS[reason.code] ?? reason.message,
        });
      },
      // High accuracy (GPS when available) and no cached position: we want the current one.
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 },
    );
  }, []);

  // As soon as the form opens, ask for the device's current position.
  useEffect(() => {
    locateCurrentPosition();
  }, [locateCurrentPosition]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const { latitude, longitude } = form;
    if (latitude === null || longitude === null) {
      setError("Set the farm location: use your current location or enter the coordinates.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const previous_crops = cropsText
        .split(",")
        .map((crop) => crop.trim().toLowerCase())
        .filter(Boolean)
        .map((crop) => CROP_ALIASES[crop] ?? crop);
      onCreated(await api.createFarm({ ...form, latitude, longitude, previous_crops }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setLoading(false);
    }
  }

  return {
    form,
    cropsText,
    loading,
    error,
    locationStatus,
    setField,
    setCropsText,
    locateCurrentPosition,
    submit,
  };
}
