# Quick reference (summary table)

One-page cheat sheet: keyword · section · definition · example.

**Prefer the interactive HTML table:** https://nasrineshraghi.github.io/data-engineer-sheet/table.html

**257 concepts** · [Study app](https://nasrineshraghi.github.io/data-engineer-sheet/) · [Local HTML](docs/table.html)

| Keyword | Section | Definition | Example |
|---|---|---|---|
| **API Contract / OpenAPI** | APIs for Data Engineers | Documented agreement on paths, params, schemas, and errors (often OpenAPI/Swagger). | OpenAPI spec declares `Order.total_cents` as integer required. |
| **API Key** | APIs for Data Engineers | Static secret sent in a header or query param to identify the calling app. | Header `X-API-Key: sk_live_…` |
| **Authentication vs Authorization** | APIs for Data Engineers | Authentication = who you are; authorization = what you’re allowed to do. | Service authenticates with OAuth client credentials but isn’t authorized for `/admin/exports`. |
| **Change Data via API (Incremental Extract)** | APIs for Data Engineers | Pull only new/changed rows using cursors, `updated_at` filters, or event APIs. | `GET /objects?updated_after={watermark}&sort=updated_at` |
| **Endpoint / Resource** | APIs for Data Engineers | A URL path that represents a collection or item (`/customers`, `/customers/{id}`). | `/patients/{id}/labs` returns lab results for one patient. |
| **GraphQL (Basics)** | APIs for Data Engineers | Query language API where the client asks for exact fields in one request (vs many REST round-trips). | Query `{ order(id:"O-1") { id total items { sku qty } } }` |
| **gRPC / Protobuf (Basics)** | APIs for Data Engineers | Binary RPC framework using Protocol Buffers — common for internal low-latency services. | `GetOrder(OrderRequest) returns (Order)` over HTTP/2. |
| **Idempotency Key** | APIs for Data Engineers | Client-supplied key so retries of the same write are applied once. | Header `Idempotency-Key: load-2024-01-01-batch-7` on `POST /charges`. |
| **JSON / Payload Schema** | APIs for Data Engineers | Structured body format (usually JSON) with an agreed shape for fields and types. | `{ "order_id": "O-1", "total_cents": 1999, "currency": "USD" }` |
| **OAuth 2.0 / Bearer Token** | APIs for Data Engineers | Delegated auth where the client gets a short-lived access token (often refreshable). | Client credentials → `access_token` → `Authorization: Bearer <token>`. |
| **Pagination** | APIs for Data Engineers | Splitting large result sets across pages (offset/limit, cursor/token, or page numbers). | `GET /events?cursor=eyJpZCI6MTAwfQ&limit=500` |
| **Polling vs Event-Driven** | APIs for Data Engineers | Polling periodically GETs for changes; event-driven consumes webhooks/streams as events arrive. | Poll `updated_since` every 5 minutes vs webhook on `order.updated`. |
| **Rate Limiting** | APIs for Data Engineers | Server caps how many requests you can make per window (per key, IP, or tenant). | 100 req/min; response headers `X-RateLimit-Remaining: 0`, `Retry-After: 30`. |
| **Request / Response** | APIs for Data Engineers | Client sends a request (method, URL, headers, body); server returns a response (status, headers, body). | Request `Authorization: Bearer …` → Response `200` + JSON payload. |
| **REST API** | APIs for Data Engineers | HTTP API that manipulates resources with methods like GET, POST, PUT/PATCH, DELETE and status codes. | `GET /v1/orders?updated_since=2024-01-01` → JSON list of orders. |
| **SLA / Quotas** | APIs for Data Engineers | Provider promises (latency, uptime) and hard caps (rows/day, concurrent calls). | Free tier 10k calls/day; enterprise 100 concurrent connections. |
| **Status Codes** | APIs for Data Engineers | Numeric HTTP outcomes: 2xx OK, 3xx redirect, 4xx client error, 5xx server error. | `429 Too Many Requests` → back off; `401` → refresh auth, don’t hammer. |
| **Synchronous vs Asynchronous API** | APIs for Data Engineers | Sync returns the final result in one response; async accepts work and returns a job id to poll or webhook later. | `POST /exports` → `202` + `job_id` → poll `/exports/{job_id}` until `download_url`. |
| **Timeout / Retry / Backoff** | APIs for Data Engineers | Client gives up after N ms; retries failed calls with increasing delay (and jitter). | Timeout 30s; retry 5xx/429 with exponential backoff + jitter. |
| **Versioning** | APIs for Data Engineers | Evolving an API without breaking clients (`/v1`, `/v2`, or header versions). | `/v1/orders` keeps old shape while `/v2/orders` renames fields. |
| **Webhook** | APIs for Data Engineers | Server pushes an HTTP callback to your URL when an event happens (vs you polling). | Stripe sends `POST /hooks/stripe` with `invoice.paid` payload. |
| **Backfill** | Airflow | Intentionally run a DAG for past logical dates. | Backfill last 30 days after fixing a currency join. |
| **Catchup** | Airflow | Airflow auto-schedules missed past runs between start_date and now. | Deploy DAG with old `start_date` and `catchup=True` → hundreds of runs. |
| **DAG** | Airflow | Directed Acyclic Graph of tasks with dependencies — Airflow’s unit of workflow. | `extract >> transform >> test >> publish`. |
| **Dataset Scheduling** | Airflow | Trigger downstream DAGs when upstream datasets update (Airflow 2.4+). | `publish_orders` updates dataset → `marts_orders` DAG runs. |
| **Execution Date / Data Interval** | Airflow | Logical time range a run represents (Airflow 2: data interval), not “when it ran”. | Daily DAG for `2024-01-01` processes that day’s partition even if it runs on Jan 2. |
| **Pool / Slot** | Airflow | Concurrency limits for tasks (pools) and worker parallelism (slots). | Pool `snowflake_heavy` with 4 slots for large transforms. |
| **Schedule / Timetable** | Airflow | When DAG runs are created (cron, timetable, dataset-triggered). | `@daily` with `data_interval` ending at midnight UTC. |
| **Sensor** | Airflow | Task that waits for a condition (file arrives, partition ready, external DAG success). | `S3KeySensor` waits for `dt={{ ds }}/_SUCCESS`. |
| **SLA / Callback** | Airflow | Time expectations and hooks on success/failure/retry (email, Slack, PagerDuty). | SLA miss callback posts to #data-alerts. |
| **Task / Operator** | Airflow | A unit of work in a DAG; operators are task templates (Bash, Python, SparkSubmit, etc.). | `BashOperator` runs `dbt run --select fct_orders`. |
| **XCom** | Airflow | Cross-communication — small metadata passed between tasks. | Task A pushes `row_count`; Task B branches if zero. |
| **Change Data Capture (CDC)** | CDC & SCD | Continuously capture inserts/updates/deletes from a source system (often via logs) instead of full reloads. | Debezium reads Postgres WAL → Kafka topics → Spark/Flink applies to Delta. |
| **Effective Dating** | CDC & SCD | `effective_start` / `effective_end` (or `is_current`) defines when a dim version is valid. | Join fact `order_date` to dim where `start <= order_date < end`. |
| **Late-Arriving Dimension** | CDC & SCD | Fact arrives before its dimension row exists. | Order for new customer lands before `dim_customer` CDC catches up. |
| **Late-Arriving Fact** | CDC & SCD | Fact event arrives after its business date / reporting window closed. | Store posts yesterday’s sale two days late → merge into prior partition. |
| **Log-Based CDC** | CDC & SCD | Read the database transaction log (WAL/binlog/redo) to emit change events. | MySQL binlog → Debezium → `orders` topic with before/after images. |
| **Natural Key** | CDC & SCD | Business identifier from the source system (`customer_id`, `sku`). | Same person has different natural keys in CRM and billing → MDM/matching. |
| **Query-Based CDC** | CDC & SCD | Poll source tables using timestamps or version columns to find changes. | `SELECT * FROM orders WHERE updated_at > :last_watermark`. |
| **SCD Type 1** | CDC & SCD | Overwrite attributes in place; no history kept. | Customer address updated → old address gone forever in the dim. |
| **SCD Type 2** | CDC & SCD | Keep history by inserting a new dimension row with effective dates / current flag. | Segment changes → close old row (`end_date`), insert new row with new surrogate key. |
| **SCD Type 3** | CDC & SCD | Store limited history in extra columns (e.g., current + previous). | `region` and `prior_region` columns on `dim_customer`. |
| **Soft Delete vs Hard Delete** | CDC & SCD | Soft delete marks a row inactive (`is_deleted=true`); hard delete removes the row. | Source hard-delete → CDC tombstone → target marks deleted or removes row. |
| **Surrogate Key** | CDC & SCD | Warehouse-generated key (usually integer/UUID) independent of source natural keys. | `customer_sk` changes on type-2 version; `customer_id` natural key stays. |
| **Abnormal / Critical Flags** | Clinical Data — Meds & Labs | Lab- or EHR-assigned markers that a result is abnormal, high/low, or critically out of range. | Flag `HH` (critically high) on potassium triggers rapid notification workflows. |
| **Active Medication List** | Clinical Data — Meds & Labs | Medications believed current for the patient (home meds + active inpatient orders), not the full history. | Active: metformin, lisinopril. Historical: finished amoxicillin course last month. |
| **Clinical Event Time vs System Time** | Clinical Data — Meds & Labs | Event time = when it happened clinically (collected, administered); system time = when the EHR recorded/updated the row. | Dose given at 08:00, documented at 11:30 — administration event time is 08:00. |
| **Encounter / Visit Context** | Clinical Data — Meds & Labs | The visit (inpatient encounter, ED visit, outpatient appointment) tying meds and labs to a care episode. | Join `lab_result.encounter_id` to inpatient stay for length-of-stay cohorts. |
| **Lab Order vs Lab Result** | Clinical Data — Meds & Labs | Order = request for a test; result = the reported value(s) for analyte(s). | Order CBC → results for WBC, RBC, hemoglobin, platelets (multiple result rows). |
| **LOINC** | Clinical Data — Meds & Labs | Universal codes for lab observations and clinical measures (what was measured). | Serum creatinine assays from Lab A and Lab B → same LOINC `2160-0`. |
| **Medication Administration (MAR)** | Clinical Data — Meds & Labs | Record that a dose was given (or intentionally not given) to the patient — Medication Administration Record. | Nurse documents ceftriaxone 1 g IV given at 2024-01-02 08:12. |
| **Medication Dispense** | Clinical Data — Meds & Labs | Pharmacy fills/gives out a supply of medication (quantity, NDC, days supply). | One order for 30 tablets → one dispense of 30; a refill is another dispense. |
| **Medication Order** | Clinical Data — Meds & Labs | A clinician’s request for a drug (what should be given) — often before dispense or administration. | Order: “Amoxicillin 500 mg PO TID × 7 days.” May never be dispensed if patient leaves AMA. |
| **NDC (National Drug Code)** | Clinical Data — Meds & Labs | FDA product identifier for how a drug is packaged (labeler + product + package). | Two manufacturers’ bottles of sertraline 50 mg → different NDCs, same RxNorm ingredient/strength. |
| **Order → Dispense → Administration Chain** | Clinical Data — Meds & Labs | The typical inpatient med pipeline: ordered → dispensed → administered (ambulatory often stops at dispense). | “Antibiotics within 1h of sepsis” needs **administration** time, not order time. |
| **Panel vs Analyte** | Clinical Data — Meds & Labs | Panel = ordered battery (CMP, CBC); analyte = individual measurable component. | CMP order → separate rows for sodium, potassium, creatinine, glucose, … |
| **PHI in Meds & Labs** | Clinical Data — Meds & Labs | Medication and lab rows are Protected Health Information when identifiable (patient id + clinical facts). | A table of patient_id + HIV viral load is highly sensitive PHI. |
| **Quantitative vs Qualitative Results** | Clinical Data — Meds & Labs | Quantitative = numeric value; qualitative = categorical (Positive/Negative, Detected, …). | Troponin `0.04 ng/mL` (quant) vs COVID PCR `Detected` (qual). |
| **Reference Range** | Clinical Data — Meds & Labs | Lab’s expected normal low/high (or qualitative normal set) for a result, often age/sex/method specific. | K+ result `5.8` with range `3.5–5.1` → high; same number might be normal for a different assay. |
| **RxNorm** | Clinical Data — Meds & Labs | NIH normalized naming system for clinical drugs (ingredients, strength, dose form). | Map “Amox 500mg Cap” and “amoxicillin 500 mg capsule” → same RxNorm CUI/SCD. |
| **Sig / Dose / Route / Frequency** | Clinical Data — Meds & Labs | Structured (or semi-structured) instructions: how much (dose), how given (route), how often (frequency), plus free-text sig. | Dose `500`, unit `mg`, route `PO`, frequency `TID` vs sig `"one capsule by mouth three times daily"`. |
| **Specimen & Collection Time** | Clinical Data — Meds & Labs | What was collected (blood, urine, …) and **when** it was collected — distinct from result-reported time. | Blood drawn 06:00, resulted 09:40 — sepsis bundle timing uses 06:00. |
| **Units of Measure (UCUM)** | Clinical Data — Meds & Labs | Standard representation of units (e.g. `mg/dL`, `mmol/L`) so values are comparable. | Glucose `100 mg/dL` ≈ `5.6 mmol/L` — not the same number. |
| **Block Storage** | Cloud & Storage | Disk volumes attached to VMs (like SAN/local disks). | EBS/Azure Disks for Postgres data directory. |
| **Encryption at Rest** | Cloud & Storage | Data encrypted on disk/storage media. | S3 default encryption; encrypted EBS volumes. |
| **Encryption in Transit** | Cloud & Storage | Data encrypted on the network (TLS/HTTPS). | TLS to warehouses, HTTPS to APIs, SSL to Postgres. |
| **IAM** | Cloud & Storage | Identity and Access Management — who can do what on which resources. | Role for Spark job: read `s3://lake/bronze/*`, write `s3://lake/silver/*` only. |
| **KMS** | Cloud & Storage | Key Management Service — create and control encryption keys. | S3 SSE-KMS; revoke key usage to lock data access. |
| **Lifecycle Policies** | Cloud & Storage | Automatic transition/expire of objects by age/prefix (hot → cool → archive → delete). | Raw logs to Glacier after 90 days; delete after 365. |
| **Object Storage** | Cloud & Storage | Store immutable objects (files) addressed by key in buckets; virtually infinite scale. | S3, ADLS Gen2, GCS holding parquet/Delta tables. |
| **Private Endpoints** | Cloud & Storage | Private network interfaces to cloud services without public internet. | S3/GCP Private Service Connect / Azure Private Link to storage and warehouses. |
| **Secrets Management** | Cloud & Storage | Store/rotate credentials and API keys outside code. | AWS Secrets Manager / Azure Key Vault / HashiCorp Vault for DB passwords. |
| **VPC** | Cloud & Storage | Virtual Private Cloud — isolated network for your cloud resources. | Data platform subnets with no public IPs; NAT for egress. |
| **Autoscaling / Autosuspend** | Cost Optimization | Scale clusters/warehouses to zero or down when idle; up under load. | Snowflake auto-suspend 60s; Spark dynamic allocation. |
| **Column Pruning** | Cost Optimization | Read only selected columns from columnar formats (Parquet/ORC). | `SELECT user_id, amount FROM events` reads two columns, not fifty. |
| **Cost Observability** | Cost Optimization | Attribute spend to teams, jobs, tables, and queries. | Chargeback tags on Spark jobs; query cost views in Snowflake. |
| **File Size Tuning** | Cost Optimization | Target healthy output file sizes (often ~128–512MB) via coalesce/optimize. | `coalesce(200)` before write; schedule compaction. |
| **Incremental vs Full Refresh** | Cost Optimization | Prefer incremental processing; full refresh only when necessary. | Daily MERGE of changed keys vs rebuild entire history. |
| **Result Caching** | Cost Optimization | Reuse recent query results when identical SQL hits warm cache. | BI extracts cached in warehouse result cache for minutes. |
| **Right-Sizing Warehouses** | Cost Optimization | Match warehouse/cluster size to workload shape, not peak folklore. | Drop from 2XL to L after partitioning fixed scan volume. |
| **Scan Pruning / Partitioning** | Cost Optimization | Design tables so queries read only needed files/partitions. | Partition by `dt`; filter `WHERE dt = CURRENT_DATE` before joining. |
| **Spot / Preemptible Workers** | Cost Optimization | Use discounted interruptible VMs for fault-tolerant batch compute. | Spark executors on spot; driver on on-demand. |
| **Storage Tiering** | Cost Optimization | Move cold data to cheaper classes via lifecycle policies. | Raw logs → infrequent access after 30d → archive after 180d. |
| **ACID Tables** | Data Lake & Lakehouse | Atomicity, Consistency, Isolation, Durability for table operations on the lake. | A failed job leaves no half-visible partition after transactional commit. |
| **Apache Hudi** | Data Lake & Lakehouse | Open table format focused on incremental processing, upserts, and streaming ingestion. | Upsert CDC into a Hudi MOR table; readers see compacted view. |
| **Apache Iceberg** | Data Lake & Lakehouse | Open table format with snapshot metadata, hidden partitioning, strong engine interoperability. | Partition evolution without rewriting all data paths visible to users. |
| **Compaction** | Data Lake & Lakehouse | Rewrite many small files into larger optimized files. | Iceberg rewrite / Hudi compact / Delta OPTIMIZE. |
| **Data Lake** | Data Lake & Lakehouse | Central storage of raw and processed data in files (often object storage), schema-on-read. | S3/ADLS/GCS buckets with landing, bronze, silver zones as folders. |
| **Data Lakehouse** | Data Lake & Lakehouse | Lake storage + warehouse capabilities: ACID tables, governance, BI-friendly SQL. | Delta/Iceberg tables on S3 queried by Spark, Trino, and BI tools. |
| **Delta Lake** | Data Lake & Lakehouse | Open table format (Databricks-origin) with transaction log (`_delta_log`) for ACID on files. | `MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE ...` |
| **Optimize** | Data Lake & Lakehouse | Maintenance command to compact/layout data for faster reads (Delta `OPTIMIZE`). | `OPTIMIZE sales ZORDER BY (customer_id, event_date);` |
| **Schema Enforcement** | Data Lake & Lakehouse | Reject writes that don't match the table schema (or strict evolution rules). | Write with extra unexpected type fails instead of silently creating junk files. |
| **Schema Evolution** | Data Lake & Lakehouse | Safely change table schema (add/rename/drop columns) without full reload when supported. | Adding `discount_code` column to a Delta/Iceberg table. |
| **Time Travel** | Data Lake & Lakehouse | Query table as of a past version/timestamp via snapshots/logs. | ```sql SELECT * FROM orders VERSION AS OF 120; -- or TIMESTAMP AS OF '2024-06-01' ``` |
| **Vacuum** | Data Lake & Lakehouse | Delete obsolete data files no longer referenced by the table (past retention). | `VACUUM table_name RETAIN 168 HOURS;` (Delta). |
| **Z-Ordering** | Data Lake & Lakehouse | Multi-dimensional clustering of data files so related values co-locate (minmax skipping improves). | Z-Order by `user_id` so point lookups skip most files. |
| **Accuracy** | Data Quality & Governance | Data correctly represents real-world values. | Currency conversion rates match source system within tolerance. |
| **Completeness** | Data Quality & Governance | Required data is present (rows and fields). | All 24 hourly partitions arrived; `customer_id` null rate < 0.1%. |
| **Consistency** | Data Quality & Governance | Same facts agree across systems/tables within defined rules. | Sum of order lines equals order header total; warehouse matches finance extract. |
| **Data Catalog** | Data Quality & Governance | Searchable inventory of datasets with metadata, ownership, and often lineage. | DataHub, Collibra, Unity Catalog, Glue Data Catalog, OpenMetadata. |
| **Data Governance** | Data Quality & Governance | Policies, roles, and controls for data quality, security, privacy, and usage. | PII classification, access reviews, approved metric definitions. |
| **Data Lineage** | Data Quality & Governance | Trace where data came from and where it flows (table/column/job level). | `raw.orders` → `stg_orders` → `fct_orders` → dashboard KPI. |
| **Data Profiling** | Data Quality & Governance | Statistical survey of a dataset: nulls, distincts, distributions, patterns. | 12% null `email`; `amount` min/max/p99; top values of `status`. |
| **Data Stewardship** | Data Quality & Governance | Human ownership of domain data quality and definitions. | Finance steward owns `revenue` definition and approves changes. |
| **Data Validation** | Data Quality & Governance | Automated checks that data meets rules (schema, ranges, uniqueness, referential). | Great Expectations / dbt tests: `order_id` unique, `amount >= 0`, FK to customers. |
| **Freshness** | Data Quality & Governance | How up-to-date the data is vs expectation (SLA/SLO). | "Orders table max `updated_at` < 1 hour ago". |
| **Master Data Management (MDM)** | Data Quality & Governance | Processes/systems to create a single trusted master for core entities (customer, product). | Merge CRM + billing customers into golden `customer_id` with survivorship rules. |
| **Metadata** | Data Quality & Governance | Data about data: schema, owners, freshness, partitions, descriptions. | Table description, column glossary, last update time, PII tags. |
| **Observability** | Data Quality & Governance | Ability to understand pipeline health via metrics, logs, traces, and data checks. | Freshness, row-count anomalies, schema drift alerts, job duration SLOs. |
| **Accumulating Snapshot** | Data Warehouse Concepts | One row per process instance; columns updated as milestones complete (pipeline pipeline). | Order fulfillment: `ordered_at`, `packed_at`, `shipped_at`, `delivered_at` on one row, updated in place. |
| **Additive Facts** | Data Warehouse Concepts | Measures that can be summed across any dimension. | `sales_amount`, `quantity_sold` — sum by day, store, product all valid. |
| **Bridge Table** | Data Warehouse Concepts | Helper table resolving many-to-many between fact and dimension (or between dims). | Order with multiple sales reps → `bridge_order_rep` with allocation weights. |
| **Conformed Dimension** | Data Warehouse Concepts | Shared dimension with consistent keys and attributes across facts/marts. | Same `customer_key` and customer attributes in sales and support marts. |
| **Degenerate Dimension** | Data Warehouse Concepts | Dimension-like identifier stored in the fact table with no separate dimension table. | `order_id`, `invoice_number` living on the fact row. |
| **Factless Fact Table** | Data Warehouse Concepts | Fact table with keys only (no numeric measures) — records events or coverage. | Student attendance: `student_key`, `class_key`, `date_key` — count rows = attendance events. |
| **Grain** | Data Warehouse Concepts | Exact meaning of one fact row (business level of detail). | "One row per order line per day" vs "one row per order". |
| **Granularity** | Data Warehouse Concepts | Same idea as grain — how fine or coarse the data is. Often used interchangeably with grain in DW. | Daily grain vs monthly rollup tables. |
| **Junk Dimension** | Data Warehouse Concepts | Single dimension table combining low-cardinality flags/indicators. | `is_gift`, `payment_type`, `channel` packed into `dim_order_flags`. |
| **Mini Dimension** | Data Warehouse Concepts | Split frequently changing attributes into a smaller dimension to limit type-2 explosion on the main dim. | `dim_customer` stable attrs + `dim_customer_profile` for segment/score that changes monthly. |
| **Non-Additive Facts** | Data Warehouse Concepts | Cannot be summed meaningfully; ratios, percentages, temperatures. | `profit_margin` — store `profit` and `revenue`, compute margin at query time. |
| **Periodic Snapshot** | Data Warehouse Concepts | New fact rows taken at regular intervals for all entities (day/week/month). | End-of-day account balance for every account every day. |
| **Role-Playing Dimension** | Data Warehouse Concepts | Same dimension reused for multiple roles via different foreign keys. | `order_date_key`, `ship_date_key` both point to `dim_date`. |
| **Semi-Additive Facts** | Data Warehouse Concepts | Summable across some dimensions, not others (often not across time). | Account balance — sum across customers OK; sum across days wrong (use last/average). |
| **Snapshot Fact** | Data Warehouse Concepts | Fact capturing state at a point in time (generic term; often periodic). | Daily inventory on-hand per SKU per warehouse. |
| **B-Tree Index** | Database & SQL Concepts | Balanced tree index supporting equality and range lookups; default in most RDBMS. | B-tree on `email` → fast `WHERE email = 'a@b.com'`. |
| **Bitmap Index** | Database & SQL Concepts | Index storing bitmaps per distinct value; good for low-cardinality columns and AND/OR of predicates. | Bitmap on `gender`, `region`, `status` for warehouse filters. |
| **Cardinality** | Database & SQL Concepts | Number of distinct values in a column (or relation size: number of rows). | `country` has ~200 distinct values (low cardinality). `user_id` may have millions (high cardinality). |
| **Clustered vs Non-Clustered Index** | Database & SQL Concepts | - **Clustered:** table rows stored in index key order (often primary key); typically one per table. - **Non-clustered:** separate structure pointing to rows;… | Clustered on `order_date` makes date-range queries fast; random UUIDs as clustered keys can fragment inserts. |
| **Composite Index** | Database & SQL Concepts | Index on multiple columns in a defined order. | Index `(customer_id, order_date)` helps `WHERE customer_id = ?` and `WHERE customer_id = ? AND order_date > ?`, not `WHERE order_date > ?` alone (usually). |
| **Cost-Based Optimizer (CBO)** | Database & SQL Concepts | Chooses execution plan by estimating cost using table/column statistics. | With stats, CBO picks broadcast hash join for a small dimension; without stats, may shuffle both sides. |
| **Covering Index** | Database & SQL Concepts | Index that contains all columns a query needs, so the table heap/base isn't touched. | Query selects `id, email` with index on `(id) INCLUDE (email)` → covering. |
| **Data Distribution** | Database & SQL Concepts | How values are spread across a column (uniform, skewed, sparse). | 80% of orders from one country → that partition/key dominates shuffle. |
| **Execution Plan** | Database & SQL Concepts | The concrete operators the engine will run (scans, joins, aggregates, sorts). | Plan shows `SortMergeJoin` + large `Exchange` (shuffle) → expensive. |
| **Explain Plan** | Database & SQL Concepts | Command/API that prints the logical and/or physical plan without always running the full query. | ```sql EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date = '2024-01-01'; -- Spark: df.explain(True) or EXPLAIN EXTENDED / COST ``` |
| **Granularity (Grain)** | Database & SQL Concepts | The level of detail one row represents (what one row means). | Orders table grain = one row per `order_id`. Order-items grain = one row per `order_id + product_id`. |
| **Histograms** | Database & SQL Concepts | Statistics summarizing value frequency distribution in a column. | Optimizer sees `status='cancelled'` is 2% of rows via histogram, not assuming uniform 25%. |
| **Partition Pruning** | Database & SQL Concepts | Skip reading partitions that cannot match the query filter. | Table partitioned by `dt`; `WHERE dt='2024-06-01'` reads only that partition. |
| **Predicate Pushdown** | Database & SQL Concepts | Move filters as close as possible to the data source so less data is read/shuffled. | `spark.read.parquet(...).filter("year=2024")` pushes year filter into file/footer reading when partitioned. |
| **Rule-Based Optimizer (RBO)** | Database & SQL Concepts | Rewrites queries using fixed heuristic rules (e.g., push filters early), not cost estimates. | Always push `WHERE` before `JOIN` regardless of table size. |
| **Seek vs Scan** | Database & SQL Concepts | - **Seek:** jump to a specific key/range in the index. - **Scan:** read a contiguous slice (or all) of index/table. | `WHERE id = 10` → seek. `WHERE id BETWEEN 1 AND 1000000` → range scan. |
| **Selectivity** | Database & SQL Concepts | Fraction of rows a predicate returns. High selectivity = few rows (selective filter). | `WHERE user_id = 42` is highly selective. `WHERE status = 'active'` on 90% active rows is not. |
| **Statistics** | Database & SQL Concepts | Metadata about tables/columns: row counts, NDV, min/max, histograms, size. | ```sql ANALYZE TABLE orders COMPUTE STATISTICS FOR COLUMNS customer_id, amount; ``` |
| **Table Scan vs Index Scan** | Database & SQL Concepts | - **Table (full) scan:** read all rows/pages. - **Index scan:** walk an index (may still touch many rows). | Selecting 2% of rows by PK → index. Selecting 70% → full scan often better. |
| **CI/CD** | DevOps for Data | Continuous Integration / Continuous Delivery — automate test and deploy of code/config. | PR runs unit tests + SQL lint → merge deploys DAG to Airflow. |
| **Docker** | DevOps for Data | Package app + dependencies into portable container images. | Image with `spark-submit` entrypoint and pinned library versions. |
| **GitOps** | DevOps for Data | Desired system state lives in Git; controllers sync cluster to match. | Argo CD applies Helm charts from `infra` repo on merge to main. |
| **Helm** | DevOps for Data | Package manager for Kubernetes — charts template K8s manifests. | `helm upgrade --install airflow bitnami/airflow -f values.yaml`. |
| **Infrastructure as Code (IaC)** | DevOps for Data | Define and version infrastructure in code (Terraform, CloudFormation, Pulumi, Bicep). | Dev/stage/prod lakes created from the same modules with different variables. |
| **Kubernetes** | DevOps for Data | Orchestrates containers: scheduling, scaling, restarts, service discovery. | SparkApplication CRD submits driver/executors as pods. |
| **Terraform** | DevOps for Data | Declarative Infrastructure as Code tool (HCL) for cloud resources. | Terraform creates S3 lake buckets, Glue catalog DB, IAM roles. |
| **BASE** | Distributed Systems | Basically Available, Soft state, Eventually consistent — alternative mindset to strict ACID across distributed services. | Shopping cart eventually syncs across regions; brief stale reads OK. |
| **CAP Theorem** | Distributed Systems | In a network partition, a system can provide Consistency or Availability, not both (Partition tolerance assumed in distributed DBs). | During partition, CP system rejects writes; AP system accepts writes that may conflict. |
| **Consensus** | Distributed Systems | Nodes agree on a value/order of operations despite failures. | Agreeing on the next committed Kafka controller epoch or Raft log entry. |
| **Eventual Consistency** | Distributed Systems | If no new updates, all replicas converge to the same value eventually. | Read-after-write may fail briefly across regions; later reads agree. |
| **Fault Tolerance** | Distributed Systems | System continues correctly despite component failures. | Spark recomputes lost partitions; Kafka replicates partitions. |
| **High Availability (HA)** | Distributed Systems | Minimize downtime via redundancy and fast failover. | Multi-AZ brokers; standby scheduler; health checks + auto restart. |
| **Horizontal Scaling** | Distributed Systems | Add more nodes to increase capacity. | Add Spark executors or Kafka brokers. |
| **Leader Election** | Distributed Systems | Cluster chooses a primary coordinator for writes or decisions. | ZooKeeper/etcd/Raft elect Kafka controller or DB primary. |
| **Paxos** | Distributed Systems | Classic family of consensus protocols (Multi-Paxos, etc.). | Google Chubby historically influenced by Paxos. |
| **Raft** | Distributed Systems | Consensus algorithm emphasizing understandability: leader, log replication, terms. | etcd stores K8s state via Raft. |
| **Replication** | Distributed Systems | Keep multiple copies of data for durability and/or read scale. | Kafka topic RF=3; Postgres primary + replicas; S3 cross-region copy. |
| **Strong Consistency** | Distributed Systems | After a write commits, all subsequent reads see it (linearizability / similar guarantees vary by system). | Financial ledger balance must be strongly consistent. |
| **Vertical Scaling** | Distributed Systems | Give one machine more CPU/RAM/disk. | Upsize a warehouse warehouse node or driver machine. |
| **Compaction (Kafka)** | Kafka | Log compaction keeps the latest value per key; older keys garbage-collected. | `customer_profile` compacted topic always has latest profile per `customer_id`. |
| **Consumer Group** | Kafka | Set of consumers sharing work on a topic; each partition goes to one member. | 6 partitions, 3 consumers in group `billing` → ~2 partitions each. |
| **Dead Letter Topic** | Kafka | Topic receiving poison / failed records after retries. | Deserialization failures → `orders.dlq` with headers explaining error. |
| **Exactly-Once Semantics (EOS)** | Kafka | Kafka transactions / idempotent produce so a read-process-write cycle doesn’t dup effects (within Kafka). | Kafka Streams transactional write to output topic. |
| **ISR (In-Sync Replicas)** | Kafka | Replicas fully caught up with the leader; eligible for failover. | Leader waits for ISR acks before acknowledging the produce. |
| **Offset** | Kafka | Position of a consumer within a partition log. | Commit offset 1050 after processing; restart resumes at 1051 (depending on config). |
| **Partition** | Kafka | Ordered, append-only log slice of a topic; unit of parallelism. | Key by `customer_id` so one customer’s events stay ordered in one partition. |
| **Producer / Consumer** | Kafka | Writer vs reader clients of Kafka topics. | Producer `acks=all`; consumer `enable.auto.commit=false` with manual commits. |
| **Replication Factor** | Kafka | How many broker copies of each partition exist. | RF=3, min ISR=2 for production topics. |
| **Schema Registry** | Kafka | Service storing Avro/Protobuf/JSON schemas for topic payloads with compatibility rules. | BACKWARD compatibility for `orders-value` subject. |
| **Topic** | Kafka | Named stream of records; publishers write, consumers read. | Producers write to `payments.completed`; three services consume independently. |
| **Broadcast Join** | Performance Tuning | Replicate the small side to all executors; join locally (map-side). | Fact × small dimension (`broadcast(dim)`). |
| **Bucket Join** | Performance Tuning | Tables pre-bucketed (and often sorted) on the same key so joins avoid full shuffle. | Both tables bucketed by `user_id` into 200 buckets → bucket join. |
| **Caching** | Performance Tuning | Keep a dataset in memory/disk across actions to avoid recomputation. | `df.cache()` before multiple joins/aggregations on same base. |
| **Data Skew** | Performance Tuning | Uneven key/partition sizes so a few tasks do most of the work. | `null` or popular `country_code` holds 50% of join keys. |
| **Hash Join** | Performance Tuning | Build hash table on one side, probe with the other (in-memory or spilled). | Broadcast hash join = hash join with replicated build side. |
| **Parallelism** | Performance Tuning | Degree of concurrent tasks (related to partitions and cores). | `repartition(200)` to use ~200 cores effectively for a stage. |
| **Partition Sizing** | Performance Tuning | Choosing number/size of partitions (and output files) for balanced work. | Target ~128–256 MB per partition file for many lake workloads (rule of thumb, not law). |
| **Persistence Levels** | Performance Tuning | Storage level for cached data: memory only, memory+disk, disk only, serialized, replicated. | `MEMORY_AND_DISK` safer than `MEMORY_ONLY` for large frames. |
| **Salting** | Performance Tuning | Add a random salt to hot keys to spread them across partitions, then remove/aggregate. | Hot `customer_id` → `customer_id + salt_0..N` on both sides for join, then drop salt. |
| **Shuffle Join** | Performance Tuning | Generic term for joins that redistribute both sides by join key (often sort-merge or shuffle-hash). | Large `orders` ⋈ large `payments` on `order_id`. |
| **Small File Problem** | Performance Tuning | Too many tiny files → heavy listing, task overhead, slow queries. | 100k files of 1 MB instead of 400 files of 256 MB. |
| **Sort Merge Join** | Performance Tuning | Shuffle both sides by key, sort, then merge — Spark's common large-large join. | Default for two big DataFrames when broadcast isn't chosen. |
| **Backoff Strategy** | Pipeline Design | Increase wait between retries (often exponential + jitter). | Wait 1s, 2s, 4s, 8s with random jitter. |
| **Checkpointing** | Pipeline Design | Persist progress (offsets/state) so recovery resumes cleanly. | Spark Structured Streaming checkpoint location stores offsets + state. |
| **Circuit Breaker** | Pipeline Design | Stop calling a failing dependency temporarily after error threshold; probe later. | After 50 warehouse connection failures, open circuit for 60s, then half-open trial. |
| **Data Contracts** | Pipeline Design | Explicit agreement on schema, semantics, SLAs, and ownership between producers and consumers. | Producer guarantees `orders.v2` fields + daily freshness < 2h; CI validates schema. |
| **Dead Letter Queue (DLQ)** | Pipeline Design | Side channel for records that fail processing after retries. | Malformed JSON → DLQ topic/table with error reason; alert and fix. |
| **Idempotency** | Pipeline Design | Running the same operation multiple times yields the same result as running once. | Upsert by primary key; overwrite partition `dt=2024-01-01` instead of append-only blindly. |
| **Metadata-Driven Pipelines** | Pipeline Design | Behavior configured by metadata (tables, mappings, rules) rather than hard-coded per table jobs. | Config table lists source, target, PK, SCD type → one generic loader. |
| **Pipeline Orchestration** | Pipeline Design | Schedule, dependency management, retries, and observability of multi-step data jobs. | Airflow/Dagster/Prefect/Azure DF: extract → transform → test → publish. |
| **Retry Strategy** | Pipeline Design | Policy for re-attempting failed work (how many, when, which errors). | Retry S3/API 429/5xx up to 5 times; fail fast on 400 auth errors. |
| **Clustering Key** | Snowflake | Optional key(s) that guide how related rows are co-located across micro-partitions. | `ALTER TABLE events CLUSTER BY (event_date, customer_id);` |
| **COPY INTO** | Snowflake | Bulk load (or unload) command between stages and tables. | `COPY INTO raw.events FROM @stage/dt=2024-01-01/ PATTERN='.*[.]parquet';` |
| **Fail-safe** | Snowflake | 7-day Snowflake-managed recovery window after Time Travel ends (not for user queries). | Accidental drop discovered after Time Travel expired → Fail-safe recovery request. |
| **Micro-partitions** | Snowflake | Immutable ~16MB columnar storage units Snowflake manages automatically (with metadata min/max). | Filter `WHERE order_date = '2024-01-01'` skips micro-partitions outside that range. |
| **Query Profile** | Snowflake | Visual breakdown of a query’s operators, pruning, spillage, and time. | Profile shows TableScan reading most micro-partitions → add filter/clustering. |
| **Result Cache** | Snowflake | Cached query results reused when identical SQL hits unchanged data (24h, no warehouse needed). | Same BI extract refreshed by many users within minutes → cache hits. |
| **Roles & RBAC** | Snowflake | Access control via roles granted privileges on warehouses, databases, schemas, tables. | `GRANT USAGE ON WAREHOUSE bi_wh TO ROLE analyst; GRANT SELECT ON ALL TABLES IN SCHEMA marts TO ROLE analyst;` |
| **Secure Data Sharing** | Snowflake | Share live database objects with other Snowflake accounts without copying data. | Share `analytics.sales_mart` to a partner reader account. |
| **Separation of Storage and Compute** | Snowflake | Data lives in cloud storage; warehouses attach compute on demand. | Finance XL warehouse and Data Eng M warehouse both query `PROD.ANALYTICS` tables. |
| **Snowpipe** | Snowflake | Continuous/auto-ingest service that loads files from stages as they arrive (often via event notifications). | S3 event → Snowpipe → `raw.events` within minutes. |
| **Stage** | Snowflake | Named location for files (internal Snowflake stage or external S3/Azure/GCS) used by COPY/Snowpipe. | `COPY INTO target FROM @my_ext_stage/path/ FILE_FORMAT = (TYPE=PARQUET);` |
| **Stream (Snowflake)** | Snowflake | Change-tracking object on a table (CDC-style inserts/updates/deletes) for incremental processing. | `CREATE STREAM orders_stream ON TABLE orders; SELECT * FROM orders_stream WHERE METADATA$ACTION = 'INSERT';` |
| **Task** | Snowflake | Scheduled SQL/procedure job in Snowflake (can chain into task trees). | Hourly task merges stream changes into a curated table. |
| **Time Travel (Snowflake)** | Snowflake | Query or restore table data as of a past timestamp/statement within retention (typically 1–90 days). | `SELECT * FROM orders AT (TIMESTAMP => '2024-06-01 12:00:00');` |
| **VARIANT** | Snowflake | Semi-structured column type for JSON/Avro/XML-like nested data. | `SELECT payload:user.id::STRING AS user_id FROM raw_events;` |
| **Virtual Warehouse** | Snowflake | Dedicated compute cluster (size XS–4XL+) that runs queries and DML; billed while running. | `CREATE WAREHOUSE etl_wh WITH WAREHOUSE_SIZE = 'M' AUTO_SUSPEND = 60;` |
| **Zero-Copy Clone** | Snowflake | Instant copy of database/schema/table that shares storage until data diverges. | `CREATE TABLE orders_dev CLONE prod.analytics.orders;` |
| **Accumulators** | Spark Internals | Write-only aggregate variables (counters) updated by executors, read on driver. | Count malformed records while mapping. |
| **Adaptive Query Execution (AQE)** | Spark Internals | Spark SQL re-optimizes the plan at runtime using size stats after shuffles (Spark 3+). | AQE converts sort-merge to broadcast when post-shuffle side is small. |
| **Broadcast Variables** | Spark Internals | Read-only copy of data sent once to each executor. | Broadcast a small dimension for map-side join / `broadcast(df)`. |
| **Catalyst Optimizer** | Spark Internals | Spark SQL's rule + cost optimizer: analysis → logical optimization → physical planning. | Constant folding, predicate pushdown, column pruning done automatically. |
| **Closure** | Spark Internals | Function + captured outer variables sent to executors. | Capturing a large Python list in a UDF serializes it to every task. |
| **Cluster Manager** | Spark Internals | Allocates resources: Standalone, YARN, Kubernetes, Mesos (legacy). | `spark.master=yarn` or `k8s://...` with dynamic allocation. |
| **DAG Scheduler** | Spark Internals | Builds a DAG of stages from the RDD/DataFrame lineage and submits stage tasks when parents finish. | `map → filter → reduceByKey` → narrow stage then shuffle stage. |
| **Driver** | Spark Internals | The process that runs your main program, builds the DAG, and coordinates executors. | Collecting a huge DataFrame to the driver (`collect()`) crashes the driver. |
| **Dynamic Partition Pruning** | Spark Internals | At runtime, prune partitions of a large fact using values from a filtered dimension join. | Join `sales` (partitioned by `date`) to `dim_date` filtered to one month → only those fact partitions scanned. |
| **Executor** | Spark Internals | JVM worker process that runs tasks and stores shuffle/cache data. | 10 executors × 4 cores → up to 40 concurrent tasks. |
| **Job → Stage → Task** | Spark Internals | - **Job:** triggered by an action (`count`, `write`, `collect`) - **Stage:** set of tasks with narrow deps between shuffles - **Task:** unit of work on one p… | One `write` action → 1 job → 3 stages → N tasks per stage. |
| **Lazy Evaluation** | Spark Internals | Transformations build a plan; work runs only on actions. | Many `filter`/`select` calls do nothing until `show()` or `write`. |
| **Lineage** | Spark Internals | Graph of transformations needed to recompute an RDD/DataFrame partition. | Lose executor → recompute lost partitions from source + lineage. |
| **Memory Management** | Spark Internals | Spark splits executor memory among execution (shuffles/joins), storage (cache), and user/overhead. | Unified memory region shared by execution and storage (post Spark 1.6). |
| **Serialization (Java/Kryo)** | Spark Internals | Convert objects to bytes for shuffle/cache/network. Kryo is faster/smaller than Java serializer when registered. | `spark.serializer=org.apache.spark.serializer.KryoSerializer` + register classes. |
| **Shuffle** | Spark Internals | Redistribute data across partitions by key (network + sort/hash). | `groupBy`, `join`, `repartition`, `distinct` often shuffle. |
| **Skew Join Optimization** | Spark Internals | Detect hot keys and split/handle them separately (AQE skew join, salting). | One `customer_id` with 40% of rows → AQE splits that partition. |
| **Spill to Disk** | Spark Internals | When memory is insufficient, intermediate data is written to local disk. | Large sort-merge join spills during sort. |
| **Task Scheduler** | Spark Internals | Assigns individual tasks to executors (resource offers from cluster manager). | Prefer `PROCESS_LOCAL` / `NODE_LOCAL` tasks when data is cached on that executor. |
| **Tungsten Engine** | Spark Internals | Execution layer: off-heap/cache-aware memory, whole-stage codegen, binary processing. | Whole-stage codegen fuses operators into Java bytecode. |
| **Wide vs Narrow Transformations** | Spark Internals | - **Narrow:** each input partition maps to ≤1 output partition (`map`, `filter`) — no shuffle - **Wide:** input partitions contribute to many outputs (`group… | `filter` narrow; `reduceByKey` wide. |
| **Worker** | Spark Internals | Cluster node process (e.g., Spark standalone worker) that hosts executors. | One worker machine runs multiple executors. |
| **At Least Once** | Streaming | Every record processed ≥1 time; duplicates possible on retry. | Restart after crash reprocesses last uncommitted batch. |
| **At Most Once** | Streaming | Process ≤1 time; may lose data on failure. | Fire metrics where loss is acceptable. |
| **CQRS** | Streaming | Command Query Responsibility Segregation — separate write model from read model(s). | Write orders to OLTP; project read-optimized order search index. |
| **Event Sourcing** | Streaming | Persist state as an append-only sequence of events; rebuild state by replay. | `OrderPlaced`, `ItemAdded`, `OrderShipped` rebuild current order. |
| **Event Time** | Streaming | Timestamp when the event actually occurred in the real world. | Click happened at 10:00; arrived at 10:07 → event time = 10:00. |
| **Exactly Once** | Streaming | Effect of each record applied once end-to-end (despite retries). | Kafka → Flink → transactional sink / idempotent sink with checkpoints. |
| **Ingestion Time** | Streaming | Time when the event enters the streaming system. | Kafka timestamp at produce/consume (depending on config). |
| **Late Data** | Streaming | Events arriving after the watermark/window allowed them. | Event time 10:01 arrives at 10:25 with 5-min watermark — late. |
| **Processing Time** | Streaming | Time on the machine when the event is processed. | Same click processed at 10:07 → processing-time window uses 10:07. |
| **Stateful Processing** | Streaming | Operators keep state across events (windows, joins, dedupe). | Running count per user; stream-stream join. |
| **Stateless Processing** | Streaming | Each event handled independently; no cross-event state. | Map parse JSON → enrich from broadcast config → filter. |
| **Watermarks** | Streaming | Engine's notion of how far event time has advanced; used to close windows. | Watermark = max_event_time - 10 minutes → close hour window when watermark passes end + grace. |
| **Windowing** | Streaming | Group stream events into finite buckets: tumbling, sliding, session. | Tumbling 5-min count of orders; session window by user inactivity gap. |
| **dbt Model** | dbt | A versioned SQL (or Python) select statement materialized as a table/view in the warehouse. | `models/marts/fct_orders.sql` builds from staging models. |
| **Documentation / Docs Site** | dbt | YAML descriptions + `dbt docs generate` catalog of models/columns. | Column description for `gross_revenue` definition. |
| **Exposures** | dbt | Declared downstream uses (dashboards, ML jobs) that depend on models. | Exposure `finance_arr_dashboard` depends on `fct_subscriptions`. |
| **Incremental Model** | dbt | Only process new/changed rows each run instead of full rebuild. | `where updated_at > (select max(updated_at) from {{ this }})` |
| **Materialization** | dbt | How dbt builds a model: view, table, incremental, ephemeral. | `{{ config(materialized='incremental', unique_key='order_id') }}` |
| **ref()** | dbt | dbt function linking models so the DAG and schema names resolve correctly. | `select * from {{ ref('stg_orders') }}` |
| **Seeds** | dbt | CSV files checked into the repo and loaded as tables. | `seeds/country_codes.csv` → `ref('country_codes')`. |
| **Slim CI / State Defer** | dbt | Run/test only modified models (and downstream) using prior manifest state. | `dbt test --select state:modified+` with defer to prod. |
| **Sources** | dbt | Declared raw upstream tables dbt reads but does not own. | `sources.yml` → `{{ source('stripe', 'payments') }}` |
| **Tests (dbt)** | dbt | Assertions on models/columns: unique, not_null, accepted_values, relationships, custom. | `unique` + `not_null` on `order_id`; relationship to `dim_customers`. |
