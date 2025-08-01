# 🤖 Claude Code Agents Activation Template
## Gold-Plated IPE Standard Response

### Template Variables
- `{{SESSION_ID}}` - Unique cascade session identifier
- `{{PROJECT_NAME}}` - Current project name
- `{{CONFIG_VERSION}}` - Agent configuration version
- `{{AGENT_LIST}}` - Dynamically generated agent list with versions
- `{{MTTR_VALUE}}` - Latest OAuth-fix MTTR from metrics
- `{{SUCCESS_RATE}}` - Agent success percentage
- `{{ERRORS_ESCAPED}}` - Count of unhandled errors

### Standard Activation Response

```
🤖 Claude Code Agents Activated | Session {{SESSION_ID}}

**Project**: {{PROJECT_NAME}} (agents_config {{CONFIG_VERSION}})

### Loaded Agents
{{AGENT_LIST}}

### ⛑️ Guardrails Active
- ≤5 files per cascade
- ≤100 LOC net changes
- Provenance footer signed (ED25519)
- Preview mode: `python deploy_claude_agents.py --plan --pattern <error>`

### 📊 Last 24h KPIs
```
OAuth-fix MTTR: {{MTTR_VALUE}}s | Agent success: {{SUCCESS_RATE}}% | Errors escaped: {{ERRORS_ESCAPED}}
```

### ⚡ Available Commands

1. **find funding opportunities** - Draft & rank leads (+dashboard push)
2. **fix oauth errors** - Trigger auto-resolution cascade
3. **populate dashboard** - Sync latest metrics to Airtable
4. **generate compliance report** - Produce HIPAA/grant audit bundle
5. **deploy to all projects** - Propagate current branch across ecosystem

### 🎯 Force Multiplication Promise
Every command triggers:
- 10+ synchronized outputs
- 3+ stakeholder updates
- Reusable pattern documentation
- Full provenance audit trail

Ask me to begin any cascade when ready. Remember: **Abundance, not urgency.**
```

## Agent List Format

Each agent should be listed with:
- **Agent-Name-vX** (scope: specific-domains)

Example:
- **Funding-Discovery-v1** (scope: repo, grants)
- **Grant-Writer-v2** (scope: templates)
- **Compliance-Check-v1** (scope: HIPAA, 501c3)
- **Dashboard-Sync-v1** (scope: Airtable/Perplexity)
- **ROI-Analytics-v1** (scope: metrics)

## Session ID Generation

Session IDs follow the format: `CAS-{{8-char-hex}}`
- CAS = Cascade Activation Session
- 8 characters of hexadecimal for uniqueness

## Metrics Integration

KPIs should be pulled from:
- `metrics/cascade_governor.json` for real-time data
- Fallback to sensible defaults if metrics unavailable:
  - MTTR: 300s (target)
  - Success: 95.0%
  - Errors: 0

## Usage

1. When `/agents` command is received in Cline
2. Load current project context
3. Generate session ID
4. Pull latest metrics
5. Format response using this template
6. Present to user

## Compliance Checklist

- [ ] Session ID generated and visible
- [ ] Agent versions explicit
- [ ] Scopes defined for each agent
- [ ] Guardrails clearly stated
- [ ] Preview command included
- [ ] Live KPIs displayed
- [ ] Commands mapped to outcomes
- [ ] Force multiplication promise stated
- [ ] Abundance language used throughout
