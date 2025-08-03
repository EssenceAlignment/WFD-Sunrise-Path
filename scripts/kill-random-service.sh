#!/usr/bin/env bash
#
# Chaos Testing Script - Validates self-healing infrastructure
# Randomly kills a container to verify automatic recovery
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
MAX_WAIT_TIME=180  # Maximum seconds to wait for recovery
CHECK_INTERVAL=10  # Seconds between health checks

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    error "Docker is not running. Please start Docker first."
fi

# Get list of running containers (exclude infrastructure containers)
CONTAINERS=$(docker ps --format '{{.Names}}' | grep -E '^rc-' | grep -v 'nginx\|redis\|prometheus\|grafana' || true)

if [ -z "$CONTAINERS" ]; then
    error "No eligible containers found for chaos testing"
fi

# Select random container
TARGET=$(echo "$CONTAINERS" | shuf -n1)

if [ -z "$TARGET" ]; then
    error "Failed to select a target container"
fi

log "🎯 Target selected: $TARGET"

# Get initial health status
INITIAL_STATUS=$(docker inspect "$TARGET" --format '{{.State.Status}}')
log "Initial status: $INITIAL_STATUS"

# Get container health check command if exists
HEALTH_CMD=$(docker inspect "$TARGET" --format '{{.Config.Healthcheck.Test}}' 2>/dev/null || echo "none")

# Kill the container
log "💀 Killing container: $TARGET"
docker kill "$TARGET" >/dev/null 2>&1

# Verify container is down
sleep 2
POST_KILL_STATUS=$(docker inspect "$TARGET" --format '{{.State.Status}}' 2>/dev/null || echo "removed")
log "Post-kill status: $POST_KILL_STATUS"

if [ "$POST_KILL_STATUS" == "running" ]; then
    error "Failed to kill container $TARGET"
fi

# Wait for recovery
log "⏳ Waiting for self-healing to recover $TARGET..."
ELAPSED=0
RECOVERED=false

while [ $ELAPSED -lt $MAX_WAIT_TIME ]; do
    sleep $CHECK_INTERVAL
    ELAPSED=$((ELAPSED + CHECK_INTERVAL))

    # Check if container is running again
    CURRENT_STATUS=$(docker inspect "$TARGET" --format '{{.State.Status}}' 2>/dev/null || echo "not_found")

    if [ "$CURRENT_STATUS" == "running" ]; then
        log "✅ Container $TARGET is running again after ${ELAPSED}s"

        # Wait for health check if available
        if [ "$HEALTH_CMD" != "none" ] && [ "$HEALTH_CMD" != "" ]; then
            log "🏥 Waiting for health check to pass..."
            HEALTH_WAIT=0
            while [ $HEALTH_WAIT -lt 60 ]; do
                HEALTH_STATUS=$(docker inspect "$TARGET" --format '{{.State.Health.Status}}' 2>/dev/null || echo "none")
                if [ "$HEALTH_STATUS" == "healthy" ]; then
                    log "✅ Container $TARGET is healthy"
                    RECOVERED=true
                    break 2
                fi
                sleep 5
                HEALTH_WAIT=$((HEALTH_WAIT + 5))
            done
            warning "Health check did not pass within 60s"
        else
            RECOVERED=true
            break
        fi
    fi

    log "Status after ${ELAPSED}s: $CURRENT_STATUS"
done

# Final verification
if [ "$RECOVERED" = true ]; then
    log "🎉 Self-healing successful! Container $TARGET recovered in ${ELAPSED}s"

    # Verify service is actually working
    case "$TARGET" in
        "rc-funding-dashboard")
            if curl -sf http://localhost:4321/health >/dev/null 2>&1; then
                log "✅ Service endpoint verified: http://localhost:4321/health"
            else
                warning "Service endpoint not responding"
            fi
            ;;
        "rc-pattern-engine")
            if curl -sf http://localhost:8080/health >/dev/null 2>&1; then
                log "✅ Service endpoint verified: http://localhost:8080/health"
            else
                warning "Service endpoint not responding"
            fi
            ;;
        "rc-agent-coordinator")
            if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
                log "✅ Service endpoint verified: http://localhost:8000/health"
            else
                warning "Service endpoint not responding"
            fi
            ;;
    esac

    # Generate metrics
    echo "---"
    echo "CHAOS TEST METRICS:"
    echo "- Service: $TARGET"
    echo "- Recovery Time: ${ELAPSED}s"
    echo "- Recovery Status: SUCCESS"
    echo "- Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "---"

    exit 0
else
    error "Self-healing FAILED! Container $TARGET did not recover within ${MAX_WAIT_TIME}s"
fi
