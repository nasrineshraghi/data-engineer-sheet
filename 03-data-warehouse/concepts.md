# Data Warehouse Concepts

---

### Grain

**Definition:** Exact meaning of one fact row (business level of detail).

**Why it matters:** Foundation of dimensional modeling; wrong grain breaks metrics.

**Example:** "One row per order line per day" vs "one row per order".

**Remember:**
- Declare grain in one sentence before designing
- All measures must match that grain

---

### Granularity

**Definition:** Same idea as grain — how fine or coarse the data is. Often used interchangeably with grain in DW.

**Why it matters:** Aggregation level must match reporting needs.

**Example:** Daily grain vs monthly rollup tables.

**Remember:**
- Finer grain → more rows, more flexibility
- Coarser → faster reports, less detail

---

### Additive Facts

**Definition:** Measures that can be summed across any dimension.

**Why it matters:** Safest metrics for rollups.

**Example:** `sales_amount`, `quantity_sold` — sum by day, store, product all valid.

**Remember:**
- Prefer additive measures when possible
- Document additivity of each measure

---

### Semi-Additive Facts

**Definition:** Summable across some dimensions, not others (often not across time).

**Why it matters:** Easy to misuse in BI (double-count balances).

**Example:** Account balance — sum across customers OK; sum across days wrong (use last/average).

**Remember:**
- Inventory and balances are classic semi-additive
- Use snapshot patterns carefully

---

### Non-Additive Facts

**Definition:** Cannot be summed meaningfully; ratios, percentages, temperatures.

**Why it matters:** Must recalculate from components, not average averages blindly.

**Example:** `profit_margin` — store `profit` and `revenue`, compute margin at query time.

**Remember:**
- Store additive components
- Aggregate then compute ratio

---

### Degenerate Dimension

**Definition:** Dimension-like identifier stored in the fact table with no separate dimension table.

**Why it matters:** Avoids empty dimension tables for transactional IDs.

**Example:** `order_id`, `invoice_number` living on the fact row.

**Remember:**
- Common for transaction numbers
- Still useful for drill-to-detail

---

### Junk Dimension

**Definition:** Single dimension table combining low-cardinality flags/indicators.

**Why it matters:** Avoids many tiny dimensions cluttering the model.

**Example:** `is_gift`, `payment_type`, `channel` packed into `dim_order_flags`.

**Remember:**
- Keep cardinality manageable
- Good for yes/no and small enums

---

### Role-Playing Dimension

**Definition:** Same dimension reused for multiple roles via different foreign keys.

**Why it matters:** One `dim_date` serves order date, ship date, delivery date.

**Example:** `order_date_key`, `ship_date_key` both point to `dim_date`.

**Remember:**
- Views/aliases per role in BI tools
- Don't duplicate date tables

---

### Conformed Dimension

**Definition:** Shared dimension with consistent keys and attributes across facts/marts.

**Why it matters:** Enables cross-process drill-across reporting.

**Example:** Same `customer_key` and customer attributes in sales and support marts.

**Remember:**
- Enterprise consistency
- Owned by a shared data team/process

---

### Mini Dimension

**Definition:** Split frequently changing attributes into a smaller dimension to limit type-2 explosion on the main dim.

**Why it matters:** Keeps large customer dims manageable when demographics change often.

**Example:** `dim_customer` stable attrs + `dim_customer_profile` for segment/score that changes monthly.

**Remember:**
- Use when type-2 history would explode
- Fact points to both keys when needed

---

### Bridge Table

**Definition:** Helper table resolving many-to-many between fact and dimension (or between dims).

**Why it matters:** Correct weighting and multi-valued attributes.

**Example:** Order with multiple sales reps → `bridge_order_rep` with allocation weights.

**Remember:**
- Watch double-counting; use weights
- Common for multi-valued dims (diagnoses, tags)

---

### Factless Fact Table

**Definition:** Fact table with keys only (no numeric measures) — records events or coverage.

**Why it matters:** Answers "did it happen?" and "what was assigned?"

**Example:** Student attendance: `student_key`, `class_key`, `date_key` — count rows = attendance events.

**Remember:**
- Event tracking and coverage/eligibility
- Measures are often counts of rows

---

### Snapshot Fact

**Definition:** Fact capturing state at a point in time (generic term; often periodic).

**Why it matters:** Measures levels (balances, inventory) over time.

**Example:** Daily inventory on-hand per SKU per warehouse.

**Remember:**
- Semi-additive measures common
- Choose periodic vs accumulating pattern

---

### Accumulating Snapshot

**Definition:** One row per process instance; columns updated as milestones complete (pipeline pipeline).

**Why it matters:** Tracks lifecycle duration and conversion.

**Example:** Order fulfillment: `ordered_at`, `packed_at`, `shipped_at`, `delivered_at` on one row, updated in place.

**Remember:**
- Fixed known milestones
- Lag metrics between dates

---

### Periodic Snapshot

**Definition:** New fact rows taken at regular intervals for all entities (day/week/month).

**Why it matters:** Time-series of levels for reporting.

**Example:** End-of-day account balance for every account every day.

**Remember:**
- Dense over time
- Storage heavy but query-friendly for trends
