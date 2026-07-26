# Database & SQL Concepts

---

### Cardinality

**Definition:** Number of distinct values in a column (or relation size: number of rows).

**Why it matters:** Optimizer uses cardinality to choose joins, indexes, and broadcast vs shuffle.

**Example:** `country` has ~200 distinct values (low cardinality). `user_id` may have millions (high cardinality).

**Remember:**
- Low cardinality → bitmap indexes / dictionaries often help
- Wrong cardinality estimates → bad plans

---

### Granularity (Grain)

**Definition:** The level of detail one row represents (what one row means).

**Why it matters:** Wrong grain causes double-counting, bad joins, and incorrect metrics.

**Example:** Orders table grain = one row per `order_id`. Order-items grain = one row per `order_id + product_id`.

**Remember:**
- Always state grain before modeling
- Never mix grains in one fact without care

---

### Selectivity

**Definition:** Fraction of rows a predicate returns. High selectivity = few rows (selective filter).

**Why it matters:** Selective predicates favor index seeks; low selectivity favors scans.

**Example:** `WHERE user_id = 42` is highly selective. `WHERE status = 'active'` on 90% active rows is not.

**Remember:**
- Selectivity ≈ matching_rows / total_rows
- Indexes help most on selective filters

---

### Data Distribution

**Definition:** How values are spread across a column (uniform, skewed, sparse).

**Why it matters:** Skew causes hot partitions, slow joins, and uneven executor load.

**Example:** 80% of orders from one country → that partition/key dominates shuffle.

**Remember:**
- Check histograms / approx_percentile for skew
- Salting and AQE help with skew

---

### Histograms

**Definition:** Statistics summarizing value frequency distribution in a column.

**Why it matters:** Help CBO estimate selectivity when values are uneven.

**Example:** Optimizer sees `status='cancelled'` is 2% of rows via histogram, not assuming uniform 25%.

**Remember:**
- Stale histograms → bad plans
- Refresh stats after large loads

---

### Cost-Based Optimizer (CBO)

**Definition:** Chooses execution plan by estimating cost using table/column statistics.

**Why it matters:** Modern warehouses and Spark SQL rely on CBO for join order and strategies.

**Example:** With stats, CBO picks broadcast hash join for a small dimension; without stats, may shuffle both sides.

**Remember:**
- Collect/analyze stats regularly
- No stats ≈ guessing

---

### Rule-Based Optimizer (RBO)

**Definition:** Rewrites queries using fixed heuristic rules (e.g., push filters early), not cost estimates.

**Why it matters:** Fast and predictable; weak when data sizes vary.

**Example:** Always push `WHERE` before `JOIN` regardless of table size.

**Remember:**
- Spark Catalyst uses both rules and cost
- RBO alone can miss better join strategies

---

### Execution Plan

**Definition:** The concrete operators the engine will run (scans, joins, aggregates, sorts).

**Why it matters:** Primary tool to debug slow queries.

**Example:** Plan shows `SortMergeJoin` + large `Exchange` (shuffle) → expensive.

**Remember:**
- Read bottom-up or follow arrows depending on engine
- Look for scans, shuffles, spills

---

### Explain Plan

**Definition:** Command/API that prints the logical and/or physical plan without always running the full query.

**Why it matters:** Inspect strategy before/while tuning.

**Example:**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date = '2024-01-01';
-- Spark: df.explain(True)  or  EXPLAIN EXTENDED / COST
```

**Remember:**
- `ANALYZE` / actual metrics beat estimated-only plans
- Compare before vs after rewrite

---

### Composite Index

**Definition:** Index on multiple columns in a defined order.

**Why it matters:** Speeds queries filtering/sorting on the leading columns.

**Example:** Index `(customer_id, order_date)` helps `WHERE customer_id = ?` and `WHERE customer_id = ? AND order_date > ?`, not `WHERE order_date > ?` alone (usually).

**Remember:**
- Column order matters (leftmost prefix)
- Don't over-index; writes get slower

---

### Covering Index

**Definition:** Index that contains all columns a query needs, so the table heap/base isn't touched.

**Why it matters:** Index-only scans are much faster for narrow queries.

**Example:** Query selects `id, email` with index on `(id) INCLUDE (email)` → covering.

**Remember:**
- Great for hot read paths
- Wider indexes cost more storage/write amp

---

### Clustered vs Non-Clustered Index

**Definition:**
- **Clustered:** table rows stored in index key order (often primary key); typically one per table.
- **Non-clustered:** separate structure pointing to rows; many allowed.

**Why it matters:** Clustered key choice affects range scans and insert patterns.

**Example:** Clustered on `order_date` makes date-range queries fast; random UUIDs as clustered keys can fragment inserts.

**Remember:**
- InnoDB PK is clustered; SQL Server similar
- Choose clustered key for common access pattern

---

### Bitmap Index

**Definition:** Index storing bitmaps per distinct value; good for low-cardinality columns and AND/OR of predicates.

**Why it matters:** Common in analytic DBs; poor for high-churn OLTP updates.

**Example:** Bitmap on `gender`, `region`, `status` for warehouse filters.

**Remember:**
- Low cardinality + analytics
- Avoid on frequently updated columns

---

### B-Tree Index

**Definition:** Balanced tree index supporting equality and range lookups; default in most RDBMS.

**Why it matters:** Workhorse for OLTP and many warehouse lookups.

**Example:** B-tree on `email` → fast `WHERE email = 'a@b.com'`.

**Remember:**
- Equality + ranges
- Not ideal alone for very low cardinality

---

### Predicate Pushdown

**Definition:** Move filters as close as possible to the data source so less data is read/shuffled.

**Why it matters:** Huge I/O and network savings on parquet/ORC and remote sources.

**Example:** `spark.read.parquet(...).filter("year=2024")` pushes year filter into file/footer reading when partitioned.

**Remember:**
- Prefer partition columns and columnar formats
- UDFs often block pushdown

---

### Partition Pruning

**Definition:** Skip reading partitions that cannot match the query filter.

**Why it matters:** Turns full scans into reading a fraction of data.

**Example:** Table partitioned by `dt`; `WHERE dt='2024-06-01'` reads only that partition.

**Remember:**
- Filter on partition columns explicitly
- Dynamic partition pruning helps joins

---

### Statistics

**Definition:** Metadata about tables/columns: row counts, NDV, min/max, histograms, size.

**Why it matters:** Fuel for CBO and good join strategies.

**Example:**
```sql
ANALYZE TABLE orders COMPUTE STATISTICS FOR COLUMNS customer_id, amount;
```

**Remember:**
- Refresh after bulk loads/deletes
- Missing stats → conservative/bad plans

---

### Table Scan vs Index Scan

**Definition:**
- **Table (full) scan:** read all rows/pages.
- **Index scan:** walk an index (may still touch many rows).

**Why it matters:** Scans aren't always bad — for large fractions of the table they can win.

**Example:** Selecting 2% of rows by PK → index. Selecting 70% → full scan often better.

**Remember:**
- Optimizer picks based on selectivity + cost
- "Index scan" ≠ cheap if it returns most of the table

---

### Seek vs Scan

**Definition:**
- **Seek:** jump to a specific key/range in the index.
- **Scan:** read a contiguous slice (or all) of index/table.

**Why it matters:** Seeks are for pinpoint lookups; scans for broader access.

**Example:** `WHERE id = 10` → seek. `WHERE id BETWEEN 1 AND 1000000` → range scan.

**Remember:**
- Seek + few rows = ideal
- Large range scan can rival table scan
