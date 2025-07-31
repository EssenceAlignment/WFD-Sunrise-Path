# Unified API Throttle & Cost Telemetry Proxy

A force-multiplying solution that provides centralized rate limiting, cost tracking, and reliability improvements for all external API integrations.

## Overview

This Envoy-based proxy service implements Option B from the strategic execution plan, providing:

- **Token-bucket rate limiting** per API and environment
- **Real-time cost telemetry** with Prometheus metrics
- **Circuit breakers** and retry logic for reliability
- **Unified configuration** for all external APIs

## Force Multiplication Benefits

### 1. Single Point of Control
- One proxy manages rate limits for CharityAPI, Airtable, Perplexity, and future APIs
- Changes to rate limits don't require code modifications
- Centralized metrics collection for all API usage

### 2. Automatic Cost Tracking
- Per-request cost calculation based on API and mode (test vs. live)
- Prometheus metrics: `api_calls_total`, `api_429s_total`, `cost_usd_total`
- Real-time cost dashboards in Grafana showing "cost per $ secured"

### 3. Proactive Rate Limit Management
- Token bucket algorithm prevents 429 errors before they happen
- 100 requests/minute default (configurable per API)
- Automatic request queuing during bursts

### 4. Enhanced Reliability
- Built-in circuit breakers prevent cascade failures
- Automatic retry with exponential backoff
- Health checks and admin interface at port 9901

## Configuration

### Environment Variables

```bash
# Enable proxy for CharityAPI client
USE_API_PROXY=true
API_PROXY_URL=http://api-proxy:8080

# API mode selection
CHARITY_API_MODE=test  # or 'live'
```

### Rate Limits (in envoy.yaml)

```yaml
token_bucket:
  max_tokens: 100        # Maximum burst size
  tokens_per_fill: 100   # Tokens added per interval
  fill_interval: 60s     # Refill interval
```

### Cost Configuration (in cost-calculator.lua)

```lua
charityapi = {
  base_cost = 0.001,     # $0.001 per request
  live_multiplier = 10   # 10x cost for live vs test
}
```

## Usage

### 1. Start the Proxy

```bash
cd recovery-compass-docker
docker-compose -f docker-compose.monitoring.yml up api-proxy
```

### 2. Configure Applications

Update your API clients to use the proxy:

```typescript
// CharityAPI automatically uses proxy when USE_API_PROXY=true
const api = new CharityAPI({
  mode: 'test'
});
```

### 3. Monitor Metrics

Access the admin interface:
- Admin UI: http://localhost:9901
- Metrics: http://localhost:9901/stats/prometheus

View in Grafana:
- API request rates by service
- Cost accumulation over time
- Rate limit violations
- Circuit breaker status

## Metrics Emitted

| Metric | Description | Labels |
|--------|-------------|--------|
| `api_request_total` | Total API requests | api, status |
| `api_request_duration_seconds` | Request latency | api, status |
| `api_rate_limit_violations_total` | Rate limit hits | api |
| `api_cost_usd_total` | Accumulated cost | api, mode |
| `api_circuit_breaker_open` | Circuit breaker status | api |

## Adding New APIs

1. Add cluster configuration in `envoy.yaml`:

```yaml
- name: new_api_cluster
  type: LOGICAL_DNS
  dns_lookup_family: V4_ONLY
  load_assignment:
    cluster_name: new_api_cluster
    endpoints:
    - lb_endpoints:
      - endpoint:
          address:
            socket_address:
              address: api.newservice.com
              port_value: 443
```

2. Add routing rules:

```yaml
- name: new_api
  domains: ["api.newservice.com"]
  routes:
  - match:
      prefix: "/"
    route:
      cluster: new_api_cluster
```

3. Update cost configuration in `cost-calculator.lua`:

```lua
new_api = {
  base_cost = 0.002,
  rate_limit = 10
}
```

## Architecture Benefits

### Immediate Wins
- CharityAPI rate limits handled automatically
- No code changes needed for rate limit adjustments
- Cost visibility for budget planning

### Future Extensions
- Add Option A (Contract Testing) by monitoring API responses
- Add Option C (Secret Rotation) by injecting rotated keys
- Support for OAuth token refresh
- Request/response caching layer
- API usage quotas and alerts

## Troubleshooting

### Proxy Not Starting
```bash
docker logs recovery-compass-api-proxy
```

### Rate Limits Too Restrictive
Adjust `max_tokens` and `tokens_per_fill` in envoy.yaml

### Metrics Not Appearing
Check Prometheus scrape config includes api-proxy:9901

### Connection Refused
Ensure proxy is in same Docker network as applications

## Next Steps

1. **Deploy proxy** with monitoring stack
2. **Configure Grafana dashboard** for API costs
3. **Set cost alerts** for budget thresholds
4. **Extend to all APIs** beyond CharityAPI

This single implementation provides the foundation for comprehensive API governance, turning a CharityAPI-specific need into a platform-wide capability.
