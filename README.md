# How much should be automated? A data-driven business decision

A data analytics portfolio project evaluating the operational and financial impact of introducing AI agents into a phone sales operation, under a hybrid human + AI workforce model — and using that evidence to define an optimal automation strategy under budget and quality constraints

## Table of contents
- [Overview](#overview)
- [Business context](#business-context)
- [Business problem](#business-problem)
- [Objectives](#objectives)
- [Research questions & hypotheses](#research-questions--hypotheses)
- [Scope](#scope)
- [Tech stack](#tech-stack)
- [Repository structure](#repository-structure)
- [Project status](#project-status)

## Overview

Companies adopting AI-powered conversational agents often frame the decision purely around cost reduction. This project treats it instead as a business decision that has to be backed by evidence: does replacing part of a human sales team with AI agents actually protect (or improve) conversion, customer satisfaction, and profitability — and if so, how far can that replacement go before something breaks?

The analysis is built as an end-to-end BI solution: dimensional data modeling, an ETL pipeline, descriptive and inferential statistics, executive and operational dashboards, and a simplified optimization model that recommends the human/AI mix that maximizes expected profit under real business constraints

## Business context

**Contact Solutions** is a fictional contact center provider serving clients across banking, retail, tourism, and professional services, with roughly 2,500 human agents. The company has launched a digital transformation initiative to gradually introduce AI agents into selected accounts

As a pilot, one of its tourism clients, **Global Experience**, ran a hybrid workforce for outbound vacation package sales over a three-month period: **150 agents total — 141 human, 9 AI**. Operational, commercial, and customer experience metrics were collected throughout, and this dataset is the basis for the analysis

Management needs to define the AI adoption strategy that maximizes expected business value while staying within a **monthly operating budget of USD 380,000** and maintaining a **minimum CSAT of 85%**, as required by the client.

## Business problem

Introducing AI agents creates a clear opportunity to cut operational costs, but its effect on conversion, customer satisfaction, and overall profitability is not yet proven. Expanding the hybrid model without evidence risks either damaging key business outcomes or leaving efficiency gains on the table. This project quantifies that impact to support an evidence-based scaling decision

## Objectives

**General objective:** analyze the operational and commercial impact of gradually introducing AI agents into a phone sales operation, to produce recommendations for expanding the hybrid model within the defined budget and quality constraints

**Specific objectives:**
1. Characterize current operational, commercial, and quality performance
2. Statistically compare the performance of human agents vs. AI agents
3. Propose a gradual adoption strategy backed by quantitative evidence and a simplified optimization model

## Research questions & hypotheses

**Main question:** What is the most convenient strategy for incorporating AI agents into a phone sales operation to maximize expected profit while balancing profitability, productivity, and service quality?

| # | Question | Type | Hypothesis |
|---|---|---|---|
| Q1 | How does the operation currently perform in terms of productivity, conversion, satisfaction, and profitability? | Exploratory | — |
| Q2 | Are there significant differences in conversion between human and AI agents? | Confirmatory | H2: No significant difference in overall conversion between agent types |
| Q3 | Do AI agents achieve higher average operational productivity than human agents? | Confirmatory | H3: AI agents show higher average operational productivity |
| Q4 | Does introducing AI agents reduce the operational cost per sale vs. human agents? | Confirmatory | H4: AI agents reduce the operational cost per sale |
| Q5 | Which variables are most associated with sales conversion? | Confirmatory | H5: Call duration, campaign type, channel, and agent type are associated with conversion probability |
| Q6 | Are there campaign segments where one agent type outperforms the other in conversion or productivity? | Exploratory | — |
| Q7 | Does profitability depend on the interaction between agent type and campaign type, or on agent type alone? | Confirmatory | H7: Profitability depends more on the agent type × campaign type combination than on agent type alone |
| Q8 | What proportion of human vs. AI agents maximizes expected profit under the budget and CSAT constraints? | Confirmatory | H8: There exists a human/AI mix that maximizes expected profit while simultaneously meeting the budget and CSAT constraints |

## Scope

**In scope**
- Analysis of one phone sales operation, for a single client (Global Experience)
- Comparative performance analysis: human vs. AI agents
- Multi-source data integration via an ETL process
- An analytical model to evaluate operational and commercial KPIs
- Executive and operational dashboards for different decision levels
- Descriptive and inferential statistical analysis on core KPIs
- A simplified optimization model to evaluate AI adoption scenarios
- Recommendations for the hybrid model's expansion strategy

**Out of scope**
- Machine Learning model development or training
- NLP or analysis of call content
- Design or implementation of the AI agents themselves
- Individual customer behavior prediction
- Real-time call routing optimization
- Integration with cloud or production infrastructure

**Constraints:** simulated data, three-month horizon, single client, no learning-curve effects, no seasonality effects, AI costs assumed constant

## Documentation

- [Business Brief](docs/business-brief.md) — Business context, objectives, stakeholders, hypotheses, and project scope

- [Methodology](docs/methodology.md) — Development approach and project workflow

- [Roadmap](docs/roadmap.md) — Project phases, deliverables, and current status

- [Operational Data Model](docs/data-model/operational-data-model.png) — Entity-relationship model of the operational database

- [Dimensional Data Model](docs/data-model/dimensional-data-model.png) — Star schema used for analytics and reporting

- [KPI Dictionary](docs/kpi-dictionary.md) — Business definitions and calculation logic for all KPIs

- [Data Dictionary](docs/data-dictionary.md) — Metadata and business rules for all analytical tables and columns

## Tech stack

- **SQL (SQLite)** — data loading and business queries
- **Python (Pandas)** — ETL, descriptive and inferential statistics
- **Power BI** — executive and operational dashboards

## Repository structure

```
contact-solutions/
│
├── README.md
├── docs/
│   ├── business-brief.md
│   ├── methodology.md
│   ├── roadmap.md
│   ├── kpi-dictionary.md
│   ├── data-dictionary.md
│   └── data-model/
│       ├── operational-data-model.dbml
│       ├── operational-data-model.png
│       ├── dimensional-data-model.dbml
│       └── dimensional-data-model.png
```

As the project advances into ETL, SQL queries, statistical analysis, the optimization model, and dashboards, the corresponding folders (`etl/`, `sql/`, `notebooks/`, `dashboards/`) will be added and documented here

## Project status

🟢 In progress

🚧 **Current phase:**
- Data Modeling
- Documentation

See the complete project roadmap in the documentation: - [Roadmap](docs/roadmap.md)

## About the Author

**Micaela Leguizamon** — Data Analyst with a background in UX Research

- LinkedIn: [linkedin.com/in/micaela-leguiz](https://www.linkedin.com/in/micaela-leguiz/)
- Portfolio: [micaelaleguiz.framer.website](https://micaelaleguiz.framer.website/)
