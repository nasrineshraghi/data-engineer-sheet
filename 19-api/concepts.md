# APIs for Data Engineers

How data engineers **pull, push, and design** APIs for pipelines — REST, auth, pagination, rate limits, webhooks, and contracts.

---

### REST API

**Definition:** HTTP API that manipulates resources with methods like GET, POST, PUT/PATCH, DELETE and status codes.

**Why it matters:** Most SaaS extracts and internal services speak REST; pipelines are HTTP clients first.

**Example:** `GET /v1/orders?updated_since=2024-01-01` → JSON list of orders.

**Remember:**
- Idempotent methods: GET, PUT, DELETE (when designed correctly)
- 2xx success, 4xx your fault, 5xx retry carefully

---

### Endpoint / Resource

**Definition:** A URL path that represents a collection or item (`/customers`, `/customers/{id}`).

**Why it matters:** Your extract grain and join keys usually follow resource design.

**Example:** `/patients/{id}/labs` returns lab results for one patient.

**Remember:**
- Path params identify; query params filter/sort/page
- Stable resource IDs beat fuzzy name matches

---

### Request / Response

**Definition:** Client sends a request (method, URL, headers, body); server returns a response (status, headers, body).

**Why it matters:** Logging only the body loses status and rate-limit headers you need to debug.

**Example:** Request `Authorization: Bearer …` → Response `200` + JSON payload.

**Remember:**
- Capture status, latency, and `Retry-After`
- Never log secrets (tokens, API keys)

---

### JSON / Payload Schema

**Definition:** Structured body format (usually JSON) with an agreed shape for fields and types.

**Why it matters:** Schema drift breaks pipelines; optional fields become required without notice.

**Example:** `{ "order_id": "O-1", "total_cents": 1999, "currency": "USD" }`

**Remember:**
- Version fields or use a schema registry/contract
- Prefer explicit nulls over omitting keys inconsistently

---

### Status Codes

**Definition:** Numeric HTTP outcomes: 2xx OK, 3xx redirect, 4xx client error, 5xx server error.

**Why it matters:** Retry logic must distinguish “bad request” from “try again.”

**Example:** `429 Too Many Requests` → back off; `401` → refresh auth, don’t hammer.

**Remember:**
- Don’t retry 400/401/403/404 blindly
- 409 conflict often needs upsert/merge semantics

---

### Authentication vs Authorization

**Definition:** Authentication = who you are; authorization = what you’re allowed to do.

**Why it matters:** A valid token can still lack scope to read the dataset you need.

**Example:** Service authenticates with OAuth client credentials but isn’t authorized for `/admin/exports`.

**Remember:**
- Check scopes/roles when extracts return empty
- Rotate credentials; store in a secret manager

---

### API Key

**Definition:** Static secret sent in a header or query param to identify the calling app.

**Why it matters:** Simple but easy to leak in logs, notebooks, and git.

**Example:** Header `X-API-Key: sk_live_…`

**Remember:**
- Prefer header over query string (URLs get logged)
- Treat like a password; never commit

---

### OAuth 2.0 / Bearer Token

**Definition:** Delegated auth where the client gets a short-lived access token (often refreshable).

**Why it matters:** Most modern SaaS APIs require token refresh in long-running pipelines.

**Example:** Client credentials → `access_token` → `Authorization: Bearer <token>`.

**Remember:**
- Refresh before expiry; handle 401 with one retry
- Cache tokens; don’t request a new one per page

---

### Pagination

**Definition:** Splitting large result sets across pages (offset/limit, cursor/token, or page numbers).

**Why it matters:** Full extracts die without pagination; naive offset pages drift under concurrent writes.

**Example:** `GET /events?cursor=eyJpZCI6MTAwfQ&limit=500`

**Remember:**
- Prefer cursor pagination for stable extracts
- Stop when next cursor is null/empty

---

### Rate Limiting

**Definition:** Server caps how many requests you can make per window (per key, IP, or tenant).

**Why it matters:** Ignoring limits causes 429s, bans, and incomplete loads.

**Example:** 100 req/min; response headers `X-RateLimit-Remaining: 0`, `Retry-After: 30`.

**Remember:**
- Respect `Retry-After`
- Parallelism × pages can explode QPS

---

### Idempotency Key

