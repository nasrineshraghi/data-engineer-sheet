# The most important 10

Ignore the 200+ topic list for now. If you only learn **these**, you can follow most DE conversations and debug common production issues.

| # | Concept | The one thing to remember |
|---|---------|---------------------------|
| 1 | **Grain** | Know what one row means before you join or aggregate |
| 2 | **Idempotency** | Safe to retry = no duplicate mess |
| 3 | **Shuffle** | Moving data across the network is usually the expensive part |
| 4 | **Partition Pruning** | Date (or key) filters should skip whole folders of data |
| 5 | **Predicate Pushdown** | Filter early so you read less |
| 6 | **Cardinality** | Distinct counts drive join and group-by cost |
| 7 | **Lazy Evaluation** | Spark builds a plan; an *action* runs it |
| 8 | **Job → Stage → Task** | How to read the Spark UI when something is slow |
| 9 | **At Least Once** | Failures often mean duplicates unless you dedupe |
| 10 | **Freshness** | Green pipeline ≠ data is recent enough |

## In the study app

- **Essentials** — learn these 10  
- **Prod** — when to use them in production ([PROD.md](PROD.md))  
- **Stories** — practice on incidents  

Readable UI: [docs/index.html?mode=essentials](docs/index.html?mode=essentials)
