# Data Engineering Knowledge Base

A practical glossary of techniques, keywords, and concepts every data engineer should know — with short definitions and examples. Not deep dives; enough to recall, interview, and apply.

## Live on GitHub Pages

| Open this | Link |
|-----------|------|
| **Summary table (all keywords)** | https://nasrineshraghi.github.io/data-engineer-sheet/table.html |
| **Study app (Essentials / Prod)** | https://nasrineshraghi.github.io/data-engineer-sheet/ |
| **Markdown summary table** (in the repo) | [QUICK_REF.md](QUICK_REF.md) |

If the Pages links 404: repo **Settings → Pages → Deploy from a branch → `gh-pages` / `(root)` → Save**.

## New here? Start with this

1. Open **[Essentials — most important 10](https://nasrineshraghi.github.io/data-engineer-sheet/?mode=essentials)** ([ESSENTIALS.md](ESSENTIALS.md))
2. Learn **when to use them** in **[Prod](https://nasrineshraghi.github.io/data-engineer-sheet/?mode=prod)** ([PROD.md](PROD.md))
3. Lookup anything in the **[summary table](https://nasrineshraghi.github.io/data-engineer-sheet/table.html)**

## Study app

**[Live summary table →](https://nasrineshraghi.github.io/data-engineer-sheet/table.html)** · **[Live study app →](https://nasrineshraghi.github.io/data-engineer-sheet/)** · **[Markdown table →](QUICK_REF.md)**

| Mode | What you get |
|------|----------------|
| **Essentials** | The 10 most important ideas ([ESSENTIALS.md](ESSENTIALS.md)) |
| **Prod** | Symptom → what to do → which concepts ([PROD.md](PROD.md)) |
| **Browse all** | Full glossary when you need a lookup |
| **Must 30** | Next layer after Essentials |
| **Cards / Quiz / Stories** | Practice applying concepts |
| **Summary table** | All keywords · definition · example ([live](https://nasrineshraghi.github.io/data-engineer-sheet/table.html) · [QUICK_REF.md](QUICK_REF.md)) |

Also: deep links `?mode=essentials` · `?mode=prod` · `?mode=must`

### GitHub Pages setup (if links 404)

1. After the **Deploy study app** Action turns green…
2. Open https://github.com/nasrineshraghi/data-engineer-sheet/settings/pages
3. Source: **Deploy from a branch**
4. Branch: **`gh-pages`** · Folder: **`/ (root)`** → **Save**
5. Wait 1–2 minutes → https://nasrineshraghi.github.io/data-engineer-sheet/table.html

## How to use

- **Study app:** [docs/index.html](docs/index.html)
- Browse keywords below → category files for full write-ups
- A–Z lookup: [INDEX.md](INDEX.md)
- Rebuild: `python3 scripts/build_search_data.py`

## Categories

| # | Category | File |
|---|----------|------|
| 1 | [Database & SQL Concepts](01-database-sql/concepts.md) | Indexes, plans, cardinality, pruning |
| 2 | [Spark Internals](02-spark-internals/concepts.md) | Driver, shuffle, Catalyst, AQE |
| 3 | [Data Warehouse Concepts](03-data-warehouse/concepts.md) | Facts, dimensions, grain, snapshots |
| 4 | [Data Lake & Lakehouse](04-data-lake-lakehouse/concepts.md) | Delta, Iceberg, Hudi, time travel |
| 5 | [Distributed Systems](05-distributed-systems/concepts.md) | CAP, consensus, scaling |
| 6 | [Streaming](06-streaming/concepts.md) | Watermarks, windows, exactly-once |
| 7 | [Pipeline Design](07-pipeline-design/concepts.md) | Idempotency, DLQ, orchestration |
| 8 | [Performance Tuning](08-performance-tuning/concepts.md) | Joins, skew, partitions, caching |
| 9 | [Data Quality & Governance](09-data-quality-governance/concepts.md) | Lineage, catalog, observability |
| 10 | [Cloud & Storage](10-cloud-storage/concepts.md) | Object storage, IAM, encryption |
| 11 | [DevOps for Data](11-devops/concepts.md) | Docker, K8s, IaC, CI/CD |
| 12 | [CDC & SCD](12-cdc-scd/concepts.md) | CDC, SCD 1/2/3, surrogate keys |
| 13 | [dbt](13-dbt/concepts.md) | Models, incremental, tests, exposures |
| 14 | [Kafka](14-kafka/concepts.md) | Topics, offsets, EOS, schema registry |
| 15 | [Airflow](15-airflow/concepts.md) | DAGs, sensors, backfill, datasets |
| 16 | [Cost Optimization](16-cost-optimization/concepts.md) | Pruning, tiering, right-sizing |
| 17 | [Snowflake](17-snowflake/concepts.md) | Warehouses, micro-partitions, Snowpipe, streams |
| 18 | [Clinical Data — Meds & Labs](18-clinical-data/concepts.md) | Orders, RxNorm/NDC, LOINC, labs, MAR |
| 19 | [APIs for Data Engineers](19-api/concepts.md) | REST, auth, pagination, webhooks, contracts |

## All keywords
### Database & SQL Concepts
[01-database-sql/concepts.md](01-database-sql/concepts.md)

- Cardinality
- Granularity (Grain)
- Selectivity
- Data Distribution
- Histograms
- Cost-Based Optimizer (CBO)
- Rule-Based Optimizer (RBO)
- Execution Plan
- Explain Plan
- Composite Index
- Covering Index
- Clustered vs Non-Clustered Index
- Bitmap Index
- B-Tree Index
- Predicate Pushdown
- Partition Pruning
- Statistics
- Table Scan vs Index Scan
- Seek vs Scan

### Spark Internals
[02-spark-internals/concepts.md](02-spark-internals/concepts.md)

- DAG Scheduler
- Task Scheduler
- Driver
- Executor
- Worker
- Cluster Manager
- Job → Stage → Task
- Lineage
- Lazy Evaluation
- Shuffle
- Spill to Disk
- Memory Management
- Serialization (Java/Kryo)
- Broadcast Variables
- Accumulators
- Closure
- Wide vs Narrow Transformations
- Adaptive Query Execution (AQE)
- Catalyst Optimizer
- Tungsten Engine
- Dynamic Partition Pruning
- Skew Join Optimization

### Data Warehouse Concepts
[03-data-warehouse/concepts.md](03-data-warehouse/concepts.md)

- Grain
- Granularity
- Additive Facts
- Semi-Additive Facts
- Non-Additive Facts
- Degenerate Dimension
- Junk Dimension
- Role-Playing Dimension
- Conformed Dimension
- Mini Dimension
- Bridge Table
- Factless Fact Table
- Snapshot Fact
- Accumulating Snapshot
- Periodic Snapshot

### Data Lake & Lakehouse
[04-data-lake-lakehouse/concepts.md](04-data-lake-lakehouse/concepts.md)

- Data Lake
- Data Lakehouse
- Delta Lake
- Apache Iceberg
- Apache Hudi
- Time Travel
- Schema Evolution
- Schema Enforcement
- ACID Tables
- Compaction
- Vacuum
- Optimize
- Z-Ordering

### Distributed Systems
[05-distributed-systems/concepts.md](05-distributed-systems/concepts.md)

- CAP Theorem
- BASE
- Eventual Consistency
- Strong Consistency
- Replication
- Leader Election
- Consensus
- Raft
- Paxos
- Fault Tolerance
- High Availability (HA)
- Horizontal Scaling
- Vertical Scaling

### Streaming
[06-streaming/concepts.md](06-streaming/concepts.md)

- Event Time
- Processing Time
- Ingestion Time
- Watermarks
- Windowing
- Late Data
- Stateful Processing
- Stateless Processing
- Exactly Once
- At Least Once
- At Most Once
- Event Sourcing
- CQRS

### Pipeline Design
[07-pipeline-design/concepts.md](07-pipeline-design/concepts.md)

- Idempotency
- Checkpointing
- Retry Strategy
- Backoff Strategy
- Circuit Breaker
- Dead Letter Queue (DLQ)
- Data Contracts
- Pipeline Orchestration
- Metadata-Driven Pipelines

### Performance Tuning
[08-performance-tuning/concepts.md](08-performance-tuning/concepts.md)

- Data Skew
- Broadcast Join
- Shuffle Join
- Sort Merge Join
- Hash Join
- Bucket Join
- Salting
- Caching
- Persistence Levels
- Parallelism
- Partition Sizing
- Small File Problem

### Data Quality & Governance
[09-data-quality-governance/concepts.md](09-data-quality-governance/concepts.md)

- Data Profiling
- Data Validation
- Data Lineage
- Metadata
- Data Catalog
- Master Data Management (MDM)
- Data Governance
- Data Stewardship
- Observability
- Freshness
- Completeness
- Accuracy
- Consistency

### Cloud & Storage
[10-cloud-storage/concepts.md](10-cloud-storage/concepts.md)

- Object Storage
- Block Storage
- Lifecycle Policies
- IAM
- Secrets Management
- KMS
- Encryption at Rest
- Encryption in Transit
- VPC
- Private Endpoints

### DevOps for Data
[11-devops/concepts.md](11-devops/concepts.md)

- Docker
- Kubernetes
- CI/CD
- GitOps
- Terraform
- Helm
- Infrastructure as Code (IaC)

### CDC & SCD
[12-cdc-scd/concepts.md](12-cdc-scd/concepts.md)

- Change Data Capture (CDC)
- Log-Based CDC
- Query-Based CDC
- Soft Delete vs Hard Delete
- SCD Type 1
- SCD Type 2
- SCD Type 3
- Surrogate Key
- Natural Key
- Effective Dating
- Late-Arriving Dimension
- Late-Arriving Fact

### dbt
[13-dbt/concepts.md](13-dbt/concepts.md)

- dbt Model
- Materialization
- Incremental Model
- Sources
- Seeds
- ref()
- Tests (dbt)
- Exposures
- Documentation / Docs Site
- Slim CI / State Defer

### Kafka
[14-kafka/concepts.md](14-kafka/concepts.md)

- Topic
- Partition
- Offset
- Consumer Group
- Producer / Consumer
- Replication Factor
- ISR (In-Sync Replicas)
- Exactly-Once Semantics (EOS)
- Compaction (Kafka)
- Dead Letter Topic
- Schema Registry

### Airflow
[15-airflow/concepts.md](15-airflow/concepts.md)

- DAG
- Task / Operator
- Sensor
- Schedule / Timetable
- Execution Date / Data Interval
- XCom
- Pool / Slot
- Backfill
- Catchup
- SLA / Callback
- Dataset Scheduling

### Cost Optimization
[16-cost-optimization/concepts.md](16-cost-optimization/concepts.md)

- Scan Pruning / Partitioning
- Column Pruning
- File Size Tuning
- Spot / Preemptible Workers
- Autoscaling / Autosuspend
- Storage Tiering
- Result Caching
- Right-Sizing Warehouses
- Cost Observability
- Incremental vs Full Refresh

### Snowflake
[17-snowflake/concepts.md](17-snowflake/concepts.md)

- Virtual Warehouse
- Separation of Storage and Compute
- Micro-partitions
- Clustering Key
- Time Travel (Snowflake)
- Fail-safe
- Zero-Copy Clone
- Stage
- COPY INTO
- Snowpipe
- Stream (Snowflake)
- Task
- VARIANT
- Result Cache
- Query Profile
- Secure Data Sharing
- Roles & RBAC

## Contributing

Add a concept in the matching category file using this template:

```markdown
### Concept Name

**Definition:** One or two sentences.

**Why it matters:** Practical impact for DEs.

**Example:** Concrete SQL / Spark / architecture example.

**Remember:** 1–3 bullet takeaways.
```

---

*Keep entries short. Detail belongs in runbooks and deep-dive docs — this repo is the map.*
