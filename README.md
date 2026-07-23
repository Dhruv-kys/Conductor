## Conductor

A distributed job queue for async AI workloads (LLM/embedding calls) where
workers can crash, restart, and pick up where they left off — no dropped or
duplicated jobs. Built in phases:

- [x] Phase 1 — Job submission API (FastAPI + Redis)
- [ ] Phase 2 — Worker pool with reliable claiming + heartbeats/leases
- [ ] Phase 3 — Idempotency keys for at-least-once delivery
- [ ] Phase 4 — Retry with exponential backoff + dead-letter queue
- [ ] Phase 5 — Rate limiting against provider APIs (token bucket)
- [ ] Phase 6 (stretch) — Leader election + throughput/latency benchmark

### Run it

```bash
# Redis (via colima, a lightweight Docker runtime)
colima start
docker run -d --name conductor-redis -p 6379:6379 redis:7-alpine

# App
uv venv --python 3.12
uv pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

API docs at `http://127.0.0.1:8000/docs` once running.
