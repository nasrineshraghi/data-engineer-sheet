# CDC & SCD

Change Data Capture and Slowly Changing Dimensions — how source changes become warehouse history.

---

### Change Data Capture (CDC)

**Definition:** Continuously capture inserts/updates/deletes from a source system (often via logs) instead of full reloads.

**Why it matters:** Cheaper, fresher pipelines; enables near-real-time lakes/warehouses.

**Example:** Debezium reads Postgres WAL → Kafka topics → Spark/Flink applies to Delta.

**Remember:**
- Prefer log-based CDC over query-based when possible
- Handle deletes and schema changes explicitly

---

### Log-Based CDC

**Definition:** Read the database transaction log (WAL/binlog/redo) to emit change events.

**Why it matters:** Low source impact, ordered, includes deletes.

**Example:** MySQL binlog → Debezium → `orders` topic with before/after images.

**Remember:**
- Needs log retention + privileges
- Clock/ordering still matters across shards

---

### Query-Based CDC

**Definition:** Poll source tables using timestamps or version columns to find changes.

**Why it matters:** Easy to start; misses deletes and can miss updates if clocks/columns are weak.

**Example:** `SELECT * FROM orders WHERE updated_at > :last_watermark`.

**Remember:**
- Soft deletes required to see removals
- Overlap windows to avoid gaps

---

### Soft Delete vs Hard Delete

**Definition:** Soft delete marks a row inactive (`is_deleted=true`); hard delete removes the row.

**Why it matters:** CDC and analytics must treat them differently for correctness.

**Example:** Source hard-delete → CDC tombstone → target marks deleted or removes row.

**Remember:**
- Tombstones/delete events are first-class
- Downstream BI must filter soft deletes

---

### SCD Type 1

**Definition:** Overwrite attributes in place; no history kept.

**Why it matters:** Simple corrections (fix typo in email) without dimension bloat.

**Example:** Customer address updated → old address gone forever in the dim.

**Remember:**
- Fast and small
- Cannot answer “what was address last year?”

---

### SCD Type 2

**Definition:** Keep history by inserting a new dimension row with effective dates / current flag.

**Why it matters:** Point-in-time correct facts (who was the customer segment at order time).

**Example:** Segment changes → close old row (`end_date`), insert new row with new surrogate key.

**Remember:**
- Facts store the surrogate key valid at event time
- Watch dimension explosion on volatile attributes

---

### SCD Type 3

**Definition:** Store limited history in extra columns (e.g., current + previous).

**Why it matters:** Lightweight “previous value” without full type-2 history.

**Example:** `region` and `prior_region` columns on `dim_customer`.

**Remember:**
- Only N prior versions
- Rare vs type 1/2 in modern lakes

---

### Surrogate Key

**Definition:** Warehouse-generated key (usually integer/UUID) independent of source natural keys.

**Why it matters:** Stable joins across SCD versions and multi-source masters.

**Example:** `customer_sk` changes on type-2 version; `customer_id` natural key stays.

**Remember:**
- Facts join on surrogate keys
- Natural keys still needed for matching

---

### Natural Key

**Definition:** Business identifier from the source system (`customer_id`, `sku`).

**Why it matters:** Matching/CDC identity; not always unique across systems.

**Example:** Same person has different natural keys in CRM and billing → MDM/matching.

**Remember:**
- Can change or collide across sources
- Pair with surrogate keys in dims

---

### Effective Dating

**Definition:** `effective_start` / `effective_end` (or `is_current`) defines when a dim version is valid.

**Why it matters:** Point-in-time joins between facts and type-2 dimensions.

**Example:** Join fact `order_date` to dim where `start <= order_date < end`.

**Remember:**
- Avoid overlapping ranges
- Index/cluster on key + dates

---

### Late-Arriving Dimension

**Definition:** Fact arrives before its dimension row exists.

**Why it matters:** Orphan facts break joins and quality checks.

**Example:** Order for new customer lands before `dim_customer` CDC catches up.

**Remember:**
- Use inferred/unknown member placeholders
- Re-key when dimension arrives

---

### Late-Arriving Fact

**Definition:** Fact event arrives after its business date / reporting window closed.

**Why it matters:** Restates historical metrics; needs idempotent merges.

**Example:** Store posts yesterday’s sale two days late → merge into prior partition.

**Remember:**
- Partition overwrite / MERGE by business key
- Communicate restatement SLAs
