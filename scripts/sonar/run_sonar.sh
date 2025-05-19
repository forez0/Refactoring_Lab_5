#!/bin/bash

# Script to run Sonarqube and Sonarscanner from the dedicated directory
# Author: Cascade
# Date: 2025-05-10

set -e

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SONAR_DIR="${PROJECT_ROOT}/sonar"

echo "Starting Sonarqube and Sonarscanner..."
echo "Using Sonar directory: ${SONAR_DIR}"

# Navigate to the sonar directory
cd "${SONAR_DIR}"

# Start the Sonarqube and Sonarscanner containers
docker-compose up -d sonarqube

echo "Sonarqube is starting up. Waiting for it to be ready before running Sonarscanner..."
echo "You can access the Sonarqube UI at http://localhost:9090"
echo "Default credentials: admin/adminadmin"

# Start the Sonarscanner container which will wait for Sonarqube to be ready
docker-compose up sonarscanner

echo "Sonarqube analysis has been completed!"
echo "You can view the results at http://localhost:9090/dashboard?id=poly-micro-frontend"