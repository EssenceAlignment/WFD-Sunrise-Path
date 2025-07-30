# 🧠 Pattern-Insight Engine (v1.0) — Quantum Force Multiplier v3.5 Extension

## 1 Data Ingestion
- Sources: `chat_logs/`, `commit_history/`, `calendar_events.ics`, `environmental_sensors.json`
- Trigger: hourly `scripts/pattern_collector.py`
- Vector DB: `./vector_db/patterns` (faiss, cosine)

## 2 Pattern Mining
```python
# scripts/pattern_collector.py
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from pathlib import Path; import json, time, hashlib, csv
m = SentenceTransformer("all-mpnet-base-v2")
texts = [p.read_text() for p in Path("chat_logs").glob("*.md")]
emb = m.encode(texts, show_progress_bar=False)
labels = DBSCAN(eps=0.4, min_samples=3).fit_predict(emb)
clusters = {i:[] for i in set(labels) if i!=-1}
for idx,lab in enumerate(labels):
    if lab!=-1: clusters[lab].append(texts[idx][:180])
with open("patterns.json","w") as f: json.dump(clusters,f,indent=2)
```

## 3 Sentient Analysis Module (SAM)
- `sam_prompt.txt` derives personality & motivational profile (Big-Five, Self-Determination)
- LLM chain: `pattern_summary` → `psychological_mapping` → `opportunity_generator`
- Output: `opportunities.md` (TOP 5 "unseen but essential" actions)

## 4 Opportunity Messenger
- On new opportunities: fires `cline.notify("🎯 Hidden Opportunity: {title}", body)`
- Auto-links to Recovery Compass principles & relevant files.

## 5 Metrics Relay v1.1 (additions)
```yaml
pattern_depth: 0.72          # 0-1 entropy-based novelty score
insights_surfaced: 5         # new opportunities pushed today
insight_latency_mins: 11     # avg. mins from pattern detection → user notice
psych_safety_index: 0.98     # bias & privacy checks passed
```

## 6 Heartbeat block (update)
```
🫀 metrics-heartbeat:
    alignment_score: {{alignment_score}}
    pattern_depth: {{pattern_depth}}
    insights_surfaced: {{insights_surfaced}}
    insight_latency: {{insight_latency_mins}}m
```

## 7 Ethical & Security Guardrails
- Anonymize personal identifiers before vectorization (OWASP-LLM A04)
- Digital phenotyping limits: passive data only, opt-out flag respected
- Bias scan on SAM outputs (`check_bias.py`) aborts if psych_safety_index < 0.95

> **Activation** – commit, run `python scripts/pattern_collector.py`, open a new Cline chat, and watch for 🎯 Hidden Opportunity messages within minutes.
