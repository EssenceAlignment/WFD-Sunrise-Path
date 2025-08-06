#!/bin/bash

# Recovery Compass Edge Storage Latency Probe
# Measures KV, R2, and D1 response times under different network conditions

echo "🌐 Recovery Compass Edge Storage Probe"
echo "====================================="

BASE_URL=${RECOVERY_COMPASS_URL:-"https://recovery-compass.org"}
PROBE_COUNT=5

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to measure endpoint latency
measure_latency() {
    local endpoint=$1
    local name=$2
    local total_time=0
    local min_time=999999
    local max_time=0

    echo -e "\n📊 Testing ${name} endpoint: ${endpoint}"
    echo "Running ${PROBE_COUNT} probes..."

    for i in $(seq 1 $PROBE_COUNT); do
        # Use curl with time_total output
        response_time=$(curl -o /dev/null -s -w "%{time_total}\n" "${BASE_URL}${endpoint}" || echo "0")
        response_time_ms=$(echo "$response_time * 1000" | bc)

        echo "  Probe $i: ${response_time_ms}ms"

        # Update statistics
        total_time=$(echo "$total_time + $response_time_ms" | bc)

        if (( $(echo "$response_time_ms < $min_time" | bc -l) )); then
            min_time=$response_time_ms
        fi

        if (( $(echo "$response_time_ms > $max_time" | bc -l) )); then
            max_time=$response_time_ms
        fi

        sleep 1
    done

    # Calculate average
    avg_time=$(echo "scale=2; $total_time / $PROBE_COUNT" | bc)

    # Determine color based on performance
    if (( $(echo "$avg_time < 100" | bc -l) )); then
        color=$GREEN
    elif (( $(echo "$avg_time < 300" | bc -l) )); then
        color=$YELLOW
    else
        color=$RED
    fi

    echo -e "\n${color}Results for ${name}:${NC}"
    echo "  Average: ${avg_time}ms"
    echo "  Min: ${min_time}ms"
    echo "  Max: ${max_time}ms"

    # Return average for JSON output
    echo "$avg_time"
}

# Test endpoints
echo "🔍 Starting edge storage probes..."
echo "Target: $BASE_URL"
echo ""

# Health check
health_avg=$(measure_latency "/api/healthcheck" "Health Check")

# KV Storage
kv_avg=$(measure_latency "/api/kv-test" "KV Storage")

# R2 Storage
r2_avg=$(measure_latency "/api/r2-test" "R2 Storage")

# D1 Database
d1_avg=$(measure_latency "/api/d1-test" "D1 Database")

# Generate JSON report
cat > edge-storage-latency-probe.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "base_url": "$BASE_URL",
  "probe_count": $PROBE_COUNT,
  "results": {
    "healthcheck": {
      "average_ms": $health_avg,
      "endpoint": "/api/healthcheck"
    },
    "kv": {
      "average_ms": $kv_avg,
      "endpoint": "/api/kv-test"
    },
    "r2": {
      "average_ms": $r2_avg,
      "endpoint": "/api/r2-test"
    },
    "d1": {
      "average_ms": $d1_avg,
      "endpoint": "/api/d1-test"
    }
  }
}
EOF

echo -e "\n✅ Edge storage probe complete!"
echo "📄 Results saved to: edge-storage-latency-probe.json"

# Check if running on 3G (Network Link Conditioner)
if networksetup -listallhardwareports | grep -q "Network Link Conditioner"; then
    echo -e "\n${YELLOW}⚠️  Network Link Conditioner detected - results reflect throttled conditions${NC}"
fi

# Summary
echo -e "\n📋 Summary:"
echo "  • Health Check: ${health_avg}ms"
echo "  • KV Storage: ${kv_avg}ms"
echo "  • R2 Storage: ${r2_avg}ms"
echo "  • D1 Database: ${d1_avg}ms"
