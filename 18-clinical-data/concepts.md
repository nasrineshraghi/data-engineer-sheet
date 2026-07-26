# Clinical Data — Medications & Labs

Concepts data engineers need to model, join, and quality-check **medication** and **lab** data from EHRs and claims. Not clinical advice — data shape and pitfalls.

---

### Medication Order

**Definition:** A clinician’s request for a drug (what should be given) — often before dispense or administration.

**Why it matters:** Orders ≠ what the patient actually received; joining order→admin without care doubles or misses doses.

**Example:** Order: “Amoxicillin 500 mg PO TID × 7 days.” May never be dispensed if patient leaves AMA.

**Remember:**
- Grain is usually one row per order (or order line)
- Status matters: draft / active / completed / cancelled

---

### Medication Dispense

**Definition:** Pharmacy fills/gives out a supply of medication (quantity, NDC, days supply).

**Why it matters:** Claims and refill analytics often live at dispense grain, not administration.

**Example:** One order for 30 tablets → one dispense of 30; a refill is another dispense.

**Remember:**
- Dispense has quantity + days_supply
- Same drug can appear as different NDCs over time

---

### Medication Administration (MAR)

**Definition:** Record that a dose was given (or intentionally not given) to the patient — Medication Administration Record.

**Why it matters:** Inpatient adherence, dosing safety, and “did they get the antibiotic?” live here.

**Example:** Nurse documents ceftriaxone 1 g IV given at 2024-01-02 08:12.

**Remember:**
- Grain: usually one row per dose event
- “Not given” reasons are first-class data

---

### Order → Dispense → Administration Chain

**Definition:** The typical inpatient med pipeline: ordered → dispensed → administered (ambulatory often stops at dispense).

**Why it matters:** Analytics fail when you pick the wrong stage for the question.

**Example:** “Antibiotics within 1h of sepsis” needs **administration** time, not order time.

**Remember:**
- State which stage your metric uses
- Left joins across stages create fan-out

---

### Active Medication List

**Definition:** Medications believed current for the patient (home meds + active inpatient orders), not the full history.

**Why it matters:** Reconciliation and “on blood thinner?” checks use the active list, not every past order.

**Example:** Active: metformin, lisinopril. Historical: finished amoxicillin course last month.

**Remember:**
- Needs start/stop (or end) logic
- Stale “active” flags are a common EHR quality issue

---

### RxNorm

**Definition:** NIH normalized naming system for clinical drugs (ingredients, strength, dose form).

**Why it matters:** Maps messy local drug names to a shared code for analytics and interoperability.

**Example:** Map “Amox 500mg Cap” and “amoxicillin 500 mg capsule” → same RxNorm CUI/SCD.

**Remember:**
- Prefer RxNorm over free-text drug names for joins
- Strength + form are part of the concept

---

### NDC (National Drug Code)

**Definition:** FDA product identifier for how a drug is packaged (labeler + product + package).

**Why it matters:** Billing, inventory, and dispense feeds key off NDC; same clinical drug has many NDCs.

**Example:** Two manufacturers’ bottles of sertraline 50 mg → different NDCs, same RxNorm ingredient/strength.

**Remember:**
- NDC changes with package/manufacturer
- Map NDC → RxNorm for clinical rollups

---

### Sig / Dose / Route / Frequency

**Definition:** Structured (or semi-structured) instructions: how much (dose), how given (route), how often (frequency), plus free-text sig.

**Why it matters:** Free-text sig breaks analytics; structured fields enable dose and adherence measures.

**Example:** Dose `500`, unit `mg`, route `PO`, frequency `TID` vs sig `"one capsule by mouth three times daily"`.

**Remember:**
- Prefer structured columns; treat sig as secondary
- Unit mismatches cause 10× dosing errors in data

---

### Lab Order vs Lab Result

**Definition:** Order = request for a test; result = the reported value(s) for analyte(s).

**Why it matters:** Pending orders aren’t results; cancelled orders still clutter feeds.

**Example:** Order CBC → results for WBC, RBC, hemoglobin, platelets (multiple result rows).

**Remember:**
- One order can fan out to many result rows (panel)
- Always filter on result status (final vs preliminary)

---

### LOINC

