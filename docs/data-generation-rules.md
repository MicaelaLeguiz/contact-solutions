# Data generation rules

> The data generation process covers four main components: dataset volume, distribution logic, functional constraints, and entity execution order

This document defines how the synthetic dataset is constructed: dataset scale, the distribution of customers and calls across tiers and campaigns, passenger count logic, age variation across campaigns, and the call result/reason generation sequence. These are structural generation rules, not formulas — the five parameter formulas (Conversion, Call duration, CSAT, Payment date, Costs) are documented separately in [`data-generation-parameters.md`](data-generation-parameters.md)

## Table of contents
- [1. Dataset scale](#1-dataset-scale)
- [2. Tier and campaign distribution](#2-tier-and-campaign-distribution)
- [3. Passenger count](#3-passenger-count)
- [4. Age variation across campaigns](#4-age-variation-across-campaigns)
- [5. Call result and call reason](#5-call-result-and-call-reason)

## 1. Dataset scale

| Parameter | Value |
|---|---|
| Calls/day per human agent | 42 to 46 |
| Calls/day per AI agent | 55 to 65 |
| Total calls/day (August baseline) | ~6850 |
| Working days — July | 23 |
| Working days — August | 21 |
| Working days — September | 22 |

The AI agent's higher daily volume is proportional to the time savings already defined in the Call duration formula (AI calls run ~33% shorter on average), rather than an arbitrarily chosen number

**Business-day rule:** `DATE_DIM.is_business_day` is `TRUE` for Monday through Friday and `FALSE` for Saturday and Sunday. Operational activity is generated only on dates where `is_business_day = TRUE`

**Scope of "calls":** the total daily/monthly call count includes **all** possible outcomes defined in `CALLS.call_result` (Answered, No Answer, Voicemail, Invalid Number, Busy, Customer Abandoned) — not only effectively answered calls. This total is projected across business days only, so monthly call volumes vary according to the number of operational days in each month

## 2. Tier and campaign distribution

Consistent with `CUSTOMERS.customer_tier` and `AGENTS.agent_type`

### 2.1 Customer tier distribution

| Tier | % of customers |
|---|---|
| Standard | 45% |
| Gold | 35% |
| Premium | 20% |

### 2.2 AI agent assignment by tier

| Tier | Human | AI |
|---|---|---|
| Standard | 94% | 6% |
| Gold | 95% | 5% |
| Premium | 96% | 4% |

This assignment mechanism, combined with the tier → campaign fidelity, creates a realistic and coherent correlation: AI is assigned more often to Standard-tier customers, who in turn are more likely to purchase simpler, lower-complexity campaigns — the same segment where the Conversion formula's agent×campaign interaction (Nacional) favors AI performance. This emerges from the combination of independently-defined rules, rather than being hardcoded

### 2.3 Calls by destination, by month

Consistent with `CAMPAIGNS.product_type` and `CAMPAIGNS.destination`

| Campaign | Destination | July | August | September |
|---|---|---|---|---|
| Cruise | Rio de Janeiro / Búzios | 33.5% | 28.3% | 32.1% |
| Cruise | Southern Caribbean & the Antilles | — | 6.4% | 14.5% |
| Europe | Madrid & Andalusia | — | 10.4% | 12.4% |
| Europe | French Riviera & Classic Italy | 8.5% | — | — |
| Caribbean | Punta Cana | 10.7% | 13.0% | 23.5% |
| Caribbean | Rivera Maya | 8.2% | 7.6% | — |
| Vacation Package (argentine destinations) | Bariloche | 16.5% | 9.2% | — |
| Vacation Package (argentine destinations) | Puerto Iguazú | 22.6% | 21.0% | 11.2% |
| Vacation Package (argentine destinations) | Ushuaia y los Cauquenes | — | 4.1% | 6.3% |

Each destination appears only in the months it is defined as active, consistent with the campaign working-month definitions established during data modeling

### 2.4 Tier → Campaign fidelity

The "recommended tier" for each campaign (defined during business rule design) is applied as a **probabilistic tendency, not an exclusivity rule** — a customer's tier increases the likelihood of purchasing a campaign recommended for that tier, but does not restrict them to it

| Tier | Fidelity to recommended campaigns |
|---|---|
| Standard | 70% |
| Gold | 70% |
| Premium | 50% |

Premium fidelity is set lower than Standard/Gold because Premium-recommended campaigns are not available every month (e.g. only one Premium destination is active in July), so a hard 70% fidelity would exceed the available Premium-campaign volume in that month. A 50% fidelity keeps every month's volume sufficient to hold the rule, while still telling a coherent business story: Premium customers are loyal, but seasonal offer availability pushes them toward Gold campaigns more often than Standard/Gold customers deviate from theirs

## 3. Passenger count

Consistent with `SALES.passenger_count`

Passenger count is defined by **three rules that must be reconciled**, since each one alone is incomplete

**Rule 1 — general probability distribution (base weights):**

| Passenger count | Probability |
|---|---|
| 1 | 11.7% |
| 2 | 61.3% |
| 3 or 4 | 18.9% |
| 5 or more | 8.1% |

**Rule 2 — allowed range by campaign (hard constraint):**

| Campaign | Allowed range |
|---|---|
| Cruise | 2 to 4 |
| Caribbean | exactly 2 |
| Europe | 1 to 4 |
| Vacation package | 2 to 4 |

**Rule 3 — preferred values by age (soft preference):**

| Age | Preferred values |
|---|---|
| 18-35 | 1-2 and 4-6 |
| 36-55 | 3-5 |
| 56+ | 2-4 |

**Reconciliation:** the destination defines the allowed range (Rule 2, hard constraint — never violated), and age tilts the probability distribution within that range (Rule 3, soft preference), starting from the general distribution (Rule 1) as the base weight before restricting/renormalizing it to the destination's allowed values. In other words: Rule 1 sets the starting weights, Rule 2 cuts the eligible values, and Rule 3 shifts weight toward the age-preferred values among what remains

## 4. Age variation across campaigns

To avoid an overly strong relationship between age and campaign in the statistical analysis (Q5), age is not generated fully independently of campaign — but it is also not perfectly correlated with it

| Campaign group | Typical age range |
|---|---|
| Standard-recommended | 18-45 |
| Gold-recommended | 36-65 |
| Premium-recommended | 46-75 |
| Gold and Premium (dual-recommended, e.g. Ushuaia y los Cauquenes) | 36-75 |

**Predominance:** 65% of customers buying a given campaign fall within that campaign's typical age range; the remaining 35% are drawn from the general customer age distribution (18-75, skewed toward older adults, as defined in the customer profile rules), not a uniform draw

## 5. Call result and call reason

### 5.1 Call result distribution

| Result | % |
|---|---|
| Answered | 54.9% |
| No Answer | 10.2% |
| Voicemail | 7.4% |
| Invalid Number | 9.4% |
| Busy | 5.1% |
| Customer Abandoned | 13.0% |

### 5.2 Call reason distribution

`call_reason` is only defined for `Answered` calls; for all other results, this field is empty

| Reason | % / Rule |
|---|---|
| Initial Contact | Governed by the first-contact rule (§ 5.3) |
| Follow-up | 39.8% |
| Commercial Inquiry | 25.5% |
| Sales Closure | Derived from the conversion outcome, not independently sampled (§ 5.3) |

### 5.3 Governing rules

- **Conversion rule:** if the per-customer conversion formula (see [`data-generation-parameters.md`](data-generation-parameters.md), §1) results in a sale, the final call in that customer's sequence is set to `call_result = Answered` and `call_reason = Sales Closure`. This is a derived outcome, not a separate random draw — `Sales Closure` cannot be sampled independently of the conversion formula, which prevents the two rules from contradicting each other
- **First-contact rule:** a customer can have only one `Initial Contact` call per `customer_id` per month
- Conversion is evaluated on answered calls, and `call_reason` is **not** used as a predictor in the conversion formula

### 5.4 Generation order

Conversion is evaluated once per customer, based on the customer's characteristics and assigned agent; it is not independently evaluated for each call

**If the customer converts:**
1. Apply the conversion rule (§ 5.3)
2. Determine how many calls it took to reach that outcome (between 1 and 15), counting **all** call attempts regardless of result (not only answered ones)
3. The last of those calls is set to `Answered` + `Sales Closure`
4. A `SALES` record is generated for that customer, referencing that call's date as `sale_date`
5. No further calls are generated for that customer
6. `Invalid Number` should not appear anywhere in a converting customer's call history — it would imply the company lost the ability to reach the customer

**If the customer does not convert:**
1. Generate up to 15 calls from the first contact, counting all attempt types
2. If any call results in `Invalid Number`, follow-up stops immediately
3. The process also stops if 20 days have passed since the first contact, whichever comes first — this cutoff can end the sequence before reaching 15 calls, but the sequence can never exceed 15 calls regardless of elapsed time
4. No `Sales Closure` reason and no `SALES` record are generated

### 5.5 Agent assignment

Each customer is assigned a single, fixed agent for the duration of a calendar month; all of that customer's calls within the month are handled by the same agent. The assignment can change from one month to the next. This resolves attribution cleanly, since `SALES` does not carry an `agent_id` — the agent (and agent type) responsible for a sale is always inferable from the customer and the month
