# Airflow

Orchestrating batch (and some streaming-trigger) data pipelines as DAGs.

---

### DAG

**Definition:** Directed Acyclic Graph of tasks with dependencies — Airflow’s unit of workflow.

**Why it matters:** Expresses order, retries, and scheduling of pipeline steps.

**Example:** `extract >> transform >> test >> publish`.

**Remember:**
- No cycles
- Keep DAGs idempotent

---

### Task / Operator

**Definition:** A unit of work in a DAG; operators are task templates (Bash, Python, SparkSubmit, etc.).

**Why it matters:** Standardizes how you call Spark, dbt, SQL, sensors.

**Example:** `BashOperator` runs `dbt run --select fct_orders`.

**Remember:**
- Prefer purpose-built operators/providers
- Heavy work should run on workers/clusters, not the scheduler

---

### Sensor

**Definition:** Task that waits for a condition (file arrives, partition ready, external DAG success).

**Why it matters:** Data-aware scheduling vs blind cron.

**Example:** `S3KeySensor` waits for `dt={{ ds }}/_SUCCESS`.

**Remember:**
- Mode poke vs reschedule affects worker slots
- Timeouts and soft_fail matter

---

### Schedule / Timetable

**Definition:** When DAG runs are created (cron, timetable, dataset-triggered).

**Why it matters:** Aligns runs with data availability and business calendars.

**Example:** `@daily` with `data_interval` ending at midnight UTC.

**Remember:**
- Understand data interval vs execution date
- Catchup can flood the cluster

---

### Execution Date / Data Interval

**Definition:** Logical time range a run represents (Airflow 2: data interval), not “when it ran”.

**Why it matters:** Partitioning and idempotent writes key off logical date.

**Example:** Daily DAG for `2024-01-01` processes that day’s partition even if it runs on Jan 2.

**Remember:**
- Use `ds` / `data_interval_start` in templates
- Don’t confuse with wall-clock start time

---

### XCom

**Definition:** Cross-communication — small metadata passed between tasks.

**Why it matters:** Handy for tiny values; dangerous for large data.

**Example:** Task A pushes `row_count`; Task B branches if zero.

**Remember:**
- Not a data bus — keep payloads tiny
- Prefer object storage paths in XCom

---

### Pool / Slot

**Definition:** Concurrency limits for tasks (pools) and worker parallelism (slots).

**Why it matters:** Protect warehouses and Spark clusters from stampede.

**Example:** Pool `snowflake_heavy` with 4 slots for large transforms.

**Remember:**
- Separate pools per expensive system
- Sensors in poke mode consume slots

---

### Backfill

**Definition:** Intentionally run a DAG for past logical dates.

**Why it matters:** Reprocess history after a fix; must be idempotent.

**Example:** Backfill last 30 days after fixing a currency join.

**Remember:**
- Rate-limit backfills
- Partition overwrite / MERGE targets

---

### Catchup

**Definition:** Airflow auto-schedules missed past runs between start_date and now.

**Why it matters:** Can create a thundering herd of historical runs.

**Example:** Deploy DAG with old `start_date` and `catchup=True` → hundreds of runs.

**Remember:**
- Default catchup carefully (often False)
- Use backfill deliberately instead

---

### SLA / Callback

**Definition:** Time expectations and hooks on success/failure/retry (email, Slack, PagerDuty).

**Why it matters:** Ops signal when data will be late.

**Example:** SLA miss callback posts to #data-alerts.

**Remember:**
- Alert on consumer impact, not every retry
- Pair with freshness checks in the warehouse

---

### Dataset Scheduling

**Definition:** Trigger downstream DAGs when upstream datasets update (Airflow 2.4+).

**Why it matters:** Event-ish orchestration without brittle time offsets.

**Example:** `publish_orders` updates dataset → `marts_orders` DAG runs.

**Remember:**
- Clear dataset naming
- Still need quality gates before publish
