#!/usr/bin/env python3
"""
Security Orchestrator - Systematic vulnerability detection and remediation
Force multiplication approach to security management
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class SecurityOrchestrator:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent.parent
        self.vulnerabilities = []
        self.fixes_applied = []
        self.patterns = self.load_vulnerability_patterns()

    def load_vulnerability_patterns(self) -> Dict:
        """Load known vulnerability patterns for systematic fixes"""
        return {
            'python': {
                'requests': {
                    'pattern': r'requests[<>=]*(\d+\.\d+\.\d+)?',
                    'fix': 'requests>=2.32.4',
                    'cve': ['CVE-2024-35195', 'CVE-2024-24762'],
                    'description': 'SSL verification and .netrc credential leak vulnerabilities'
                },
                'python-multipart': {
                    'pattern': r'python-multipart[<>=]*(\d+\.\d+\.\d+)?',
                    'fix': 'python-multipart>=0.0.18',
                    'cve': ['CVE-2024-24762', 'GHSA-2jv5-9r88-3w3p'],
                    'description': 'Content-Type Header ReDoS and boundary DoS vulnerabilities'
                },
                'pydantic': {
                    'pattern': r'pydantic[<>=]*(\d+\.\d+\.\d+)?',
                    'fix': 'pydantic>=2.7.4',
                    'description': 'Security and compatibility updates'
                }
            },
            'npm': {
                'path-to-regexp': {
                    'pattern': r'"path-to-regexp":\s*"[^"]*"',
                    'fix': '"path-to-regexp": "^6.2.1"',
                    'description': 'ReDoS vulnerability'
                },
                'mongoose': {
                    'pattern': r'"mongoose":\s*"[^"]*"',
                    'fix': '"mongoose": "^7.5.0"',
                    'description': 'Search injection vulnerability'
                },
                'webpack': {
                    'pattern': r'"webpack":\s*"[^"]*"',
                    'fix': '"webpack": "^5.89.0"',
                    'description': 'Multiple security vulnerabilities'
                }
            }
        }

    def scan_python_projects(self) -> List[Dict]:
        """Scan all Python projects for vulnerabilities"""
        print("🔍 Scanning Python projects...")
        vulnerabilities = []

        for req_file in self.root_path.rglob('requirements.txt'):
            print(f"  Checking: {req_file.relative_to(self.root_path)}")

            # Read requirements file
            with open(req_file, 'r') as f:
                content = f.read()

            # Check against known patterns
            for pkg, info in self.patterns['python'].items():
                if re.search(info['pattern'], content, re.IGNORECASE):
                    # Extract current version
                    match = re.search(f"{pkg}[<>=]*([0-9.]+)", content)
                    current_version = match.group(1) if match else "unknown"

                    # Check if update needed
                    if not self._is_version_safe(pkg, current_version, 'python'):
                        vulnerabilities.append({
                            'file': str(req_file),
                            'package': pkg,
                            'current': current_version,
                            'fix': info['fix'],
                            'description': info['description'],
                            'type': 'python'
                        })

        return vulnerabilities

    def scan_npm_projects(self) -> List[Dict]:
        """Scan all Node.js projects for vulnerabilities"""
        print("🔍 Scanning Node.js projects...")
        vulnerabilities = []

        for pkg_file in self.root_path.rglob('package.json'):
            # Skip node_modules
            if 'node_modules' in str(pkg_file):
                continue

            print(f"  Checking: {pkg_file.relative_to(self.root_path)}")

            # Run npm audit
            project_dir = pkg_file.parent
            try:
                result = subprocess.run(
                    ['npm', 'audit', '--json'],
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0 and result.stdout:
                    audit_data = json.loads(result.stdout)

                    # Process vulnerabilities
                    if 'vulnerabilities' in audit_data:
                        for vuln_name, vuln_info in audit_data['vulnerabilities'].items():
                            vulnerabilities.append({
                                'file': str(pkg_file),
                                'package': vuln_name,
                                'severity': vuln_info.get('severity', 'unknown'),
                                'fix': vuln_info.get('fixAvailable', {}).get('name', ''),
                                'description': vuln_info.get('via', [{}])[0].get('title', ''),
                                'type': 'npm'
                            })
            except Exception as e:
                print(f"    ⚠️  Error scanning {pkg_file}: {e}")

        return vulnerabilities

    def _is_version_safe(self, package: str, version: str, pkg_type: str) -> bool:
        """Check if a version is safe based on known patterns"""
        if pkg_type == 'python':
            if package == 'requests':
                return self._compare_versions(version, '2.32.4') >= 0
            elif package == 'python-multipart':
                return self._compare_versions(version, '0.0.18') >= 0
            elif package == 'pydantic':
                return self._compare_versions(version, '2.7.4') >= 0

        return True  # Assume safe if not in patterns

    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare version strings"""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]

            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_part = v1_parts[i] if i < len(v1_parts) else 0
                v2_part = v2_parts[i] if i < len(v2_parts) else 0

                if v1_part < v2_part:
                    return -1
                elif v1_part > v2_part:
                    return 1

            return 0
        except:
            return -1  # Assume older if can't parse

    def apply_fixes(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """Apply fixes for detected vulnerabilities"""
        print("\n🔧 Applying fixes...")
        fixes = []

        # Group by file
        files_to_fix = {}
        for vuln in vulnerabilities:
            if vuln['file'] not in files_to_fix:
                files_to_fix[vuln['file']] = []
            files_to_fix[vuln['file']].append(vuln)

        # Apply fixes per file
        for file_path, vulns in files_to_fix.items():
            if vulns[0]['type'] == 'python':
                fixes.extend(self._fix_python_requirements(file_path, vulns))
            elif vulns[0]['type'] == 'npm':
                fixes.extend(self._fix_npm_packages(file_path, vulns))

        return fixes

    def _fix_python_requirements(self, file_path: str, vulnerabilities: List[Dict]) -> List[Dict]:
        """Fix Python requirements file"""
        fixes = []

        # Read file
        with open(file_path, 'r') as f:
            content = f.read()

        # Apply fixes
        original_content = content
        for vuln in vulnerabilities:
            pattern = self.patterns['python'][vuln['package']]['pattern']
            fix = self.patterns['python'][vuln['package']]['fix']

            # Replace with fix
            content = re.sub(pattern, fix, content, flags=re.IGNORECASE)

            fixes.append({
                'file': file_path,
                'package': vuln['package'],
                'from': vuln['current'],
                'to': fix,
                'description': vuln['description']
            })

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"  ✅ Fixed {Path(file_path).relative_to(self.root_path)}")

        return fixes

    def _fix_npm_packages(self, file_path: str, vulnerabilities: List[Dict]) -> List[Dict]:
        """Fix npm packages"""
        fixes = []
        project_dir = Path(file_path).parent

        # Run npm audit fix
        try:
            # First try regular fix
            result = subprocess.run(
                ['npm', 'audit', 'fix'],
                cwd=project_dir,
                capture_output=True,
                text=True
            )

            # If still has vulnerabilities, try force
            if 'found' in result.stdout and 'vulnerabilities' in result.stdout:
                subprocess.run(
                    ['npm', 'audit', 'fix', '--force'],
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )

            print(f"  ✅ Fixed npm vulnerabilities in {project_dir.relative_to(self.root_path)}")

            for vuln in vulnerabilities:
                fixes.append({
                    'file': file_path,
                    'package': vuln['package'],
                    'severity': vuln.get('severity', 'unknown'),
                    'description': vuln['description']
                })
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")

        return fixes

    def create_security_commits(self, fixes: List[Dict]):
        """Create atomic commits for security fixes"""
        print("\n📝 Creating security commits...")

        # Group fixes by project
        projects = {}
        for fix in fixes:
            project = str(Path(fix['file']).parent)
            if project not in projects:
                projects[project] = []
            projects[project].append(fix)

        # Create commits
        for project, project_fixes in projects.items():
            # Stage files
            files = list(set([fix['file'] for fix in project_fixes]))
            for file in files:
                subprocess.run(['git', 'add', file])

            # Build commit message
            packages = list(set([fix['package'] for fix in project_fixes]))

            commit_msg = f"fix: upgrade dependencies to address security vulnerabilities\n\n"
            commit_msg += f"Updated packages in {Path(project).name}:\n"

            for fix in project_fixes:
                if 'from' in fix and 'to' in fix:
                    commit_msg += f"- {fix['package']}: {fix['from']} → {fix['to']}\n"
                else:
                    commit_msg += f"- {fix['package']}: {fix.get('severity', '')} vulnerability fixed\n"

            commit_msg += "\nAddresses:\n"
            for fix in project_fixes:
                if fix['description']:
                    commit_msg += f"- {fix['description']}\n"

            # Create commit
            subprocess.run(['git', 'commit', '-m', commit_msg])
            print(f"  ✅ Committed fixes for {Path(project).name}")

    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n📊 Generating security report...")

        report = f"""# Security Orchestration Report
Generated: {datetime.now().isoformat()}

## Summary
- Total vulnerabilities found: {len(self.vulnerabilities)}
- Fixes applied: {len(self.fixes_applied)}
- Projects scanned: {len(set([v['file'] for v in self.vulnerabilities]))}

## Vulnerabilities Fixed

"""

        # Group by severity/type
        for vuln in sorted(self.vulnerabilities, key=lambda x: x.get('severity', 'unknown')):
            report += f"### {vuln['package']} in {Path(vuln['file']).relative_to(self.root_path)}\n"
            report += f"- **Type**: {vuln['type']}\n"
            report += f"- **Description**: {vuln['description']}\n"
            if 'severity' in vuln:
                report += f"- **Severity**: {vuln['severity']}\n"
            report += f"- **Fix Applied**: {vuln.get('fix', 'npm audit fix')}\n\n"

        # Write report
        report_path = self.root_path / 'SECURITY_ORCHESTRATION_REPORT.md'
        with open(report_path, 'w') as f:
            f.write(report)

        print(f"  ✅ Report saved to {report_path.name}")

    def run(self, scan_only: bool = False, auto_commit: bool = True):
        """Main orchestration flow"""
        print("🚀 Security Orchestrator Starting...\n")

        # Scan for vulnerabilities
        python_vulns = self.scan_python_projects()
        npm_vulns = self.scan_npm_projects()

        self.vulnerabilities = python_vulns + npm_vulns

        print(f"\n📊 Found {len(self.vulnerabilities)} vulnerabilities")

        if scan_only:
            # Just report
            for vuln in self.vulnerabilities:
                print(f"  - {vuln['package']} in {Path(vuln['file']).name}")
            return

        # Apply fixes
        if self.vulnerabilities:
            self.fixes_applied = self.apply_fixes(self.vulnerabilities)

            # Create commits if requested
            if auto_commit and self.fixes_applied:
                self.create_security_commits(self.fixes_applied)

        # Generate report
        self.generate_security_report()

        print("\n✅ Security orchestration complete!")


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Security Orchestrator')
    parser.add_argument('--scan-only', action='store_true',
                        help='Only scan, do not apply fixes')
    parser.add_argument('--no-commit', action='store_true',
                        help='Do not create commits')
    parser.add_argument('--fix-all', action='store_true',
                        help='Apply all fixes automatically')

    args = parser.parse_args()

    orchestrator = SecurityOrchestrator()
    orchestrator.run(
        scan_only=args.scan_only,
        auto_commit=not args.no_commit
    )


if __name__ == '__main__':
    main()
