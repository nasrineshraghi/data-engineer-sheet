# Pipeline Design

---

### Idempotency

**Definition:** Running the same operation multiple times yields the same result as running once.

**Why it matters:** Retries and backfills won't duplicate or corrupt data.

**Example:** Upsert by primary key; overwrite partition `dt=2024-01-01` instead of append-only blindly.

**Remember:**
- Design sinks for safe replay
- Natural keys + MERGE / partition overwrite

---

### Checkpointing

**Definition:** Persist progress (offsets/state) so recovery resumes cleanly.

**Why it matters:** Fault-tolerant streaming and long batch stages.

**Example:** Spark Structured Streaming checkpoint location stores offsets + state.

**Remember:**
- Checkpoint path is critical state — back it up/protect it
- Changing query identity may invalidate checkpoints

---

### Retry Strategy

**Definition:** Policy for re-attempting failed work (how many, when, which errors).

**Why it matters:** Transient cloud/network faults are normal.

**Example:** Retry S3/API 429/5xx up to 5 times; fail fast on 400 auth errors.

**Remember:**
- Distinguish transient vs permanent errors
- Cap retries to avoid thundering herds

---

### Backoff Strategy

**Definition:** Increase wait between retries (often exponential + jitter).

**Why it matters:** Prevents stampeding a recovering dependency.

**Example:** Wait 1s, 2s, 4s, 8s with random jitter.

**Remember:**
- Always add jitter
- Set max backoff

---

### Circuit Breaker

**Definition:** Stop calling a failing dependency temporarily after error threshold; probe later.

**Why it matters:** Fails fast; protects both sides from cascade.

**Example:** After 50 warehouse connection failures, open circuit for 60s, then half-open trial.

**Remember:**
- Use for shared DBs/APIs
- Pair with timeouts

---

### Dead Letter Queue (DLQ)

**Definition:** Side channel for records that fail processing after retries.

**Why it matters:** Unblocks the main pipeline; enables quarantine and replay.

**Example:** Malformed JSON → DLQ topic/table with error reason; alert and fix.

**Remember:**
- Monitor DLQ depth
- Have a replay runbook

---

### Data Contracts

**Definition:** Explicit agreement on schema, semantics, SLAs, and ownership between producers and consumers.

**Why it matters:** Prevents silent breaking changes.

**Example:** Producer guarantees `orders.v2` fields + daily freshness < 2h; CI validates schema.

**Remember:**
- Version schemas
- Enforce in CI/CD and at write time

---

### Pipeline Orchestration

**Definition:** Schedule, dependency management, retries, and observability of multi-step data jobs.

**Why it matters:** Production reliability beyond a single script.

**Example:** Airflow/Dagster/Prefect/Azure DF: extract → transform → test → publish.

**Remember:**
- Prefer data-aware sensors over blind cron when possible
- Idempotent tasks + clear SLAs

---

### Metadata-Driven Pipelines

**Definition:** Behavior configured by metadata (tables, mappings, rules) rather than hard-coded per table jobs.

**Why it matters:** Scales to hundreds of similar pipelines.

**Example:** Config table lists source, target, PK, SCD type → one generic loader.

**Remember:**
- Great for ingestion patterns
- Keep escape hatches for special cases
