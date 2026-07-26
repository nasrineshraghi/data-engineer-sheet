# Data Engineering Knowledge Base

A practical glossary of techniques, keywords, and concepts every data engineer should know — with short definitions and examples. Not deep dives; enough to recall, interview, and apply.

## How to use

- Browse by category below
- Full A–Z list: [INDEX.md](INDEX.md)
- Each concept has: **Definition** · **Why it matters** · **Example** · **Remember**
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

## Quick keyword index

`Cardinality` · `Grain` · `Selectivity` · `CBO` · `Explain Plan` · `Predicate Pushdown` · `Partition Pruning` · `DAG` · `Shuffle` · `AQE` · `Catalyst` · `Tungsten` · `Degenerate Dimension` · `Bridge Table` · `Delta Lake` · `Iceberg` · `Z-Ordering` · `CAP` · `Raft` · `Watermark` · `Exactly Once` · `Idempotency` · `DLQ` · `Data Skew` · `Broadcast Join` · `Data Lineage` · `IAM` · `Terraform`

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
