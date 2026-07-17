## Distributed Job Scheduler

A task queue + scheduler where workers can crash, restart, and pick up where
they left off. Built in phases:

- [x] Phase 1 — Job submission API (FastAPI + SQLite)
- [ ] Phase 2 — Worker pool with heartbeats + leases
- [ ] Phase 3 — At-least-once delivery with idempotency keys
- [ ] Phase 4 — Retry with exponential backoff + dead-letter queue
- [ ] Phase 5 (stretch) — Leader election

### Run it

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

API docs at `http://127.0.0.1:8000/docs` once running.
