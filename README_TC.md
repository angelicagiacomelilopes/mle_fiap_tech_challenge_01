# Tech Challenge – Fase 1 | Machine Learning Engineering
# 🍷 API de Dados Vitivinícolas da Embrapa
Aluna: Angélica Giacomeli Lopes RM: 363921

## 📌 Sumário
- [Tech Challenge – Fase 1 | Machine Learning Engineering](#tech-challenge--fase-1--machine-learning-engineering)
- [🍷 API de Dados Vitivinícolas da Embrapa](#-api-de-dados-vitivinícolas-da-embrapa)
  - [📌 Sumário](#-sumário)
  - [📝  Descrição do Projeto](#--descrição-do-projeto)
  - [🚀 Funcionalidades](#-funcionalidades)
  - [💻 Tecnologias Utilizadas](#-tecnologias-utilizadas)
  - [📦 Instalação](#-instalação)
    - [Passo a passo](#passo-a-passo)
  - [🛠️ Execução e Testes](#️-execução-e-testes)
    - [Rotas disponíveis](#rotas-disponíveis)
  - [Testando a API](#testando-a-api)
  - [🌐 Deploy](#-deploy)
  - [📊 Arquitetura](#-arquitetura)
  - [🏃‍♂️ Uso Inicie o servidor local:](#️-uso-inicie-o-servidor-local)
  - [🎥 Vídeo de Apresentação](#-vídeo-de-apresentação)
  - [📄 Licença](#-licença)
  - [✉️ Contato](#️-contato)
  - [🚀 Funcionalidades](#-funcionalidades-1)


## 📝  Descrição do Projeto

Este projeto consiste em uma API pública para consulta de dados de vitivinicultura disponibilizados pela Embrapa (Produção, Processamento, Comercialização, Importação e Exportação). A solução implementa web scraping para obter os dados em tempo real do site da Embrapa, com fallback para arquivos locais em caso de indisponibilidade.

## 🚀 Funcionalidades
- Raspagem automática de dados do portal da Embrapa

- API RESTful com endpoints para consulta dos dados

- Cache local dos dados como fallback

- Documentação automática com Swagger/OpenAPI
 
## 💻 Tecnologias Utilizadas

- Backend: Flask (Python)
- Web Scraping: BeautifulSoup + requests
- Deploy: Render
- Documentação: Swagger UI
- Versionamento: Git/GitHub 

## 📦 Instalação
- Pré-requisitos
- Python 3.9+
- Pipenv (ou pip)
 
### Passo a passo
1. Clone o repositório:
git clone https://github.com/seu-usuario/vitivinicultura-api.git
cd vitivinicultura-api

2. Instale as dependências:
pipenv install --dev
pipenv shell

3. Configure as variáveis de ambiente:
cp .env.example .env
 
4. Execute a aplicação localmente:
uvicorn app.main:app --reload

## 🛠️ Execução e Testes
### Rotas disponíveis
- GET /api/producao: Dados de produção

- GET /api/processamento: Dados de processamento

- GET /api/comercializacao: Dados de comercialização

- GET /api/importacao: Dados de importação

- GET /api/exportacao: Dados de exportação

Exemplo de resposta:
{
  "data": {
    "2020": [
      {
        "produto": "VINHO DE MESA",
        "quantidade": "124.200.414",
        "categorias": [
          {"Tinto": "103.916.391"},
          {"Branco": "19.568.734"}
        ]
      }
    ]
  }
}


## Testando a API
Acesse a documentação interativa:
1. Acesse a documentação interativa:
http://localhost:8000/docs

2. Ou faça requisições diretamente:
curl http://localhost:8000/api/producao

## 🌐 Deploy
A API está disponível publicamente em:
https://vitibrasil-api.onrender.com

## 📊 Arquitetura
graph TD
    A[Client] --> B[API FastAPI]
    B --> C{Scraping Embrapa}
    C -->|Sucesso| D[Retorna dados frescos]
    C -->|Falha| E[Usa cache local]
    E --> F[Arquivos CSV/JSON]
    B --> G[Swagger UI]

## 🏃‍♂️ Uso Inicie o servidor local:
uvicorn app.main:app --reload


## 🎥 Vídeo de Apresentação
Link para o vídeo de demonstração

## 📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## ✉️ Contato
Equipe de desenvolvimento - equipe@email.com
Projeto Link: https://github.com/seu-usuario/vitivinicultura-api

## 🚀 Funcionalidades

✔️ Raspagem automática dos dados diretamente do portal da Embrapa  
✔️ Cache local dos dados como fallback  
✔️ Documentação automática com Swagger UI  
✔️ Formato JSON padronizado para todas as respostas  
✔️ Tratamento de erros e logs detalhados  



 