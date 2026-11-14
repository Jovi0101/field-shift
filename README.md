# Field Shift — Decision Dashboard

Dashboard demonstrativo para visualizar indicadores ambientais e comparar estratégias de rotação de culturas.

## Requisitos

- Python 3.10 ou superior
- pip

## Instalação

No PowerShell, na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Executar

```powershell
streamlit run app.py
```

## Estrutura

- `src/data/`: dados fictícios usados no protótipo.
- `src/models/`: modelos de indicadores e estratégias.
- `src/components/`: componentes do dashboard.
- `src/styles/`: estilos da página.
- `assets/images/`: imagens do projeto.

## Aviso

Os valores atuais são fictícios e servem apenas para desenvolver a interface.
Substitua-os por dados validados antes de apoiar decisões de produção.
