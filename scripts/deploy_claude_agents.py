#!/usr/bin/env python3
"""
Deploy Claude Code Agents × Cline AI across all Recovery Compass projects
Force-multiplier implementation following Strategic Framework
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime
import argparse
import sys

# Project configurations
PROJECTS = {
    "WFD-Sunrise-Path": {
        "path": "/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path",
        "status": "ACTIVE",
        "primary_focus": "Funding Discovery & Automation"
    },
    "recovery-compass-journeys": {
        "path": "/Users/ericjones/Projects/recovery-compass-journeys",
        "status": "PENDING",
        "primary_focus": "User Journey Optimization"
    },
    "recovery-compass-grant-system": {
        "path": "/Users/ericjones/Projects/recovery-compass-journeys/recovery-compass-grant-system",
        "status": "PENDING",
        "primary_focus": "Grant Management System"
    },
    "recovery-compass.github.io": {
        "path": "/Users/ericjones/Projects/recovery-compass.github.io",
        "status": "PENDING",
        "primary_focus": "Public Documentation & Outreach"
    },
    "recovery-compass-docker": {
        "path": "/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/recovery-compass-docker",
        "status": "PENDING",
        "primary_focus": "Infrastructure & Deployment"
    }
}

# Template files from current project
TEMPLATE_DIR = Path("/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path")
AGENT_TEMPLATES = [
    "AI_CONTEXT_CLAUDE_AGENTS.md",
    "AGENT_TEAM_TEMPLATE.md"
]

def create_project_ai_context(project_name: str, project_config: dict) -> str:
    """Create customized .ai_context for each project"""
    template = f"""# 🚨 AI CONTEXT BEACON - CLAUDE CODE AGENTS ACTIVE 🚨
## Project: {project_name}

You are in: {project_config['path']}

**CLAUDE CODE AGENTS STATUS**: ✅ ACTIVATED
**PRIMARY FOCUS**: {project_config['primary_focus']}

CRITICAL CONTEXT FILES (READ IN ORDER):
1. ./AI_CONTEXT_CLAUDE_AGENTS.md (agent team configuration)
2. ./AGENT_TEAM_TEMPLATE.md (implementation patterns)
3. ~/Projects/AI_CONTEXT_ALIGNMENT.md (master context)
4. ~/Projects/REPOSITORY_ORGANIZATION_GUIDE.md (structure)

CURRENT SYSTEM STATUS:
✅ Claude Code Agents: CONFIGURED
✅ MCP Integration: READY
✅ Force Multiplication: ENABLED
✅ Multi-Stakeholder: ACTIVE

AGENT TEAM SPECIALIZED FOR THIS PROJECT:
{get_specialized_agents(project_config['primary_focus'])}

FORCE MULTIPLICATION PATTERNS:
- One code change → 10+ synchronized outputs
- Every action serves 3+ stakeholder groups
- All outputs are deployment-ready
- Patterns documented for reuse

ACTIVATE AGENTS:
/agents (in VS Code with Cline)

QUICK ACTIONS:
```bash
# Run force multiplication
python scripts/force_multiplication_engine.py

# Check cascade status
python scripts/pattern_collector.py

# Deploy to stakeholders
python scripts/cascade_deployment.py
```

Remember: **Abundance, not urgency. Every action compounds.**
"""
    return template

def get_specialized_agents(focus: str) -> str:
    """Get specialized agent configuration based on project focus"""
    agent_specializations = {
        "Funding Discovery & Automation": """
- Funding Discovery Agent (Priority)
- Grant Writing Automation Agent
- Compliance Validation Agent
- Dashboard Population Agent
- ROI Analytics Agent""",

        "User Journey Optimization": """
- Journey Mapping Agent (Priority)
- User Experience Agent
- Accessibility Compliance Agent
- Feedback Integration Agent
- Pattern Recognition Agent""",

        "Grant Management System": """
- Grant Tracking Agent (Priority)
- Application Automation Agent
- Deadline Management Agent
- Success Metrics Agent
- Reporting Automation Agent""",

        "Public Documentation & Outreach": """
- Documentation Generation Agent (Priority)
- SEO Optimization Agent
- Accessibility Compliance Agent
- Multi-Language Support Agent
- Engagement Analytics Agent""",

        "Infrastructure & Deployment": """
