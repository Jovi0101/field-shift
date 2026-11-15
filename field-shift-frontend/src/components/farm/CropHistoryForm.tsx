interface Props {
  value: string;
  onChange: (value: string) => void;
}

export function CropHistoryForm({ value, onChange }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Histórico de culturas</legend>
      <label>
        Culturas anteriores
        <input value={value} onChange={(event) => onChange(event.target.value)} placeholder="Ex.: soja, milho" />
      </label>
      <p className="field-help">Separe as culturas por vírgula. O último item é tratado como a cultura mais recente.</p>
    </fieldset>
  );
}
