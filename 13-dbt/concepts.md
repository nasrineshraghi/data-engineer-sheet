# dbt

Analytics engineering patterns for SQL transforms, tests, and documentation as code.

---

### dbt Model

**Definition:** A versioned SQL (or Python) select statement materialized as a table/view in the warehouse.

**Why it matters:** Transforms become testable, documented, DAG-aware units.

**Example:** `models/marts/fct_orders.sql` builds from staging models.

**Remember:**
- One model ≈ one relation
- Name by layer: staging / intermediate / marts

---

### Materialization

**Definition:** How dbt builds a model: view, table, incremental, ephemeral.

**Why it matters:** Cost/performance tradeoff per model.

**Example:** `{{ config(materialized='incremental', unique_key='order_id') }}`

**Remember:**
- Views = cheap to build, pay at query time
- Incrementals need a correct strategy

---

### Incremental Model

**Definition:** Only process new/changed rows each run instead of full rebuild.

**Why it matters:** Scales large facts; easy to get wrong (duplicates/misses).

**Example:** `where updated_at > (select max(updated_at) from {{ this }})`

**Remember:**
- Define unique key + late-data strategy
- Periodic full-refresh still needed

---

### Sources

**Definition:** Declared raw upstream tables dbt reads but does not own.

**Why it matters:** Freshness checks and clear boundary raw → staging.

**Example:** `sources.yml` → `{{ source('stripe', 'payments') }}`

**Remember:**
- Sources are ingest landing zones
- Test source freshness SLAs

---

### Seeds

**Definition:** CSV files checked into the repo and loaded as tables.

**Why it matters:** Small mapping/reference data under version control.

**Example:** `seeds/country_codes.csv` → `ref('country_codes')`.

**Remember:**
- Not for large facts
- Great for simple lookups

---

### ref()

**Definition:** dbt function linking models so the DAG and schema names resolve correctly.

**Why it matters:** Dependency graph + environment-aware relation names.

**Example:** `select * from {{ ref('stg_orders') }}`

**Remember:**
- Prefer `ref` over hard-coded table names
- Circular refs are errors

---

### Tests (dbt)

**Definition:** Assertions on models/columns: unique, not_null, accepted_values, relationships, custom.

**Why it matters:** Data quality gates in CI and prod runs.

**Example:** `unique` + `not_null` on `order_id`; relationship to `dim_customers`.

**Remember:**
- Fail builds on critical tests
- Custom tests for business rules

---

### Exposures

**Definition:** Declared downstream uses (dashboards, ML jobs) that depend on models.

**Why it matters:** Impact analysis when changing a mart.

**Example:** Exposure `finance_arr_dashboard` depends on `fct_subscriptions`.

**Remember:**
- Document owners and maturity
- Ties lineage to consumers

---

### Documentation / Docs Site

**Definition:** YAML descriptions + `dbt docs generate` catalog of models/columns.

**Why it matters:** Self-serve understanding of metrics and tables.

**Example:** Column description for `gross_revenue` definition.

**Remember:**
- Docs without ownership rot
- Link to data contracts where possible

---

### Slim CI / State Defer

**Definition:** Run/test only modified models (and downstream) using prior manifest state.

**Why it matters:** Fast PRs on large projects.

**Example:** `dbt test --select state:modified+` with defer to prod.

**Remember:**
- Needs a trusted prod manifest
- Still full-refresh periodically
