#!/bin/bash
echo "Starting Recovery Compass with monitoring..."
docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml up -d
echo "Waiting for services to be ready..."
sleep 10
echo ""
echo "✅ Services available at:"
echo "   App: http://localhost:3000"
echo "   Grafana: http://localhost:3001 (admin/password from .env.secrets.grafana)"
echo "   Prometheus: http://localhost:9090"
echo "   Traefik: http://localhost:8080"
echo "   pgAdmin: http://localhost:5050"
echo "   Redis Insight: http://localhost:8001"
echo ""
echo "📊 To view logs: docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml logs -f"
