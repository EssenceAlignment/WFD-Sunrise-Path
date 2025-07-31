#!/bin/bash

# Setup script for Recovery Compass Docker monitoring stack
# Optimized for Apple M3 Pro with MCP Integration
# Supports profiles for selective service deployment

set -e

# Parse command line arguments
WITH_LOGGING=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --with-logging)
            WITH_LOGGING=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --with-logging    Include Loki and Promtail for log aggregation"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use $0 --help for usage information"
            exit 1
            ;;
    esac
done

echo "🚀 Setting up Recovery Compass monitoring infrastructure..."
if [ "$WITH_LOGGING" = true ]; then
    echo "📝 Including logging services (Loki & Promtail)"
else
    echo "📊 Setting up metrics-only stack (skipping Loki & Promtail)"
fi

# Create directory structure
echo "📁 Creating monitoring directories..."
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p monitoring/loki
mkdir -p monitoring/promtail
mkdir -p monitoring/traefik/dynamic
mkdir -p data/postgres
mkdir -p data/redis

# Create secrets files if they don't exist
echo "🔐 Setting up secrets..."
if [ ! -f .env.secrets ]; then
    cat > .env.secrets <<EOF
DB_PASSWORD=recovery_compass_secure_password_$(openssl rand -hex 16)
EOF
    echo "Created .env.secrets with generated password"
fi

if [ ! -f .env.secrets.grafana ]; then
    echo "grafana_secure_password_$(openssl rand -hex 16)" > .env.secrets.grafana
    echo "Created .env.secrets.grafana"
fi

if [ ! -f .env.secrets.pgadmin ]; then
    echo "pgadmin_secure_password_$(openssl rand -hex 16)" > .env.secrets.pgadmin
    echo "Created .env.secrets.pgadmin"
fi

# Create Grafana datasources configuration
echo "📊 Configuring Grafana datasources..."
cat > monitoring/grafana/datasources/prometheus.yml <<EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true

  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: recovery_compass
    user: postgres
    secureJsonData:
      password: \$__file{/run/secrets/db_password}
    jsonData:
      sslmode: 'disable'
    editable: true

  - name: Redis
    type: redis-datasource
    access: proxy
    url: redis://redis:6379
    editable: true
EOF

# Create Grafana dashboard provisioning
echo "📈 Setting up Grafana dashboards..."
cat > monitoring/grafana/dashboards/dashboard.yml <<EOF
apiVersion: 1

providers:
  - name: 'Recovery Compass Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF

# Create main dashboard JSON
cat > monitoring/grafana/dashboards/recovery-compass-main.json <<'EOF'
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "mappings": [],
          "thresholds": {
            "mode": "percentage",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 70
              },
              {
                "color": "red",
                "value": 90
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 6,
        "x": 0,
        "y": 0
      },
      "id": 1,
      "options": {
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true
      },
      "pluginVersion": "8.0.0",
      "targets": [
        {
          "expr": "100 * (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])))",
          "refId": "A"
        }
      ],
      "title": "CPU Usage",
      "type": "gauge"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "mappings": [],
          "thresholds": {
            "mode": "percentage",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 70
              },
              {
                "color": "red",
                "value": 90
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 6,
        "x": 6,
        "y": 0
      },
      "id": 2,
      "options": {
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true
      },
      "pluginVersion": "8.0.0",
      "targets": [
        {
          "expr": "100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))",
          "refId": "A"
        }
      ],
      "title": "Memory Usage",
      "type": "gauge"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 6,
        "x": 12,
        "y": 0
      },
      "id": 3,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "8.0.0",
      "targets": [
        {
          "expr": "pg_stat_activity_count",
          "refId": "A"
        }
      ],
      "title": "PostgreSQL Connections",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "ops"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 6,
        "x": 18,
        "y": 0
      },
      "id": 4,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "8.0.0",
      "targets": [
        {
          "expr": "rate(redis_commands_processed_total[1m])",
          "refId": "A"
        }
      ],
      "title": "Redis Ops/sec",
      "type": "stat"
    }
  ],
  "schemaVersion": 27,
  "style": "dark",
  "tags": ["recovery-compass", "monitoring"],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "Recovery Compass Performance Dashboard",
  "version": 0
}
EOF

# Create Loki configuration
echo "📝 Configuring Loki..."
cat > monitoring/loki/loki-config.yaml <<EOF
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
  - from: 2020-05-15
    store: boltdb
    object_store: filesystem
    schema: v11
    index:
      prefix: index_
      period: 168h

