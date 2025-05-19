#!/bin/bash

echo "Waiting for SonarQube..."
for i in {1..60}; do
  STATUS=$(curl -s "$SONAR_HOST_URL/api/system/status" | jq -r '.status')
  if [ "$STATUS" == "UP" ]; then
    echo "SonarQube is ready!"
    break
  fi
  sleep 5
done
