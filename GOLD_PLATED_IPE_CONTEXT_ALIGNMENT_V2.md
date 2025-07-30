# 🔒 Gold-Plated IPE Context Alignment Upgrade (v2.0)

## 1 Context Loader (extension entry point)
- **contextLoader.ts**
  - On activation: read every `*.context.md` and `objectives.yml` at repo root.
  - Watcher: `vscode.workspace.createFileSystemWatcher('**/*.{context.md,yml}')`
  - On change: refresh in-memory context and broadcast `cline.context.updated`.

## 2 Objective Registry
- **objectives.yml**
  - id, category, priority, status, last_updated, owner
  - Maintained by weekly `npm run snapshot:objectives`.

## 3 Alignment Test Harness
- **alignment_tests/** → markdown scenarios + expected key phrases.
- **package.json** scripts
  ```json
  "scripts": {
    "eval": "openai tools evals ./alignment_tests --model gpt-4o",
    "test": "npm run eval && echo '✅ Alignment passed'"
  }
  ```
  - Fails CI if expected phrases absent.

## 4 Sentinel × Judge Voting
- `sentinelModel='gpt-3.5-turbo'` pre-screens responses.
- If sentinel flags missing critical tags (`[PRIORITY-1]`, `[ABUNDANCE]`), abort before user sees output.

## 5 Context Heartbeat
- Each AI call injects:
  ```
  🫀 context-heartbeat:
      ai_context_alignment.md:  {{hash}}
      objectives.yml:           {{updated_at}}
  ```
- If any timestamp > 7 days old → automatic "refresh-needed" prompt.

## 6 Pre-commit Gate
```bash
pre-commit install     # one-time
echo 'npm run test' > .pre-commit-hooks.yaml
```
Blocks commit on failed alignment tests.

## 7 Force-Multiplication Intelligence Loop
- Nightly `npm run scan:gems` → mines commit history for overlooked high-impact changes; appends them to `hidden_gems.context.md`.
- Weekly scorecard script computes coverage ratio across priority domains and updates `AI_CONTEXT_ALIGNMENT.md`.

## 8 Abundance Guardrails
- Linter rejects urgency verbs ("right now", "ASAP").
- Response filter enforces calm, mission-driven tone.

---

> **Outcome** – Cline always starts with the freshest Recovery Compass context, self-tests for drift, and refuses to proceed when alignment weakens. Copy this block into your next Cline message and run the listed scripts to activate.
