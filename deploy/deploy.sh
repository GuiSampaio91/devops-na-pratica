#!/usr/bin/env bash
#
# Deploy da API de Tarefas a partir da imagem publicada no GitHub Container Registry.
# Puxa a imagem (tag 'latest' por padrão, ou a tag informada) e sobe o container
# via docker compose.
#
# Uso:
#   ./deploy.sh           # usa a tag 'latest'
#   ./deploy.sh <tag>     # usa uma tag específica (ex.: o SHA do commit)
#
set -euo pipefail

IMAGE_TAG="${1:-latest}"
COMPOSE_FILE="$(dirname "$0")/docker-compose.prod.yml"

echo ">> Deploy da imagem com a tag: ${IMAGE_TAG}"

# Baixa a imagem do registry e (re)cria o container em segundo plano
IMAGE_TAG="${IMAGE_TAG}" docker compose -f "${COMPOSE_FILE}" pull
IMAGE_TAG="${IMAGE_TAG}" docker compose -f "${COMPOSE_FILE}" up -d

echo ">> Aguardando a aplicação responder..."
sleep 5
docker compose -f "${COMPOSE_FILE}" ps

echo ">> Deploy concluído. API disponível em http://localhost:5000"
