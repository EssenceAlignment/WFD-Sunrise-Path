#!/bin/bash
echo "Recovery Compass Monitoring Status:"
echo "=================================="
docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml ps
echo ""
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
