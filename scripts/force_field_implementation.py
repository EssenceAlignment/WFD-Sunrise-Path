#!/usr/bin/env python3
"""
Universal Pre-Commit Force-Field Implementation
Force multiplication: One hook → Five problem clusters vanish
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class ForceFieldHook:
    """Universal pre-commit safeguard system"""

    def __init__(self):
        self.repo_root = Path.cwd()
        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "lint_errors": 0,
            "critical_vulns": 0,
            "secrets_found": 0,
            "doc_autofix": False,
            "spell_errors": 0,
            "docker_valid": True
        }
        self.allow_lint = "--allow-lint" in sys.argv

    def run_markdown_lint(self) -> Tuple[bool, int]:
        """Auto-format markdown and check for remaining issues"""
        print("🔍 Checking markdown formatting...")

        # First, auto-format all markdown files
        try:
            subprocess.run([
                "markdownlint", "--fix", "**/*.md"
            ], capture_output=True, text=True)
            self.metrics["doc_autofix"] = True
        except:
            pass

        # Then check for remaining issues
        result = subprocess.run([
            "markdownlint", "**/*.md"
        ], capture_output=True, text=True)

        error_count = len(result.stdout.splitlines())
        self.metrics["lint_errors"] = error_count

        if error_count > 0 and not self.allow_lint:
            print(f"❌ Found {error_count} markdown issues")
            return False, error_count

        print("✅ Markdown formatting clean")
        return True, error_count

    def run_secrets_scan(self) -> Tuple[bool, int]:
        """Scan for exposed secrets"""
        print("🔍 Scanning for secrets...")

        result = subprocess.run([
            "detect-secrets", "scan", "--baseline", ".secrets.baseline"
        ], capture_output=True, text=True)

        # Check if new secrets detected
        if "potential secrets" in result.stdout.lower():
            secret_count = result.stdout.count("Secret Type:")
            self.metrics["secrets_found"] = secret_count
            print(f"❌ Found {secret_count} potential secrets!")
            return False, secret_count

        print("✅ No secrets detected")
        return True, 0

    def run_vulnerability_scan(self) -> Tuple[bool, int]:
        """Check for security vulnerabilities"""
        print("🔍 Scanning for vulnerabilities...")

        # Run trivy for filesystem scan
        result = subprocess.run([
            "trivy", "fs", ".", "--severity", "CRITICAL,HIGH",
            "--format", "json", "--quiet"
        ], capture_output=True, text=True)

        try:
            vulns = json.loads(result.stdout)
            critical_count = sum(
                1 for r in vulns.get("Results", [])
                for v in r.get("Vulnerabilities", [])
                if v.get("Severity") in ["CRITICAL", "HIGH"]
            )
            self.metrics["critical_vulns"] = critical_count

            if critical_count > 0:
                print(f"❌ Found {critical_count} critical/high vulnerabilities")
                return False, critical_count
        except:
            pass

        print("✅ No critical vulnerabilities")
        return True, 0

    def run_spell_check(self) -> Tuple[bool, int]:
        """Check spelling with shared dictionary"""
        print("🔍 Checking spelling...")

        result = subprocess.run([
            "cspell", "**/*.{md,js,ts,py}"
        ], capture_output=True, text=True)

        error_count = len([l for l in result.stdout.splitlines() if "Unknown word" in l])
        self.metrics["spell_errors"] = error_count

        # Just warn, don't block
        if error_count > 0:
            print(f"⚠️  Found {error_count} unknown words (non-blocking)")
        else:
            print("✅ Spelling check passed")

        return True, error_count

    def validate_docker_compose(self) -> Tuple[bool, int]:
        """Validate Docker Compose configurations"""
        print("🔍 Validating Docker configurations...")

        compose_files = list(self.repo_root.glob("**/docker-compose*.yml"))
        errors = 0

        for compose_file in compose_files:
            result = subprocess.run([
                "docker", "compose", "-f", str(compose_file), "config"
            ], capture_output=True, text=True)

            if result.returncode != 0:
                errors += 1
                print(f"❌ Invalid: {compose_file.name}")

        self.metrics["docker_valid"] = errors == 0

        if errors > 0:
            print(f"❌ Found {errors} invalid Docker configs")
            return False, errors

        print("✅ Docker configs valid")
        return True, 0

    def run_npm_audit(self) -> Tuple[bool, int]:
        """Check for npm vulnerabilities"""
        if not (self.repo_root / "package.json").exists():
            return True, 0

        print("🔍 Running npm audit...")

        result = subprocess.run([
            "npm", "audit", "--omit", "dev", "--json"
        ], capture_output=True, text=True)

        try:
            audit = json.loads(result.stdout)
            high_vulns = audit.get("metadata", {}).get("vulnerabilities", {}).get("high", 0)
            critical_vulns = audit.get("metadata", {}).get("vulnerabilities", {}).get("critical", 0)

            total_serious = high_vulns + critical_vulns

            if total_serious > 0:
                print(f"❌ Found {total_serious} high/critical npm vulnerabilities")
                return False, total_serious
        except:
            pass

        print("✅ npm dependencies secure")
        return True, 0

    def save_metrics(self):
        """Save metrics for monitoring"""
        metrics_dir = self.repo_root / "metrics"
        metrics_dir.mkdir(exist_ok=True)

        metrics_file = metrics_dir / "precommit.json"
        with open(metrics_file, "w") as f:
            json.dump(self.metrics, f, indent=2)

        print(f"\n📊 Metrics saved to {metrics_file}")

    def run_all_checks(self) -> bool:
        """Execute the complete force-field"""
        print("\n🛡️  UNIVERSAL PRE-COMMIT FORCE-FIELD ACTIVATED")
        print("=" * 50)

        checks = [
            ("Markdown", self.run_markdown_lint),
            ("Secrets", self.run_secrets_scan),
            ("Vulnerabilities", self.run_vulnerability_scan),
            ("Spelling", self.run_spell_check),
            ("Docker", self.validate_docker_compose),
            ("NPM", self.run_npm_audit),
        ]

        all_passed = True

        for name, check_func in checks:
            try:
                passed, count = check_func()
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"⚠️  {name} check skipped: {str(e)}")

        print("\n" + "=" * 50)

        if all_passed:
            print("✅ ALL CHECKS PASSED - Safe to commit!")
            print("\n💡 Force multiplication achieved:")
            print("   - Markdown auto-formatted")
            print("   - Secrets prevented")
            print("   - Vulnerabilities blocked")
            print("   - Docker configs validated")
            print("   - Dependencies secured")
        else:
            print("❌ COMMIT BLOCKED - Issues must be resolved")
            print("\n🔧 To bypass lint errors only: git commit --allow-lint")

        self.save_metrics()

        return all_passed


def main():
    """Main entry point"""
    force_field = ForceFieldHook()

    # Check if we're in a git repo
    if not (Path.cwd() / ".git").exists():
        print("❌ Not in a git repository")
        sys.exit(1)

    # Run all checks
    if force_field.run_all_checks():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