storage_config:
  boltdb:
    directory: /loki/index

  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s
EOF

# Create Promtail configuration
echo "🔍 Configuring Promtail..."
cat > monitoring/promtail/promtail-config.yml <<EOF
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log
    pipeline_stages:
      - json:
          expressions:
            output: log
            stream: stream
            attrs:
      - json:
          expressions:
            tag:
          source: attrs
      - regex:
          expression: (?P<container_name>(?:[^|]*))\|(?P<image_name>(?:[^|]*))
          source: tag
      - timestamp:
          format: RFC3339Nano
          source: time
      - labels:
          stream:
          container_name:
          image_name:
      - output:
          source: output
EOF

# Create Traefik dynamic configuration
echo "🌐 Configuring Traefik..."
cat > monitoring/traefik/traefik.yml <<EOF
api:
  dashboard: true
  debug: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
  file:
    directory: "/dynamic"
    watch: true

metrics:
  prometheus:
    buckets:
      - 0.1
      - 0.3
      - 1.2
      - 5.0

log:
  level: INFO

accessLog: {}
EOF

# Create hosts file entries
echo "🌐 Adding local DNS entries..."
cat > monitoring/hosts.txt <<EOF
# Add these entries to your /etc/hosts file:
127.0.0.1 recovery-compass.local
127.0.0.1 monitoring.recovery-compass.local
127.0.0.1 metrics.recovery-compass.local
127.0.0.1 pgadmin.recovery-compass.local
127.0.0.1 redis.recovery-compass.local
127.0.0.1 traefik.recovery-compass.local
127.0.0.1 kibana.recovery-compass.local
EOF

# Create convenience scripts
echo "🛠️ Creating convenience scripts..."

# Start script
cat > start-monitoring.sh <<'EOF'
#!/bin/bash

# Parse command line arguments
PROFILE="metrics"  # Default to metrics only
while [[ $# -gt 0 ]]; do
    case $1 in
        --with-logging)
            PROFILE="metrics,logging"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --with-logging    Include Loki and Promtail for log aggregation"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use $0 --help for usage information"
            exit 1
            ;;
    esac
done

echo "Starting Recovery Compass with monitoring..."
if [ "$PROFILE" = "metrics,logging" ]; then
    echo "📝 Including logging services (Loki & Promtail)"
else
    echo "📊 Starting metrics-only stack (no logging)"
fi

COMPOSE_PROFILES=$PROFILE docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml up -d
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
if [ "$PROFILE" = "metrics,logging" ]; then
    echo "   Loki: http://localhost:3100"
fi
echo ""
echo "📊 To view logs: COMPOSE_PROFILES=$PROFILE docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml logs -f"
EOF

# Stop script
cat > stop-monitoring.sh <<'EOF'
#!/bin/bash
echo "Stopping Recovery Compass monitoring stack..."
# Stop all services regardless of profile
COMPOSE_PROFILES=metrics,logging docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml down
EOF

# Status script
cat > status-monitoring.sh <<'EOF'
#!/bin/bash
echo "Recovery Compass Monitoring Status:"
echo "=================================="
# Show all services regardless of profile
COMPOSE_PROFILES=metrics,logging docker compose -f docker-compose.m3-optimized.yml -f docker-compose.monitoring.yml ps
echo ""
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
EOF

chmod +x start-monitoring.sh stop-monitoring.sh status-monitoring.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review and update secrets in .env.secrets files"
echo "2. Add entries from monitoring/hosts.txt to your /etc/hosts file"
echo "3. Enable MCP servers in Docker Desktop:"
echo "   - Docker Hub"
echo "   - Grafana"
echo "   - GitHub Official"
echo "4. Launch the stack:"
echo "   - Metrics only: ./start-monitoring.sh"
echo "   - With logging: ./start-monitoring.sh --with-logging"
echo ""
echo "🔍 Troubleshooting Loki pull issues:"
echo "   If you experience Docker Hub timeouts with Loki:"
echo "   1. Run ./test-loki-pull.sh to diagnose the issue"
echo "   2. Start with metrics-only mode"
echo "   3. Try pulling during off-peak hours"
echo "   4. Consider setting up a Docker registry mirror"
echo ""
echo "🎯 Performance optimization complete for Apple M3 Pro!"
EOF

chmod +x setup-monitoring.sh
