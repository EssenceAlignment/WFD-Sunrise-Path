#!/bin/bash
echo "Stopping Recovery Compass monitoring stack..."
docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml down