**Definition:** Client-supplied key so retries of the same write are applied once.

**Why it matters:** Network timeouts cause duplicate POSTs without idempotency.

**Example:** Header `Idempotency-Key: load-2024-01-01-batch-7` on `POST /charges`.

**Remember:**
- Critical for payment and webhook-driven writes
- Keys should be deterministic per business event

---

### Webhook

**Definition:** Server pushes an HTTP callback to your URL when an event happens (vs you polling).

**Why it matters:** Near-real-time ingest without constant polling cost.

**Example:** Stripe sends `POST /hooks/stripe` with `invoice.paid` payload.

**Remember:**
- Verify signatures; reject unsigned calls
- Make handlers idempotent — deliveries retry

---

### Polling vs Event-Driven

**Definition:** Polling periodically GETs for changes; event-driven consumes webhooks/streams as events arrive.

**Why it matters:** Polling is simple but laggy/expensive; events need reliable endpoints.

**Example:** Poll `updated_since` every 5 minutes vs webhook on `order.updated`.

**Remember:**
- Polling needs a high-water mark
- Combine: webhook + nightly reconcile poll

---

### API Contract / OpenAPI

**Definition:** Documented agreement on paths, params, schemas, and errors (often OpenAPI/Swagger).

**Why it matters:** Contracts let you generate clients and catch breaking changes in CI.

**Example:** OpenAPI spec declares `Order.total_cents` as integer required.

**Remember:**
- Consumer-driven checks on staging
- Breaking change = version bump

---

### Versioning

**Definition:** Evolving an API without breaking clients (`/v1`, `/v2`, or header versions).

**Why it matters:** Unversioned breaking changes silently empty or corrupt warehouses.

**Example:** `/v1/orders` keeps old shape while `/v2/orders` renames fields.

**Remember:**
- Pin version in pipeline config
- Run dual-read during migrations

---

### Timeout / Retry / Backoff

**Definition:** Client gives up after N ms; retries failed calls with increasing delay (and jitter).

**Why it matters:** Aggressive retries amplify outages; no retries drop data.

**Example:** Timeout 30s; retry 5xx/429 with exponential backoff + jitter.

**Remember:**
- Cap max retries and total time
- Idempotent retries only for safe/write-keyed calls

---

### Synchronous vs Asynchronous API

**Definition:** Sync returns the final result in one response; async accepts work and returns a job id to poll or webhook later.

**Why it matters:** Big exports are often async — treating them as sync causes timeouts.

**Example:** `POST /exports` → `202` + `job_id` → poll `/exports/{job_id}` until `download_url`.

**Remember:**
- Store job ids for recovery
- Don’t block an Airflow worker for hours without deferral

---

### GraphQL (Basics)

**Definition:** Query language API where the client asks for exact fields in one request (vs many REST round-trips).

**Why it matters:** Flexible reads; easy to over-fetch or hit cost/complexity limits.

**Example:** Query `{ order(id:"O-1") { id total items { sku qty } } }`

**Remember:**
- Paginate connections explicitly
- Watch rate/cost limits on nested queries

---

### gRPC / Protobuf (Basics)

**Definition:** Binary RPC framework using Protocol Buffers — common for internal low-latency services.

**Why it matters:** Faster than JSON REST inside the datacenter; schemas are strongly typed.

**Example:** `GetOrder(OrderRequest) returns (Order)` over HTTP/2.

**Remember:**
- Need stub generation and proto versioning
- Harder to curl; invest in tooling

---

### Change Data via API (Incremental Extract)

**Definition:** Pull only new/changed rows using cursors, `updated_at` filters, or event APIs.

**Why it matters:** Full dumps don’t scale; incremental needs trustworthy watermarks.

**Example:** `GET /objects?updated_after={watermark}&sort=updated_at`

**Remember:**
- Overlap windows to avoid missing late updates
- Periodic full reconcile catches API gaps

---

### SLA / Quotas

**Definition:** Provider promises (latency, uptime) and hard caps (rows/day, concurrent calls).

**Why it matters:** Pipeline design must fit quotas or fail mid-load.

**Example:** Free tier 10k calls/day; enterprise 100 concurrent connections.

**Remember:**
- Budget calls per DAG run
- Alert before quota exhaustion
