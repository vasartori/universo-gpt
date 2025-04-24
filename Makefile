# 📁 Makefile para rodar modelo GGUF com python nativo (fora do Conda)

ENV_DIR := .venv
PYTHON := $(ENV_DIR)/bin/python
PIP := $(ENV_DIR)/bin/pip

.PHONY: all setup run clean

all: setup run

setup:
	@echo "🚀 Criando ambiente virtual com Python do sistema (fora do Conda)..."
	/usr/bin/python3 -m venv $(ENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

run:
	@echo "🧠 Executando modelo localmente com ambiente limpo..."
	gunicorn app:app --bind 0.0.0.0:5000 --worker-class gevent --timeout 300

clean:
	@echo "🧹 Removendo ambiente virtual..."
	rm -rf $(ENV_DIR)
