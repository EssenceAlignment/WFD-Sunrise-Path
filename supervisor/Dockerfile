FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    aiohttp==3.9.1 \
    asyncio \
    prometheus-client==0.19.0

# Copy governor code
COPY cascade_governor.py /app/
COPY integration/ /app/integration/

# Create metrics directory
RUN mkdir -p /app/metrics

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the governor
CMD ["python", "-u", "cascade_governor.py"]

EXPOSE 8080
