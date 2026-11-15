import { api } from "./api";
import type { Farm, FarmCreate } from "../types/api";

export const farmService = {
  create: (farm: FarmCreate): Promise<Farm> => api.createFarm(farm),
};
