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

### Cron Expression

**Definition:** Compact schedule string (usually 5 fields: minute hour day-of-month month day-of-week) that says when a job should fire.

**Why it matters:** Still the lingua franca for schedules — OS crontab, Airflow, K8s CronJob, cloud schedulers all speak cron-ish dialects.

**Example:** `0 6 * * 1-5` = 06:00 every weekday; `*/15 * * * *` = every 15 minutes.

**Remember:**
- Field order: minute → hour → day → month → weekday (seconds field is a non-standard 6th)
- `*` = every; `*/n` = every n; lists and ranges vary slightly by tool

---

### Crontab / Cron Job

**Definition:** OS or host-level job launcher that runs a command when a cron expression matches (classic `/etc/crontab` or user crontab).

**Why it matters:** Fine for one machine / one script; weak for dependencies, retries, observability, and multi-step pipelines.

**Example:** `0 2 * * * /opt/etl/load_orders.sh >> /var/log/orders.log 2>&1`

**Remember:**
- No DAG: jobs don’t know about upstream readiness
- Overlaps, silent failures, and timezone bugs are common
- Prefer an orchestrator once you have dependencies or SLAs

---

### Cron Timezone Pitfalls

**Definition:** Cron fires in the scheduler’s timezone (often UTC on servers); DST and “local business midnight” confuse partition dates.

**Why it matters:** Wrong tz → wrong `dt=` partition, missed business-day runs, or double runs around DST.

**Example:** Job meant for “US Eastern midnight” scheduled as `0 0 * * *` on a UTC host runs at 19:00 ET previous day.

**Remember:**
- Prefer UTC everywhere and convert for business calendars explicitly
- Document which clock the schedule uses
- Airflow: set DAG timezone deliberately

---

### Overlapping Cron Runs

**Definition:** Next scheduled start begins while the previous run is still executing (slow job + frequent cron).

**Why it matters:** Duplicate writes, lock fights, or corrupted partial loads unless the job is idempotent and concurrency-safe.

**Example:** Hourly job still running at :00 next hour → two loaders append the same partition.

**Remember:**
- Use locks (`flock`), `max_active_runs=1`, or skip-if-running
- Make writes idempotent even when overlaps happen
- Lengthen the interval or speed up the job

---

### Cron vs Orchestrator

**Definition:** Cron starts a command on a clock; an orchestrator (Airflow/Dagster/etc.) manages DAGs, sensors, retries, backfill, and lineage of runs.

**Why it matters:** Clock ≠ data ready. Blind cron races upstream; orchestrators can wait on files/datasets and recover cleanly.

**Example:** Cron: always start at 6am. Orchestrator: sensor waits for `_SUCCESS`, then transform → test → publish.

**Remember:**
- Cron for simple single-host tasks; orchestrator for production pipelines
- Dataset/sensor triggers beat fixed cron when latency varies

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
