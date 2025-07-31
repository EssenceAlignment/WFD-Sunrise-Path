FROM envoyproxy/envoy:v1.29-latest

# Copy custom Envoy configuration
COPY envoy.yaml /etc/envoy/envoy.yaml

# Add cost calculation script
COPY cost-calculator.lua /etc/envoy/cost-calculator.lua

# Ensure proper permissions
RUN chmod 644 /etc/envoy/envoy.yaml /etc/envoy/cost-calculator.lua

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:9901/ready || exit 1

CMD ["/usr/local/bin/envoy", "-c", "/etc/envoy/envoy.yaml"]
