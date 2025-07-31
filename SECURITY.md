# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < main  | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow these steps:

1. **DO NOT** open a public issue
2. Email security concerns to: security@recovery-compass.org
3. Include the following information:
   - Type of vulnerability
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Any special configuration required to reproduce the issue
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Resolution Target**:
  - Critical: 24 hours
  - High: 72 hours
  - Medium: 7 days
  - Low: 30 days

## Security Measures

### Automated Scanning
- Daily Dependabot scans for dependency vulnerabilities
- Weekly CodeQL analysis for code vulnerabilities
- Pre-commit hooks for security validation
- Automated npm audit on all pull requests

### Current Known Issues
As of July 30, 2025, we are aware of vulnerabilities in example applications:
- `welcome-to-docker/`: Example app with known vulnerabilities (use at own risk)
- `multi-container-app/`: Example app with known vulnerabilities (use at own risk)
- `multi-container-app-2/`: Example app with known vulnerabilities (use at own risk)

**Note**: These example applications are provided for educational purposes only and should not be used in production environments without proper security remediation.

### Security Best Practices
1. Keep all dependencies up to date
2. Run `npm audit` before committing changes
3. Use the provided Docker base images with security patches
4. Follow OWASP guidelines for web application security
5. Implement proper input validation and sanitization

## Vulnerability Disclosure Policy

We follow responsible disclosure practices:
1. Security researchers are given credit for discovered vulnerabilities
2. We work with researchers to understand and resolve issues
3. Public disclosure occurs after patches are available
4. We maintain a security advisory page for resolved issues

## Security Configuration

### Required Security Headers
```javascript
// Recommended security headers for production
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

### Environment Variables
Never commit sensitive data. Use environment variables for:
- API keys
- Database credentials
- JWT secrets
- Third-party service credentials

## Contact

Security Team: security@recovery-compass.org
Project Maintainers: @EssenceAlignment

---

*Last Updated: July 30, 2025*
