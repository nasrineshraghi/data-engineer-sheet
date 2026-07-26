# File Formats for Data Engineers

Columnar and row formats you’ll meet in lakes, warehouses, and pipelines — especially **Parquet**, plus Avro, ORC, and text formats.

---

### Parquet

**Definition:** Columnar binary file format with per-column compression, stats (min/max), and nested types (often via Arrow/Spark).

**Why it matters:** Default for analytics lakes — scans read only needed columns and prune with stats.

**Example:** `df.write.mode("overwrite").parquet("s3://lake/events/")`

**Remember:**
- Great for OLAP; not ideal for single-row point lookups
- Schema is embedded in the file footer

---

### Columnar vs Row-Oriented

**Definition:** Columnar stores values by column across rows; row-oriented stores whole rows together (CSV, JSON lines, Avro records).

**Why it matters:** Analytics queries touch few columns — columnar cuts I/O dramatically.

**Example:** SELECT `user_id, amount` from a 200-column Parquet table reads ~2 columns, not all 200.

**Remember:**
- Lakes/warehouses → columnar
- Event logs / streaming payloads → often row (Avro/JSON)

---

### Compression Codec

**Definition:** Algorithm used inside a format (Snappy, ZSTD, Gzip, LZ4, Brottli, …).

**Why it matters:** Codec tradeoff is CPU vs size vs splittability for parallel reads.

**Example:** Parquet + Snappy for fast ETL; ZSTD for colder, denser storage.

**Remember:**
- Prefer splittable codecs for large files in Spark
- Don’t double-compress (Gzip whole file *and* inner Parquet)

---

### Snappy / ZSTD / Gzip

**Definition:** Common codecs — Snappy (fast), ZSTD (strong ratio, tunable), Gzip (ubiquitous, often slower / less friendly for splits).

**Why it matters:** Wrong codec slows jobs or bloats S3 bills.

**Example:** `parquet.compression=zstd` in Spark writer options.

**Remember:**
- Snappy ≈ speed; ZSTD ≈ size
- Gzip’d CSV is common but painful at scale

---

### Row Group / Stripe

**Definition:** Parquet row group (or ORC stripe) — a horizontal chunk of rows with its own column chunks and stats.

**Why it matters:** Predicate pushdown and parallelism operate at this granularity.

**Example:** 128MB row groups; filter `dt='2024-01-01'` skips row groups whose max(dt) is older.

**Remember:**
- Too-small row groups → many footers / files overhead
- Too-large → weaker prune + heavy memory

---

### Page / Column Chunk

**Definition:** Inside a row group, each column is stored as chunks/pages (data + optional dictionary page).

**Why it matters:** Dictionary encoding and page stats speed decoding and filters.

**Example:** Low-cardinality `country` column stores a dictionary once per chunk.

**Remember:**
- Dictionary encoding shines on low cardinality
- High-cardinality strings may skip dictionaries

---

### Parquet Footer / Footer Statistics

**Definition:** Trailing metadata in a Parquet file: schema, row-group offsets, and min/max/null counts per column chunk.

**Why it matters:** Engines read the footer first to prune row groups without scanning data.

**Example:** Query `WHERE amount > 1000` skips row groups with `max(amount) <= 1000`.

**Remember:**
- Corrupt/truncated footers make files unreadable
- Stats enable skip; they don’t replace partition layout

---

### Predicate Pushdown (Files)

**Definition:** Pushing filters into the scan so the reader skips row groups/pages using stats (and partitions).

**Why it matters:** “Filter early” only works if the format + layout expose prune-able metadata.

**Example:** Spark reads Parquet with `filter("event_date = '2024-01-01'")` → partition + row-group prune.

**Remember:**
- Works best with Parquet/ORC + partition columns
- Casts/functions on columns can disable prune

---

### Schema Evolution (Files)

**Definition:** Adding/renaming/dropping fields over time while old files remain readable.

**Why it matters:** Lakes accumulate files written under different schemas.

**Example:** New column `device_type` added; old Parquet files return null for that field.

**Remember:**
- Prefer additive changes; renames break readers
- Table formats (Iceberg/Delta) track schema history better than raw files alone

---

### Avro

**Definition:** Row-oriented binary format with a JSON schema; common in Kafka and streaming.

**Why it matters:** Compact, schema’d events; evolved with Schema Registry.

**Example:** Produce `OrderCreated` Avro to Kafka; Spark Structured Streaming reads with from_avro.

**Remember:**
- Better for write-heavy / record-at-a-time than wide analytics scans
- Pair with schema registry for compatibility

---

### ORC

