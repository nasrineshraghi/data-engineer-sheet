# Must-know 30

Do **[The most important 10](ESSENTIALS.md)** first. These 30 are the next layer.

Readable UI: [Essentials](docs/index.html?mode=essentials) · [Must 30](docs/index.html?mode=must) · [Prod playbook](docs/index.html?mode=prod)

## 1. Cardinality

Number of distinct values in a column (or relation size: number of rows).

```
SELECT COUNT(DISTINCT user_id) AS cardinality FROM events;
```

**In prod:** Bad join strategy because NDV was underestimated.

---

## 2. Grain

Exact meaning of one fact row (business level of detail).

```
-- Fact grain: 1 row = 1 completed checkout
-- Always declare grain before designing the fact
```

**In prod:** KPI doesn't match finance because grains differ.

---

## 3. Predicate Pushdown

Move filters as close as possible to the data source so less data is read/shuffled.

```
df = spark.read.parquet("s3://lake/events").filter("dt = '2024-01-01'")
# filter pushed into scan / partition prune
```

**In prod:** Full scan of years of data for a one-day query.

---

## 4. Partition Pruning

Skip reading partitions that cannot match the query filter.

```
SELECT * FROM sales WHERE dt BETWEEN '2024-01-01' AND '2024-01-07';
-- only those partitions are read
```

**In prod:** Query reads every partition folder despite a date filter.

---

## 5. Shuffle

Redistribute data across partitions by key (network + sort/hash).

```
df.groupBy("user_id").count()  # wide transform → shuffle
# Spark UI: Shuffle Read/Write bytes
```

**In prod:** Stage stuck; network/disk dominated by shuffle.

---

## 6. Job → Stage → Task

- **Job:** triggered by an action (`count`, `write`, `collect`) - **Stage:** set of tasks with narrow deps between shuffles - **Task:** unit of work on one partition

```
# action → job; shuffle boundary → stage; partition → task
df.write.parquet(path)  # triggers a job
```

**In prod:** Confused debugging — looking at tasks without finding the slow stage.

---

## 7. Lazy Evaluation

Transformations build a plan; work runs only on actions.

```
f = df.filter(...).select(...)  # builds plan only
f.count()                     # action runs the job
```

**In prod:** Thinking transforms already ran; surprise cost on first action.

---

## 8. Wide vs Narrow Transformations

- **Narrow:** each input partition maps to ≤1 output partition (`map`, `filter`) — no shuffle - **Wide:** input partitions contribute to many outputs (`groupByKey`, `join`) — shuffle

```
# narrow: map/filter (no shuffle)
# wide: groupBy/join/repartition (shuffle)
```

**In prod:** Extra wide transforms inflate runtime for little gain.

---

## 9. Adaptive Query Execution (AQE)

Spark SQL re-optimizes the plan at runtime using size stats after shuffles (Spark 3+).

```
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**In prod:** Static plan picks sort-merge when broadcast would win.

---

## 10. Catalyst Optimizer

Spark SQL's rule + cost optimizer: analysis → logical optimization → physical planning.

```
df.explain(True)  # parsed/analyzed/optimized/physical plans
```

**In prod:** Python UDF blocks optimizations → slower than SQL expr.

---

## 11. Broadcast Join

Replicate the small side to all executors; join locally (map-side).

```
from pyspark.sql.functions import broadcast
fact.join(broadcast(dim), "id")
```

**In prod:** Shuffling a tiny dimension across the cluster.

---

## 12. Sort Merge Join

Shuffle both sides by key, sort, then merge — Spark's common large-large join.

```
# default large-large join after shuffle+sort
big.join(other_big, "user_id")
```

**In prod:** Join spills to disk; one key's partition is huge.

---

## 13. Data Skew

Uneven key/partition sizes so a few tasks do most of the work.

```
df.groupBy("key").count().orderBy(desc("count")).show(20)
# then salt hot keys or enable AQE skew join
```

**In prod:** One task runs 10× longer than the rest of the stage.

---

## 14. Small File Problem

Too many tiny files → heavy listing, task overhead, slow queries.

```
df.coalesce(64).write.mode("overwrite").parquet(path)
# or OPTIMIZE / compaction on lakehouse tables
```

**In prod:** Driver spends ages listing; thousands of tiny tasks.

---

## 15. Conformed Dimension

Shared dimension with consistent keys and attributes across facts/marts.

```
-- same customer_key + attributes shared by sales & support facts
```

**In prod:** Two marts define "customer" differently; dashboards disagree.

---

## 16. Delta Lake

Open table format (Databricks-origin) with transaction log (`_delta_log`) for ACID on files.

```
MERGE INTO target t USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**In prod:** Concurrent jobs overwrite parquet folders; readers see partial data.

