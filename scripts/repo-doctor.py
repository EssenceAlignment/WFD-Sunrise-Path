#!/usr/bin/env python3
"""
Repository Doctor - Force Multiplication System
Automatically diagnoses and fixes common repository issues
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class RepositoryDoctor:
    """Diagnoses and fixes common repository issues automatically"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.issues = []
        self.fixes_applied = []
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "repository": str(self.repo_path),
            "health_score": 100,
            "issues": [],
            "fixes": [],
            "recommendations": []
        }

    def run_diagnosis(self) -> Dict:
        """Run complete repository health check"""
        print("🏥 Repository Doctor - Starting diagnosis...")

        # Check if it's a git repository
        if not self._is_git_repo():
            self.report["issues"].append("Not a git repository")
            self.report["health_score"] = 0
            return self.report

        # Run all health checks
        self._check_gitignore()
        self._check_large_files()
        self._check_uncommitted_changes()
        self._check_branch_hygiene()
        self._check_commit_conventions()
        self._check_dependencies()
        self._check_security()
        self._check_documentation()

        # Calculate final health score
        self.report["health_score"] = max(0, 100 - len(self.report["issues"]) * 10)

        return self.report

    def apply_fixes(self, auto_fix: bool = False) -> List[str]:
        """Apply automatic fixes for discovered issues"""
        if not auto_fix:
            print("\n🔧 Available fixes:")
            for i, fix in enumerate(self.report["recommendations"]):
                print(f"{i+1}. {fix}")

            if input("\nApply all fixes? (y/n): ").lower() != 'y':
                return []

        print("\n🛠️  Applying fixes...")

        # Apply gitignore fixes
        if "Missing comprehensive .gitignore" in str(self.report["issues"]):
            self._fix_gitignore()

        # Clean up large files
        if any("Large files" in issue for issue in self.report["issues"]):
            self._fix_large_files()

        # Set up pre-commit
        if "No pre-commit hooks" in str(self.report["issues"]):
            self._fix_precommit()

        return self.fixes_applied

    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return (self.repo_path / ".git").exists()

    def _check_gitignore(self):
        """Check for comprehensive .gitignore"""
        gitignore_path = self.repo_path / ".gitignore"

        if not gitignore_path.exists():
            self.report["issues"].append("Missing .gitignore file")
            self.report["recommendations"].append("Create comprehensive .gitignore")
            return

        with open(gitignore_path, 'r') as f:
            content = f.read()

        # Check for common patterns
        missing_patterns = []
        essential_patterns = [
            "__pycache__", "venv/", "node_modules/", ".env",
            "*.log", ".DS_Store", ".idea/", ".vscode/"
        ]

        for pattern in essential_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)

        if missing_patterns:
            self.report["issues"].append(f"Missing gitignore patterns: {missing_patterns}")
            self.report["recommendations"].append("Update .gitignore with universal patterns")

    def _check_large_files(self):
        """Check for large files that shouldn't be in git"""
        try:
            # Find large files in git
            result = subprocess.run(
                ["git", "ls-files", "-z"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode == 0:
                large_files = []
                for file in result.stdout.split('\0'):
                    if file and os.path.exists(self.repo_path / file):
                        size = os.path.getsize(self.repo_path / file)
                        if size > 1024 * 1024:  # 1MB
                            large_files.append((file, size))

                if large_files:
                    self.report["issues"].append(f"Large files in repository: {len(large_files)} files")
                    self.report["recommendations"].append("Remove or add large files to .gitignore")
        except Exception as e:
            print(f"Error checking large files: {e}")

    def _check_uncommitted_changes(self):
        """Check for uncommitted changes"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode == 0 and result.stdout.strip():
                changes = len(result.stdout.strip().split('\n'))
                self.report["issues"].append(f"Uncommitted changes: {changes} files")

                # Check for common problematic patterns
                if "venv/" in result.stdout or "__pycache__" in result.stdout:
                    self.report["recommendations"].append("Add Python virtual environment files to .gitignore")

        except Exception as e:
            print(f"Error checking git status: {e}")

    def _check_branch_hygiene(self):
        """Check for branch management issues"""
        try:
            # Check current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode == 0:
                current_branch = result.stdout.strip()
                if current_branch in ["master", "main"]:
                    # Check if there are local changes on main branch
                    status = subprocess.run(
                        ["git", "status", "--porcelain"],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_path
                    )

                    if status.stdout.strip():
                        self.report["issues"].append("Working directly on main/master branch with changes")
                        self.report["recommendations"].append("Create feature branch for changes")

        except Exception as e:
            print(f"Error checking branches: {e}")

    def _check_commit_conventions(self):
        """Check if commits follow conventions"""
        try:
            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                unconventional = 0

                for commit in commits:
                    # Simple check for conventional commits
                    if not any(prefix in commit.lower() for prefix in
                             ['feat:', 'fix:', 'docs:', 'style:', 'refactor:',
                              'test:', 'chore:', 'build:', 'ci:']):
                        unconventional += 1

                if unconventional > 5:
                    self.report["issues"].append("Not following commit conventions")
                    self.report["recommendations"].append("Use conventional commit messages")

        except Exception as e:
            print(f"Error checking commits: {e}")

    def _check_dependencies(self):
        """Check for dependency management issues"""
        # Check Python
        if (self.repo_path / "requirements.txt").exists():
            if not (self.repo_path / "requirements-dev.txt").exists():
                self.report["recommendations"].append("Consider separating dev dependencies")

        # Check Node.js
        if (self.repo_path / "package.json").exists():
            if not (self.repo_path / "package-lock.json").exists() and \
               not (self.repo_path / "yarn.lock").exists():
                self.report["issues"].append("Missing package lock file")
                self.report["recommendations"].append("Run npm install to generate package-lock.json")

    def _check_security(self):
        """Check for security issues"""
        # Check for .env file in git
        try:
            result = subprocess.run(
                ["git", "ls-files", ".env"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.stdout.strip():
                self.report["issues"].append("CRITICAL: .env file tracked in git")
                self.report["recommendations"].append("Remove .env from git and add to .gitignore")

        except Exception:
            pass

    def _check_documentation(self):
        """Check documentation health"""
        essential_docs = ["README.md", "LICENSE", ".gitignore"]
        missing_docs = []

        for doc in essential_docs:
            if not (self.repo_path / doc).exists():
                missing_docs.append(doc)

        if missing_docs:
            self.report["issues"].append(f"Missing essential files: {missing_docs}")
            self.report["recommendations"].append("Create missing documentation files")

    def _fix_gitignore(self):
        """Apply comprehensive gitignore fix"""
        universal_gitignore = self.repo_path / ".gitignore.universal"
        target_gitignore = self.repo_path / ".gitignore"

        if universal_gitignore.exists():
            # Backup existing .gitignore
            if target_gitignore.exists():
                backup_path = target_gitignore.with_suffix('.gitignore.backup')
                target_gitignore.rename(backup_path)
                self.fixes_applied.append(f"Backed up existing .gitignore to {backup_path}")

            # Copy universal .gitignore
            universal_gitignore.rename(target_gitignore)
            self.fixes_applied.append("Applied universal .gitignore template")

            # Remove tracked files that should be ignored
            subprocess.run(["git", "rm", "-r", "--cached", "."], cwd=self.repo_path)
            subprocess.run(["git", "add", "."], cwd=self.repo_path)
            self.fixes_applied.append("Removed newly ignored files from git tracking")

    def _fix_large_files(self):
        """Remove large files from tracking"""
        # This is a placeholder - in production, would implement git-filter-branch
        # or BFG Repo Cleaner integration
        self.fixes_applied.append("Large file cleanup requires manual intervention")

    def _fix_precommit(self):
        """Set up pre-commit hooks"""
        try:
            subprocess.run(["pip", "install", "pre-commit"], check=True)
            subprocess.run(["pre-commit", "install"], cwd=self.repo_path, check=True)
            self.fixes_applied.append("Installed pre-commit hooks")
        except Exception as e:
            print(f"Error setting up pre-commit: {e}")

    def generate_report(self, output_file: str = None):
        """Generate detailed health report"""
        report_content = f"""
# Repository Health Report
Generated: {self.report['timestamp']}
Repository: {self.report['repository']}

## Health Score: {self.report['health_score']}/100

## Issues Found ({len(self.report['issues'])})
"""
        for issue in self.report['issues']:
            report_content += f"- ❌ {issue}\n"

        report_content += f"\n## Recommendations ({len(self.report['recommendations'])})\n"
        for rec in self.report['recommendations']:
            report_content += f"- 💡 {rec}\n"

        if self.fixes_applied:
            report_content += f"\n## Fixes Applied ({len(self.fixes_applied)})\n"
            for fix in self.fixes_applied:
                report_content += f"- ✅ {fix}\n"

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_content)

        return report_content


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Repository Doctor - Diagnose and fix repository issues")
    parser.add_argument("--path", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--fix", action="store_true", help="Automatically apply fixes")
    parser.add_argument("--report", help="Output report to file")

    args = parser.parse_args()

    doctor = RepositoryDoctor(args.path)

    # Run diagnosis
    doctor.run_diagnosis()

    # Generate and display report
    report = doctor.generate_report(args.report)
    print(report)

    # Apply fixes if requested
    if args.fix or (doctor.report['issues'] and
                   input("\nApply recommended fixes? (y/n): ").lower() == 'y'):
        fixes = doctor.apply_fixes(auto_fix=args.fix)
        if fixes:
            print(f"\n✅ Applied {len(fixes)} fixes")
            print("\n🎯 Next steps:")
            print("1. Review changes with: git status")
            print("2. Commit improvements with: git commit -m 'chore: apply repository health fixes'")

    print(f"\n📊 Final Health Score: {doctor.report['health_score']}/100")


if __name__ == "__main__":
    main()
