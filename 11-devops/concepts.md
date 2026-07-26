# DevOps for Data

---

### Docker

**Definition:** Package app + dependencies into portable container images.

**Why it matters:** Same Spark/Python job runs locally, CI, and prod.

**Example:** Image with `spark-submit` entrypoint and pinned library versions.

**Remember:**
- Pin base image digests for reproducibility
- Keep images lean; separate build vs runtime if needed

---

### Kubernetes

**Definition:** Orchestrates containers: scheduling, scaling, restarts, service discovery.

**Why it matters:** Common runtime for Spark-on-K8s, Airflow, Flink, microservices.

**Example:** SparkApplication CRD submits driver/executors as pods.

**Remember:**
- Requests/limits matter for stability
- Persistent volumes for stateful components

---

### CI/CD

**Definition:** Continuous Integration / Continuous Delivery — automate test and deploy of code/config.

**Why it matters:** Safe, repeatable pipeline and dbt/SQL changes.

**Example:** PR runs unit tests + SQL lint → merge deploys DAG to Airflow.

**Remember:**
- Test data contracts in CI
- Separate deploy of code vs heavy data backfills

---

### GitOps

**Definition:** Desired system state lives in Git; controllers sync cluster to match.

**Why it matters:** Auditable infra and app deploys.

**Example:** Argo CD applies Helm charts from `infra` repo on merge to main.

**Remember:**
- Git is source of truth
- PRs become change control

---

### Terraform

**Definition:** Declarative Infrastructure as Code tool (HCL) for cloud resources.

**Why it matters:** Reproducible buckets, IAM, warehouses, networks.

**Example:** Terraform creates S3 lake buckets, Glue catalog DB, IAM roles.

**Remember:**
- Remote state + locks
- Plan before apply; module wisely

---

### Helm

**Definition:** Package manager for Kubernetes — charts template K8s manifests.

**Why it matters:** Standard way to deploy Airflow, Spark operator, monitoring stacks.

**Example:** `helm upgrade --install airflow bitnami/airflow -f values.yaml`.

**Remember:**
- values.yaml is your config surface
- Version charts carefully

---

### Infrastructure as Code (IaC)

**Definition:** Define and version infrastructure in code (Terraform, CloudFormation, Pulumi, Bicep).

**Why it matters:** Repeatable environments; peer-reviewed changes.

**Example:** Dev/stage/prod lakes created from the same modules with different variables.

**Remember:**
- No click-ops for critical paths
- Codify networking, IAM, and data stores together
