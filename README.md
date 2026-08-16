# How much should be automated?
## A data-driven approach to optimizing Human–AI workforce allocation

# ¿Cuánto automatizar?
## Un enfoque basado en datos para optimizar la combinación de agentes humanos e IA

*A data analytics portfolio project evaluating the operational and financial impact of introducing AI agents into a phone sales operation under a hybrid human–AI workforce model, using data to define an optimal automation strategy within budget and service quality constraints.*

---

> The project documentation is written in English. A brief introduction is also provided in Spanish
> 
---

## Table of contents
- [Overview](#1-overview)
- [Overview (Spanish)](#1-descripción-general)
- [Business context](#2-business-context)
- [Business problem](#3-business-problem)
- [Objectives](#4-objectives)
- [Research questions](#5-research-questions)
- [Scope](#6-scope)
- [Documentation](#7-documentation)
- [Tech stack](#8-tech-stack)
- [Repository structure](#9-repository-structure)
- [Project status](#10-project-status)
- [About the author](#11-about-the-author)

## 1. Overview

As AI-powered conversational agents become increasingly capable, organizations face a critical business question: **How much of a customer-facing operation should actually be automated?**

Replacing human agents with AI promises lower operating costs, but reducing costs alone does not guarantee better business outcomes. Conversion, customer satisfaction, and profitability may improve—or deteriorate—as automation increases. This project approaches AI adoption as a business decision rather than a technology initiative. It develops an end-to-end Business Intelligence solution to evaluate the operational and financial impact of introducing AI agents into a phone sales operation and determine the workforce composition that maximizes expected profit while respecting budget and service quality constraints. The solution combines dimensional data modeling, ETL processes, statistical analysis, executive and operational dashboards, and a simplified optimization model respecting budget and service quality constraints

Although the case study focuses on a contact center, the analytical framework can be applied to organizations across different industries facing similar automation decisions

## 1. Descripción general

> Spanish summary. The complete project documentation is available in English

La incorporación de agentes conversacionales impulsados por inteligencia artificial plantea una pregunta cada vez más relevante para las organizaciones: **¿cuánto conviene automatizar una operación sin comprometer los resultados del negocio?**

Reemplazar agentes humanos por IA promete reducir costos operativos, pero hacerlo no garantiza mejores niveles de conversión, satisfacción del cliente o rentabilidad. Este proyecto aborda la automatización como una decisión de negocio respaldada por datos. Para ello desarrolla una solución integral de Business Intelligence que combina procesos ETL, modelado dimensional, análisis estadístico, dashboards ejecutivo y operacional y un modelo simplificado de optimización para identificar la combinación de agentes humanos e IA que maximiza el beneficio esperado respetando restricciones de presupuesto y calidad del servicio

Aunque el caso de estudio se desarrolla sobre un contact center, la metodología puede aplicarse a organizaciones de diferentes industrias que enfrenten decisiones similares sobre automatización

## 2. Business context

**Contact Solutions** is a fictional contact center provider serving clients across banking, retail, tourism, and professional services, with roughly 2,500 human agents. The company has launched a digital transformation initiative to gradually introduce AI agents into selected accounts

As a pilot, one of its tourism clients, **Global Experience**, ran a hybrid workforce for outbound vacation package sales over a three-month period: **150 agents total — 141 human, 9 AI**. Operational, commercial, and customer experience metrics were collected throughout, and this dataset is the basis for the analysis

Management needs to define the AI adoption strategy that maximizes expected business value while staying within a **monthly operating budget of USD 380,000** and maintaining a **minimum CSAT of 85%**, as required by the client

## 3. Business problem

Introducing AI agents creates a clear opportunity to cut operational costs, but its effect on conversion, customer satisfaction, and overall profitability is not yet proven. Expanding the hybrid model without evidence risks either damaging key business outcomes or leaving efficiency gains on the table. This project quantifies that impact to support an evidence-based scaling decision

## 4. Objectives

**Objective:** analyze the operational and commercial impact of gradually introducing AI agents into a phone sales operation, to produce recommendations for expanding the hybrid model within the defined budget and quality constraints

**Specific objectives:**
1. Characterize current operational, commercial, and quality performance
2. Statistically compare the performance of human agents vs. AI agents
3. Propose a gradual adoption strategy backed by quantitative evidence and a simplified optimization model

## 5. Research questions

This project investigates the following business questions:

- What is the optimal human/AI workforce composition for a phone sales operation?
- Do AI agents perform differently from human agents in terms of conversion, productivity, costs, and customer satisfaction?
- Which operational factors have the greatest impact on sales conversion?
- How can statistical analysis and optimization support AI adoption decisions?

The complete list of research questions and hypotheses is available in the [Business brief](docs/business-brief.md)

## 6. Scope

### In scope

- Comparative analysis of human and AI agents in a phone sales operation
- Design and generation of a synthetic dataset with a documented, business-driven generation logic
- ETL pipeline integrating multiple operational data sources, with two analytical destinations (SQLite and BigQuery)
- Analytical data model and KPI framework
- Executive (Power BI) and operational (Looker Studio) dashboards
- Descriptive, inferential, and optimization-based analysis
- Business recommendations for AI adoption

### Out of scope

- Machine Learning model development
- NLP and conversation analysis
- AI implementation
- Real-time optimization
- Integration with live production systems or real-time infrastructure

See the complete project scope, assumptions, and constraints in the [Business brief](docs/business-brief.md)

## 7. Documentation

- [Business brief](docs/business-brief.md) — Business context, objectives, stakeholders, hypotheses, and project scope
- [Methodology](docs/methodology.md) — Development approach and project workflow
- [Roadmap](docs/roadmap.md) — Project phases, deliverables, and current status
- [Operational data model](docs/data-model/operational-data-model.dbml) ([View image](docs/data-model/operational-data-model.png)) — Entity-relationship model of the operational database
- [Dimensional data model](docs/data-model/dimensional-data-model.dbml) ([View image](docs/data-model/dimensional-data-model.png)) — Schema used for analytics and reporting
- [KPI dictionary](docs/kpi-dictionary.md) — Business definitions and calculation logic for all KPIs
- [Data dictionary](docs/data-dictionary.md) — Metadata and business rules for all analytical tables and columns
- [Data generation parameters](docs/data-generation-parameters.md) — The core formulas (Conversion, Call duration, CSAT, Payment date, Costs) used to generate the synthetic dataset, with business rationale for each parameter
- [Data generation rules](docs/data-generation-rules.md) — Dataset construction rules: volume, tier/campaign distribution, passenger count logic, age variation, and call generation order
- [Data quality plan](docs/data-quality-plan.md) — Data quality issues intentionally introduced into the dataset, with detection and correction logic

## 8. Tech stack

- **Python (Pandas)** — ETL, data transformation, and statistical analysis
- **SQLite** — local analytical database
- **BigQuery** — cloud analytical data warehouse
- **SQL** — analytical queries
- **Power BI** — executive dashboard
- **Looker Studio** — operational dashboard

## 9. Repository structure

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
│   ├── data-generation-parameters.md
│   ├── data-generation-rules.md
│   ├── data-quality-plan.md
│   └── data-model/
│       ├── operational-data-model.dbml
│       ├── operational-data-model.png
│       ├── dimensional-data-model.dbml
│       └── dimensional-data-model.png
```

As the project advances into ETL, SQL queries, statistical analysis, the optimization model, and dashboards, the corresponding folders (`etl/`, `sql/`, `notebooks/`, `dashboards/`) will be added and documented here

## 10. Project status

🟢 In progress

See the complete project roadmap in: - [Roadmap](docs/roadmap.md)}

## 11. About the author

**Micaela Leguizamon** — Data Analyst with a background in UX Research

- LinkedIn: [linkedin.com/in/micaela-leguiz](https://www.linkedin.com/in/micaela-leguiz/)
- Portfolio: [micaelaleguiz.framer.website](https://micaelaleguiz.framer.website/en)
