# Forzy Digital Twin - Interface e Observabilidade

>Este é o repositório do Front-end do nosso projeto integrado (Governança em IA + Front-end) para o desafio da Forzy.

A ideia aqui é tirar o monitoramento de ativos do papel e colocar numa interface visual amigável. Para este checkpoint, estamos focando na base da nossa "escada": os Sensores. Embora a visão de longo prazo do projeto abranja a fábrica inteira, aqui o escopo é garantir que a leitura de dados esteja funcionando e que ela seja rastreável.

## Arquitetura do Front-end

Por ter mais costume e acharmos mais prático, optamos por construir a interface utilizando Streamlit.

### Funcionamento:

Consumo de API: O front não conversa direto com o banco de dados. Nós usamos a biblioteca requests do Python para bater nos três endpoints principais da nossa API em FastAPI:

GET /v1/sensores/{tag}/leitura-atual: Traz o status ao vivo e a severidade do sensor.

GET /v1/sensores/{tag}/historico: Puxa a série temporal para montarmos os gráficos e tabelas de tendência.

GET /v1/observabilidade: Onde a mágica da governança acontece (traz os logs de quem acessou o quê).

Navegação em Escada (Conceito): A UI foi pensada para, no futuro, permitir o drill-down (Fábrica -> Setor -> Máquina -> Sensor). Na versão atual, focamos na renderização limpa da telemetria do motor (ex: motor WEG W22).

Renderização: Usamos componentes nativos do Streamlit para plotar os gráficos de histórico e exibir os cards com os valores atuais de forma bem responsiva.

## Como aplicamos a Governança de IA aqui?

Considerando que a gente não saberia de onde a requisição viria ou quanto tempo ela demoraria, aplicamos o nosso contrato de observabilidade.

Toda vez que a nossa interface faz um request para a API do FastAPI, nós injetamos Headers de Contexto (como X-Session-Id e X-Feature).

Basicamente, o front "carimba" cada chamada. O back-end recebe isso, calcula a latência, junta com o timestamp e salva. Depois, o nosso próprio front consome o endpoint de /observabilidade para exibir um relatório de auditoria direto na tela. Assim, se um limite de completude ou freshness estourar, a gente sabe exatamente onde e quando o gargalo aconteceu.

## Como rodar localmente

O setup é bem simples, só precisa do Python instalado na máquina.

Clone este repositório:

git clone [URL_DO_SEU_REPOSITORIO]


Crie e ative um ambiente virtual (recomendado):

python -m venv venv
## No Windows: venv\Scripts\activate
## No Linux/Mac: source venv/bin/activate


Instale os pacotes necessários (As dependências estão no requirements.txt):

pip install streamlit requests pandas plotly


Suba a aplicação:

streamlit run app.py


(Lembrando: para o front funcionar preenchido, a API FastAPI precisa estar rodando em paralelo)

## Integrantes do Grupo (Dota):

[Nome do Integrante 1] - [RM]

[Nome do Integrante 2] - [RM]

[Nome do Integrante 3] - [RM]
