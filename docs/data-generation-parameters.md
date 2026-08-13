# Data generation parameters

> How much each variable changes

This document defines the five core formulas used to generate the synthetic dataset: conversion, call duration, CSAT, payment date, and costs. Each formula follows the same logic — a **base value** plus a set of **adjustments** that apply depending on the characteristics of the specific call, customer, or period, plus a small amount of **random noise** so the dataset does not look artificially clean

For categorical adjustments (e.g. campaign, age bracket), only the term that matches that specific row applies — the others are treated as 0, not summed together

Construction rules that are not formulas in themselves (dataset volume, tier/campaign distribution, passenger count, age variation across campaigns, call result/reason generation order) are documented separately in [`data-generation-rules.md`](data-generation-rules.md)

## Table of contents
- [1. Conversion](#1-conversion)
- [2. Call duration](#2-call-duration)
- [3. CSAT](#3-csat)
- [4. Payment date](#4-payment-date)
- [5. Costs](#5-costs)
- [6. Provisional items](#6-provisional-items)

## 1. Conversion

Conversion is evaluated **once per customer**, not once per call — see the generation order in [`data-generation-rules.md`](data-generation-rules.md). It determines whether a customer's contact cycle ends in a sale

### 1.1 Main effects

| Factor | Value | Rationale |
|---|---|---|
| **Base** (human agent, customer 36-45, Caribbean campaign) | 35% | Reasonable starting point for an effectively-contacted consultative sale |
| Agent = AI | +2 points | Small, deliberate effect — supports H2 (no significant difference), combined with AI's naturally small sample size (9 of 150 agents) |
| Age 18-25 | -3 points | Lower purchase decision power for costly travel products |
| Age 26-35 | -1 point | Close to the reference group |
| Age 36-45 | 0 (reference) | — |
| Age 46+ | +4 points | More established buyers, higher decision confidence |
| Campaign: Europe | -5 points | High price, harder decision |
| Campaign: Caribbean | 0 (reference) | — |
| Campaign: Cruise | -5 points | Same reasoning as Europe |
| Campaign: Vacation package | +5 points | Argentine destinations. Simple, low-price product, easier sale |

### 1.2 Agent × Campaign interaction (tests H7)

Applies **only** when the agent is AI; for human agents this adjustment is always 0 (already represented by the main effects above)

Consistent with `CAMPAIGN.product_type` and `AGENTS.agent_type`

| Campaign | AI adjustment | Rationale |
|---|---|---|
| Europe | -8 points | Humans clearly outperform AI on high-complexity, consultative sales |
| Caribbean | 0 | AI and human performance are comparable |
| Cruise | -6 points | Same reasoning as Europe |
| Vacation package | +10 points | Argentine destinations. AI outperforms on simple, low-touch sales |

### 1.3 Statistical design note (H2)

Non-significance for H2 is expected to emerge from the combination of a small main effect (+2 points) and the naturally small AI sample size (9 of 150 agents), not from adjusting a p-value directly

## 2. Call duration

Measured in seconds, consistent with `CALLS.call_duration_seconds` and related fields in the data model

| Factor | Value | Rationale |
|---|---|---|
| **Base** (human agent, Caribbean campaign, customer 36-45) | 360 sec | Typical consultative sale of medium complexity |
| Agent = AI | -120 sec | Less hold time, near-instant after-call work |
| Campaign: Europe | +180 sec | High complexity, requires consultative guidance |
| Campaign: Caribbean | 0 (reference) | — |
| Campaign: Cruise | +120 sec | Medium-high complexity |
| Campaign: Vacation package | -90 sec | Argentine destinations. Low complexity |
| Price > $2,500 | +90 sec | More negotiation on higher-ticket sales |
| Age 18-25 | -60 sec | More direct decision-making |
| Age 46+ | +90 sec | Longer calls, consistent with more passengers/consideration for this group |
| Random noise | ± normal, SD ~62-95 sec | Natural variability |

**Constraint:** for `call_result = Answered`, duration cannot go below **30-40 seconds** (a real conversation has a practical floor). This floor is specific to answered calls with a genuine conversation; unanswered/voicemail/busy calls follow a separate, near-zero floor defined in [`data-generation-rules.md`](data-generation-rules.md)

## 3. CSAT

Measured on a **1-10 scale**, consistent with `CALLS.csat_score`

| Factor | Value | Rationale |
|---|---|---|
| **Base** (human agent, average duration, no conversion) | 8.3 | Calibrated so the current pilot mix (94% human / 6% AI) averages above the 85% CSAT floor, while leaving room for the mix to matter |
| Conversion occurred | +1.5 | Strongest single driver of satisfaction |
| Agent = AI | -0.7 | Small, secondary effect — AI is not "worse" outright, only slightly less personal |
| Long duration (> 480 sec) | -0.3 | Friction/fatigue on calls that run long |
| Random noise | ± 0.3 to 0.5 | Normal survey variability |

**Business threshold translation:** the Brief's "minimum CSAT of 85%" is defined as `CSAT% = (average csat_score / 10) × 100`, i.e. **average csat_score ≥ 8.5**

With these parameters and the current pilot mix, the projected average CSAT is approximately **8.7-8.8**, comfortably above the 8.5 floor. The projected break-even point, where average CSAT would cross below 8.5 as AI share increases — is approximately **38-39% AI agents**, which gives the optimization model (H8) a meaningful, non-trivial constraint to respect rather than one that is always satisfied or always violated. CSAT scores are constrained to the valid 1–10 range after applying all adjustments and random noise

## 4. Payment date

Measured in days, added to the date of the call flagged as `Sales Closure`. Only exists if a sale occurred (see constraints)

| Factor | Value | Rationale |
|---|---|---|
| **Base** (customer 36-45, price ~$1,500, 2 passengers) | 5 days | Typical time between agreeing to purchase and completing payment |
| Age 18-25 | -3 days | More direct decision-making, faster payment |
| Age 46+ | +4 days | More passengers to coordinate, more deliberate decision |
| Price > $2,500 | +3 days | Needs to gather/finance a larger amount |
| Passenger count ≥ 5 | +2 days | Coordinating payment across several travelers takes longer |
| Random noise | ± 1 to 3 days | Natural variability |

**Constraints:** minimum 1 day after the sale closure call (never before, never same-day); maximum 20 days after sale closure

## 5. Costs

Costs are generated at a **monthly grain by cost category and agent type**, not per call or per sale — consistent with `FactCosts` in the dimensional model. Unit costs are multiplied by the number of agents/volume relevant to each cost category, so the same parameters can be recalculated for any human/AI mix the optimization model evaluates (not only the current 141/9 split)

### 5.1 Internal costs (paid by Contact Solutions)

| Category | Agent type | Cost type | Unit cost | Notes |
|---|---|---|---|---|
| Payroll (PHF) | Human | Fixed | $800/agent/month | Deliberately above the low end of the local market, to reduce attrition, a real and common BPO retention strategy |
| Commission to human agents (CHV) | Human | Variable, % of `sale_amount` | Nacional: 0.8% · Caribe: 1.1% · Cruceros/Europa: 1.5% | Tiered by campaign complexity, incentivizing higher-value/complex sales — smaller than independent travel-advisor commissions (5-20%) because these agents are salaried employees, not commission-only workers |
| Training (THF) | Human | Fixed | $60/agent/month | Amortized monthly cost of a $1,000-2,000 one-time onboarding investment |
| AI License (AIF) | AI | Fixed | $4,500/month base (proportional ~$500/agent) | Platform licensing fee, modeled as a flat fee split across AI agents for simplicity |
| Cloud Infrastructure (CAF) | AI | Fixed | $1,800/month | Base infrastructure cost for the AI voice platform |
| AI Usage (AIV) | AI | Variable | $0.0019/second of call time | In line with production conversational AI voice pricing |
| Supervision (SSF) | Shared | Fixed | $1,500/supervisor/month | Not pre-allocated between human and AI in the raw data, proportional allocation, if needed, happens in the analysis layer |

### 5.2 External revenue (paid by Global Experience to Contact Solutions)

| Campaign complexity | `commission_rate` (% of `sale_amount`) |
|---|---|
| Vacation package (argentine destination) | 10% |
| Caribbean | 12% |
| Cruise / Europe | 15% |

**Scope decision:** revenue is modeled exclusively as this variable, per-sale commission. No fixed monthly management fee is included — documented as an explicit scope decision in [`business-brief.md`](business-brief.md), since a constant fee does not change the optimal point of the optimization model regardless of its size

## 6. Provisional items

The following values are calibrated on illustrative volume assumptions and should be re-validated once real call and sale volumes exist (Phase 8 — Data Quality Validation):

- **Monthly budget constraint ($380,000):** whether this figure creates genuine tension between the CSAT floor and the budget across different human/AI mixes depends on the actual sales volume and campaign distribution generated in Phase 5. Confirm with real generated data before treating it as a fixed constraint in the optimization model
- **Commission-driven cost scaling:** the tiered `CHV`/`commission_rate` percentages are sized to stay within budget at illustrative volumes; confirm against actual generated `SALES` volume
