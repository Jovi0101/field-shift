# Field Shift

MVP for farm crop-rotation analysis using farm profile data, climate summaries, and agronomic recommendations.

## Local database

1. Copy `.env.example` to `.env` and adjust local settings if needed.
2. Start PostgreSQL with `docker compose up -d db`.
3. Check status with `docker compose ps`; stop it with `docker compose down`.

The Compose file starts PostgreSQL only. Backend and frontend setup will be added alongside their application code. PostgreSQL data persists in the `postgres_data` volume.

## API contract

See [docs/api-contracts.md](docs/api-contracts.md) for the draft farm, climate, and rotation JSON shapes. The backend's FastAPI OpenAPI document should be treated as the live contract once routes exist.
