# Recovery Compass Docker Secrets Management

## Overview

This document defines how Recovery Compass handles secrets in containerized environments, ensuring compliance with HIPAA and 501(c)(3) security requirements.

## Secret Categories

### 1. API Credentials
- Airtable API keys
- Perplexity API keys
- GitHub tokens
- MCP server credentials

### 2. Database Credentials
- PostgreSQL passwords
- Redis passwords
- Connection strings

### 3. Service-to-Service Auth
- JWT signing keys
- Internal API tokens
- Health check tokens

## Secret Injection Strategy

### Development Environment

```bash
# .env.secrets (git-ignored)
AIRTABLE_API_KEY=key_xxx
PERPLEXITY_API_KEY=pplx_xxx
POSTGRES_PASSWORD=secure_password
JWT_SECRET=your_jwt_secret
```

### Production Environment

Using Docker Secrets (Swarm/Enterprise):
```yaml
secrets:
  airtable_key:
    external: true
  postgres_password:
    external: true

services:
  funding-engine:
    secrets:
      - airtable_key
      - postgres_password
    environment:
      AIRTABLE_API_KEY_FILE: /run/secrets/airtable_key
```

### CI/CD Environment

GitHub Actions secrets:
```yaml
- name: Run tests
  env:
    AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
    POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
```

## Security Best Practices

### 1. Never Store Secrets In:
- Docker images (use build args carefully)
- Git repositories
- Container environment variables (in production)
- Log files

### 2. Always:
- Use file-based secrets in production
- Rotate secrets quarterly
- Use least-privilege access
- Monitor secret access

### 3. Secret Rotation Process:
1. Generate new secret
2. Update in secret store
3. Deploy with both old and new
4. Verify new secret works
5. Remove old secret

## Implementation Checklist

- [ ] Create `.env.secrets.example` with dummy values
- [ ] Add `.env.secrets` to `.gitignore`
- [ ] Configure GitHub Secrets for CI
- [ ] Set up Docker Secrets for production
- [ ] Enable secret scanning in repos
- [ ] Document rotation schedule

## Compliance Requirements

### HIPAA Compliance:
- Encrypt secrets at rest
- Audit secret access
- Implement access controls
- Regular security reviews

### Grant Compliance:
- Document security measures
- Demonstrate best practices
- Regular vulnerability scans
- Incident response plan

## Secret Template

```bash
# .env.secrets.example
# Copy to .env.secrets and fill with real values

# External APIs
AIRTABLE_API_KEY=your_airtable_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
GITHUB_TOKEN=your_github_token_here

# Database
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_USER=recovery_compass
DB_CONNECTION_STRING=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_PASSWORD=your_redis_password_here

# Security
JWT_SECRET=your_jwt_secret_here
ENCRYPTION_KEY=your_encryption_key_here

# Service Tokens
INTERNAL_API_KEY=your_internal_api_key_here
HEALTH_CHECK_TOKEN=your_health_token_here

# MCP Configuration
MCP_FILESYSTEM_PATH=/path/to/mcp/data
MCP_CLOUDFLARE_TOKEN=your_cloudflare_token_here
```

## Verification

Run these commands to verify secret security:

```bash
# Check for secrets in code
trivy fs . --security-checks secret

# Verify Docker images don't contain secrets
trivy image recovery-compass/funding-engine:latest

# Check git history for secrets
git secrets --scan-history
