// Espelho dos schemas Pydantic em field-shift-backend/app/schemas/.
// Se mudar um lado, mude o outro no MESMO pull request.

export type SoilType = "clay" | "sandy" | "loam" | "silt";

export interface FarmCreate {
  name: string;
  latitude: number;
  longitude: number;
  area_hectares: number;
  soil_type: SoilType;
  irrigation: boolean;
  previous_crops: string[];
}

export interface Farm extends FarmCreate {
  id: string;
}

export interface MonthlyClimate {
  month: string; // YYYY-MM
  temperature_c: number;
  precipitation_mm_day: number;
}

export interface ClimateResponse {
  location: { latitude: number; longitude: number };
  period: string;
  temperature_avg_c: number;
  precipitation_avg_mm_day: number;
  monthly: MonthlyClimate[];
  source: string;
  is_mock: boolean;
}

export interface Priorities {
  soil_health: number;
  water_efficiency: number;
  climate_resilience: number;
  diversification: number;
}

export interface RotationAnalyzeRequest {
  farm_id: string;
  priorities: Priorities;
}

export interface Recommendation {
  strategy: string;
  score: number;
  crops: string[];
  criteria: Record<string, number>;
  benefits: string[];
  risks: string[];
  rationale: string[];
}

export interface RotationAnalyzeResponse {
  farm_id: string;
  recommendations: Recommendation[];
  is_mock: boolean;
}

export interface Crop {
  id: string;
  name: string;
  family: string;
  season: string;
  nitrogen_fixing: boolean;
  water_demand: string;
  temperature_range_c: [number, number];
}
