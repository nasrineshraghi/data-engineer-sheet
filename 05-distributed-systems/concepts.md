# Distributed Systems

---

### CAP Theorem

**Definition:** In a network partition, a system can provide Consistency or Availability, not both (Partition tolerance assumed in distributed DBs).

**Why it matters:** Forces explicit tradeoffs in data platforms.

**Example:** During partition, CP system rejects writes; AP system accepts writes that may conflict.

**Remember:**
- Real systems tune the C/A tradeoff
- "CA without P" isn't realistic for multi-node

---

### BASE

**Definition:** Basically Available, Soft state, Eventually consistent — alternative mindset to strict ACID across distributed services.

**Why it matters:** Many large-scale stores and caches lean BASE.

**Example:** Shopping cart eventually syncs across regions; brief stale reads OK.

**Remember:**
- Soft state may change without input (anti-entropy)
- Pair with application-level conflict handling

---

### Eventual Consistency

**Definition:** If no new updates, all replicas converge to the same value eventually.

**Why it matters:** Default for many geo-replicated and highly available systems.

**Example:** Read-after-write may fail briefly across regions; later reads agree.

**Remember:**
- Document staleness windows for consumers
- Use stronger reads when needed (quorum/linearizable APIs)

---

### Strong Consistency

**Definition:** After a write commits, all subsequent reads see it (linearizability / similar guarantees vary by system).

**Why it matters:** Simpler app logic; higher latency/cost.

**Example:** Financial ledger balance must be strongly consistent.

**Remember:**
- Costs latency and availability under partitions
- Use where correctness > availability

---

### Replication

**Definition:** Keep multiple copies of data for durability and/or read scale.

**Why it matters:** Failure domains and read throughput.

**Example:** Kafka topic RF=3; Postgres primary + replicas; S3 cross-region copy.

**Remember:**
- Sync vs async replication tradeoffs
- Replica lag affects read-your-writes

---

### Leader Election

**Definition:** Cluster chooses a primary coordinator for writes or decisions.

**Why it matters:** Avoids split-brain conflicting writes.

**Example:** ZooKeeper/etcd/Raft elect Kafka controller or DB primary.

**Remember:**
- Fencing tokens prevent old leaders writing
- Elections add brief unavailability

---

### Consensus

**Definition:** Nodes agree on a value/order of operations despite failures.

**Why it matters:** Metadata, configs, and transaction logs need agreement.

**Example:** Agreeing on the next committed Kafka controller epoch or Raft log entry.

**Remember:**
- Quorum majority required
- Expensive; keep consensus sets small

---

### Raft

**Definition:** Consensus algorithm emphasizing understandability: leader, log replication, terms.

**Why it matters:** Used by etcd, Consul, many modern systems.

**Example:** etcd stores K8s state via Raft.

**Remember:**
- Strong leader model
- Majority of voters must ack

---

### Paxos

**Definition:** Classic family of consensus protocols (Multi-Paxos, etc.).

**Why it matters:** Theoretical foundation; still in older systems (Chubby-like).

**Example:** Google Chubby historically influenced by Paxos.

**Remember:**
- Harder to implement correctly than Raft
- Same goal: agree under failures

---

### Fault Tolerance

**Definition:** System continues correctly despite component failures.

**Why it matters:** Commodity hardware fails; jobs and stores must survive.

**Example:** Spark recomputes lost partitions; Kafka replicates partitions.

**Remember:**
- Detect, isolate, recover
- Design for failure, not perfection

---

### High Availability (HA)

**Definition:** Minimize downtime via redundancy and fast failover.

**Why it matters:** SLAs for pipelines and serving layers.

**Example:** Multi-AZ brokers; standby scheduler; health checks + auto restart.

**Remember:**
- HA ≠ zero data loss (depends on durability config)
- Measure MTTR and availability %

---

### Horizontal Scaling

**Definition:** Add more nodes to increase capacity.

**Why it matters:** Default for big data systems.

**Example:** Add Spark executors or Kafka brokers.

**Remember:**
- Needs partitionable workloads
- Shuffle/network can become bottleneck

---

### Vertical Scaling

**Definition:** Give one machine more CPU/RAM/disk.

**Why it matters:** Simple until limits/cost/HA constraints hit.

**Example:** Upsize a warehouse warehouse node or driver machine.

**Remember:**
- Ceiling exists; single point of failure risk
- Mix: scale out data plane, scale up hot coordinators carefully
