# Estado do MVP — Field Shift

Atualizado para a versão de hackathon. O objetivo é provar o fluxo de valor
de ponta a ponta, não entregar uma plataforma agrícola completa.

## Já está pronto para a demo

| Área | Entrega | Estado |
| --- | --- | --- |
| Cadastro | Nome, área, coordenadas, solo, irrigação e histórico de culturas | Pronto |
| Localização | Coordenadas validadas e link para conferir o ponto no OpenStreetMap | Pronto para MVP |
| Clima | Consulta mensal da NASA POWER (últimos 5 anos completos), normalização, cache e fallback demonstrativo | Pronto |
| Catálogo | Cinco culturas com família, época, demanda hídrica e faixa de temperatura | Pronto para MVP |
| Motor de rotação | Três cenários; pesos de prioridade, ajustes por solo/irrigação/histórico e explicação da nota | Pronto para MVP |
| Dashboard | Resumo climático, histórico visual, perfil da propriedade, pesos e comparação de cenários | Pronto |
| Contratos | Schemas Pydantic espelhados em TypeScript e testes de contrato | Pronto |
| Infraestrutura | CORS, healthcheck, proxy do Vite e `docker-compose` para Postgres futuro | Pronto para desenvolvimento |

## O que ficou intencionalmente fora do MVP

| Item | Motivo | Próximo passo depois da validação |
| --- | --- | --- |
| PostgreSQL e migrations | A persistência em memória reduz atrito na apresentação | Implementar modelo SQLAlchemy, repository e migration inicial |
| Mapa clicável | Coordenadas e link de conferência validam o fluxo sem uma dependência visual extra | Adicionar Leaflet ou MapLibre com seleção de ponto |
| GPM | NASA POWER já entrega precipitação suficiente para o cenário demonstrado | Avaliar se a resolução adicional muda alguma decisão |
| Motor agronômico científico | As regras atuais são explicáveis, mas não são prescrições | Validar culturas, pesos e limites com agrônomo; documentar fontes |
| Autenticação e multiusuário | Não altera a hipótese principal do hackathon | Adicionar contas, propriedades por usuário e autorização |
| Histórico salvo e relatórios | O usuário só precisa ver a primeira análise na demo | Persistir análises e exportar PDF/CSV |
| Testes de interface e deploy | Ainda não são necessários para comprovar a proposta | Automatizar build, testes de browser e publicar ambiente de demonstração |

## Roteiro recomendado de apresentação

1. Começar em **Fazenda Demo** e mostrar os campos que compõem o perfil da área.
2. Conferir as coordenadas no mapa por meio do link, se alguém perguntar sobre localização.
3. Enviar o cadastro e apontar o resumo climático com a fonte NASA POWER.
4. Mostrar o histórico de temperatura e chuva, sem apresentar a ferramenta como previsão.
5. Definir **Diversificação** em 70% e os demais critérios em 10%; atualizar: a alternativa com feijão assume o topo.
6. Definir **Saúde do solo** em 70% e os demais critérios em 10%; atualizar: cobertura de inverno assume o topo.
7. Abrir “Por que esta alternativa?” e encerrar reforçando que o resultado orienta a conversa com o agrônomo.

## Critério de sucesso no hackathon

Uma pessoa consegue cadastrar uma área e entender, em poucos minutos, por que
uma rotação aparece antes de outra ao mudar seu objetivo. Se isso acontecer,
a hipótese do Field Shift foi validada; o restante pode evoluir após feedback
de produtores e especialistas.
