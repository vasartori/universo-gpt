# Frontend - Assistente IA

Este diretório contém a interface web do Assistente IA, um chatbot que se comunica com um backend local executando um modelo LLM. A interface é construída com Streamlit, oferecendo uma experiência interativa e simples para o usuário.

## Funcionalidades

- Interface conversacional no estilo chat
- Suporte a streaming de tokens da resposta (em tempo real)
- Histórico de mensagens por sessão
- Suporte a formatação de código e markdown

## Como rodar

### 1. Via terminal (modo desenvolvimento)

```bash
pip install -r requirements.txt
export CHAT_API_URL=localhost
export CHAT_API_PORT=5000
streamlit run frontend.py
```

### 2. Via Docker

```bash
docker build -t assistente-frontend .
docker run -p 8501:8501 -e CHAT_API_URL=<ip-backend> -e CHAT_API_PORT=5000 assistente-frontend
```

## Variáveis de Ambiente

- `CHAT_API_URL`: IP ou hostname do backend (padrão: `localhost`)
- `CHAT_API_PORT`: Porta do backend (padrão: `5000`)

## Requisitos

- Python 3.10+
- Backend em execução e acessível via HTTP (veja o diretório raiz do projeto)

## Deploy com Kubernetes
Na pasta `deploy/` há os manifests prontos para:
- `frontend.yaml`: frontend
- `ing.yaml`: Ingress para expor via hostname

