# CLAUDE.md — Repo Rules for Claude

## Scope
- Only modify files under: /src, /docs
- Do not touch: /infra, /.github/workflows (unless explicitly asked)

## Behavior
- For pull requests: create a feature branch, open a PR, and summarize changes.
- For UI: follow Tailwind tokens (ink/line/card/rc.green/wfd.navy) and 8‑pt spacing.
- Numeric typography: use `tabular-nums` and `toLocaleString("en-US")`.

## Safety
- Never write secrets to logs or code.
- Ask for confirmation before deleting files or force-pushing.
- If build fails, post logs and exit without retry loops.

After opening the PR, stop and wait for me to:
- Install the Claude GitHub App on this repo
- Add the ANTHROPIC_API_KEY secret in GitHub → Settings → Secrets → Actions

Post the PR URL when done.

