# Cost Optimization

Spend less without killing freshness, correctness, or developer speed.

---

### Scan Pruning / Partitioning

**Definition:** Design tables so queries read only needed files/partitions.

**Why it matters:** Cloud warehouses/lakes bill on bytes scanned and compute time.

**Example:** Partition by `dt`; filter `WHERE dt = CURRENT_DATE` before joining.

**Remember:**
- Partition on common filters
- Over-partitioning creates small files / high list costs

---

### Column Pruning

**Definition:** Read only selected columns from columnar formats (Parquet/ORC).

**Why it matters:** Wide tables waste money on `SELECT *`.

**Example:** `SELECT user_id, amount FROM events` reads two columns, not fifty.

**Remember:**
- Ban `SELECT *` in prod marts
- Wide nested types still costly

---

### File Size Tuning

**Definition:** Target healthy output file sizes (often ~128–512MB) via coalesce/optimize.

**Why it matters:** Too small → metadata/task overhead; too big → poor parallelism.

**Example:** `coalesce(200)` before write; schedule compaction.

**Remember:**
- Streaming ingest needs regular compaction
- Measure before/after query cost

---

### Spot / Preemptible Workers

**Definition:** Use discounted interruptible VMs for fault-tolerant batch compute.

**Why it matters:** Large Spark/Flink savings when retries are safe.

**Example:** Spark executors on spot; driver on on-demand.

**Remember:**
- Idempotent jobs required
- Keep critical coordinators stable

---

### Autoscaling / Autosuspend

**Definition:** Scale clusters/warehouses to zero or down when idle; up under load.

**Why it matters:** Idle warehouses dominate waste.

**Example:** Snowflake auto-suspend 60s; Spark dynamic allocation.

**Remember:**
- Warm-up latency vs savings tradeoff
- Separate prod vs ad-hoc warehouses

---

### Storage Tiering

**Definition:** Move cold data to cheaper classes via lifecycle policies.

**Why it matters:** Lakes grow forever; most bytes are rarely read.

**Example:** Raw logs → infrequent access after 30d → archive after 180d.

**Remember:**
- Align with compliance retention
- Retrieval can be slow/expensive

---

### Result Caching

**Definition:** Reuse recent query results when identical SQL hits warm cache.

**Why it matters:** Dashboards refetching the same query burn credits.

**Example:** BI extracts cached in warehouse result cache for minutes.

**Remember:**
- Great for repetitive dashboards
- Don’t confuse with data freshness SLAs

---

### Right-Sizing Warehouses

**Definition:** Match warehouse/cluster size to workload shape, not peak folklore.

**Why it matters:** Bigger isn’t always faster enough to justify 2× cost.

**Example:** Drop from 2XL to L after partitioning fixed scan volume.

**Remember:**
- Fix data layout before scaling up
- Track $/query and $/TB scanned

---

### Cost Observability

**Definition:** Attribute spend to teams, jobs, tables, and queries.

**Why it matters:** You can’t optimize what you can’t see.

**Example:** Chargeback tags on Spark jobs; query cost views in Snowflake.

**Remember:**
- Tag every production job
- Alert on spend anomalies, not only failures

---

### Incremental vs Full Refresh

**Definition:** Prefer incremental processing; full refresh only when necessary.

**Why it matters:** Full rebuilds of multi-TB facts are expensive and slow.

**Example:** Daily MERGE of changed keys vs rebuild entire history.

**Remember:**
- Schedule periodic full refresh for drift repair
- Measure bytes processed per run
