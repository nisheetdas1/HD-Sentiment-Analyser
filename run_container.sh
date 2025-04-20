#!/bin/bash

# Variables
IMAGE_NAME="nisheetdas1/hd-sentiment-analyzer"
CONTAINER_NAME="hd-sentiment-analyzer"
PORT=3000

# Stop and remove existing container if it exists
echo "Stopping and removing existing container (if any)..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run the container
echo "Starting container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:$PORT \
  -e PORT=$PORT \
  $IMAGE_NAME

echo "Application is running at http://localhost:$PORT"
