# Recovery Compass Docker Repository Topology Decision

## Date: July 30, 2025

## Decision: Keep Docker Stack in Current Repository

### Recommendation: **Option 1 - Subdirectory in Current Repo**

After analyzing the project structure and considering force multiplication principles, the recommendation is to keep the Docker configuration as a subdirectory within the current repository.

## Analysis

### Option 1: Subdirectory (RECOMMENDED) ✅

**Structure:**
```
WFD-Sunrise-Path/
├── recovery-compass-docker/     # Docker configuration
│   ├── docker-compose.yml
│   ├── services/
│   ├── Makefile
│   └── docs/
├── scripts/                     # Existing automation
├── .github/                     # CI/CD workflows
└── ...                         # Other project files
```

**Advantages:**
- ✅ Simplified CI/CD - no submodule updates
- ✅ Single repository to clone and manage
- ✅ Easier for contributors and partners
- ✅ Unified version control
- ✅ Shared GitHub Actions workflows
- ✅ Can reference parent scripts directly

**Disadvantages:**
- ❌ Larger repository size
- ❌ Docker changes trigger main repo notifications

### Option 2: Separate Repository with Submodule

**Structure:**
```
recovery-compass-docker/         # Separate repo
├── docker-compose.yml
├── services/
└── ...

WFD-Sunrise-Path/
└── recovery-compass-docker/     # Git submodule reference
```

**Advantages:**
- ✅ Clean separation of concerns
- ✅ Independent versioning
- ✅ Smaller main repository

**Disadvantages:**
- ❌ Complex CI/CD (submodule updates)
- ❌ Extra steps for contributors
- ❌ Potential sync issues
- ❌ Harder to reference parent scripts

## Implementation Plan for Option 1

### 1. Directory Structure (Already Started)
```bash
recovery-compass-docker/
├── READINESS_ASSESSMENT.md      ✅ Created
├── SECRETS_MANAGEMENT.md        ✅ Created
├── SERVICE_CONTRACTS.md         ✅ Created
├── .env.secrets.example         ✅ Created
├── REPOSITORY_TOPOLOGY_DECISION.md  ✅ This file
├── docker-compose.yml           📋 Next
├── docker-compose.override.yml  📋 Dev overrides
├── docker-compose.prod.yml      📋 Production
├── Makefile                     📋 Common commands
├── .dockerignore               📋 Build ignores
├── services/                   📋 Service definitions
│   ├── funding-engine/
│   ├── erd-platform/
│   ├── metrics-relay/
│   ├── partner-portal/
│   └── pattern-engine/
└── docs/                       📋 Documentation
    ├── DEPLOYMENT.md
    └── PARTNER_SETUP.md
```

### 2. CI/CD Integration

Update `.github/workflows/docker-security.yml` paths:
```yaml
paths:
  - 'recovery-compass-docker/**'
  - '.github/workflows/docker-security.yml'
```

### 3. Script References

Services can reference parent scripts:
```dockerfile
# In funding-engine/Dockerfile
COPY ../../scripts/populate_funding_dashboard_mcp.py /app/
```

Or via volume mounts:
```yaml
volumes:
  - ./scripts:/app/shared-scripts:ro
```

### 4. Documentation Updates

Update main README.md:
```markdown
## Docker Deployment

See [recovery-compass-docker/](./recovery-compass-docker/) for containerized deployment.

Quick start:
```bash
cd recovery-compass-docker
make up
```
```

## Decision Rationale

Keeping the Docker configuration in the current repository as a subdirectory aligns with Recovery Compass's force multiplication philosophy:

1. **One Repository = Ten Benefits**
   - Unified CI/CD
   - Shared security scanning
   - Common documentation
   - Integrated testing
   - Single clone operation
   - Unified issues/PRs
   - Shared GitHub Apps
   - Common secrets management
   - Integrated deployment
   - Simplified partner onboarding

2. **Soft Power Approach**
   - Lower barrier to entry
   - Natural discovery of Docker option
   - Gradual adoption path
   - No forced complexity

## Next Steps

1. ✅ Gate 5 Decision: **Subdirectory in current repo**
2. 📋 Create docker-compose.yml
3. 📋 Add Makefile for common operations
4. 📋 Create service Dockerfiles
5. 📋 Update CI/CD for Docker builds

## Approval

- [x] Technical Decision: Subdirectory approach
- [ ] Team Review: Pending
- [ ] Implementation: Ready to proceed

*Decision made: July 30, 2025*
*Decision maker: Recovery Compass Technical Team*
