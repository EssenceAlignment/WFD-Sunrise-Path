# 🤖 Recovery Compass Agent Team Configuration

## Core Agent Roles

### 1. **Compliance Automation Agent**
```yaml
role: compliance_automation
constraints:
  - trauma_informed: true
  - multi_agency_format: true
  - deployment_ready: true
  - privacy_preserving: true
capabilities:
  - Generate audit scripts
  - Create compliance reports
  - Validate multi-stakeholder requirements
  - Ensure HIPAA/regulatory adherence
output_formats:
  - TypeScript code
  - Test suites
  - Deployment YAML
  - Executive summaries
```

### 2. **Pilot Integration Agent**
```yaml
role: pilot_integration
constraints:
  - environmental_response: true
  - real_assessment_flows: true
  - partner_dashboard_metrics: true
capabilities:
  - Bridge assessment flows
  - Integrate WFD reporting
  - Sync FQHC dashboards
  - Generate partner metrics
output_formats:
  - API connectors
  - Dashboard components
  - Metric visualizations
  - Integration guides
```

### 3. **Review/Refactor Agent**
```yaml
role: review_refactor
constraints:
  - impact_translation: true
  - multi_stakeholder_reuse: true
  - compounding_benefit: true
capabilities:
  - Code optimization
  - Pattern recognition
  - Stakeholder alignment
  - Documentation generation
output_formats:
  - Refactored code
  - Impact translations
  - Best practice guides
  - Migration scripts
```

### 4. **Force Multiplier Agent**
```yaml
role: force_multiplier
constraints:
  - one_action_ten_outputs: true
  - systematic_compounding: true
  - multi_domain_benefit: true
capabilities:
  - Cascade generation
  - Cross-system propagation
  - Automated distribution
  - Value multiplication
output_formats:
  - Cascade workflows
  - Distribution scripts
  - Multiplication metrics
  - ROI dashboards
```

### 5. **Dashboard Population Agent**
```yaml
role: dashboard_population
constraints:
  - real_time_sync: true
  - multi_source_integration: true
  - accuracy_validation: true
capabilities:
  - Airtable synchronization
  - Perplexity data fetch
  - Metric calculation
  - Automated reporting
output_formats:
  - Population scripts
  - Sync configurations
  - Validation reports
  - Performance metrics
```

## Agent Cascade Patterns

### Pattern 1: Funding Discovery Cascade
```
Discovery Agent → Validation Agent → Population Agent → Notification Agent → Analytics Agent
```

### Pattern 2: Compliance Cascade
```
Audit Agent → Documentation Agent → Validation Agent → Distribution Agent → Archive Agent
```

### Pattern 3: Integration Cascade
```
API Agent → Transform Agent → Validation Agent → Dashboard Agent → Alert Agent
```

## Force Multiplication Rules

1. **Every Action Must**:
   - Generate 3+ outputs minimum
   - Serve 2+ stakeholder groups
   - Create reusable components
   - Document patterns learned

2. **Quality Gates**:
   - Trauma-informed communication ✓
   - Multi-stakeholder benefit ✓
   - Deployment readiness ✓
   - Compounding value ✓

3. **Output Requirements**:
   - Code + Tests + Docs + Dashboards
   - Immediate + 30-day + 90-day value
   - Technical + Executive summaries
   - Metrics + Visualizations

## MCP Tool Registration

```javascript
// Register agent tools with MCP
const agentTools = {
  populate_funding_dashboard: {
    description: "Populate funding opportunities dashboard",
    inputs: ["source", "filters", "validation_rules"],
    outputs: ["dashboard_data", "metrics", "reports"]
  },
  generate_audit_package: {
    description: "Generate compliance audit package",
    inputs: ["scope", "requirements", "timeframe"],
    outputs: ["audit_scripts", "reports", "evidence", "summaries"]
  },
  cascade_deployment: {
    description: "Deploy force-multiplier cascade",
    inputs: ["cascade_type", "targets", "validation"],
    outputs: ["deployment_status", "metrics", "next_actions"]
  }
};
```

## Implementation Checklist

- [ ] Create `.ai_context` beacon file
- [ ] Configure agent team roles
- [ ] Set up MCP tool registrations
- [ ] Implement cascade patterns
- [ ] Create validation workflows
- [ ] Set up metric tracking
- [ ] Configure auto-deployment
- [ ] Document force multipliers
