# Kafka

Event streaming backbone — topics, partitions, consumer groups, and delivery semantics.

---

### Topic

**Definition:** Named stream of records; publishers write, consumers read.

**Why it matters:** Logical channel for a type of event (`orders`, `clicks`).

**Example:** Producers write to `payments.completed`; three services consume independently.

**Remember:**
- Topics are multi-subscriber
- Plan naming + retention up front

---

### Partition

**Definition:** Ordered, append-only log slice of a topic; unit of parallelism.

**Why it matters:** Throughput and ordering are per partition, not global.

**Example:** Key by `customer_id` so one customer’s events stay ordered in one partition.

**Remember:**
- More partitions → more parallelism
- Rebalancing and key design matter

---

### Offset

**Definition:** Position of a consumer within a partition log.

**Why it matters:** Progress tracking and replay.

**Example:** Commit offset 1050 after processing; restart resumes at 1051 (depending on config).

**Remember:**
- Commit too early → loss; too late → duplicates
- External stores can hold offsets too

---

### Consumer Group

**Definition:** Set of consumers sharing work on a topic; each partition goes to one member.

**Why it matters:** Scale reads horizontally without double-processing inside the group.

**Example:** 6 partitions, 3 consumers in group `billing` → ~2 partitions each.

**Remember:**
- Extra consumers beyond partition count sit idle
- Rebalance pauses briefly

---

### Producer / Consumer

**Definition:** Writer vs reader clients of Kafka topics.

**Why it matters:** Different configs for durability, batching, and commit strategy.

**Example:** Producer `acks=all`; consumer `enable.auto.commit=false` with manual commits.

**Remember:**
- Idempotent producer reduces dupes
- Consumer commit policy defines at-least-once behavior

---

### Replication Factor

**Definition:** How many broker copies of each partition exist.

**Why it matters:** Durability and availability when brokers die.

**Example:** RF=3, min ISR=2 for production topics.

**Remember:**
- RF=1 risks data loss
- Costs disk and network

---

### ISR (In-Sync Replicas)

**Definition:** Replicas fully caught up with the leader; eligible for failover.

**Why it matters:** Durability guarantees with `acks=all`.

**Example:** Leader waits for ISR acks before acknowledging the produce.

**Remember:**
- Under-replicated partitions are a red alert
- Tune replica lag thresholds

---

### Exactly-Once Semantics (EOS)

**Definition:** Kafka transactions / idempotent produce so a read-process-write cycle doesn’t dup effects (within Kafka).

**Why it matters:** Stronger stream processing guarantees end-to-end still need idempotent sinks.

**Example:** Kafka Streams transactional write to output topic.

**Remember:**
- EOS ≠ automatic exactly-once into your warehouse
- Pair with idempotent sinks outside Kafka

---

### Compaction (Kafka)

**Definition:** Log compaction keeps the latest value per key; older keys garbage-collected.

**Why it matters:** Changelog / compacted topics for state and CDC mirrors.

**Example:** `customer_profile` compacted topic always has latest profile per `customer_id`.

**Remember:**
- Not a substitute for short retention on high-volume events
- Tombstones delete keys

---

### Dead Letter Topic

**Definition:** Topic receiving poison / failed records after retries.

**Why it matters:** Unblocks consumers; enables quarantine and replay.

**Example:** Deserialization failures → `orders.dlq` with headers explaining error.

**Remember:**
- Monitor DLQ lag/depth
- Have a replay runbook

---

### Schema Registry

**Definition:** Service storing Avro/Protobuf/JSON schemas for topic payloads with compatibility rules.

**Why it matters:** Prevents breaking consumers on schema changes.

**Example:** BACKWARD compatibility for `orders-value` subject.

**Remember:**
- Enforce compatibility in CI
- Version schemas intentionally
