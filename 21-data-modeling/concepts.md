# Data Modeling Patterns

How you **shape tables for analytics**: dimensional (star/snowflake), Data Vault, and One Big Table (OBT) — when each wins and how they fit together.

---

### Dimensional Modeling (Kimball)

**Definition:** Analytics design that centers on **facts** (measures at a declared grain) and **dimensions** (descriptive context), usually published as star or snowflake marts.

**Why it matters:** Matches how BI users think (“sales by product by day”) and keeps metric definitions tied to grain.

**Example:** `fact_order_line` + `dim_product` + `dim_customer` + `dim_date` for revenue reporting.

**Remember:**
- Declare grain in one sentence before keys and measures
- Conformed dimensions unlock drill-across across marts

---

### Star Schema

**Definition:** Fact table in the center with denormalized dimension tables around it (few joins, wide dims).

**Why it matters:** Simple for BI tools and analysts; usually the default serving layer for dashboards.

**Example:** `fact_sales` → `dim_store`, `dim_product`, `dim_date` (product attributes live on `dim_product`, not nested tables).

**Remember:**
- Prefer star for marts / gold serving
- Dimensions are often denormalized on purpose

---

### Snowflake Schema

**Definition:** Dimensions are normalized into related sub-tables (product → brand → category), so the model “snowflakes” outward.

**Why it matters:** Saves storage and avoids repeating attributes, but adds joins and complexity for BI.

**Example:** `dim_product` → `dim_brand` → `dim_category` instead of repeating brand/category on every product row.

**Remember:**
- Use sparingly; most teams stay star at the mart
- Fine in warehouse storage layer if tools hide the joins

---

### Fact Table

**Definition:** Table of events or measurements at a fixed grain; foreign keys to dimensions plus numeric measures.

**Why it matters:** Facts are where KPIs live; wrong grain or missing keys break every report built on top.

**Example:** One row per order line: `order_line_key`, `date_key`, `product_key`, `qty`, `amount`.

**Remember:**
- Keys + measures; grain first
- Transaction, periodic snapshot, accumulating snapshot are common patterns

---

### Dimension Table

**Definition:** Descriptive attributes used to filter, group, and label facts (who, what, where, when).

**Why it matters:** Stable, conformed dims make metrics comparable across domains.

**Example:** `dim_customer` with name, segment, region; facts store `customer_key`.

**Remember:**
- Surrogate keys + natural/business keys
- Slowly changing dims (SCD) when history matters

---

### One Big Table (OBT)

**Definition:** A single wide, denormalized table with facts and dimension attributes flattened into columns (often the final “gold” or ML feature table).

**Why it matters:** Fast and simple for one use case (dashboard, notebook, model training); painful when many consumers need different grains or shared definitions.

**Example:** `orders_obt` with `order_id`, `amount`, `customer_name`, `customer_segment`, `product_name`, `category` all on one row.

**Remember:**
- Great for a single product/team slice; weak as the enterprise source of truth
- Duplication and SCD history explode unless carefully designed
- Common pattern: Vault or 3NF → star → optional OBT for a consumer

---

### Data Vault

**Definition:** Modeling method for the **enterprise integration** layer: Hubs (business keys), Links (relationships), Satellites (descriptive/history) — built for auditability and multi-source change.

**Why it matters:** Absorbs source change and history without rewriting marts every time; separates “what happened” storage from “how we present it.”

**Example:** Hub Customer, Hub Product, Link Order, Satellites for customer attributes from CRM and ERP.

**Remember:**
- Vault is usually raw/integration (silver), not the BI star
- Build dimensional or OBT marts **on top** of Vault
- Insert-mostly / historized by design

---

### Hub (Data Vault)

**Definition:** Table that stores a unique **business key** (and load metadata) for a core business entity — no descriptive attributes.

**Why it matters:** Stable identity across sources; hubs don’t churn when attributes change.

**Example:** `hub_customer(customer_hk, customer_bk, load_dts, record_source)`.

**Remember:**
- Business key only (+ hash key, load timestamp, source)
- Attributes go in satellites

---

### Link (Data Vault)

**Definition:** Table that records a **relationship** (or transaction) between hubs — the association, not the descriptions.

**Why it matters:** Many-to-many and multi-source relationships stay explicit and historized.

**Example:** `link_order(order_hk, customer_hk, product_hk, load_dts, record_source)` for “customer bought product.”

**Remember:**
- Links connect hubs; satellites hang off hubs or links
- Same relationship from two sources can share structure carefully

---

### Satellite (Data Vault)

**Definition:** Descriptive and historized attributes for a hub or link — where SCD-like change lives in Vault.

**Why it matters:** Source systems change fields independently; satellites isolate that churn.

**Example:** `sat_customer_crm` (name, email, segment) and `sat_customer_erp` (credit_limit) on the same hub.

**Remember:**
- One satellite per rate-of-change / source family is common
- Load timestamp + hashdiff for change detection

---

### Raw Vault vs Business Vault

**Definition:** **Raw Vault** mirrors source-driven hubs/links/sats with minimal business rules; **Business Vault** adds soft rules, computed satellites, and cleaned keys closer to enterprise meaning.

**Why it matters:** Keeps auditable raw history separate from interpreted business logic.

**Example:** Raw: CRM customer as loaded. Business: standardized phone, golden customer match key, derived “active_flag.”

**Remember:**
- Don’t bury heavy BI metrics in Raw Vault
- Marts still sit above Business Vault / information marts

---

### Inmon (CIF / EDW)

**Definition:** Enterprise warehouse approach: normalized integration model (often 3NF) as the system of record, then departmental dimensional marts for consumption.

**Why it matters:** Strong for enterprise consistency; heavier to build and change than pure Kimball marts.

**Example:** Normalized EDW tables for customer/order → sales mart star for Finance.

**Remember:**
- Inmon ≈ integrate normalized first; Kimball ≈ marts first
- Modern lakes often mix: Vault/3NF silver + Kimball/OBT gold

---

### Modeling Pattern Choice

**Definition:** Picking Vault / dimensional / OBT (or a layered mix) based on change rate, consumers, and who owns metrics.

**Why it matters:** Wrong pattern → either endless remapping (too rigid) or metric chaos (too flat).

**Example:** Multi-source core → Data Vault; Finance KPIs → star mart; one ML feature set → OBT built from the mart/Vault.

**Remember:**
- Integration layer: Vault or normalized EDW
- Serving layer: star (shared metrics) or OBT (single consumer)
- Don’t make OBT your only enterprise model
