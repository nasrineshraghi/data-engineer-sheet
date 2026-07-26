# Spark Internals

---

### DAG Scheduler

**Definition:** Builds a DAG of stages from the RDD/DataFrame lineage and submits stage tasks when parents finish.

**Why it matters:** Explains why shuffles create stage boundaries and how failures recompute.

**Example:** `map → filter → reduceByKey` → narrow stage then shuffle stage.

**Remember:**
- Stages split at wide dependencies (shuffles)
- Failed tasks recompute from lineage

---

### Task Scheduler

**Definition:** Assigns individual tasks to executors (resource offers from cluster manager).

**Why it matters:** Locality, speculation, and stragglers live here.

**Example:** Prefer `PROCESS_LOCAL` / `NODE_LOCAL` tasks when data is cached on that executor.

**Remember:**
- One task ≈ one partition
- Speculation helps slow stragglers

---

### Driver

**Definition:** The process that runs your main program, builds the DAG, and coordinates executors.

**Why it matters:** Driver OOM or GC pauses stall the whole job.

**Example:** Collecting a huge DataFrame to the driver (`collect()`) crashes the driver.

**Remember:**
- Keep driver light
- Avoid large `collect` / broadcast of huge objects

---

### Executor

**Definition:** JVM worker process that runs tasks and stores shuffle/cache data.

**Why it matters:** Memory, cores, and disk per executor dominate performance.

**Example:** 10 executors × 4 cores → up to 40 concurrent tasks.

**Remember:**
- Tune `executor-memory` and cores together
- Watch spill and GC

---

### Worker

**Definition:** Cluster node process (e.g., Spark standalone worker) that hosts executors.

**Why it matters:** Distinguishes machine vs JVM process.

**Example:** One worker machine runs multiple executors.

**Remember:**
- Worker ≠ executor
- YARN/K8s abstract workers differently

---

### Cluster Manager

**Definition:** Allocates resources: Standalone, YARN, Kubernetes, Mesos (legacy).

**Why it matters:** How cores/memory are requested and released.

**Example:** `spark.master=yarn` or `k8s://...` with dynamic allocation.

**Remember:**
- Dynamic allocation needs external shuffle service (classic YARN)
- K8s common in modern platforms

---

### Job → Stage → Task

**Definition:**
- **Job:** triggered by an action (`count`, `write`, `collect`)
- **Stage:** set of tasks with narrow deps between shuffles
- **Task:** unit of work on one partition

**Why it matters:** UI debugging language.

**Example:** One `write` action → 1 job → 3 stages → N tasks per stage.

**Remember:**
- Actions create jobs
- Shuffles create stages
- Partitions create tasks

---

### Lineage

**Definition:** Graph of transformations needed to recompute an RDD/DataFrame partition.

**Why it matters:** Fault tolerance without replicating all data.

**Example:** Lose executor → recompute lost partitions from source + lineage.

**Remember:**
- Checkpoint breaks long lineages
- Lineage is logical, not always stored data

---

### Lazy Evaluation

**Definition:** Transformations build a plan; work runs only on actions.

**Why it matters:** Enables whole-stage optimization and predicate pushdown.

**Example:** Many `filter`/`select` calls do nothing until `show()` or `write`.

**Remember:**
- Chain transforms freely
- Actions trigger compute (and cost)

---

### Shuffle

**Definition:** Redistribute data across partitions by key (network + sort/hash).

**Why it matters:** Usually the most expensive part of a job.

**Example:** `groupBy`, `join`, `repartition`, `distinct` often shuffle.

**Remember:**
- Minimize shuffles
- Watch shuffle read/write in Spark UI

---

### Spill to Disk

**Definition:** When memory is insufficient, intermediate data is written to local disk.

**Why it matters:** Correctness preserved; speed drops.

**Example:** Large sort-merge join spills during sort.

**Remember:**
- Spill ≠ failure; it's a warning sign
- Increase memory, reduce partition size, or fix skew

---

### Memory Management

**Definition:** Spark splits executor memory among execution (shuffles/joins), storage (cache), and user/overhead.

