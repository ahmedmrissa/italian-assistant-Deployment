#!/bin/bash

# Deployment script for Italian Teacher Assistant

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example"
    cp .env.example .env
    echo "Please update the .env file with your Supabase credentials and then run this script again."
    exit 1
fi

# Build and start the services
echo "Building and starting services..."
docker-compose up -d

echo "Services started successfully!"
echo "Rasa server is running on http://localhost:5005"
echo "Action server is running on http://localhost:5055"

# Show logs
echo "Showing logs (press Ctrl+C to exit)..."
docker-compose logs -f