# Forzy Digital Twin - Interface e Observabilidade

> Este é o repositório do Front-end e Back-end do nosso projeto integrado (Governança em IA + Front-end) para o desafio da Forzy.

A ideia aqui é tirar o monitoramento de ativos do papel e colocar numa interface visual amigável. Para este checkpoint, estamos focando na base da nossa "escada": os Sensores. Embora a visão de longo prazo do projeto abranja a fábrica inteira (Planta -> Setor -> Ativo -> Sensores), aqui o escopo é garantir que a leitura de dados base esteja funcionando e que ela seja rastreável.

## 🎥 Vídeo de Demonstração
[Link para o vídeo no YouTube](LINK)

## Arquitetura do Repositório

```text
checkpoint_GBA_Front/
│
├── backend/                  
│   └── api.py                
│
├── frontend/
│   ├── providers/
│   │   └── api_provider.py   
│   └── main.py               
│
├── .gitignore                
├── .env                      
├── requirements.txt          
├── README.md                 
└── Checkpoint_GBA_FE.pdf
```

### Funcionamento:

- Consumo de API: O front não conversa direto com o banco de dados. Nós usamos a biblioteca *requests* do Python para bater nos três endpoints principais da nossa API em FastAPI:

#Traz o status ao vivo e a severidade do sensor.
>GET /v1/sensores/{tag}/leitura-atual
>
#Puxa a série temporal para montar os gráficos e tabelas de tendência.
>GET /v1/sensores/{tag}/historico
>
#Traz os logs de quem acessou o quê.
>GET /v1/observabilidade

- Navegação em Escada (Conceito): A UI foi pensada para, no futuro, permitir o drill-down (Fábrica -> Setor -> Máquina -> Sensor). Na versão atual, focamos na renderização limpa da telemetria do motor (ex: motor WEG W22).

- Renderização: Usamos componentes nativos do Streamlit para plotar os gráficos de histórico e exibir os cards com os valores atuais de forma bem responsiva.

## Como aplicamos a Governança de IA?

Considerando que a gente não saberia de onde a requisição viria ou quanto tempo ela demoraria, aplicamos o nosso contrato de observabilidade.

Toda vez que a nossa interface faz um request para a API do FastAPI, nós injetamos Headers de Contexto (como X-Session-Id, X-Feature, X-Client-Platform e X-App-Version).

Então, em resumo, nosso front "carimba" cada chamada. O back-end recebe, calcula a latência, junta com o timestamp e salva. Depois, o nosso próprio front consome o endpoint de /observabilidade para exibir um relatório de auditoria direto na tela. Isso ajuda a gente a saber exatamente onde e quando o gargalo aconteceu, se um limite de completude estourar.

## Como rodar localmente

O setup é bem simples, só precisa do Python instalado na máquina.

- Clonar este repositório:

>git clone https://github.com/DMGravina/checkpoint_GBA_Front

- Criar e ativar um ambiente virtual:

>python -m venv venv
---
### No Windows: 
>venv\Scripts\activate
### No Linux/Mac: 
>source venv/bin/activate
---

- Instalar os pacotes necessários:

>pip install -r requirements.txt

- Subir a aplicação

Abra dois terminais:

>#No Terminal 1, iniciar a API FastAPI
>uvicorn backend.api:app --reload

>#No Terminal 2, iniciar a interface Gradio
>python frontend/main.py

(Lembrando: A interface do Gradio abrirá automaticamente no navegador)

## Integrantes do Grupo (Dota):

>Davi Gravina – RM 565619
>
>Henry Andrade Browne – RM 562089
>
>Luis Filipe Chaves – RM 564706
>
>Luiz Felipe dos Santos Tragi – RM 565009
>
>Marcelo Roberto Maso Junior – RM 562163
