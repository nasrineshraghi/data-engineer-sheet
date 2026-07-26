# Performance Tuning

---

### Data Skew

**Definition:** Uneven key/partition sizes so a few tasks do most of the work.

**Why it matters:** Stage time ≈ slowest task.

**Example:** `null` or popular `country_code` holds 50% of join keys.

**Remember:**
- Detect via task duration histograms
- Fix with salting, AQE skew join, or pre-agg

---

### Broadcast Join

**Definition:** Replicate the small side to all executors; join locally (map-side).

**Why it matters:** Avoids shuffling the large side.

**Example:** Fact × small dimension (`broadcast(dim)`).

**Remember:**
- Small side must fit memory
- Best default for star-schema dims

---

### Shuffle Join

**Definition:** Generic term for joins that redistribute both sides by join key (often sort-merge or shuffle-hash).

**Why it matters:** Expensive but necessary for two large tables.

**Example:** Large `orders` ⋈ large `payments` on `order_id`.

**Remember:**
- Ensure join keys have good distribution
- Filter early before shuffle

---

### Sort Merge Join

**Definition:** Shuffle both sides by key, sort, then merge — Spark's common large-large join.

**Why it matters:** Scalable; sensitive to skew and spill.

**Example:** Default for two big DataFrames when broadcast isn't chosen.

**Remember:**
- Watch sort spill
- AQE may switch strategy

---

### Hash Join

**Definition:** Build hash table on one side, probe with the other (in-memory or spilled).

**Why it matters:** Fast when build side fits (or partially).

**Example:** Broadcast hash join = hash join with replicated build side.

**Remember:**
- Build = smaller side ideally
- OOM if build side underestimated

---

### Bucket Join

**Definition:** Tables pre-bucketed (and often sorted) on the same key so joins avoid full shuffle.

**Why it matters:** Speeds repeated joins on stable keys.

**Example:** Both tables bucketed by `user_id` into 200 buckets → bucket join.

**Remember:**
- Bucket count must match (or be compatible)
- Worth it for heavy reuse patterns

---

### Salting

**Definition:** Add a random salt to hot keys to spread them across partitions, then remove/aggregate.

**Why it matters:** Manual skew fix when AQE isn't enough.

**Example:** Hot `customer_id` → `customer_id + salt_0..N` on both sides for join, then drop salt.

**Remember:**
- Increases rows temporarily
- Choose salt range from skew severity

---

### Caching

**Definition:** Keep a dataset in memory/disk across actions to avoid recomputation.

**Why it matters:** Iterative algorithms and multi-action reuse.

**Example:** `df.cache()` before multiple joins/aggregations on same base.

**Remember:**
- Unpersist when done
- Cache only reused expensive stages

---

### Persistence Levels

**Definition:** Storage level for cached data: memory only, memory+disk, disk only, serialized, replicated.

**Why it matters:** Trade speed vs memory pressure vs reliability.

**Example:** `MEMORY_AND_DISK` safer than `MEMORY_ONLY` for large frames.

**Remember:**
- DataFrames: `cache` ≈ MEMORY_AND_DISK
- Replication costs memory

---

### Parallelism

**Definition:** Degree of concurrent tasks (related to partitions and cores).

**Why it matters:** Too low = idle cluster; too high = scheduling overhead.

**Example:** `repartition(200)` to use ~200 cores effectively for a stage.

**Remember:**
- Target a few partitions per core
- Aim for reasonable partition file sizes

---

### Partition Sizing

**Definition:** Choosing number/size of partitions (and output files) for balanced work.

**Why it matters:** Core lever for Spark/Hive performance.

**Example:** Target ~128–256 MB per partition file for many lake workloads (rule of thumb, not law).

**Remember:**
- Too small → small files
- Too large → spill/OOM risk

---

### Small File Problem

**Definition:** Too many tiny files → heavy listing, task overhead, slow queries.

**Why it matters:** Streaming/micro-batch ingest often creates this.

**Example:** 100k files of 1 MB instead of 400 files of 256 MB.

**Remember:**
- Compact regularly
- Coalesce/repartition before write; avoid over-partitioning
