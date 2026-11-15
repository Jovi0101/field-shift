interface Props {
  latitude: number;
  longitude: number;
  onLatitudeChange: (value: number) => void;
  onLongitudeChange: (value: number) => void;
}

/**
 * Para o MVP a localização é informada por coordenadas. O link permite validar
 * o ponto no OpenStreetMap sem introduzir uma dependência de mapa na demo.
 */
export function FarmLocationMap({ latitude, longitude, onLatitudeChange, onLongitudeChange }: Props) {
  const mapUrl = `https://www.openstreetmap.org/?mlat=${latitude}&mlon=${longitude}#map=10/${latitude}/${longitude}`;

  return (
    <fieldset className="form-section">
      <legend>Localização da propriedade</legend>
      <p className="field-help">Informe as coordenadas ou confira o ponto no mapa antes de analisar.</p>
      <div className="form-grid">
        <label>
          Latitude
          <input type="number" step="any" min="-90" max="90" value={latitude} onChange={(event) => onLatitudeChange(Number(event.target.value))} required />
        </label>
        <label>
          Longitude
          <input type="number" step="any" min="-180" max="180" value={longitude} onChange={(event) => onLongitudeChange(Number(event.target.value))} required />
        </label>
      </div>
      <a className="map-link" href={mapUrl} target="_blank" rel="noreferrer">Conferir ponto no mapa ↗</a>
    </fieldset>
  );
}
