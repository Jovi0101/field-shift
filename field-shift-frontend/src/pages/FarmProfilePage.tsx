import { FarmForm } from "../components/farm/FarmForm";
import { useFarm } from "../hooks/useFarm";
import type { Farm } from "../types/api";

export default function FarmProfilePage({ onCreated }: { onCreated: (farm: Farm) => void }) {
  const farm = useFarm(onCreated);
  return (
    <FarmForm
      form={farm.form}
      cropsText={farm.cropsText}
      loading={farm.loading}
      error={farm.error}
      locationStatus={farm.locationStatus}
      onFieldChange={farm.setField}
      onCropsChange={farm.setCropsText}
      onUseCurrentLocation={farm.locateCurrentPosition}
      onSubmit={farm.submit}
    />
  );
}
