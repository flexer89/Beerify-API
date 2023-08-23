#!/bin/bash

# Image and container names
IMAGE_NAME="beerify-api-image"
CONTAINER_NAME="beerify-api"

# Check if container exists
if [[ "$(docker ps -aq -f name=$CONTAINER_NAME)" == "" ]]; then
    echo "Building the Docker image..."
    docker build -t $IMAGE_NAME .

    echo "Creating and starting the Docker container..."
    docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
else
    echo "Starting the Docker container..."
    docker start $CONTAINER_NAME
fi