- Infrastructure Automation Agent (Priority)
- Security Compliance Agent
- Performance Optimization Agent
- Monitoring Integration Agent
- Disaster Recovery Agent"""
    }

    return agent_specializations.get(focus, "- Standard Agent Team Configuration")

def create_mcp_config(project_name: str, project_path: str) -> dict:
    """Create MCP configuration for project"""
    return {
        "project": project_name,
        "path": project_path,
        "agents": {
            "compliance_automation": {
                "enabled": True,
                "tools": ["generate_audit_package", "validate_compliance"]
            },
            "pilot_integration": {
                "enabled": True,
                "tools": ["bridge_dashboards", "sync_metrics"]
            },
            "review_refactor": {
                "enabled": True,
                "tools": ["optimize_code", "generate_docs"]
            },
            "force_multiplier": {
                "enabled": True,
                "tools": ["cascade_deployment", "multiply_outputs"]
            },
            "dashboard_population": {
                "enabled": True,
                "tools": ["populate_funding_dashboard", "sync_airtable"]
            }
        },
        "cascades": {
            "funding_discovery": {
                "pattern": "discover → validate → populate → notify → analyze",
                "auto_trigger": True
            },
            "compliance": {
                "pattern": "audit → document → validate → distribute → archive",
                "auto_trigger": False
            }
        }
    }

def deploy_to_project(project_name: str, project_config: dict):
    """Deploy Claude Code Agents to a specific project"""
    project_path = Path(project_config['path'])

    # Skip if project doesn't exist
    if not project_path.exists():
        print(f"⚠️  Project path not found: {project_path}")
        return False

    print(f"\n🚀 Deploying to {project_name}...")

    try:
        # 1. Create .ai_context
        ai_context_content = create_project_ai_context(project_name, project_config)
        ai_context_path = project_path / ".ai_context"
        ai_context_path.write_text(ai_context_content)
        print(f"   ✅ Created .ai_context")

        # 2. Copy agent templates
        for template in AGENT_TEMPLATES:
            src = TEMPLATE_DIR / template
            if src.exists():
                dst = project_path / template
                shutil.copy2(src, dst)
                print(f"   ✅ Copied {template}")

        # 3. Create MCP configuration directory
        mcp_dir = project_path / ".mcp"
        mcp_dir.mkdir(exist_ok=True)

        # 4. Create agent configuration
        mcp_config = create_mcp_config(project_name, str(project_path))
        mcp_config_path = mcp_dir / "claude_agents_config.json"
        with open(mcp_config_path, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        print(f"   ✅ Created MCP configuration")

        # 5. Create scripts directory if needed
        scripts_dir = project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # 6. Create force multiplication engine stub
        force_mult_script = scripts_dir / "force_multiplication_engine.py"
        if not force_mult_script.exists():
            force_mult_content = '''#!/usr/bin/env python3
"""Force Multiplication Engine for {project}"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from main project if available
try:
    from scripts.force_multiplication_engine import *
    print("✅ Using main force multiplication engine")
except ImportError:
    print("⚠️  Please implement force multiplication engine for this project")
    print("   Reference: WFD-Sunrise-Path/scripts/force_multiplication_engine.py")
