# Organization Repository Template

This template provides a standardized structure for all Recovery Compass repositories with built-in security, compliance, and platform policies.

## 🚀 Features

- **Automated Security Scanning**: TruffleHog, Trivy, and Dependabot pre-configured
- **Docker Platform Slice**: Profile-aware compose with health checks and registry mirroring
- **Secret Management**: GitHub Secrets integration with push protection
- **CI/CD Pipeline**: Reusable workflows with Kompose validation
- **Compliance Ready**: HIPAA, 501(c)(3), and grant compliance templates

## 📁 Repository Structure

```
.
├── .github/
│   ├── workflows/
│   │   ├── platform-check.yml    # Calls the reusable platform-slice workflow
│   │   └── security-scan.yml     # Automated security scanning
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE/
│   └── dependabot.yml
├── recovery-compass-docker/
│   ├── docker-compose.yml         # Your service definitions
│   └── secrets/                   # .gitignored secrets directory
├── .ai_context                    # AI assistant context
├── .gitignore
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── README.md
```

## 🎯 Quick Start

1. **Create New Repository from Template**
   - Click "Use this template" button
   - Name your repository following the pattern: `recovery-compass-[service-name]`

2. **Configure Secrets**
   ```bash
   # Required secrets in GitHub repository settings:
   - POSTGRES_PASSWORD
   - REDIS_PASSWORD
   - GRAFANA_ADMIN_PASSWORD (optional)
   - SNYK_TOKEN (for dependency scanning)
   ```

3. **Customize Docker Services**
   - Edit `recovery-compass-docker/docker-compose.yml`
   - Follow the platform-slice pattern for new services
   - Use profiles for optional components

4. **Enable Security Features**
   - Push protection is automatically enabled
   - Dependabot will create PRs for vulnerabilities
   - Security scanning runs on every push

## 🔒 Security Policies

- **No hardcoded secrets**: Use GitHub Secrets or Docker secrets
- **Tag-pinned images**: Prevent version drift
- **Health checks required**: All services must define health checks
- **Registry mirroring**: Use GHCR to avoid Docker Hub rate limits

## 📊 Monitoring Profiles

```bash
# Core services only (default)
docker compose up -d

# With metrics
COMPOSE_PROFILES=metrics docker compose up -d

# With logging
COMPOSE_PROFILES=logging docker compose up -d

# Full stack
COMPOSE_PROFILES=full docker compose up -d
```

## 🏗️ CI/CD Pipeline

The platform-slice workflow automatically:
- ✅ Validates Docker Compose syntax
- ✅ Checks Kompose compatibility
- ✅ Runs security scans
- ✅ Tests health checks
- ✅ Pushes images to GHCR

## 📝 Compliance Templates

- `SECURITY.md`: Security policies and vulnerability reporting
- `CODE_OF_CONDUCT.md`: Community guidelines
- `.ai_context`: AI assistant instructions for consistency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all CI checks pass
5. Submit a pull request

## 📞 Support

- Security issues: security@recovery-compass.org
- General questions: Create an issue
- Documentation: See `/docs` directory

---

*This repository follows Recovery Compass platform standards v1.0*
