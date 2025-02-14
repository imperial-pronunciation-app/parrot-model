#!/bin/bash

set -e  # Exit on any error

# Required environment variables
: "${DOCKERHUB_USERNAME:?Must set DOCKERHUB_USERNAME}"
: "${DOCKERHUB_ACCESS_TOKEN:?Must set DOCKERHUB_ACCESS_TOKEN}"
: "${IMAGE_NAME:?Must set IMAGE_NAME}"
: "${IMAGE_TAG:?Must set IMAGE_TAG}"
: "${MODEL:?Must set MODEL}"
: "${LANG_ID:?Must set LANG_ID}"

COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME:-"parrot-model-${MODEL_ID}"}

echo "🔑 Logging into Docker Hub..."
echo "$DOCKERHUB_ACCESS_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

echo "⬇️ Pulling image ${IMAGE_NAME}:${IMAGE_TAG}..."
docker pull "${IMAGE_NAME}:${IMAGE_TAG}"

echo "🛑 Stopping existing container..."
# docker stop "$CONTAINER_NAME" || true
# docker rm "$CONTAINER_NAME" || true
docker compose -p "$COMPOSE_PROJECT_NAME" --profile prod down || true

echo "🚀 Starting services with Docker Compose..."
# docker run -d \
#   --name "$CONTAINER_NAME" \
#   --restart unless-stopped \
#   -p "${HOST_PORT}:${CONTAINER_PORT}" \
#   "${IMAGE_NAME}:${IMAGE_TAG}"
docker compose -p "$COMPOSE_PROJECT_NAME" \
  --profile prod \
  up -d \
  --build \
  --pull always

echo "🧹 Cleaning up unused resources..."
docker system prune -a -f

echo "✅ Deployment complete!"