**Definition:** Columnar format popular in Hive ecosystems (stripes, indexes, ACID tables historically).

**Why it matters:** Still common in Hadoop/Hive estates alongside Parquet.

**Example:** Hive table `STORED AS ORC` with ZLIB compression.

**Remember:**
- Similar goals to Parquet (columnar + stats)
- Prefer one columnar standard per lake when possible

---

### Arrow (In-Memory)

**Definition:** Columnar in-memory representation (and IPC/flight) used by pandas, Spark, DuckDB, etc.

**Why it matters:** Zero-copy interchange between engines; Parquet ↔ Arrow is a common path.

**Example:** `pyarrow.parquet.read_table(...)` → Arrow table → pandas.

**Remember:**
- Arrow ≠ on-disk lake format (though IPC files exist)
- Speeds Python/Spark handoffs

---

### CSV

**Definition:** Delimited text rows; no embedded types or compression standards.

**Why it matters:** Universal exchange format; terrible default for large analytics.

**Example:** `user_id,event_time,amount`

**Remember:**
- Ambiguous types, escaping, encodings (UTF-8 vs Latin-1)
- Convert to Parquet early in the lake

---

### JSON / JSON Lines (NDJSON)

**Definition:** JSON objects — as an array file or one object per line (JSONL/NDJSON).

**Why it matters:** APIs and logs emit JSON; nested fields map unevenly to tables.

**Example:** `{"id":1,"items":[{"sku":"A"}]}` per line in `.jsonl`.

**Remember:**
- JSONL streams better than one giant array
- Inferring schema from JSON is fragile — enforce a contract

---

### Delta / Iceberg / Hudi Data Files

**Definition:** Open table formats that store data mainly as Parquet (sometimes ORC) plus transaction metadata.

**Why it matters:** You still tune Parquet layout; the table layer adds ACID, time travel, and compaction.

**Example:** Delta `OPTIMIZE` rewrites small Parquet files into larger ones.

**Remember:**
- Table format ≠ replacing Parquet — it orchestrates Parquet files
- Small-file problems are still Parquet layout problems

---

### File Size Tuning

**Definition:** Targeting healthy on-disk sizes (often ~128MB–1GB compressed) per file for engine parallelism.

**Why it matters:** Tiny files kill listing/planning; huge files hurt split balance and recovery.

**Example:** Compact 10,000 × 2MB Parquet files → ~200 × 100MB files.

**Remember:**
- Streaming micro-batches create small files — schedule compaction
- Aim for fewer, fatter files in hot tables

---

### Splittable File

**Definition:** A file that workers can read in byte-range splits in parallel (e.g. uncompressed or block-compressed Parquet).

**Why it matters:** Non-splittable Gzip CSV forces one task per file.

**Example:** 8GB Gzip CSV → one giant task; 8GB Parquet → many parallel tasks.

**Remember:**
- Parquet/ORC are designed for parallel reads
- Avoid Gzip-on-the-outside for big batch inputs

---

### Partition Layout (Files on Disk)

**Definition:** Directory layout like `dt=2024-01-01/country=US/*.parquet` that engines prune by path.

**Why it matters:** Partition columns are the coarsest, cheapest filter.

**Example:** `s3://lake/events/dt=2024-01-01/*.parquet`

**Remember:**
- Don’t over-partition (e.g. by user_id → millions of folders)
- Partition on selective, commonly filtered columns (often date)

---

### Manifest / File List

**Definition:** Inventory of data files belonging to a table version (Iceberg/Delta manifests; Hive directory listing).

**Why it matters:** Planning queries means knowing which files to read — listing millions of objects is slow.

**Example:** Iceberg manifest lists Parquet paths for snapshot `N`.

**Remember:**
- Table formats avoid repeated S3 LIST storms
- Raw Hive-style dirs scale poorly with file count

---

### Bloom Filter (Parquet)

**Definition:** Optional probabilistic structure to skip row groups that definitely don’t contain a value.

**Why it matters:** Helps selective point-ish filters on high-cardinality columns when stats alone aren’t enough.

**Example:** Enable bloom filters on `order_id` for “fetch these ids” style scans.

**Remember:**
- Not a replacement for an index/DBMS
- Extra write CPU and metadata size

---

### Encoding (Dictionary / RLE / Plain)

**Definition:** How column values are packed — dictionary, run-length, delta, plain bytes, etc.

**Why it matters:** Right encoding shrinks files and speeds decode for repetitive data.

**Example:** Booleans and repeated enums compress extremely well with RLE/dictionary.

**Remember:**
- Engines usually choose encodings automatically
- Cardinality drives dictionary effectiveness
