# Snowflake

Cloud data warehouse concepts every data engineer should know — compute, storage, loading, and governance.

---

### Virtual Warehouse

**Definition:** Dedicated compute cluster (size XS–4XL+) that runs queries and DML; billed while running.

**Why it matters:** Scale compute independently of storage; isolate workloads (ETL vs BI).

**Example:** `CREATE WAREHOUSE etl_wh WITH WAREHOUSE_SIZE = 'M' AUTO_SUSPEND = 60;`

**Remember:**
- Auto-suspend saves credits
- Separate warehouses for noisy ETL vs dashboards

---

### Separation of Storage and Compute

**Definition:** Data lives in cloud storage; warehouses attach compute on demand.

**Why it matters:** Many teams/warehouses can query the same data without copying.

**Example:** Finance XL warehouse and Data Eng M warehouse both query `PROD.ANALYTICS` tables.

**Remember:**
- Storage ≈ cheap continuous cost; compute ≈ bursty credits
- No classic “resize the cluster that holds the data”

---

### Micro-partitions

**Definition:** Immutable ~16MB columnar storage units Snowflake manages automatically (with metadata min/max).

**Why it matters:** Enable pruning; clustering improves locality for filters.

**Example:** Filter `WHERE order_date = '2024-01-01'` skips micro-partitions outside that range.

**Remember:**
- You don’t create micro-partitions manually
- Clustering keys guide co-location as data grows

---

### Clustering Key

**Definition:** Optional key(s) that guide how related rows are co-located across micro-partitions.

**Why it matters:** Better pruning on large tables filtered by those columns.

**Example:** `ALTER TABLE events CLUSTER BY (event_date, customer_id);`

**Remember:**
- Useful on multi-TB tables with repeated filter patterns
- Over-clustering wastes recluster credits

---

### Time Travel (Snowflake)

**Definition:** Query or restore table data as of a past timestamp/statement within retention (typically 1–90 days).

**Why it matters:** Undo bad loads; audit historical state.

**Example:** `SELECT * FROM orders AT (TIMESTAMP => '2024-06-01 12:00:00');`

**Remember:**
- Longer retention → more storage cost
- Different from Fail-safe

---

### Fail-safe

**Definition:** 7-day Snowflake-managed recovery window after Time Travel ends (not for user queries).

**Why it matters:** Disaster recovery last resort via Snowflake Support.

**Example:** Accidental drop discovered after Time Travel expired → Fail-safe recovery request.

**Remember:**
- Not a substitute for Time Travel / backups you control
- Historical data access only through Snowflake

---

### Zero-Copy Clone

**Definition:** Instant copy of database/schema/table that shares storage until data diverges.

**Why it matters:** Fast DEV/QA copies without duplicating bytes upfront.

**Example:** `CREATE TABLE orders_dev CLONE prod.analytics.orders;`

**Remember:**
- Cheap until writes cause divergence
- Great for experiments and backfill tests

---

### Stage

**Definition:** Named location for files (internal Snowflake stage or external S3/Azure/GCS) used by COPY/Snowpipe.

**Why it matters:** Standard landing zone for bulk loads.

**Example:** `COPY INTO target FROM @my_ext_stage/path/ FILE_FORMAT = (TYPE=PARQUET);`

**Remember:**
- External stages need storage integration / credentials
- Prefer patterned paths by date

---

### COPY INTO

**Definition:** Bulk load (or unload) command between stages and tables.

**Why it matters:** High-throughput ingestion workhorse.

**Example:** `COPY INTO raw.events FROM @stage/dt=2024-01-01/ PATTERN='.*[.]parquet';`

**Remember:**
- Idempotent-ish with force/purge options — design carefully
- Validate file formats and error options

---

### Snowpipe

**Definition:** Continuous/auto-ingest service that loads files from stages as they arrive (often via event notifications).

**Why it matters:** Near-real-time landing without scheduling heavy COPY jobs.

**Example:** S3 event → Snowpipe → `raw.events` within minutes.

**Remember:**
- Great for many small files; watch pipe errors
- Downstream transforms still need orchestration

---

### Stream (Snowflake)

**Definition:** Change-tracking object on a table (CDC-style inserts/updates/deletes) for incremental processing.

**Why it matters:** Build incremental ETL without re-scanning full tables.

**Example:** `CREATE STREAM orders_stream ON TABLE orders; SELECT * FROM orders_stream WHERE METADATA$ACTION = 'INSERT';`

**Remember:**
- Consuming a stream advances offsets — design transactions carefully
- Pair with Tasks for scheduled apply

---

### Task

**Definition:** Scheduled SQL/procedure job in Snowflake (can chain into task trees).

**Why it matters:** Lightweight in-platform orchestration for SQL transforms.

**Example:** Hourly task merges stream changes into a curated table.

**Remember:**
- Not a full Airflow replacement for complex multi-system DAGs
- Monitor failed task history

---

### VARIANT

**Definition:** Semi-structured column type for JSON/Avro/XML-like nested data.

**Why it matters:** Land flexible payloads then flatten into relational models.

**Example:** `SELECT payload:user.id::STRING AS user_id FROM raw_events;`

**Remember:**
- Queryable without predefined schema
- Flatten hot paths into typed columns for BI performance

---

### Result Cache

**Definition:** Cached query results reused when identical SQL hits unchanged data (24h, no warehouse needed).

**Why it matters:** Repeated dashboard SQL can be nearly free/instant.

**Example:** Same BI extract refreshed by many users within minutes → cache hits.

**Remember:**
- Any underlying data change invalidates
- Different from local warehouse disk cache

---

### Query Profile

**Definition:** Visual breakdown of a query’s operators, pruning, spillage, and time.

**Why it matters:** Primary Snowflake performance debugging tool.

**Example:** Profile shows TableScan reading most micro-partitions → add filter/clustering.

**Remember:**
- Look for partition scan %, spilling, exploding joins
- Fix data layout before upsizing warehouse

---

### Secure Data Sharing

**Definition:** Share live database objects with other Snowflake accounts without copying data.

**Why it matters:** Provider/consumer data products with governance.

**Example:** Share `analytics.sales_mart` to a partner reader account.

**Remember:**
- Consumers query shared objects in their account
- Revoke access instantly vs sending flat files

---

### Roles & RBAC

**Definition:** Access control via roles granted privileges on warehouses, databases, schemas, tables.

**Why it matters:** Least-privilege for ETL roles vs analyst roles.

**Example:** `GRANT USAGE ON WAREHOUSE bi_wh TO ROLE analyst; GRANT SELECT ON ALL TABLES IN SCHEMA marts TO ROLE analyst;`

**Remember:**
- Users activate a primary role (plus secondary roles if enabled)
- Own objects carefully — avoid personal ownership in prod
