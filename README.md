# Field Shift

MVP de análise e recomendação de rotação de culturas. O produtor cadastra um
perfil simples da propriedade, visualiza contexto climático e compara cenários
de rotação conforme as prioridades da safra.

O resultado é um apoio inicial à conversa técnica — não é uma recomendação
agronômica prescrita.

## Fluxo demonstrável

1. Cadastrar a propriedade, coordenadas, solo, irrigação e histórico recente.
2. Consultar dados climáticos da NASA POWER, ou usar o modo demonstrativo.
3. Escolher o peso de solo, água, clima e diversificação.
4. Comparar estratégias com pontuações, benefícios, riscos e justificativas.

## Estrutura

- `field-shift-backend/`: FastAPI, contratos Pydantic, regras do MVP e cliente NASA POWER.
- `field-shift-frontend/`: React, TypeScript e Vite para formulário e dashboard.
- `docs/`: contratos e documentação do projeto.

## Rodar localmente

Pré-requisitos: Node 20 LTS, Python 3.12+ e Docker (opcional, para PostgreSQL).

### Banco de dados

```bash
copy .env.example .env
docker compose up -d db
docker compose ps
```

Os dados do PostgreSQL persistem no volume `postgres_data`. Para encerrar:

```bash
docker compose down
```

### Backend

```bash
cd field-shift-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

A API fica em `http://localhost:8000` e a documentação interativa em
`http://localhost:8000/docs`.

Para uma demo sem internet, acrescente `USE_MOCK_CLIMATE=true` ao `.env` do
backend. O retorno indicará que os dados são demonstrativos.

### Frontend

```bash
cd field-shift-frontend
npm install
npm run dev
```

O frontend abre em `http://localhost:5173`; o Vite encaminha `/api` ao backend.

### Testes

```bash
cd field-shift-backend
pytest

cd ../field-shift-frontend
npm run build
```

## Contratos de API

Consulte [docs/api-contracts.md](docs/api-contracts.md) para os formatos JSON
de fazenda, clima e rotação. O OpenAPI gerado pelo FastAPI é o contrato vivo
quando as rotas estiverem disponíveis.

| Método | Rota | Estado no MVP |
| --- | --- | --- |
| `POST` | `/api/v1/farms` | cadastro |
| `GET` | `/api/v1/farms` e `/api/v1/farms/{farm_id}` | consulta |
| `GET` | `/api/v1/environment/climate` | NASA POWER, com modo offline |
| `GET` | `/api/v1/crops` | catálogo de culturas |
| `POST` | `/api/v1/rotation/analyze` | motor de regras parametrizado |
