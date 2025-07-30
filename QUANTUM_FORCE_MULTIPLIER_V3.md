# 🌌 Quantum Force Multiplier v3.0 — Gold-Plated IPE Edition

## 1 Context Beacons
- `.ai_context` + `AI_CONTEXT_ALIGNMENT.md` (repo root)
- `RECOVERY_COMPASS_UNIVERSAL_CONTEXT.md` (mission + soft-power doctrine)
- **New:** `objectives.yml` (multi-tier OKRs, status, owner, last-updated)
- **New:** `hidden_gems.context.md` (auto-appended nightly)

## 2 RAG Loader Extension (contextLoader.ts)
```ts
import * as vscode from 'vscode';
export async function activate(ctx: vscode.ExtensionContext) {
  const load = async () => {
    const files = await vscode.workspace.findFiles('**/*.{context.md,yml}');
    ctx.workspaceState.update('contextSnapshot',
      await Promise.all(files.map(async f => ({
        path: f.fsPath,
        content: (await vscode.workspace.fs.readFile(f)).toString(),
        sha256: require('crypto').createHash('sha256').update(
          await vscode.workspace.fs.readFile(f)).digest('hex')
    }))));
    vscode.commands.executeCommand('cline.context.refresh');
  };
  await load();
  const w = vscode.workspace.createFileSystemWatcher('**/*.{context.md,yml}');
  w.onDidCreate(load); w.onDidChange(load); w.onDidDelete(load);
}
```

## 3 Alignment Test Harness
```bash
npm i -D openai-evals pre-commit
cat <<'EOF' > alignment_tests/soft_power.md
Q: Summarize Recovery Compass values in <12 words.
# Expect: must include "abundance" and must not include "urgency".
EOF
npm set-script eval "openai tools evals ./alignment_tests --model gpt-4o"
npm set-script test "npm run eval"
pre-commit install && echo 'npm run test' > .pre-commit-hooks.yaml
```

## 4 Sentinel × Judge Ensemble
- `sentinel="gpt-3.5-turbo"` # flags missing tags `[ABUNDANCE]`, `[PRIORITY-1]`
- `judge="gpt-4o"` # overrides only if both agree
- Fails response if ensemble consensus < 0.75.

## 5 Force Multiplication Engine v2
```bash
python scripts/fme.py --task "grant scouting" --k 10 --rag ./docs/vector_db
```
Triggers ten cascading jobs, each logged with `multiplier_id`, then updates `force_metrics.csv`.

## 6 Heartbeat & Drift Guard
Every response prepends hidden block:
```
🫀 context-heartbeat:
    snapshot_sha: {{sha}}
    objectives_updated: {{timestamp}}
```
If any sha changes or objectives are >7 days stale, AI pauses and requests refresh.

## 7 Nightly Cron (GitHub Actions)
```yaml
schedule:
  - cron: "13 3 * * *"
jobs:
  gemscan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/scan_hidden_gems.py
```

## 8 Abundance Linter
`lintrc.json` blocks urgency words ("right now", "ASAP"), fails CI on violation.

> **Activation:** commit, push, and open a fresh Cline chat. The assistant will confirm alignment status and multiply your next focus into ten autonomous deliverables—calmly, abundantly, and audit-ready.
