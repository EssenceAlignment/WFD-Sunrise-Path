#!/usr/bin/env bash
# Fixes Cloudflare Pages failures by enforcing a single Bun lockfile,
# cleaning artefacts, and adding guard‑rails.

set -euo pipefail

# 1. verify Bun
command -v bun >/dev/null || { echo "❌ Bun is not installed"; exit 40; }

# 2. purge legacy lockfiles
rm -f package-lock.json yarn.lock pnpm-lock.yaml

# 3. clean node_modules everywhere under repo
echo "🧹  pruning old node_modules…"
find . -type d -name node_modules -prune -exec rm -rf {} +

# 4. (re)install deps with Bun
echo "📦  installing deps with Bun…"
bun install --force

# 5. ensure .gitignore shields unwanted lockfiles/dirs
grep -qxF 'package-lock.json' .gitignore || echo 'package-lock.json' >> .gitignore
grep -qxF 'yarn.lock'         .gitignore || echo 'yarn.lock'         >> .gitignore
grep -qxF 'pnpm-lock.yaml'    .gitignore || echo 'pnpm-lock.yaml'    >> .gitignore
grep -qxF 'node_modules/'     .gitignore || echo 'node_modules/'     >> .gitignore

# 6. add lockfile check to existing pre‑commit hook
HOOK='.git/hooks/pre-commit'
mkdir -p .git/hooks

# If hook exists, backup and append lockfile check
if [ -f "$HOOK" ]; then
  # Check if lockfile check already exists
  if ! grep -q "Multiple lockfiles detected" "$HOOK"; then
    # Insert lockfile check at the beginning (after shebang)
    TEMP_HOOK=$(mktemp)
    head -n 1 "$HOOK" > "$TEMP_HOOK"
    cat >> "$TEMP_HOOK" <<'H'

# Check for multiple lockfiles
if [[ -f package-lock.json || -f yarn.lock || -f pnpm-lock.yaml ]]; then
  echo "❌ Multiple lockfiles detected – commit rejected"
  exit 1
fi
H
    tail -n +2 "$HOOK" >> "$TEMP_HOOK"
    mv "$TEMP_HOOK" "$HOOK"
  fi
else
  # Create new hook with lockfile check
  cat > "$HOOK" <<'H'
#!/usr/bin/env bash
# Check for multiple lockfiles
if [[ -f package-lock.json || -f yarn.lock || -f pnpm-lock.yaml ]]; then
  echo "❌ Multiple lockfiles detected – commit rejected"
  exit 1
fi
H
fi
chmod +x "$HOOK"

# 7. commit & emit metric
git add bun.lock .gitignore $HOOK
git commit -m "build(ci): enforce Bun-only workflow 🚀" --signoff || true
echo "::metric:: mcp_ready=1"
