# 🤖 How to Activate Claude Code Agents in VS Code

## Important: `/agents` is a Cline Extension Command

The `/agents` command is used **inside VS Code**, not in the terminal.

## Steps to Activate Agents:

### 1. Open Project in VS Code
```bash
# For example, to open the current project:
code .

# Or open a specific project:
code ~/Projects/recovery-compass-journeys
```

### 2. Ensure Cline Extension is Active
- Look for the Cline icon in the VS Code sidebar
- Or press `Cmd+Shift+P` and search for "Cline"

### 3. Use the `/agents` Command
- Open a new Cline chat (click Cline icon or use keyboard shortcut)
- In the Cline chat window, type: `/agents`
- Press Enter

### 4. Verify Agent Activation
The agents will load the context from:
- `.ai_context` file (project-specific context)
- `AI_CONTEXT_CLAUDE_AGENTS.md` (agent configuration)
- `AGENT_TEAM_TEMPLATE.md` (agent templates)

## Testing Agent Cascades

Once agents are activated, test with a simple task:

```
"Check for OAuth errors in the logs and fix them"
```

Or:

```
"Run the force multiplication engine to populate funding dashboard"
```

## Deployed Projects Status

✅ **Successfully Deployed (4/5)**:
- WFD-Sunrise-Path
- recovery-compass-journeys
- recovery-compass-grant-system
- recovery-compass-docker

❓ **Check Path For**:
- recovery-compass.github.io (may need path update)

## Quick Terminal Commands

While `/agents` is for VS Code, here are useful terminal commands:

```bash
# Test OAuth pattern detection
python3 supervisor/patterns/oauth_errors.py

# Preview OAuth fixes
python3 scripts/deploy_claude_agents.py --plan --pattern oauth_redirect

# Run force multiplication engine
python3 scripts/force_multiplication_engine.py
```

## Remember

- `/agents` = VS Code Cline command
- Not a terminal/bash command
- Must be inside VS Code with Cline extension active

The agents are now ready to multiply your actions 10x across all projects!
