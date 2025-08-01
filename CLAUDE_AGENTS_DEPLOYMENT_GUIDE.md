# 🚀 Claude Code Agents × Cline AI Deployment Guide
## Force-Multiplier Implementation Across Recovery Compass

### Projects Ready for Deployment

1. **recovery-compass-journeys** ✅
2. **recovery-compass-funding** ✅
3. **recovery-compass-github.io** ✅
4. **WFD-Sunrise-Path** ✅ (Current Project)
5. **recovery-compass-docker** ✅
6. **recovery-compass-grant-system** ✅

## Step 1: Install Dependencies

```bash
# Install PyNaCl for cryptographic signatures
pip install pynacl
```

## Step 2: Deploy Agents to All Projects

### Option A: Full Deployment (All Projects)
```bash
# Deploy Claude Code Agents to all Recovery Compass projects
python3 scripts/deploy_claude_agents.py
```

### Option B: Deploy with OAuth Fix Pattern
```bash
# Preview first
python3 scripts/deploy_claude_agents.py --plan --pattern oauth_redirect

# If preview looks good, execute
python3 scripts/deploy_claude_agents.py --pattern oauth_redirect
```

## Step 3: Activate Agents in VS Code

For each project:

1. Open project in VS Code
2. Ensure Cline extension is active
3. Run `/agents` command to activate agent teams
4. Verify `.ai_context` is loaded

## Step 4: Configure MCP Servers

Each project will have:
- `.mcp/claude_agents_config.json` - Agent configuration
- `AI_CONTEXT_CLAUDE_AGENTS.md` - Agent context
- `AGENT_TEAM_TEMPLATE.md` - Agent definitions

## Step 5: Test Agent Cascades

### Test OAuth Error Resolution
```python
# Simulate OAuth error
from supervisor.patterns.oauth_errors import OAuthErrorPatterns

detector = OAuthErrorPatterns()
test_log = "Error: No redirect uri set!"
detections = detector.detect_patterns(test_log)

# Should trigger OAuth → Token migration cascade
```

### Test Force Multiplication
```bash
# Run force multiplication engine
python3 scripts/force_multiplication_engine.py

# Check cascade metrics
python3 scripts/pattern_collector.py
```

## Step 6: Monitor Deployment

### Key Metrics to Track
- **Cascade Success Rate**: Target > 90%
- **MTTR**: Target < 300 seconds
- **Force Multiplier**: Target 10x outputs
- **Error Detection Rate**: Patterns/hour

### Dashboard Locations
- Cascade Governor: `http://localhost:8080`
- Metrics: `metrics/cascade_governor.json`
- Provenance Logs: `supervisor/logs/snippets/`

## Step 7: Operational Procedures

### Daily Operations
1. Monitor cascade queue depth
2. Check circuit breaker states
3. Review MTTR metrics
4. Validate provenance signatures

### Weekly Operations
1. Analyze pattern frequency
2. Review suggested patterns
3. Update pattern library
4. Clean old snippets (automated)

### Monthly Operations
1. Audit provenance trails
2. Update agent configurations
3. Review force multiplication metrics
4. Optimize cascade patterns

## Agent Specializations by Project

### recovery-compass-journeys
- **Primary**: Journey Mapping Agent
- **Secondary**: User Experience, Accessibility
- **Focus**: User journey optimization

### recovery-compass-funding
- **Primary**: Funding Discovery Agent
- **Secondary**: Grant Writing, Compliance
- **Focus**: Automated funding discovery

### recovery-compass-github.io
- **Primary**: Documentation Generation Agent
- **Secondary**: SEO, Multi-Language
- **Focus**: Public documentation

### recovery-compass-docker
- **Primary**: Infrastructure Automation Agent
- **Secondary**: Security, Performance
- **Focus**: Container orchestration

### recovery-compass-grant-system
- **Primary**: Grant Tracking Agent
- **Secondary**: Application Automation, Deadlines
- **Focus**: Grant management

## Troubleshooting

### Common Issues

1. **"PyNaCl not installed"**
   ```bash
   pip install pynacl
   ```

2. **"Project path not found"**
   - Verify project paths in `scripts/deploy_claude_agents.py`
   - Update PROJECTS dictionary with correct paths

3. **"Circuit breaker OPEN"**
   - Check cascade governor metrics
   - Review error logs for root cause
   - Wait for timeout or manually reset

4. **"Rate limit exceeded"**
   - Check API quotas in cascade governor
   - Reduce cascade frequency
   - Implement backoff strategy

## Security Considerations

- **Keys**: Stored in `supervisor/.keys/` (git-ignored)
- **Logs**: No PII in provenance snippets
- **Retention**: 30-day automatic cleanup
- **Access**: Role-based cascade permissions

## Success Criteria

✅ All 6 projects have `.ai_context` files
✅ Agent teams activated in each project
✅ OAuth error patterns detected and resolved
✅ Provenance tracking operational
✅ Metrics flowing to dashboards
✅ Force multiplication > 10x achieved

## Next Phase: Expansion

1. **Add More Patterns**
   - Database connection errors
   - API timeout patterns
   - Configuration mismatches

2. **Enhance Agents**
   - ML-based pattern learning
   - Predictive error prevention
   - Cross-project intelligence

3. **Scale Operations**
   - Multi-region deployment
   - Distributed cascade processing
   - Global pattern library

## Remember

> **"Every agent action creates abundance through force multiplication."**

The Claude Code Agents are now your 100+ person AI workforce, ready to transform single actions into cascading benefits across the entire Recovery Compass ecosystem.

---

**Deployment Status**: Ready
**Force Multiplier**: Active
**Abundance Mode**: Engaged
