#!/bin/bash

# Stop script on error
set -e

# Variables
IMAGE_NAME="nisheetdas1/hd-sentiment-analyzer"
TAG="latest"

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME:$TAG..."
docker build -t $IMAGE_NAME:$TAG .

echo "Docker image build complete."
echo "To run the container, use: docker run -p 3000:3000 $IMAGE_NAME:$TAG"
