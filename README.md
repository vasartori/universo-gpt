# Chatbot LLM On-Prem — Universo TOTVS 2025

Este repositório contém o código-fonte de uma aplicação que demonstra como executar um modelo de linguagem de grande porte (LLM) localmente, sem depender de serviços de nuvem pública. Essa aplicação será apresentada no **Universo TOTVS 2025**.

O sistema é dividido em dois componentes:
- **Backend** (`app.py`): API Flask que roda localmente um modelo LLM usando `llama.cpp`
- **Frontend** (`frontend/`): Interface utilizando o StreamLit para interação com a LLM

## Funcionalidades

- Inferência local com modelos LLM em GGUF (ex: Mistral 7B)
- Respostas em português, com contexto e stream de tokens
- Contêiner Docker para backend e frontend
- Deploy simples com manifests Kubernetes incluídos

## Como rodar localmente

1. **Baixe um modelo compatível (.gguf)** e coloque na pasta `./models`.
   - Exemplo: `Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf`
2. **Configure as variáveis de ambiente** (opcional):

```bash
export IA_NAME="Sofia"
export LLM_MAX_TOKENS=4096
export LLM_TEMPERATURE=0.8
export LLM_TOP_P=0.95
```

3. **Execute com o Flask diretamente**:

```bash
pip install -r requirements.txt
python app.py
```

Ou use o **Docker** (build disponível somente para devices que suportam CUDA):

```bash
docker build -t chatbot-backend .
docker run -p 5000:5000 -v $(pwd)/models:/app/models chatbot-backend
```

## Deploy com Kubernetes

Na pasta `deploy/` há os manifests prontos para:
- `app.yaml`: backend
- `frontend.yaml`: interface
- `ing.yaml`: Ingress para expor via hostname

## Requisitos

- Python 3.10+
- GPU com suporte CUDA (recomendado)
- Modelo `.gguf` compatível com `llama_cpp`

## Dependências

Todas as dependências estão listadas no `requirements.txt`. Para instalar, execute:

```bash
pip install -r requirements.txt
```