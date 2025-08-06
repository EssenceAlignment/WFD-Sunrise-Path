#!/usr/bin/env python3
"""
Script to remove hardcoded secrets from Python files and replace with environment variables
"""

import os
import re
import sys

def replace_secrets_in_file(filepath):
    """Replace hardcoded secrets with environment variables"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Replace Airtable API key
    content = re.sub(
        r"self\.airtable_api_key\s*=\s*['\"]patMwDeT8VWbBMHf8\.[\w]+['\"]",
        "self.airtable_api_key = os.getenv('AIRTABLE_API_KEY')",
        content
    )

    # Replace Perplexity API key
    content = re.sub(
        r"self\.perplexity_api_key\s*=\s*['\"]pplx-[\w]+['\"]",
        "self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')",
        content
    )

    # Replace standalone API key assignments
    content = re.sub(
        r"self\.api_key\s*=\s*['\"]patMwDeT8VWbBMHf8\.[\w]+['\"]",
        "self.api_key = os.getenv('AIRTABLE_API_KEY')",
        content
    )

    # Ensure os is imported
    if "import os" not in content:
        # Add after the first import statement or at the beginning
        import_match = re.search(r'^(import\s+\w+|from\s+\w+)', content, re.MULTILINE)
        if import_match:
            insert_pos = import_match.start()
            content = content[:insert_pos] + "import os\n" + content[insert_pos:]
        else:
            content = "import os\n" + content

    # Add validation for environment variables after __init__ method
    init_pattern = r'(def __init__\(self.*?\):\s*\n(?:.*?\n)*?)((?=\s*def|\s*$))'

    validation_code = """
        # Validate environment variables
        if not self.airtable_api_key:
            raise ValueError("AIRTABLE_API_KEY environment variable not set")
"""

    # Check if we need Perplexity validation
    if "perplexity_api_key" in content:
        validation_code += """        if not self.perplexity_api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")
"""

    # Insert validation code if not already present
    if "Validate environment variables" not in content:
        def add_validation(match):
            init_content = match.group(1)
            return init_content + validation_code + match.group(2)

        content = re.sub(init_pattern, add_validation, content, flags=re.MULTILINE | re.DOTALL)

    # Write updated content
    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✅ Updated: {filepath}")

def main():
    """Main function to process all files"""

    files_to_update = [
        "./scripts/check_and_populate_airtable.py",
        "./scripts/populate_airtable_funding.py",
        "./scripts/populate_funding_dashboard.py",
        "./scripts/populate_funding_dashboard_mcp.py",
        "./dist/scripts/check_and_populate_airtable.py",
        "./dist/scripts/populate_airtable_funding.py",
        "./dist/scripts/populate_funding_dashboard.py",
        "./dist/scripts/populate_funding_dashboard_mcp.py",
        "./ios/App/App/public/scripts/check_and_populate_airtable.py",
        "./ios/App/App/public/scripts/populate_airtable_funding.py",
        "./ios/App/App/public/scripts/populate_funding_dashboard.py",
        "./ios/App/App/public/scripts/populate_funding_dashboard_mcp.py"
    ]

    print("🔐 Removing hardcoded secrets from Python files...")
    print("=" * 60)

    for filepath in files_to_update:
        if os.path.exists(filepath):
            try:
                replace_secrets_in_file(filepath)
            except Exception as e:
                print(f"❌ Error updating {filepath}: {e}")
        else:
            print(f"⚠️  File not found: {filepath}")

    print("\n✅ Secret removal complete!")
    print("\n📝 Next steps:")
    print("1. Create .env file with:")
    print("   AIRTABLE_API_KEY=your_airtable_key_here")
    print("   PERPLEXITY_API_KEY=your_perplexity_key_here")
    print("2. Add these secrets to GitHub Secrets")
    print("3. Update CI/CD workflows to pass secrets as environment variables")

if __name__ == "__main__":
    main()
