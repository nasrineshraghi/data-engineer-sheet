# Data Lake & Lakehouse

---

### Data Lake

**Definition:** Central storage of raw and processed data in files (often object storage), schema-on-read.

**Why it matters:** Cheap scale for diverse data; weak governance if unmanaged.

**Example:** S3/ADLS/GCS buckets with landing, bronze, silver zones as folders.

**Remember:**
- Storage ≠ warehouse
- Needs catalog, quality, and access control

---

### Data Lakehouse

**Definition:** Lake storage + warehouse capabilities: ACID tables, governance, BI-friendly SQL.

**Why it matters:** One copy of data for batch, streaming, and analytics.

**Example:** Delta/Iceberg tables on S3 queried by Spark, Trino, and BI tools.

**Remember:**
- Open table formats are the core
- Combines lake cost with warehouse reliability

---

### Delta Lake

**Definition:** Open table format (Databricks-origin) with transaction log (`_delta_log`) for ACID on files.

**Why it matters:** Upserts, time travel, schema enforcement on object storage.

**Example:** `MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE ...`

**Remember:**
- Transaction log is source of truth
- `OPTIMIZE` + `VACUUM` for maintenance

---

### Apache Iceberg

**Definition:** Open table format with snapshot metadata, hidden partitioning, strong engine interoperability.

**Why it matters:** Multi-engine lakehouse (Spark, Flink, Trino, Athena).

**Example:** Partition evolution without rewriting all data paths visible to users.

**Remember:**
- Snapshots + manifests
- Hidden partitioning is a key feature

---

### Apache Hudi

**Definition:** Open table format focused on incremental processing, upserts, and streaming ingestion.

**Why it matters:** Near-real-time lakes with copy-on-write or merge-on-read.

**Example:** Upsert CDC into a Hudi MOR table; readers see compacted view.

**Remember:**
- COW vs MOR tradeoffs (write vs read cost)
- Strong for CDC / incremental pipelines

---

### Time Travel

**Definition:** Query table as of a past version/timestamp via snapshots/logs.

**Why it matters:** Reproduce reports, debug bad writes, audit.

**Example:**
```sql
SELECT * FROM orders VERSION AS OF 120;
-- or TIMESTAMP AS OF '2024-06-01'
```

**Remember:**
- Retention limited by vacuum/expire settings
- Great for "what did we have yesterday?"

---

### Schema Evolution

**Definition:** Safely change table schema (add/rename/drop columns) without full reload when supported.

**Why it matters:** Pipelines and producers change over time.

**Example:** Adding `discount_code` column to a Delta/Iceberg table.

**Remember:**
- Additive changes are safest
- Breaking changes need contracts + migration

---

### Schema Enforcement

**Definition:** Reject writes that don't match the table schema (or strict evolution rules).

**Why it matters:** Stops corrupt/partial schemas from poisoning the lake.

**Example:** Write with extra unexpected type fails instead of silently creating junk files.

**Remember:**
- Enforce at write boundary
- Pair with data contracts

---

### ACID Tables

**Definition:** Atomicity, Consistency, Isolation, Durability for table operations on the lake.

**Why it matters:** Readers never see partial commits; concurrent writers coordinated.

**Example:** A failed job leaves no half-visible partition after transactional commit.

**Remember:**
- File formats alone aren't ACID — table formats add it
- Isolation level still matters for readers

---

### Compaction

**Definition:** Rewrite many small files into larger optimized files.

**Why it matters:** Fixes small-file problem; improves scan speed.

**Example:** Iceberg rewrite / Hudi compact / Delta OPTIMIZE.

**Remember:**
- Schedule regularly on hot tables
- Trade compute now for faster reads later

---

### Vacuum

**Definition:** Delete obsolete data files no longer referenced by the table (past retention).

**Why it matters:** Reclaims storage; ends time-travel past retention.

**Example:** `VACUUM table_name RETAIN 168 HOURS;` (Delta).

**Remember:**
- Too aggressive vacuum breaks time travel / long readers
- Coordinate retention with consumers

---

### Optimize

**Definition:** Maintenance command to compact/layout data for faster reads (Delta `OPTIMIZE`).

**Why it matters:** Combines small files; optional Z-Order clustering.

**Example:** `OPTIMIZE sales ZORDER BY (customer_id, event_date);`

**Remember:**
- Run on tables with heavy small-file ingest
- Not free — schedule off-peak

---

### Z-Ordering

**Definition:** Multi-dimensional clustering of data files so related values co-locate (minmax skipping improves).

**Why it matters:** Faster filters on high-cardinality columns that aren't partition keys.

**Example:** Z-Order by `user_id` so point lookups skip most files.

**Remember:**
- Complement to partitioning, not a replacement
- Best for selective multi-column filters
