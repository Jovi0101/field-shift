import type { LocationStatus } from "../../hooks/useFarm";

interface Props {
  latitude: number | null;
  longitude: number | null;
  status: LocationStatus;
  onLatitudeChange: (value: number | null) => void;
  onLongitudeChange: (value: number | null) => void;
  onUseCurrentLocation: () => void;
}

function parseCoordinate(raw: string): number | null {
  return raw.trim() === "" ? null : Number(raw);
}

function statusText(status: LocationStatus): string {
  switch (status.state) {
    case "locating":
      return "Getting the device's current location...";
    case "located":
      return `Current location found (accuracy ±${Math.round(status.accuracy)} m).`;
    case "manual":
      return "Coordinates entered manually.";
    case "error":
      return `${status.message} Allow location access or enter the coordinates.`;
    default:
      return "We use the device's current location; check the point on the map before analyzing.";
  }
}

/**
 * The location comes from the browser's geolocation (GPS when available).
 * The fields stay editable for users registering a farm while away from it.
 */
export function FarmLocationMap({
  latitude,
  longitude,
  status,
  onLatitudeChange,
  onLongitudeChange,
  onUseCurrentLocation,
}: Props) {
  const hasPoint = latitude !== null && longitude !== null;
  const mapUrl = hasPoint
    ? `https://www.openstreetmap.org/?mlat=${latitude}&mlon=${longitude}#map=16/${latitude}/${longitude}`
    : null;

  return (
    <fieldset className="form-section">
      <legend>Farm location</legend>
      <p className={status.state === "error" ? "field-help location-error" : "field-help"} role="status">
        {statusText(status)}
      </p>
      <div className="form-grid">
        <label>
          Latitude
          <input
            type="number"
            step="any"
            min="-90"
            max="90"
            value={latitude ?? ""}
            placeholder={status.state === "locating" ? "Locating..." : ""}
            onChange={(event) => onLatitudeChange(parseCoordinate(event.target.value))}
            required
          />
        </label>
        <label>
          Longitude
          <input
            type="number"
            step="any"
            min="-180"
            max="180"
            value={longitude ?? ""}
            placeholder={status.state === "locating" ? "Locating..." : ""}
            onChange={(event) => onLongitudeChange(parseCoordinate(event.target.value))}
            required
          />
        </label>
      </div>
      <div className="location-actions">
        <button type="button" className="back-button" onClick={onUseCurrentLocation} disabled={status.state === "locating"}>
          {status.state === "locating" ? "Locating..." : "Use my current location"}
        </button>
        {mapUrl && (
          <a className="map-link" href={mapUrl} target="_blank" rel="noreferrer">Check point on map ↗</a>
        )}
      </div>
    </fieldset>
  );
}
