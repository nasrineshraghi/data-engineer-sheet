# Streaming

---

### Event Time

**Definition:** Timestamp when the event actually occurred in the real world.

**Why it matters:** Correct windows despite late/out-of-order arrival.

**Example:** Click happened at 10:00; arrived at 10:07 → event time = 10:00.

**Remember:**
- Prefer event time for analytics windows
- Requires watermarks for progress

---

### Processing Time

**Definition:** Time on the machine when the event is processed.

**Why it matters:** Simple but wrong for delayed data.

**Example:** Same click processed at 10:07 → processing-time window uses 10:07.

**Remember:**
- OK for monitoring ops latency
- Bad for business "hourly sales"

---

### Ingestion Time

**Definition:** Time when the event enters the streaming system.

**Why it matters:** Middle ground; stable clock at entry, not true event time.

**Example:** Kafka timestamp at produce/consume (depending on config).

**Remember:**
- Better than processing time for some cases
- Still not true business event time

---

### Watermarks

**Definition:** Engine's notion of how far event time has advanced; used to close windows.

**Why it matters:** Trade completeness vs latency for late data.

**Example:** Watermark = max_event_time - 10 minutes → close hour window when watermark passes end + grace.

**Remember:**
- Too tight → drop late events
- Too loose → high latency/state

---

### Windowing

**Definition:** Group stream events into finite buckets: tumbling, sliding, session.

**Why it matters:** Aggregations need bounded scopes.

**Example:** Tumbling 5-min count of orders; session window by user inactivity gap.

**Remember:**
- Tumbling: fixed, non-overlap
- Sliding: overlap; session: activity-based

---

### Late Data

**Definition:** Events arriving after the watermark/window allowed them.

**Why it matters:** Reality of mobile/offline producers.

**Example:** Event time 10:01 arrives at 10:25 with 5-min watermark — late.

**Remember:**
- Side outputs / allowed lateness / update previous results
- Decide drop vs correct

---

### Stateful Processing

**Definition:** Operators keep state across events (windows, joins, dedupe).

**Why it matters:** Enables real aggregations; needs checkpointing and TTL.

**Example:** Running count per user; stream-stream join.

**Remember:**
- State grows — set TTL
- Checkpoint state for exactly-once

---

### Stateless Processing

**Definition:** Each event handled independently; no cross-event state.

**Why it matters:** Easier scale and recovery.

**Example:** Map parse JSON → enrich from broadcast config → filter.

**Remember:**
- Prefer when possible
- Filter/map/flatMap style ops

---

### Exactly Once

**Definition:** Effect of each record applied once end-to-end (despite retries).

**Why it matters:** No double-counting in sinks.

**Example:** Kafka → Flink → transactional sink / idempotent sink with checkpoints.

**Remember:**
- Needs idempotent or transactional sinks
- "Exactly once" is end-to-end, not just processing

---

### At Least Once

**Definition:** Every record processed ≥1 time; duplicates possible on retry.

**Why it matters:** Common default; simpler than exactly-once.

**Example:** Restart after crash reprocesses last uncommitted batch.

**Remember:**
- Pair with idempotent writes
- Often "good enough" with dedupe keys

---

### At Most Once

**Definition:** Process ≤1 time; may lose data on failure.

**Why it matters:** Lowest latency/complexity; rare for critical pipelines.

**Example:** Fire metrics where loss is acceptable.

**Remember:**
- Don't use for money/inventory
- Explicit tradeoff: loss over duplicates

---

### Event Sourcing

**Definition:** Persist state as an append-only sequence of events; rebuild state by replay.

**Why it matters:** Auditability and temporal queries.

**Example:** `OrderPlaced`, `ItemAdded`, `OrderShipped` rebuild current order.

**Remember:**
- Source of truth = event log
- Snapshots speed replay

---

### CQRS

**Definition:** Command Query Responsibility Segregation — separate write model from read model(s).

**Why it matters:** Scale reads/writes independently; tailor projections.

**Example:** Write orders to OLTP; project read-optimized order search index.

**Remember:**
- Often paired with event sourcing
- Read models can be eventually consistent
