import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// O proxy evita problemas de CORS em dev: o frontend chama /api/... e o Vite repassa ao FastAPI.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
