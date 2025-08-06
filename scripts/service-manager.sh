#!/bin/bash
#
# Service Manager - Self-healing infrastructure orchestration
# Ensures all services are always running and healthy
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$ROOT_DIR/logs/service-manager"
PLIST_DIR="$HOME/Library/LaunchAgents"

# Create log directory
mkdir -p "$LOG_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/service-manager.log"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_DIR/service-manager.log"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_DIR/service-manager.log"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        error "Docker is not running. Starting Docker..."
        open -a Docker
        sleep 10

        # Wait for Docker to start
        while ! docker info >/dev/null 2>&1; do
            sleep 2
        done
        log "Docker started successfully"
    fi
}

# Function to create LaunchAgent plist files
create_launch_agents() {
    log "Creating LaunchAgent configurations..."

    # Recovery Compass Services LaunchAgent
    cat > "$PLIST_DIR/com.recovery-compass.services.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.recovery-compass.services</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/service-manager.sh</string>
        <string>maintain</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG_DIR/launchd-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/launchd-stderr.log</string>
    <key>WorkingDirectory</key>
    <string>$ROOT_DIR</string>
</dict>
</plist>
EOF

    # Health Check LaunchAgent
    cat > "$PLIST_DIR/com.recovery-compass.health-check.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.recovery-compass.health-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/service-manager.sh</string>
        <string>health-check</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>$LOG_DIR/health-check-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/health-check-stderr.log</string>
</dict>
</plist>
EOF

    log "LaunchAgent configurations created"
}

# Function to start all services
start_services() {
    log "Starting all services..."

    check_docker

    # Start Docker Compose services
    cd "$ROOT_DIR"
    docker-compose up -d

    # Load LaunchAgents
    for plist in "$PLIST_DIR"/com.recovery-compass.*.plist; do
        if [ -f "$plist" ]; then
            launchctl load "$plist" 2>/dev/null || true
            log "Loaded $(basename "$plist")"
        fi
    done

    # Start local Python services if not in containers
    if [ -f "$ROOT_DIR/scripts/funding_dashboard.py" ]; then
        if ! pgrep -f "funding_dashboard.py" > /dev/null; then
            nohup python3 "$ROOT_DIR/scripts/funding_dashboard.py" > "$LOG_DIR/funding-dashboard.log" 2>&1 &
            log "Started funding dashboard (PID: $!)"
        fi
    fi

    log "All services started"
}

# Function to stop all services
stop_services() {
    log "Stopping all services..."

    # Stop Docker Compose services
    cd "$ROOT_DIR"
    docker-compose down

    # Unload LaunchAgents
    for plist in "$PLIST_DIR"/com.recovery-compass.*.plist; do
        if [ -f "$plist" ]; then
            launchctl unload "$plist" 2>/dev/null || true
            log "Unloaded $(basename "$plist")"
        fi
    done

    # Stop Python processes
    pkill -f "funding_dashboard.py" || true
    pkill -f "pattern_" || true

    log "All services stopped"
}

# Function to check service health
health_check() {
    log "Performing health checks..."

    unhealthy=0

    # Check Docker services
    if docker ps >/dev/null 2>&1; then
        services=$(docker-compose ps --services 2>/dev/null || true)
        for service in $services; do
            if docker-compose ps "$service" | grep -q "Up"; then
                log "✓ $service is healthy"
            else
                error "✗ $service is down"
                unhealthy=$((unhealthy + 1))
            fi
        done
    else
        error "Docker is not running"
        unhealthy=$((unhealthy + 1))
    fi

    # Check localhost endpoints
    endpoints=(
        "http://localhost:4321/health"
        "http://localhost:8080/health"
        "http://localhost:8000/health"
        "http://localhost:3000"  # Grafana
        "http://localhost:9090"  # Prometheus
    )

    for endpoint in "${endpoints[@]}"; do
        if curl -s -f "$endpoint" >/dev/null 2>&1; then
            log "✓ $endpoint is accessible"
        else
            warning "✗ $endpoint is not accessible"
        fi
    done

    if [ $unhealthy -gt 0 ]; then
        error "Found $unhealthy unhealthy services. Attempting recovery..."
        recover_services
    else
        log "All services are healthy"
    fi
}

# Function to recover unhealthy services
recover_services() {
    log "Attempting service recovery..."

    # Restart unhealthy Docker containers
    unhealthy_containers=$(docker ps -a --filter "status=exited" --format "{{.Names}}" | grep "rc-" || true)
    for container in $unhealthy_containers; do
        log "Restarting $container..."
        docker start "$container"
    done

    # Restart Docker Compose if needed
    cd "$ROOT_DIR"
    docker-compose up -d

    # Give services time to start
    sleep 10

    # Re-check health
    health_check
}

# Function to maintain services (keep them running)
maintain_services() {
    log "Entering maintenance mode..."

    while true; do
        health_check
        sleep 60
    done
}

# Function to show status
show_status() {
    echo -e "\n${GREEN}=== Recovery Compass Service Status ===${NC}\n"

    # Docker services
    if docker ps >/dev/null 2>&1; then
        echo -e "${GREEN}Docker Services:${NC}"
        docker-compose ps
    else
        echo -e "${RED}Docker is not running${NC}"
    fi

    echo -e "\n${GREEN}LaunchAgents:${NC}"
    launchctl list | grep recovery-compass || echo "No LaunchAgents loaded"

    echo -e "\n${GREEN}Port Usage:${NC}"
    lsof -i -P | grep LISTEN | grep -E "(4321|8080|8000|3000|9090)" || echo "No services listening on expected ports"

    echo -e "\n${GREEN}Recent Logs:${NC}"
    tail -n 10 "$LOG_DIR/service-manager.log" 2>/dev/null || echo "No logs available"
}

# Main command handler
case "$1" in
    start)
        create_launch_agents
        start_services
        show_status
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        show_status
        ;;
    status)
        show_status
        ;;
    health-check)
        health_check
        ;;
    maintain)
        maintain_services
        ;;
    recover)
        recover_services
        ;;
    setup)
        create_launch_agents
        log "Setup complete. Run '$0 start' to start services"
        ;;
    *)
        echo "Recovery Compass Service Manager"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|health-check|maintain|recover|setup}"
        echo ""
        echo "Commands:"
        echo "  start        - Start all services and enable auto-start"
        echo "  stop         - Stop all services"
        echo "  restart      - Restart all services"
        echo "  status       - Show service status"
        echo "  health-check - Check health of all services"
        echo "  maintain     - Run continuous health monitoring"
        echo "  recover      - Attempt to recover failed services"
        echo "  setup        - Create LaunchAgent configurations"
        exit 1
        ;;
esac
