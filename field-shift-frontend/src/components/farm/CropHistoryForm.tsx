interface Props {
  value: string;
  onChange: (value: string) => void;
}

export function CropHistoryForm({ value, onChange }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Crop history</legend>
      <label>
        Previous crops
        <input value={value} onChange={(event) => onChange(event.target.value)} placeholder="e.g. soybean, corn" />
      </label>
      <p className="field-help">Separate crops with commas. The last item is treated as the most recent crop.</p>
    </fieldset>
  );
}
