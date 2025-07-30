# Recovery Compass Docker Makefile
# Force multiplication through simple commands

.PHONY: help up down status logs restart clean build test

# Default target - show help
help:
	@echo "Recovery Compass Docker Commands:"
	@echo "  make up        - Start all services"
	@echo "  make up-min    - Start minimal services (postgres + redis only)"
	@echo "  make down      - Stop all services"
	@echo "  make status    - Show service status"
	@echo "  make logs      - Show service logs"
	@echo "  make restart   - Restart all services"
	@echo "  make clean     - Stop services and remove volumes"
	@echo "  make build     - Build all service images"
	@echo "  make test      - Run health checks"

# Start all services
up:
	docker compose up -d

# Start minimal services only
up-min:
	docker compose -f docker-compose.minimal.yml up -d

# Stop all services
down:
	docker compose down
	docker compose -f docker-compose.minimal.yml down

# Show service status
status:
	@echo "=== Full Stack Status ==="
	-docker compose ps
	@echo "\n=== Minimal Stack Status ==="
	-docker compose -f docker-compose.minimal.yml ps

# Show logs
logs:
	docker compose logs -f

# Show logs for minimal stack
logs-min:
	docker compose -f docker-compose.minimal.yml logs -f

# Restart services
restart:
	$(MAKE) down
	$(MAKE) up

# Clean everything (including volumes)
clean:
	docker compose down -v
	docker compose -f docker-compose.minimal.yml down -v

# Build service images
build:
	docker compose build

# Test database connections
test:
	@echo "Testing PostgreSQL..."
	@docker exec recovery-compass-postgres pg_isready -U recovery_compass || echo "PostgreSQL not ready"
	@echo "\nTesting Redis..."
	@docker exec recovery-compass-redis redis-cli ping || echo "Redis not ready"

# Database shell access
db-shell:
	docker exec -it recovery-compass-postgres psql -U recovery_compass

# Redis shell access
redis-shell:
	docker exec -it recovery-compass-redis redis-cli

# Create .env.secrets from template
init-secrets:
	@if [ ! -f .env.secrets ]; then \
		cp .env.secrets.example .env.secrets; \
		echo "Created .env.secrets - please fill in your actual values"; \
	else \
		echo ".env.secrets already exists"; \
	fi

# Show environment
show-env:
	@echo "=== Current Environment ==="
	@cat .env
	@echo "\n=== Secrets Status ==="
	@if [ -f .env.secrets ]; then \
		echo "✅ .env.secrets exists"; \
	else \
		echo "❌ .env.secrets missing - run 'make init-secrets'"; \
	fi
