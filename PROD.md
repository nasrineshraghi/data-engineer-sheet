# Production playbook — when to use what

Good data engineers don’t memorize every topic. They **start from a symptom**, ask a few questions, then apply a small set of ideas.

## The habit (use this every time)

1. **What broke?** wrong numbers · slow · expensive · missing · duplicated · stale  
2. **Where in the path?** source → ingest → transform → serve → consume  
3. **Ask the 5 DE questions** (below)  
4. Open **Essentials** / this playbook — don’t browse all 200 topics  
5. Fix the **system** (retry safety, grain, prune, freshness), not only the ticket  

## The 5 questions that unlock most work

| If you’re unsure about… | Ask | Concept |
|-------------------------|-----|---------|
| Joins / KPIs / “numbers don’t match” | What does **one row** mean? | Grain |
| Retries / backfills / “ran twice” | Is this job **safe to rerun**? | Idempotency |
| Slow Spark / big shuffle | Are we **moving too much data**? | Shuffle · Pruning · Pushdown |
| Green DAG, wrong dashboard | Is the data **fresh enough**? | Freshness |
| Duplicates after failure | Did we get data **at least once** without dedupe? | At Least Once |

## Symptom → what to do

| You see this in prod | Do this | Concepts |
|----------------------|---------|----------|
| Revenue / KPI suddenly 2–3× after a join or backfill | Check grain of both sides; aggregate before summing; make writes overwrite/MERGE | Grain · Idempotency · Additive Facts |
| Job failed, rerun, now duplicates | Design for rerun: partition overwrite, MERGE on keys, deterministic IDs | Idempotency · At Least Once |
| One Spark task forever; others done | Look for hot keys in shuffle; skew / salt / AQE | Data Skew · Shuffle · Salting |
| Query scans years of data for one day | Filter on partition columns; push filters early | Partition Pruning · Predicate Pushdown |
| DAG green, execs say “yesterday’s numbers” | Alert on data arrival / max(event_time), not only task success | Freshness · Observability · SLA |
| Lake queries get slower every week | Too many tiny files; compact / target file size | Small Files · Compaction |
| Warehouse bill spiked | Stop `SELECT *`; prune columns & partitions; find heavy queries | Column Pruning · Cost Observability |
| Metrics change hours later | Use event time + watermarks; define late-data policy | Event Time · Watermarks · Late Data |
| Producer renamed a field; night jobs die | Contracts + schema enforce + registry compatibility | Data Contracts · Schema Registry |
| Historical report shows today’s attributes | Point-in-time: SCD2 + effective dates | SCD Type 2 · Surrogate Key |

## What “good in production” looks like

- **Declare grain** before building a fact or dashboard metric  
- **Every pipeline is rerunnable** (idempotent) by default  
- **Filter/prune early** — never “read everything then filter in Python”  
- **Measure freshness and volume**, not just job success  
- **Own the blast radius** — schema contracts, alerts, runbooks  
- **Debug with evidence** — Spark UI stages, bytes scanned, row counts in/out  

## In the study app

- **Prod** tab — this playbook, searchable  
- **Stories** — practice: pick which 3 concepts apply  
- **Essentials** — the 10 ideas behind almost every row above  

Readable UI: [docs/index.html?mode=prod](docs/index.html?mode=prod)
