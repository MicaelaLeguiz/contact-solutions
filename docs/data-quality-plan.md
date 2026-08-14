# Data quality plan

This document defines the data quality issues intentionally introduced into the synthetic dataset, along with their business rationale, expected sample size, and the SQL/Power Query technique used to detect and correct each one. Injecting realistic, explainable data quality issues — rather than generating a "too clean" dataset — is a deliberate design choice: it demonstrates real cleaning and transformation work in Phase 6 (ETL) and gives Phase 8 (Data quality validation) something concrete to check against

Each issue below is tied to a business reason already established elsewhere in this project's documentation (data source ownership, refresh cadence, or a payment/business rule) — none are injected arbitrarily

## Table of contents
- [1. COSTS (Excel source)](#1-costs-excel-source)
- [2. CALLS](#2-calls)
- [3. SALES](#3-sales)
- [4. CAMPAIGNS](#4-campaigns)
- [5. Validation approach](#5-validation-approach)

## 1. COSTS (Excel source)

**Scope:** 100% of records. Unlike the issues below, these are not random/row-level errors — they reflect the *structural format* in which the source file is always exported, consistent with `FactCosts` being sourced from a Finance-maintained Excel file rather than the main ETL pipeline (documented in `data-dictionary.md`)

| # | Issue | Business rationale | Fix (Power Query) |
|---|---|---|---|
| 1 | Date exported as `mm-aaaa` instead of a proper date | Common export format from accounting/ERP systems | Transform to the first day of the month — matches `FactCosts`' monthly grain |
| 2 | Amount exported as text instead of a number | Very common in accounting/ERP exports | Change type: text → number |
| 3 | Decimal separator is `.` instead of `,` | Finance uses an international ERP that exports in US number format, while the rest of the project uses Argentine/European format | Locale-aware number conversion |
| 4 | Wide format: cost categories as columns instead of rows | Typical layout for a Finance-maintained report | **Unpivot** — this is the transformation that justifies loading this specific source through Power Query rather than the main SQL pipeline |
| 5 | Extra header rows above the real table (company title, export date, a simulated logo) | Typical of manually-maintained Finance reports | "Remove top rows" before the Unpivot step |
| 6 | `agent_type` in Spanish ("Humano"/"IA"/"Compartido") instead of English ("Human"/"AI"/"Shared"), as used in the dimensional model | Reflects that this source comes from a different team (Contact Solutions Finance) than `AGENTS`, which comes from the CRM — the same "two systems, two owners" dynamic already documented for the operational model | Value standardization (`CASE`/replace step) |

## 2. CALLS

**Sample size:** stated per month. Issues **can overlap on the same row** (e.g. a call can be both a duplicate and carry a negative duration) — this is intentional, reflecting how data quality issues actually compound in production data rather than occurring in isolation
| # | Issue | Sample size | Business rationale | Detection (SQL) |
|---|---|---|---|---|
| 1 | Duplicate `call_id` | 3% of monthly calls | Simulates the source system re-logging the same event on retry | `GROUP BY ... HAVING COUNT(*) > 1`, or `ROW_NUMBER() OVER (PARTITION BY call_id ...)` to keep a single version |
| 2 | Negative `call_duration_seconds` | 1% of monthly calls | Simulates a capture glitch — the duration is first calculated normally (as the sum of its component fields) and then flipped negative, rather than being generated as a nonsensical value directly | Recalculate from the underlying duration components (ACD + retention + ACW) |
| 3 | Orphan records (`customer_id` not found in `CUSTOMERS`) | 3% of monthly calls | `CUSTOMERS` refreshes monthly while `CALLS` are captured continuously (documented refresh cadence in `data-dictionary.md`) — a customer added by Global Experience mid-month can start receiving calls before appearing in the next customer master update | `LEFT JOIN CUSTOMERS ON CALLS.customer_id = CUSTOMERS.customer_id WHERE CUSTOMERS.customer_id IS NULL` |

**Orphan record resolution process** (documented here since it is a multi-step process, not a single query):
1. Detect orphans with the `LEFT JOIN` above
2. Isolate them in a separate table (`calls_quarantine`) — do not silently drop them or leave them mixed into the clean dataset
3. Quantify and document them in the data quality report (Phase 8): what % of calls were orphaned, and why
4. In a production pipeline, these would be reprocessed against the next customer master update. In this fixed 3-month dataset, the orphan records remain quarantined and are excluded from the clean analytical layer

## 3. SALES

**Sample size:** determined by the `payment_status` distribution — Paid: 90.1%, Pending: 7.6%, Cancelled: 2.3%

| Issue | Business rationale | Fix (SQL) |
|---|---|---|
| `paid_amount = 0` used as a "filler" value when `payment_status` is `Pending` or `Cancelled`, instead of `NULL` | If a payment hasn't been completed yet, no amount has actually been collected — `0` is not a real observed value, it is a placeholder that the cleaning step needs to correct | Convert to true `NULL`, surgically, only for the affected rows: `UPDATE sales_clean SET paid_amount = NULL WHERE payment_status IN ('Pending','Cancelled') AND paid_amount = 0;` — rows with `payment_status = 'Paid'` are never touched by this rule |

This is a case of a null with a genuine business justification, not a missing-data error — the cleaning logic reflects that distinction rather than blindly imputing or dropping the value

## 4. CAMPAIGNS

**Sample size:** 100% of records. Like the Costs Excel source, this is a structural formatting issue in how the CRM exports this field, not a random per-row error

| Issue | Business rationale | Fix (SQL) |
|---|---|---|
| `country` and `destination` arrive concatenated in a single field (e.g. `"ARGENTINA-BARILOCHE"`), fully uppercased | Reflects the raw CRM export format, before the ETL applies the dimensional model's already-defined `destination`/`country` columns | Split the field (`SUBSTRING`/`SPLIT` on the delimiter) into two columns, then apply proper-case formatting |

This transformation is applied to a **raw staging version** of `CAMPAIGNS`, not the already-modeled dimensional table — the SQL split/format step is what turns the raw CRM extract into the clean `destination`/`country` columns already defined in the dimensional model

## 5. Validation approach

Each issue above has a known, documented sample size. When the SQL cleaning queries run against the generated dataset (Phase 6 of 8), the count of detected and corrected rows should match. For row-level issues, detected counts should match the expected percentages within a small margin. Structural source-format issues should affect 100% of the relevant records by design.

This turns the document into a validation checklist, not just a design record: if a cleaning query finds a significantly different count than what was designed here, it signals a need to check the generation script rather than assume the query is correct
