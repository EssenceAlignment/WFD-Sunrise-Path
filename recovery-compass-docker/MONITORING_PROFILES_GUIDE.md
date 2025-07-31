# Monitoring Stack Profiles Guide

This guide explains how to use Docker Compose profiles to selectively enable services in the monitoring stack, particularly useful when experiencing Docker Hub timeouts with Loki.

## Quick Start

### Metrics-Only Mode (Recommended for CI)
```bash
# Start Prometheus + Grafana without Loki
./start-monitoring.sh

# Or manually:
COMPOSE_PROFILES=metrics docker compose -f docker-compose.monitoring.yml up -d
```

### Full Stack with Logging
```bash
# Start all services including Loki & Promtail
./start-monitoring.sh --with-logging

# Or manually:
COMPOSE_PROFILES=metrics,logging docker compose -f docker-compose.monitoring.yml up -d
```

## CI Pipeline Usage

The CI pipeline now runs metrics-only by default to avoid Loki pull timeouts:

```yaml
# In .github/workflows/docker-compose-ci.yml
COMPOSE_PROFILES=metrics docker compose -f docker-compose.monitoring.yml up -d
```

## Troubleshooting Loki Pull Issues

### 1. Run Diagnostics
```bash
cd recovery-compass-docker
./test-loki-pull.sh
```

This will:
- Test basic Docker Hub connectivity
- Attempt to pull a small Alpine image
- Try pulling Loki 2.9.0
- Show network information
- Display Docker version info

### 2. Common Solutions

#### Use Specific Tags
We've switched from `latest` to `2.9.0` to reduce image size and improve stability:
```yaml
loki:
  image: grafana/loki:2.9.0  # Instead of :latest
```

#### Schedule Pulls During Off-Peak Hours
If running locally, try pulling images during non-business hours when Docker Hub traffic is lower.

#### Set Up a Registry Mirror
Create a local registry cache to avoid repeated pulls from Docker Hub:

```bash
# Start a local registry
docker run -d -p 5000:5000 --restart=always --name registry registry:2

# Configure Docker to use it as a mirror
# Add to /etc/docker/daemon.json:
{
  "registry-mirrors": ["http://localhost:5000"]
}
```

## Profile Configuration

### Services by Profile

**Default (no profile required):**
- Prometheus
- Grafana
- Node Exporter
- PostgreSQL Exporter
- Redis Exporter
- PgAdmin
- RedisInsight
- Traefik

**`logging` profile:**
- Loki
- Promtail

**`search` profile:**
- Elasticsearch
- Kibana

### Using Multiple Profiles
```bash
# Enable both logging and search
COMPOSE_PROFILES=logging,search docker compose -f docker-compose.monitoring.yml up -d
```

## Grafana Configuration

Grafana is configured to work with or without Loki:
- The Loki datasource is pre-configured but won't cause errors if Loki isn't running
- Dashboards will gracefully handle missing Loki data
- Metrics from Prometheus will work regardless of logging services

## Verification Commands

### Check Running Services
```bash
# Show all services (including those not running due to profiles)
COMPOSE_PROFILES=metrics,logging docker compose -f docker-compose.monitoring.yml ps
```

### Health Checks
```bash
# Prometheus
curl -f http://localhost:9090/-/healthy

# Grafana
curl -f http://localhost:3001/api/health

# Loki (if running)
curl -f http://localhost:3100/ready
```

## Best Practices

1. **Start with metrics-only** in CI environments to ensure reliability
2. **Add logging locally** when you need to debug issues
3. **Use specific image tags** instead of `latest` to avoid surprises
4. **Monitor pull times** with the diagnostic script to identify patterns
5. **Consider alternatives** like Fluentd or Vector if Loki continues to have issues

## Alternative Registry Options

If Docker Hub continues to be problematic:

### GitHub Container Registry (GHCR)
While Grafana doesn't officially publish to GHCR, you can mirror images:
```bash
# Pull from Docker Hub
docker pull grafana/loki:2.9.0

# Tag for GHCR
docker tag grafana/loki:2.9.0 ghcr.io/YOUR_ORG/loki:2.9.0

# Push to GHCR
docker push ghcr.io/YOUR_ORG/loki:2.9.0
```

### Amazon ECR Public
Some organizations mirror popular images to ECR Public for better availability.

## Summary

The profile-based approach provides:
- ✅ Immediate CI unblocking by skipping problematic pulls
- ✅ Flexibility to enable logging when needed
- ✅ Graceful degradation when services are unavailable
- ✅ Easy troubleshooting with diagnostic tools
- ✅ Future-proof architecture for adding more optional services
