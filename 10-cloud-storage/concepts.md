# Cloud & Storage

---

### Object Storage

**Definition:** Store immutable objects (files) addressed by key in buckets; virtually infinite scale.

**Why it matters:** Default substrate for data lakes.

**Example:** S3, ADLS Gen2, GCS holding parquet/Delta tables.

**Remember:**
- Eventually consistent listing quirks are rarer now but design carefully
- Cheap capacity; watch request/API costs

---

### Block Storage

**Definition:** Disk volumes attached to VMs (like SAN/local disks).

**Why it matters:** Databases, Kafka brokers, Spark local shuffle disks.

**Example:** EBS/Azure Disks for Postgres data directory.

**Remember:**
- Higher IOPS for stateful services
- Not the primary lake storage

---

### Lifecycle Policies

**Definition:** Automatic transition/expire of objects by age/prefix (hot → cool → archive → delete).

**Why it matters:** Cost control for lakes and logs.

**Example:** Raw logs to Glacier after 90 days; delete after 365.

**Remember:**
- Align with compliance retention
- Archive retrieval can be slow/expensive

---

### IAM

**Definition:** Identity and Access Management — who can do what on which resources.

**Why it matters:** Security boundary for every cloud data platform.

**Example:** Role for Spark job: read `s3://lake/bronze/*`, write `s3://lake/silver/*` only.

**Remember:**
- Least privilege
- Prefer roles over long-lived keys

---

### Secrets Management

**Definition:** Store/rotate credentials and API keys outside code.

**Why it matters:** Prevent leaks in repos and logs.

**Example:** AWS Secrets Manager / Azure Key Vault / HashiCorp Vault for DB passwords.

**Remember:**
- Never commit secrets
- Rotate and audit access

---

### KMS

**Definition:** Key Management Service — create and control encryption keys.

**Why it matters:** Separate permission to use keys from permission to see data.

**Example:** S3 SSE-KMS; revoke key usage to lock data access.

**Remember:**
- Key policies are critical
- Audit key usage

---

### Encryption at Rest

**Definition:** Data encrypted on disk/storage media.

**Why it matters:** Protects against disk theft and some breach scenarios.

**Example:** S3 default encryption; encrypted EBS volumes.

**Remember:**
- Usually mandatory in enterprises
- Combine with IAM + KMS

---

### Encryption in Transit

**Definition:** Data encrypted on the network (TLS/HTTPS).

**Why it matters:** Protects against eavesdropping on the wire.

**Example:** TLS to warehouses, HTTPS to APIs, SSL to Postgres.

**Remember:**
- Enforce TLS everywhere practical
- Mind internal service mesh policies

---

### VPC

**Definition:** Virtual Private Cloud — isolated network for your cloud resources.

**Why it matters:** Network security and private connectivity.

**Example:** Data platform subnets with no public IPs; NAT for egress.

**Remember:**
- Segment public/private subnets
- Control egress for cost and security

---

### Private Endpoints

**Definition:** Private network interfaces to cloud services without public internet.

**Why it matters:** Keep data plane traffic off public network.

**Example:** S3/GCP Private Service Connect / Azure Private Link to storage and warehouses.

**Remember:**
- Prefer for production lake + warehouse access
- DNS and firewall rules matter
