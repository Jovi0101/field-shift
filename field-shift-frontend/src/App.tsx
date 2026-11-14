import { useState } from "react";
import type { Farm } from "./types/api";
import FarmProfilePage from "./pages/FarmProfilePage";
import DashboardPage from "./pages/DashboardPage";

// Fluxo do MVP: cadastrar propriedade (Integrante 03) -> dashboard (Integrante 04).
export default function App() {
  const [farm, setFarm] = useState<Farm | null>(null);

  return (
    <div className="app">
      <h1>Field Shift</h1>
      {farm ? (
        <DashboardPage farm={farm} onBack={() => setFarm(null)} />
      ) : (
        <FarmProfilePage onCreated={setFarm} />
      )}
    </div>
  );
}
