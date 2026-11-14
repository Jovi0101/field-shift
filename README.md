# Field Shift

Recomendações de rotação de culturas usando dados ambientais da NASA.

- **Backend:** Python + FastAPI (`field-shift-backend/`)
- **Frontend:** React + TypeScript + Vite (`field-shift-frontend/`)
- **Banco:** PostgreSQL via Docker (opcional até o marco de 60% — as fazendas ficam em memória por enquanto)

## Pré-requisitos

Python 3.12+, Node 20 LTS, Git. Docker Desktop só quando o Postgres entrar.

## Rodando

**Backend** (http://localhost:8000, documentação em http://localhost:8000/docs):

```bash
cd field-shift-backend
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env          # Linux/macOS: cp .env.example .env
uvicorn main:app --reload
```

Testes de contrato: `pytest` (dentro de `field-shift-backend/`).

**Frontend** (http://localhost:5173; `/api` é repassado para o backend pelo proxy do Vite):

```bash
cd field-shift-frontend
npm install
npm run dev
```

**Banco** (quando for usar): `docker compose up -d db`

## Contratos de API

A fonte da verdade são os schemas Pydantic em `field-shift-backend/app/schemas/`, espelhados em
`field-shift-frontend/src/types/api.ts`. Mudou um, muda o outro **no mesmo PR**.

| Rota | Dono | Estado |
| --- | --- | --- |
| `POST /api/v1/farms` → retorna a fazenda com `id` | 05 | em memória |
| `GET /api/v1/farms/{id}` | 05 | em memória |
| `GET /api/v1/environment/climate?latitude=&longitude=` | 01 | **NASA POWER real** (mensal 2020–2024; `USE_MOCK_CLIMATE=true` para offline) |
| `POST /api/v1/rotation/analyze` | 02 | mock fixo |

Unidades: temperatura em °C, precipitação em **mm/dia** (como a NASA POWER entrega).
Respostas mockadas trazem `"is_mock": true`.

## Quem mexe onde

| Integrante | Arquivos principais |
| --- | --- |
| 01 NASA Data | `app/integrations/nasa/`, `app/services/climate_service.py` |
| 02 Agronomic Engine | `app/services/crop_catalog.py`, `app/services/rotation_service.py` |
| 03 Farm Profile | `src/pages/FarmProfilePage.tsx`, componentes de mapa |
| 04 Dashboard | `src/pages/DashboardPage.tsx`, componentes de gráficos |
| 05 Integration | `schemas/`, `types/api.ts`, `tests/`, `docker-compose.yml`, repositório |

## Fluxo de Git

`main` sempre roda. Cada um trabalha no próprio branch (`feat/nasa-client`, `feat/dashboard`...)
e abre PR pequeno. Antes do PR: `pytest` no backend e `npm run build` no frontend.