**Definition:** Universal codes for lab observations and clinical measures (what was measured).

**Why it matters:** Local test names differ by lab; LOINC lets you compare “the same test” across sites.

**Example:** Serum creatinine assays from Lab A and Lab B → same LOINC `2160-0`.

**Remember:**
- Join/analytics on LOINC, not display name
- Same analyte can have multiple LOINCs (method/specimen)

---

### Reference Range

**Definition:** Lab’s expected normal low/high (or qualitative normal set) for a result, often age/sex/method specific.

**Why it matters:** “Abnormal” flags and clinical decision support depend on the range in force at result time.

**Example:** K+ result `5.8` with range `3.5–5.1` → high; same number might be normal for a different assay.

**Remember:**
- Store range with the result (don’t assume today’s range)
- Ranges differ by specimen and method

---

### Units of Measure (UCUM)

**Definition:** Standard representation of units (e.g. `mg/dL`, `mmol/L`) so values are comparable.

**Why it matters:** Mixing `mg/dL` and `mmol/L` without conversion silently corrupts trends.

**Example:** Glucose `100 mg/dL` ≈ `5.6 mmol/L` — not the same number.

**Remember:**
- Never chart mixed units without conversion
- Prefer UCUM codes alongside display units

---

### Specimen & Collection Time

**Definition:** What was collected (blood, urine, …) and **when** it was collected — distinct from result-reported time.

**Why it matters:** Clinical timelines use collection time; pipelines often only get result timestamp.

**Example:** Blood drawn 06:00, resulted 09:40 — sepsis bundle timing uses 06:00.

**Remember:**
- Prefer `collected_at` over `resulted_at` for physiology
- Wrong specimen type → wrong LOINC interpretation

---

### Quantitative vs Qualitative Results

**Definition:** Quantitative = numeric value; qualitative = categorical (Positive/Negative, Detected, …).

**Why it matters:** Averaging “Positive” or casting text to float fails; schemas must allow both.

**Example:** Troponin `0.04 ng/mL` (quant) vs COVID PCR `Detected` (qual).

**Remember:**
- Keep `value_num` and `value_text` (or typed columns)
- Don’t force all labs into one numeric column

---

### Abnormal / Critical Flags

**Definition:** Lab- or EHR-assigned markers that a result is abnormal, high/low, or critically out of range.

**Why it matters:** Alerts and quality metrics often key off flags, not only raw values.

**Example:** Flag `HH` (critically high) on potassium triggers rapid notification workflows.

**Remember:**
- Flags are not a substitute for storing the value + range
- Flag vocabularies differ by vendor

---

### Panel vs Analyte

**Definition:** Panel = ordered battery (CMP, CBC); analyte = individual measurable component.

**Why it matters:** Facts are usually at analyte-result grain; panel codes alone don’t give the numbers.

**Example:** CMP order → separate rows for sodium, potassium, creatinine, glucose, …

**Remember:**
- Model results at analyte grain
- Panel code is useful lineage, not the measure

---

### Encounter / Visit Context

**Definition:** The visit (inpatient encounter, ED visit, outpatient appointment) tying meds and labs to a care episode.

**Why it matters:** “Labs during admission” and “meds given this encounter” need encounter keys.

**Example:** Join `lab_result.encounter_id` to inpatient stay for length-of-stay cohorts.

**Remember:**
- Some labs are outpatient with weak encounter links
- Declare whether grain is patient-day, encounter, or event

---

### Clinical Event Time vs System Time

**Definition:** Event time = when it happened clinically (collected, administered); system time = when the EHR recorded/updated the row.

**Why it matters:** Late charting makes “system time” look like delayed care.

**Example:** Dose given at 08:00, documented at 11:30 — administration event time is 08:00.

**Remember:**
- Prefer clinical event timestamps for outcomes
- Keep both; use system time for pipeline freshness

---

### PHI in Meds & Labs

**Definition:** Medication and lab rows are Protected Health Information when identifiable (patient id + clinical facts).

**Why it matters:** Exports, logs, and lower environments need de-identification and access controls.

**Example:** A table of patient_id + HIV viral load is highly sensitive PHI.

**Remember:**
- Minimize columns in analytic extracts
- Audit access; never log full result payloads casually