**Why it matters:** Contention between cache and shuffle causes eviction/spill.

**Example:** Unified memory region shared by execution and storage (post Spark 1.6).

**Remember:**
- Don't cache everything
- Tune fraction only after measuring

---

### Serialization (Java/Kryo)

**Definition:** Convert objects to bytes for shuffle/cache/network. Kryo is faster/smaller than Java serializer when registered.

**Why it matters:** Slow serialization burns CPU on every shuffle.

**Example:** `spark.serializer=org.apache.spark.serializer.KryoSerializer` + register classes.

**Remember:**
- Prefer DataFrames (Catalyst/Tungsten) over RDDs of custom objects
- Kryo helps RDD/custom types

---

### Broadcast Variables

**Definition:** Read-only copy of data sent once to each executor.

**Why it matters:** Avoids shipping large lookup tables per task.

**Example:** Broadcast a small dimension for map-side join / `broadcast(df)`.

**Remember:**
- Size must fit executor memory
- Default auto-broadcast threshold exists in Spark SQL

---

### Accumulators

**Definition:** Write-only aggregate variables (counters) updated by executors, read on driver.

**Why it matters:** Lightweight metrics without collecting data.

**Example:** Count malformed records while mapping.

**Remember:**
- Updates inside transforms may be recomputed on retry — use carefully
- Prefer built-in Spark metrics when possible

---

### Closure

**Definition:** Function + captured outer variables sent to executors.

**Why it matters:** Accidental capture of huge objects (DB connections, full DataFrames) causes OOM or slow shipping.

**Example:** Capturing a large Python list in a UDF serializes it to every task.

**Remember:**
- Don't capture huge objects
- Prefer broadcast for shared lookups

---

### Wide vs Narrow Transformations

**Definition:**
- **Narrow:** each input partition maps to ≤1 output partition (`map`, `filter`) — no shuffle
- **Wide:** input partitions contribute to many outputs (`groupByKey`, `join`) — shuffle

**Why it matters:** Wide = stage boundary + cost.

**Example:** `filter` narrow; `reduceByKey` wide.

**Remember:**
- Pipeline narrow transforms in one stage
- Wide transforms need justification

---

### Adaptive Query Execution (AQE)

**Definition:** Spark SQL re-optimizes the plan at runtime using size stats after shuffles (Spark 3+).

**Why it matters:** Fixes bad static estimates: coalesces partitions, switches join strategy, handles skew.

**Example:** AQE converts sort-merge to broadcast when post-shuffle side is small.

**Remember:**
- Enable AQE in modern Spark (`spark.sql.adaptive.enabled`)
- Helps skew join and partition coalescing

---

### Catalyst Optimizer

**Definition:** Spark SQL's rule + cost optimizer: analysis → logical optimization → physical planning.

**Why it matters:** Why DataFrames beat handwritten RDDs for SQL-like work.

**Example:** Constant folding, predicate pushdown, column pruning done automatically.

**Remember:**
- Prefer DataFrame/Dataset API
- UDFs limit Catalyst optimizations

---

### Tungsten Engine

**Definition:** Execution layer: off-heap/cache-aware memory, whole-stage codegen, binary processing.

**Why it matters:** Faster CPU and less GC than row-object RDDs.

**Example:** Whole-stage codegen fuses operators into Java bytecode.

**Remember:**
- Works best with native expressions (not Python UDFs)
- Columnar formats amplify gains

---

### Dynamic Partition Pruning

**Definition:** At runtime, prune partitions of a large fact using values from a filtered dimension join.

**Why it matters:** Star-schema queries read far less data.

**Example:** Join `sales` (partitioned by `date`) to `dim_date` filtered to one month → only those fact partitions scanned.

**Remember:**
- Needs partitioned fact + filter on dimension
- Related to AQE / DPP features

---

### Skew Join Optimization

**Definition:** Detect hot keys and split/handle them separately (AQE skew join, salting).

**Why it matters:** One key can stall an entire stage.

**Example:** One `customer_id` with 40% of rows → AQE splits that partition.

**Remember:**
- Check Spark UI for straggler tasks
- Salting is the manual fallback
