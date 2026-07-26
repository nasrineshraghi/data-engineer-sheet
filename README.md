# Data Engineering Knowledge Base

A practical glossary of techniques, keywords, and concepts every data engineer should know — with short definitions and examples. Not deep dives; enough to recall, interview, and apply.

## How to use

- Browse keywords below → open the category file for **Definition · Why it matters · Example · Remember**
- A–Z lookup: [INDEX.md](INDEX.md)
- Search the repo (`Ctrl/Cmd + Shift + F`) by keyword

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

## All keywords

### Database & SQL Concepts
[concepts.md](01-database-sql/concepts.md)

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
[concepts.md](02-spark-internals/concepts.md)

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
[concepts.md](03-data-warehouse/concepts.md)

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
[concepts.md](04-data-lake-lakehouse/concepts.md)

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
[concepts.md](05-distributed-systems/concepts.md)

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
[concepts.md](06-streaming/concepts.md)

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
[concepts.md](07-pipeline-design/concepts.md)

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
[concepts.md](08-performance-tuning/concepts.md)

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
[concepts.md](09-data-quality-governance/concepts.md)

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
[concepts.md](10-cloud-storage/concepts.md)

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
[concepts.md](11-devops/concepts.md)

- Docker
- Kubernetes
- CI/CD
- GitOps
- Terraform
- Helm
- Infrastructure as Code (IaC)

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
