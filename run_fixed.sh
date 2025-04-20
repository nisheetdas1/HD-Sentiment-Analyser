#!/bin/bash

# Stop script on error
set -e

# Variables
IMAGE_NAME="nisheetdas1/hd-sentiment-analyzer"
CONTAINER_NAME="hd-analyzer"
PORT=3000

# Create a Dockerfile.fixed with proper command
cat > Dockerfile.fixed << EOL
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 3000

# Create a direct command that explicitly sets the host to 0.0.0.0
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:3000
EOL

# Build the Docker image
echo "Building Docker image with fixed configuration..."
docker build -t $IMAGE_NAME:fixed -f Dockerfile.fixed .

# Stop and remove existing container if it exists
echo "Stopping and removing existing container (if any)..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run the container
echo "Starting container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:$PORT \
  $IMAGE_NAME:fixed

echo "Application is running at http://localhost:$PORT"
