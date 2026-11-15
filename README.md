# Field Shift

MVP de recomendação de rotação de culturas para a demonstração de hackathon.
O produtor cadastra um perfil simples da propriedade, visualiza o contexto
climático da NASA e compara cenários de rotação que respondem às prioridades
da safra.

O estado detalhado do escopo está em [docs/MVP_STATUS.md](docs/MVP_STATUS.md).

## Fluxo demonstrável

1. Cadastrar a propriedade, coordenadas, solo, irrigação e histórico recente.
2. Consultar dados climáticos da NASA POWER (ou o modo demonstrativo).
3. Escolher o peso de solo, água, clima e diversificação.
4. Comparar três estratégias, com pontuações, benefícios, riscos e justificativas.

O resultado é um apoio inicial à conversa técnica — não é uma recomendação
agronômica prescrita.

## Estrutura atual

- `field-shift-backend/`: FastAPI, contratos Pydantic, regras do MVP e cliente NASA POWER.
- `field-shift-frontend/`: React + TypeScript + Vite, formulário e dashboard.
- `docs/`: escopo, estado das entregas e roteiro de apresentação.

No backend, os routers HTTP exercem o papel de handler e chamam serviços e
repositórios. O repositório de fazendas fica em memória de propósito neste
recorte; trocar para PostgreSQL depois não altera os contratos públicos.

## Rodar localmente

Pré-requisitos: Node 20 LTS e Python 3.12+.

### Backend

```bash
cd field-shift-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

A API fica em `http://localhost:8000` e a documentação interativa em
`http://localhost:8000/docs`.

Para uma demo que não dependa de internet, acrescente `USE_MOCK_CLIMATE=true`
ao arquivo `field-shift-backend/.env`. O retorno exibirá que os dados são
demonstrativos.

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

Os schemas Pydantic em `field-shift-backend/app/schemas/` são a fonte da
verdade; os tipos em `field-shift-frontend/src/types/api.ts` os espelham.
Qualquer mudança de contrato deve atualizar os dois no mesmo pull request.

| Método | Rota | Estado no MVP |
| --- | --- | --- |
| `POST` | `/api/v1/farms` | cadastro em memória |
| `GET` | `/api/v1/farms` e `/api/v1/farms/{farm_id}` | consulta em memória |
| `GET` | `/api/v1/environment/climate` | NASA POWER real, com modo demonstrativo offline |
| `GET` | `/api/v1/crops` | catálogo de cinco culturas do MVP |
| `POST` | `/api/v1/rotation/analyze` | motor de regras transparente e parametrizado |
