#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Create .env file if does not exists
[ -f .env ] || touch .env

echo "🧹 Removing old container..."
docker rm -f autosync || true  # Ignore error if container doesn't exist

echo "📦 Building Docker image..."
docker build -t autosync -f Dockerfile .

echo "🚀 Running new container..."
docker run -d --env-file .env -v ./.env:/app/.env --name autosync -p 8000:8000 autosync

echo "📜 Following logs..."
docker logs -tf autosync