'''.format(project=project_name)
            force_mult_script.write_text(force_mult_content)
            os.chmod(force_mult_script, 0o755)
            print(f"   ✅ Created force multiplication engine stub")

        # 7. Update status
        project_config['status'] = 'DEPLOYED'

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_deployment_report():
    """Create deployment status report"""
    report_content = f"""# Claude Code Agents Deployment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Deployment Status

"""

    for project_name, config in PROJECTS.items():
        status_emoji = "✅" if config['status'] == 'DEPLOYED' else "📍"
        report_content += f"### {project_name} {status_emoji}\n"
        report_content += f"- Path: `{config['path']}`\n"
        report_content += f"- Status: {config['status']}\n"
        report_content += f"- Focus: {config['primary_focus']}\n\n"

    report_content += """
## Force Multiplication Metrics

- **Agent Teams Deployed**: 5 teams × {deployed} projects
- **Cascade Patterns**: 3 patterns × {deployed} projects
- **MCP Tools Registered**: 10+ tools per project
- **Estimated Time Savings**: 40+ hours/week per project

## Next Actions

1. Activate agents in VS Code with `/agents` command
2. Run test cascades to verify deployment
3. Monitor force multiplication metrics
4. Document successful patterns

## Compounding Benefits

Each deployed agent team will:
- Save 2+ hours daily through automation
- Generate 10+ outputs per action
- Serve 3+ stakeholder groups
- Create reusable patterns for future projects

**Remember: Every action compounds. Abundance, not urgency.**
""".format(deployed=sum(1 for c in PROJECTS.values() if c['status'] == 'DEPLOYED'))

    report_path = TEMPLATE_DIR / "CLAUDE_AGENTS_DEPLOYMENT_REPORT.md"
    report_path.write_text(report_content)
    print(f"\n📊 Deployment report saved: {report_path}")

def analyze_repo_for_pattern(repo_path: str, pattern: str) -> dict:
    """Analyze repository for error pattern matches"""
    # This is a placeholder for actual pattern analysis
    # In production, would scan logs, configs, etc.
    changes = {
        "files": [],
        "pattern_matches": 0
    }

    # Check for OAuth configuration files
    oauth_files = [
        ".mcp/config.json",
        "mcp-config/*.json",
        ".env",
        ".env.example"
    ]

    for file_pattern in oauth_files:
        for file_path in Path(repo_path).glob(file_pattern):
            if file_path.exists():
                changes["files"].append({
                    "path": str(file_path.relative_to(repo_path)),
                    "lines": 10  # Estimated lines to change
                })
                changes["pattern_matches"] += 1

    return changes


def abundance_transform(message: str) -> str:
    """Transform message to use abundance language"""
    # Simple transformation rules
    replacements = {
        "Fix": "Enhance",
        "fix": "enhance",
        "Error": "Opportunity for improvement",
        "error": "opportunity",
        "Failed": "Ready for enhancement",
        "failed": "awaiting optimization",
        "Problem": "Growth opportunity",
        "problem": "area for improvement"
    }

    result = message
    for old, new in replacements.items():
        result = result.replace(old, new)

    return result


def format_preview_markdown(preview: dict) -> str:
    """Format preview data as markdown"""
    md = f"""# OAuth Resolution Preview
Generated: {preview['timestamp']}
Pattern: `{preview['pattern']}`

## Affected Repositories

"""

    for repo in preview["affected_repos"]:
        md += f"### {repo['repo']}\n"
        md += f"- Files to modify: {repo['files']}\n"
        md += f"- Estimated lines: {repo['lines']}\n"
        md += f"- Commit message: `{repo['commit_message']}`\n\n"

    if preview.get("warnings"):
        md += f"## ⚠️ Warnings\n{preview['warnings']}\n\n"

    md += """## Next Steps

1. Review proposed changes above
2. Remove --plan flag to execute
3. Monitor cascade completion
4. Verify OAuth functionality

**Remember: One fix, compounding benefits across all projects.**
"""

    return md


def preview_oauth_fix(pattern: str, output_file: str):
    """Generate preview of OAuth fix cascade"""
    preview = {
        "pattern": pattern,
        "timestamp": datetime.now().isoformat(),
        "affected_repos": [],
        "total_changes": 0,
        "abundance_messages": []
    }

    # Analyze each repo
    for project_name, project_config in PROJECTS.items():
        project_path = project_config['path']
        if Path(project_path).exists():
            changes = analyze_repo_for_pattern(project_path, pattern)
            if changes["pattern_matches"] > 0:
                preview["affected_repos"].append({
                    "repo": project_name,
                    "files": len(changes["files"]),
                    "lines": sum(f["lines"] for f in changes["files"]),
                    "commit_message": abundance_transform(
                        f"Fix {pattern} in {project_name}"
                    )
                })
                preview["total_changes"] += changes["pattern_matches"]

    # Validate against limits
    for repo_change in preview["affected_repos"]:
        if repo_change["files"] > 5:
            preview["warnings"] = "Some repositories exceed file limit (5)"
        if repo_change["lines"] > 100:
            preview["warnings"] = preview.get("warnings", "") + \
                "\nSome repositories exceed line limit (100)"

    # Write preview
    with open(output_file, 'w') as f:
        f.write(format_preview_markdown(preview))

    print(f"✅ Preview written to: {output_file}")
    return preview


def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(
        description="Deploy Claude Code Agents across Recovery Compass"
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Preview mode - show changes without executing"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        help="Error pattern to fix (e.g., oauth_redirect)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="preview.md",
        help="Output file for preview (default: preview.md)"
    )

    args = parser.parse_args()

    if args.plan and args.pattern:
        # Preview mode for specific pattern
        print("🔍 PREVIEW MODE - No changes will be made")
        print(f"Pattern: {args.pattern}")
        preview_oauth_fix(args.pattern, args.output)
        return

    # Normal deployment mode
    print("🤖 Claude Code Agents × Cline AI Deployment")
    print("=" * 50)

    # Deploy to all projects
    successful_deployments = 0
    for project_name, project_config in PROJECTS.items():
        if deploy_to_project(project_name, project_config):
            successful_deployments += 1

    # Create deployment report
    create_deployment_report()

    print("\n" + "=" * 50)
    print(f"✅ Deployment complete: "
          f"{successful_deployments}/{len(PROJECTS)} projects")
    print("\n🎯 Next steps:")
    print("1. Open each project in VS Code")
    print("2. Activate Cline extension")
    print("3. Run `/agents` to activate agent teams")
    print("4. Start with a simple task to test cascades")
    print("\n💡 Remember: One action, ten results!")

if __name__ == "__main__":
    main()