---

## 17. Time Travel

Query table as of a past version/timestamp via snapshots/logs.

```
SELECT * FROM orders VERSION AS OF 120;
-- or TIMESTAMP AS OF '2024-06-01'
```

**In prod:** Can't reproduce yesterday's report after a bad overwrite.

---

## 18. Schema Evolution

Safely change table schema (add/rename/drop columns) without full reload when supported.

```
df.write.format("delta").option("mergeSchema", "true").mode("append").save(path)
```

**In prod:** Producer adds a column; downstream jobs break or ignore it silently.

---

## 19. CAP Theorem

In a network partition, a system can provide Consistency or Availability, not both (Partition tolerance assumed in distributed DBs).

```
# In a partition: choose Consistency or Availability
# Document the tradeoff for your store/queue
```

**In prod:** Expecting strong reads from an AP system during a region blip.

---

## 20. Event Time

Timestamp when the event actually occurred in the real world.

```
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "1 hour")).count()
```

**In prod:** Hourly metrics shift when late mobile events arrive.

---

## 21. Watermarks

Engine's notion of how far event time has advanced; used to close windows.

```
.withWatermark("event_time", "15 minutes")
# closes windows; late data policy after this
```

**In prod:** State grows forever, or late events are dropped too aggressively.

---

## 22. Exactly Once

Effect of each record applied once end-to-end (despite retries).

```
# Need checkpointing + idempotent/transactional sink
query = df.writeStream.option("checkpointLocation", ckpt).foreachBatch(...)
```

**In prod:** Duplicates after restart even though processing "felt" safe.

---

## 23. At Least Once

Every record processed ≥1 time; duplicates possible on retry.

```
# retries may re-send — make sink upsert/idempotent
# ON CONFLICT (id) DO UPDATE ...
```

**In prod:** Counts inflate after every pipeline retry.

---

## 24. Idempotency

Running the same operation multiple times yields the same result as running once.

```
# overwrite a partition instead of blind append
df.write.mode("overwrite").partitionBy("dt").parquet(path)
```

**In prod:** Re-running a failed day duplicates rows in the target.

---

## 25. Checkpointing

Persist progress (offsets/state) so recovery resumes cleanly.

```
writeStream.option("checkpointLocation", "s3://ops/checkpoints/job_a")
```

**In prod:** Streaming job reprocesses from earliest offsets after path loss.

---

## 26. Dead Letter Queue (DLQ)

Side channel for records that fail processing after retries.

```
try:
    process(record)
except BadRecord as e:
    dlq.send(record, error=str(e))
```

**In prod:** One poison message blocks the whole consumer group.

---

## 27. Data Contracts

Explicit agreement on schema, semantics, SLAs, and ownership between producers and consumers.

```
# CI: fail PR if producer schema breaks consumer contract
# enforce required fields + types at write boundary
```

**In prod:** Silent column rename breaks 12 downstream jobs overnight.

---

## 28. Data Lineage

Trace where data came from and where it flows (table/column/job level).

```
# raw.orders → stg_orders → fct_orders → BI KPI
# track table + column lineage in the catalog
```

**In prod:** Can't tell which dashboard breaks if a source column is dropped.

---

## 29. Freshness

How up-to-date the data is vs expectation (SLA/SLO).

```
SELECT MAX(updated_at) FROM fct_orders;
-- alert if now() - max_updated_at > SLA
```

**In prod:** Job is green but data is 18 hours stale.

---

## 30. Object Storage

Store immutable objects (files) addressed by key in buckets; virtually infinite scale.

```
s3://lake/bronze/events/dt=2024-01-01/part-000.parquet
# lake tables live as objects + metadata
```

**In prod:** Treating S3 like a local FS; millions of tiny LIST requests.

---
