# Data Quality & Governance

---

### Data Profiling

**Definition:** Statistical survey of a dataset: nulls, distincts, distributions, patterns.

**Why it matters:** Baseline before modeling and for anomaly detection.

**Example:** 12% null `email`; `amount` min/max/p99; top values of `status`.

**Remember:**
- Profile new sources early
- Re-profile after major changes

---

### Data Validation

**Definition:** Automated checks that data meets rules (schema, ranges, uniqueness, referential).

**Why it matters:** Catch bad data before it hits consumers.

**Example:** Great Expectations / dbt tests: `order_id` unique, `amount >= 0`, FK to customers.

**Remember:**
- Fail or quarantine on critical rules
- Warn on softer anomalies

---

### Data Lineage

**Definition:** Trace where data came from and where it flows (table/column/job level).

**Why it matters:** Impact analysis, debugging, compliance.

**Example:** `raw.orders` → `stg_orders` → `fct_orders` → dashboard KPI.

**Remember:**
- Column-level lineage is gold for audits
- Automate from orchestrator/SQL parsers/catalog

---

### Metadata

**Definition:** Data about data: schema, owners, freshness, partitions, descriptions.

**Why it matters:** Discoverability and safe use.

**Example:** Table description, column glossary, last update time, PII tags.

**Remember:**
- Treat metadata as a product
- Stale metadata is worse than none if trusted blindly

---

### Data Catalog

**Definition:** Searchable inventory of datasets with metadata, ownership, and often lineage.

**Why it matters:** "Where is customer revenue defined?"

**Example:** DataHub, Collibra, Unity Catalog, Glue Data Catalog, OpenMetadata.

**Remember:**
- Integrate with ingestion + BI
- Ownership + certification badges help trust

---

### Master Data Management (MDM)

**Definition:** Processes/systems to create a single trusted master for core entities (customer, product).

**Why it matters:** Deduped golden records across systems.

**Example:** Merge CRM + billing customers into golden `customer_id` with survivorship rules.

**Remember:**
- Matching + survivorship + stewardship
- Hard organizationally, not just technically

---

### Data Governance

**Definition:** Policies, roles, and controls for data quality, security, privacy, and usage.

**Why it matters:** Trust, compliance (GDPR etc.), consistent definitions.

**Example:** PII classification, access reviews, approved metric definitions.

**Remember:**
- People + process + platform
- Embed in pipelines, not only documents

---

### Data Stewardship

**Definition:** Human ownership of domain data quality and definitions.

**Why it matters:** Governance without stewards doesn't stick.

**Example:** Finance steward owns `revenue` definition and approves changes.

**Remember:**
- Assign stewards per domain
- Stewards ≠ only platform engineers

---

### Observability

**Definition:** Ability to understand pipeline health via metrics, logs, traces, and data checks.

**Why it matters:** Detect silent data failures, not just job crashes.

**Example:** Freshness, row-count anomalies, schema drift alerts, job duration SLOs.

**Remember:**
- Observe data + compute
- Alert on symptoms that matter to consumers

---

### Freshness

**Definition:** How up-to-date the data is vs expectation (SLA/SLO).

**Why it matters:** Stale dashboards mislead decisions.

**Example:** "Orders table max `updated_at` < 1 hour ago".

**Remember:**
- Define per table SLA
- Alert on breach, not only job fail

---

### Completeness

**Definition:** Required data is present (rows and fields).

**Why it matters:** Missing partitions/nulls break KPIs.

**Example:** All 24 hourly partitions arrived; `customer_id` null rate < 0.1%.

**Remember:**
- Partition completeness checks
- Critical field null thresholds

---

### Accuracy

**Definition:** Data correctly represents real-world values.

**Why it matters:** Valid schema can still be wrong.

**Example:** Currency conversion rates match source system within tolerance.

**Remember:**
- Often needs business reconciliation
- Sample audits + source compares

---

### Consistency

**Definition:** Same facts agree across systems/tables within defined rules.

**Why it matters:** Conflicting numbers destroy trust.

**Example:** Sum of order lines equals order header total; warehouse matches finance extract.

**Remember:**
- Cross-system reconciliations
- Define which system is source of truth
