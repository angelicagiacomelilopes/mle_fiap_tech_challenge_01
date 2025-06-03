# Tech Challenge – Fase 1 | Machine Learning Engineering
# 🍷 API de Dados Vitivinícolas da Embrapa
Aluna: Angélica Giacomeli Lopes RM: 363921

Respositório do Tech Challenge FIAP de Machine Leaning 
Link: https://github.com/angelicagiacomelilopes/mle_fiap_tech_challenge_01.git
Entrega 03/06/2025


## 📌 Sumário
- [Tech Challenge – Fase 1 | Machine Learning Engineering](#tech-challenge--fase-1--machine-learning-engineering)
- [🍷 API de Dados Vitivinícolas da Embrapa](#-api-de-dados-vitivinícolas-da-embrapa)
  - [📌 Sumário](#-sumário)
  - [📝  Descrição do Projeto](#--descrição-do-projeto)
  - [🚀 Funcionalidades](#-funcionalidades)
  - [💻 Tecnologias Utilizadas](#-tecnologias-utilizadas)
  - [📊 Arquitetura](#-arquitetura)
  - [📁 Estrutura das pastas](#-estrutura-das-pastas)
  - [📦 Instalação](#-instalação)
  - [📋 Passo a passo](#-passo-a-passo)
  - [🛠️ Execução e Testes](#️-execução-e-testes)
    - [Rotas disponíveis](#rotas-disponíveis)
    - [Utilizado para validar rota - usado apenas para testes de desenvolvimento](#utilizado-para-validar-rota---usado-apenas-para-testes-de-desenvolvimento)
  - [Testando a API Via Produção](#testando-a-api-via-produção)
  - [Testando a API Localmente](#testando-a-api-localmente)
  - [🎯 Exemplos de consumo da API](#-exemplos-de-consumo-da-api)
    - [Primeira etapa - Autorizacação](#primeira-etapa---autorizacação)
    - [Segunda etapa - Acesso aos recursos disponíveis](#segunda-etapa---acesso-aos-recursos-disponíveis)
    - [Produção](#produção)
    - [Processamento](#processamento)
    - [Exportacao](#exportacao)
    - [Importacao](#importacao)
    - [Comercializacao](#comercializacao)
  - [🎥 Vídeo de Apresentação](#-vídeo-de-apresentação)
  - [📄 Licença](#-licença)
  - [✉️ Contato](#️-contato)


## 📝  Descrição do Projeto

Este projeto consiste em criar uma API pública para consulta de dados de vitivinicultura disponibilizados pela Embrapa:
- Produção
- Processamento
- Comercialização
- Importação 
- Exportação. 
  
A solução implementa web scraping para obter os dados em tempo real do site da Embrapa, com fallback para arquivos locais em caso de indisponibilidade.

## 🚀 Funcionalidades
```
✔️ Raspagem automática dos dados diretamente do portal da Embrapa  
✔️ Cache local dos dados como fallback  
✔️ Documentação automática com Swagger UI  
✔️ Formato JSON padronizado para todas as respostas  
✔️ Tratamento de erros e logs detalhados  
```
## 💻 Tecnologias Utilizadas

- Backend: Flask (Python)
- Web Scraping: BeautifulSoup + requests
- Deploy: Render
- Documentação: Swagger UI
- Versionamento: Git/GitHub 

## 📊 Arquitetura
```mermaid
graph TD
    A[Clientes] --> B[API Flask]
    B --> C[Web Scraping Embrapa]
    B --> D[Cache Local]
    B --> E[Autenticação JWT]
    C --> F[Portal Embrapa]
    D --> G[Arquivos JSON]
```

## 📁 Estrutura das pastas
```
mle_fiap_tech_challenge_01/
├── 📁 app/
│   ├── 📄 __init__.py
│   ├── 📁 api/
│   │   ├── 📁 routes/               # 🛣️ Rotas da API
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 🔐 token_route.py    
│   │   │   ├── 🍇 producao_route.py       
│   │   │   ├── 📊 comercializacao_route.py  
│   │   │   ├── 🌍 exportacao_route.py      
│   │   │   ├── 🛳️ importacao_route.py      
│   │   │   ├── 🏭 processamento_route.py   
│   │   │   └── 📁 docs/                # 📚 Documentação Swagger
│   │   │       ├── 📁 comercializacao/
│   │   │       │   └── 📄 get_comercializacao.yaml
│   │   │       ├── 📁 exportacao/
│   │   │       │   └── 📄 get_exportacao.yaml
│   │   │       ├── 📁 importacao/
│   │   │       │   └── 📄 get_importacao.yaml
│   │   │       ├── 📁 processamento/
│   │   │       │   └── 📄 get_processamento.yaml
│   │   │       ├── 📁 producao/
│   │   │       │   └── 📄 get_producao.yaml
│   │   │       └── 📁 token/
│   │   │           └── 📄 post_token.yaml
│   │
│   ├── 📁 config/
│   │   ├── ⚙️ settings.py           
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 dto/                      # 🧩 Objetos de Dados
│   │   ├── 📄 comercializacao_dto.py
│   │   ├── 📄 producao_dto.py
│   │   ├── 📄 importacao_dto.py
│   │   ├── 📄 exportacao_dto.py
│   │   ├── 📄 processamento_dto.py
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 infra/
│   │   ├── 📁 auth/                # 🔐 Autenticação
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 token_service.py
│   │   │
│   │   └── 📁 service/             # ⚒️ Serviços
│   │       ├── 📄 __init__.py
│   │       ├── 📄 comercializacao_service.py
│   │       ├── 📄 exportacao_service.py
│   │       ├── 📄 importacao_service.py
│   │       ├── 📄 processamento_service.py
│   │       └── 📄 producao_service.py
│   │
├── 📁 tests/                       # 🧪 Testes
│   ├── 📁 integration/
│   └── 📁 unit/
│
├── 📁 data/                        # 🗃️ Dados locais
│   ├── 📄 comercializacao_backup.csv
│   ├── 📄 exportacao_backup.py
│   ├── 📄 importacao_backup.py
│   ├── 📄 processamento_backup.py
│   └── 📄 producao_backup.csv
│
├── 🚀 main.py                      
├── 📦 requirements.txt             
├── 📄 README.md               
└── 📄 READMEFIAP.md
```

## 📦 Instalação
- Pré-requisitos
- Python 3.10+
- Pipenv (ou pip)

## 📋 Passo a passo
1. 🔄 Clone o Repositório
   
```bash
git clone https://github.com/angelicagiacomelilopes/mle_fiap_tech_challenge_01.git
```
2. 🐍 Configure o Ambiente
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows   
```

3. 📦 Instale Dependências
```bash
pip install -r requirements.txt
```

5. 🚀 Execute Localmente
```bash
python main.py
```

## 🛠️ Execução e Testes
### Rotas disponíveis
```
✔️ GET /producao: Dados de produção
✔️ GET /processamento: Dados de processamento
✔️ GET /comercializacao: Dados de comercialização
✔️ GET /importacao: Dados de importação
✔️ GET /exportacao: Dados de exportação
✔️ POST /login : Autenticação JWT
```
### Utilizado para validar rota - usado apenas para testes de desenvolvimento
```
✔️ GET /producao/health: Validacao da rota
✔️ GET /processamento/health: Validacao da rota
✔️ GET /comercializacao/health: Validacao da rota
✔️ GET /importacao/health: Validacao da rota
✔️ GET /exportacao/health: Validacao da rota
✔️ GET /token/health: Validacao da rota
```

## Testando a API Via Produção
Acesse a documentação Swagger
1. Acesse a documentação: https://mle-fiap-tech-challenge-01.onrender.com/apidocs

2. API está disponível em:
   https://mle-fiap-tech-challenge-01.onrender.com/

## Testando a API Localmente
Acesse a documentação Swagger
1. Acesse a documentação: http://127.0.0.1:5000/apidocs

2. API está disponível em:
   http://127.0.0.1:5000/


## 🎯 Exemplos de consumo da API
Observação: Para ambiente produtivo, mude o endereço conforme descrito acima.

### Primeira etapa - Autorizacação
Essa api funciona com autorização via JWT

Acessar o endereço: http://127.0.0.1:5000/login
<b>Metodo:</b> POST
<b>Payload (enviar no body):</b>
```bash
{
    "username":"embrapa_fiap_mlet_giacang",
    "password":"1234"
}
```

<b>Retorno Exemplo JSON: </b>
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImVtYnJhcGFfZmlhcF9tbGV0X2dpYWNhbmciLCJleHAiOjE3NDg5MDY1NTh9.QgaDzpmgc4IYmTUjkshjsZHYlBTwsnf-xpK_A8wFX_4"
}
``` 

### Segunda etapa - Acesso aos recursos disponíveis
Essa api funciona com autorização via JWT, então deve ser adicionado o token gerado pela autorização via Bearer.

### Produção
Acessar o endereço: http://127.0.0.1:5000/producao
<b>Metodo:</b> GET
<b>Bearer Auth: </b> Token de autenticação
<b>Payload (enviar no body):</b>
<b> Parametros de filtro:</b>

1. Sem filtro: Retorna todos os dados existentes [1971 a 2023]
2. ano: retorna os dados do ano desejado
3. produto: retorna o produto disponível pelo embraba, exemplo: DERIVADOS
4. categoria: retorna o sub produto de cada produto, exemplo: Espumante

<b>Filtro apenas  ano </b>
```bash
{
  "ano": 2020
}
```

<b>Filtro ano e produto</b>
```bash
{
  "ano": 2020,
  "produto": "DERIVADOS"
}
```

<b>Filtro ano, produto e categoria</b>
```bash
{
  "ano": 2020,
  "produto": "DERIVADOS",
  "categoria": "Espumante"
}
```

 
<b>Retorno Exemplo JSON: </b>
```json
{
    "data": {
        "2020": [
            {
                "produto": [
                    {
                        "Nome": "DERIVADOS",
                        "Quantidade_total_litros": "92.533.804",
                        "categorias": [
                            {
                                "categoria": "Espumante",
                                "quantidade_litros": "32.399"
                            }
                    ]
                }
            }
        ]
    }
    "metadata": {
        "fonte": "http://vitibrasil.cnpuv.embrapa.br",
        "unidade_quantidade": "litros"
    }
}
``` 


### Processamento
Acessar o endereço: http://127.0.0.1:5000/processamento
<b>Metodo:</b> GET
<b>Bearer Auth: </b> Token de autenticação
<b>Payload (enviar no body):</b>
<b> Parametros de filtro:</b>

1. Sem filtro: Retorna todos os dados existentes [1971 a 2023]
2. ano: retorna os dados do ano desejado
3. tipo: retorna os tipos disponível pelo embraba, exemplo: Viníferas, Americanas e Hibridas, etc...
4. subtipo: retorna o sub tipo de cada tipo, exemplo: BRANCAS E ROSADAS
5. cutivar: retorna o cultivar de cada subtipo: Alvarinho

<b>Filtro apenas  ano </b>
```bash
{
  "ano": 2020
}
```

<b>Filtro ano e tipo</b>
```bash
{
  "ano": 2020,
  "tipo": "Viníferas"
}
```

<b>Filtro ano, tipo e subtipo</b>
```bash
{
  "ano": 2020,
  "produto": "DERIVADOS",
  "subtipo":"BRANCAS E ROSADAS"
}
```

<b>Filtro ano, tipo, subtipo e cultivar</b>
```bash
{
  "ano": 2020,
  "produto": "DERIVADOS",
  "subtipo":"BRANCAS E ROSADAS",
  "cultivar":"Alvarinho"
}
```
 
<b>Retorno Exemplo JSON: </b>
```json
{
    "data": {
        "2020": {
            "Viníferas": [
                {
                    "Nome": "BRANCAS E ROSADAS",
                    "Quantidade_total": "41.004.206",
                    "cultivares": [
                        {
                            "cultivar": "Alvarinho",
                            "quantidade": "46.574"
                        }
                    ]
                }
            ]
        }
    },
    "metadata": {
        "fonte": "http://vitibrasil.cnpuv.embrapa.br",
        "unidade_quantidade": "kg ou litros conforme o produto"
    }
}
``` 

### Exportacao
Acessar o endereço: http://127.0.0.1:5000/exportacao
<b>Metodo:</b> GET
<b>Bearer Auth: </b> Token de autenticação
<b>Payload (enviar no body):</b>
<b> Parametros de filtro:</b>

1. Sem filtro: Retorna todos os dados existentes [1971 a 2023]
2. ano: retorna os dados do ano desejado
3. tipo: retorna os tipos disponível pelo embraba, exemplo: Viníferas, Americanas e Hibridas, etc...
4. pais: retorna o pais de exportacao

<b>Filtro apenas  ano </b>
```bash
{
  "ano": 2020
}
```

<b>Filtro ano e tipo</b>
```bash
{
  "ano": 2020,
  "tipo": "Espumantes" 
}
```

<b>Filtro ano, tipo e pais</b>
```bash
{
  "ano": 2020,
  "tipo": "Espumantes",
  "pais": "Alemanha"
}
```
 
<b>Retorno Exemplo JSON: </b>
```json
{
    "data": {
        "2020": {
            "Espumantes": {
                "paises": {
                    "Alemanha": {
                        "quantidade": "2.388",
                        "valor": "14.767"
                    }
                },
                "total_paises": 1
            }
        }
    },
    "metadata": {
        "fonte": "http://vitibrasil.cnpuv.embrapa.br",
        "unidade_quantidade": "kg ou litros conforme o produto",
        "unidade_valor": "US$"
    }
}
```

### Importacao
Acessar o endereço: http://127.0.0.1:5000/importacao
<b>Metodo:</b> GET
<b>Bearer Auth: </b> Token de autenticação
<b>Payload (enviar no body):</b>
<b> Parametros de filtro:</b>

1. Sem filtro: Retorna todos os dados existentes [1971 a 2023]
2. ano: retorna os dados do ano desejado
3. tipo: retorna os tipos disponível pelo embraba, exemplo: Viníferas, Americanas e Hibridas, etc...
4. pais: retorna o pais de importacao

<b>Filtro apenas  ano </b>
```bash
{
  "ano": 2020
}
```

<b>Filtro ano e tipo</b>
```bash
{
  "ano": 2020,
  "tipo": "Espumantes" 
}
```

<b>Filtro ano, tipo e pais</b>
```bash
{
  "ano": 2020,
  "tipo": "Espumantes",
  "pais": "Alemanha"
}
```
 
<b>Retorno Exemplo JSON: </b>
```json
{
    "data": {
        "2020": {
            "Espumantes": {
                "paises": {
                    "Alemanha": {
                        "quantidade": "21.174",
                        "valor": "65.359"
                    }
                },
                "total_paises": 1
            }
        }
    },
    "metadata": {
        "fonte": "http://vitibrasil.cnpuv.embrapa.br",
        "unidade_quantidade": "kg ou litros conforme o produto",
        "unidade_valor": "US$"
    }
}
```

### Comercializacao
Acessar o endereço: http://127.0.0.1:5000/comercializacao
<b>Metodo:</b> GET
<b>Bearer Auth: </b> Token de autenticação
<b>Payload (enviar no body):</b>
<b> Parametros de filtro:</b>

1. Sem filtro: Retorna todos os dados existentes [1971 a 2023]
2. ano: retorna os dados do ano desejado
3. tipo: retorna os tipos disponível pelo embraba, exemplo: ESPUMANTES
4. categoria: retorna a categoria do tipo

<b>Filtro apenas  ano </b>
```bash
{
  "ano": 2020
}
```

<b>Filtro ano e tipo</b>
```bash
{
  "ano": 2020,
  "tipo": "ESPUMANTES" 
}
```

<b>Filtro ano, tipo e categoria</b>
```bash
{
  "ano": "2020",
  "produto": "ESPUMANTES",
  "categoria":"Espumante  Moscatel"
}
```
 
<b>Retorno Exemplo JSON: </b>
```json
{
    "data": {
        "2020": {
            "ESPUMANTES": [
                {
                    "Nome": "Espumante  Moscatel",
                    "Quantidade_total_litros": "22.610.762",
                    "categorias": [
                        {
                            "categoria": "Espumante  Moscatel",
                            "quantidade_litros": "9.298.571"
                        }
                    ]
                }
            ]
        }
    },
    "metadata": {
        "fonte": "http://vitibrasil.cnpuv.embrapa.br",
        "unidade_quantidade": "litros"
    }
}
```

## 🎥 Vídeo de Apresentação
Confira o [video][docs] do projeto.

[docs]: https://github.com/angelicagiacomelilopes/mle_fiap_tech_challenge_01/blob/feature/criacao_estrutura/videoprojeto.mp4 "Documentação completa"



## 📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## ✉️ Contato
Responsável - giacomeliangelica@email.com

Projeto Link: https://mle-fiap-tech-challenge-01.onrender.com/


