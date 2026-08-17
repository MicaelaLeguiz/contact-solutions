# Business brief

# How much should be automated?
## A data-driven approach to optimizing Human–AI workforce allocation

# ¿Cuánto automatizar?
## Un enfoque basado en datos para optimizar la combinación de agentes humanos e IA

---

> The project documentation is written in English. A brief introduction is also provided in Spanish

---
## Table of contents
- [Executive summary](#1-executive-summary)
- [Executive summary (Spanish)](#1-resumen-ejecutivo)
- [Business context](#2-business-context)
- [Business problem](#3-business-problem)
- [Objectives](#4-objectives)
- [Research questions & hypotheses](#5-research-questions--hypotheses)
- [Stakeholders](#6-stakeholders)
- [Project scope](#7-project-scope)
- [Assumptions and constraints](#8-assumptions-and-constraints)

---

## 1. Executive summary

The adoption of AI-powered conversational agents is transforming customer-facing operations across a wide range of industries. While this project focuses on a contact center sales operation, the analytical framework and decision-making approach can be applied to any organization seeking to balance human expertise and AI-driven automation

This project develops an end-to-end Business Intelligence solution to evaluate the operational and financial impact of a hybrid workforce composed of human and AI agents. The solution integrates ETL processes, dimensional data modeling, statistical analysis, executive dashboards, and a simplified optimization model to determine the workforce composition that maximizes expected profit while satisfying budget and customer satisfaction constraints

Rather than evaluating AI adoption from a purely technological perspective, the project addresses it as a business decision supported by data, providing a framework that can be adapted to different industries facing similar automation challenges


## 1. Resumen ejecutivo

> This section is provided in Spanish as a brief introduction. The complete project documentation is available in English

La incorporación de agentes conversacionales impulsados por Inteligencia Artificial está transformando las operaciones de atención al cliente en una amplia variedad de industrias. Si bien este proyecto se desarrolla sobre una operación de ventas en un contact center, el enfoque analítico y la metodología de toma de decisiones propuesta pueden aplicarse a cualquier organización que busque encontrar el equilibrio óptimo entre la experiencia humana y la automatización mediante IA

Este proyecto desarrolla una solución integral de Business Intelligence para evaluar el impacto operativo y financiero de un modelo híbrido de agentes humanos e Inteligencia Artificial. La solución integra procesos ETL, modelado dimensional de datos, análisis estadístico, dashboards ejecutivos y un modelo simplificado de optimización para determinar la combinación de agentes que maximiza el beneficio esperado respetando restricciones presupuestarias y de calidad del servicio

Más que analizar la incorporación de Inteligencia Artificial desde una perspectiva exclusivamente tecnológica, este proyecto la aborda como una decisión estratégica de negocio respaldada por datos, proporcionando un marco de análisis que puede adaptarse a diferentes organizaciones e industrias que enfrentan desafíos similares en sus procesos de automatización

---

## 2. Business context

Many organizations are incorporating AI-powered agents to reduce operational costs, increase productivity, and improve service availability. However, automation may also affect key business metrics such as sales conversion, customer satisfaction, and overall profitability

**Contact Solutions** is a fictional contact center service provider that supports clients across multiple industries, including banking, retail, tourism, and professional services. The company currently employs approximately **2,500 human agents** and has recently launched a digital transformation initiative focused on gradually introducing AI agents into selected operations

As a pilot project, one of its tourism clients, **Global Experience**, implemented a hybrid workforce for its outbound vacation package sales operation over a three-month period. The operation consists of **150 agents**, including **141 human agents** and **9 AI agents**. The operation runs Monday through Friday. During this period, operational, commercial, and customer experience metrics were collected to assess the performance of the hybrid model

Senior management aims to evaluate the results of this pilot in order to define the optimal AI adoption strategy that maximizes expected business value while remaining within the monthly operating budget of **USD 380,000**. Additionally, to meet the service quality requirements established by Global Experience, the operation must maintain a minimum **Customer Satisfaction (CSAT) score of 85%**

---

## 3. Business problem

The introduction of AI agents creates an opportunity to reduce operational costs, but its impact on sales conversion, customer satisfaction, and overall profitability remains uncertain. Expanding the hybrid workforce without sufficient evidence could either negatively affect key business outcomes or prevent the organization from realizing potential efficiency gains

Management requires a data-driven assessment of this initial implementation to quantify the operational and commercial impact of AI agents and support evidence-based decisions regarding the future expansion of the hybrid workforce

---

## 4. Objectives

### Objective

Assess the operational and commercial impact of gradually introducing AI agents into a phone sales operation in order to recommend a hybrid workforce strategy that maximizes business value while meeting predefined budget and service quality constraints

### Specific objectives

1. Assess the current operational performance using operational, commercial, and customer experience KPIs

2. Statistically compare the performance of human and AI agents using descriptive, inferential, and association analysis techniques

3. Recommend a data-driven AI adoption strategy supported by quantitative evidence and a simplified optimization model

---

## 5. Research questions & hypotheses

**Main question:** What is the optimal strategy for introducing AI agents into a phone sales operation to maximize expected profit while balancing profitability, productivity, and customer service quality?

| # | Question | Type | Hypothesis |
|---|---|---|---|
| Q1 | How does the operation currently perform in terms of productivity, conversion, satisfaction, and profitability? | Exploratory | — |
| Q2 | Are there significant differences in conversion rates between human and AI agents? | Confirmatory | H2: No significant difference in overall conversion between agent types |
| Q3 | Do AI agents achieve higher average operational productivity than human agents? | Confirmatory | H3: AI agents achieve higher average operational productivity |
| Q4 | Does introducing AI agents reduce the operational cost per sale compared to human agents? | Confirmatory | H4: AI agents reduce the operational cost per sale |
| Q5 | Which operational variables are most strongly associated with sales conversion? | Confirmatory | H5: Call duration, campaign type, channel, and agent type are associated with conversion probability |
| Q6 | Are there campaign segments where one agent type outperforms the other in conversion or productivity? | Exploratory | — |
| Q7 | Does profitability depend on the interaction between agent type and campaign type, or on agent type alone? | Confirmatory | H7: Profitability depends more on the agent type × campaign type combination than on agent type alone |
| Q8 | What proportion of human vs. AI agents maximizes expected profit under the budget and CSAT constraints? | Confirmatory | H8: There is an optimal mix of human and AI agents that maximizes expected profit while satisfying both the budget and CSAT constraints |

---

## 6. Stakeholders

The primary stakeholders of this project are Contact Solutions' executive board, the operations management team, account supervisors, the finance department, and the client (Global Experience), all of whom require different levels of operational and strategic information to support decision-making

| Stakeholder | Business need |
|---|---|
| Executive Board | Define the long-term AI adoption strategy while balancing profitability, operational efficiency, and customer satisfaction |
| Operations Management | Monitor operational performance, identify improvement opportunities, and support workforce planning |
| Account Supervisors | Track daily performance, monitor agent productivity, and identify coaching opportunities |
| Finance Department | Evaluate operational costs, profitability, and the financial impact of AI adoption |
| Global Experience | Ensure customer satisfaction and monitor the commercial performance of the sales operation |

---

## 7. Project scope

### In scope

- Analyze a phone sales operation for a single client (Global Experience)
- Compare the performance of human and AI agents across operational, commercial, and customer experience metrics
- Integrate multiple data sources through an ETL process
- Build an analytical data model to evaluate operational and commercial KPIs
- Develop executive and operational dashboards tailored to different decision-making levels
- Perform descriptive and inferential statistical analysis on the main business KPIs
- Develop a simplified optimization model to evaluate AI adoption scenarios
- Provide data-driven recommendations to support the expansion of the hybrid workforce model

### Out of scope

- Developing or training Machine Learning models
- Natural Language Processing (NLP) or conversation content analysis
- Designing or implementing AI agents
- Predicting individual customer behavior
- Real-time call routing optimization
- Integration with Global Experience's live production systems or real-time infrastructure

## 8. Assumptions and constraints

- Contact Solutions' revenue is modeled exclusively as a variable commission per closed sale; no fixed monthly management fee is assumed, since a constant fee would not affect the optimization model's optimal point regardless of its size
- All data used in the project is simulated
- The operation runs Monday through Friday, with Saturdays and Sundays considered non-operating days
- Only one client (Global Experience) is included
- No learning curve effects are considered for AI or human agents
- AI operational costs are assumed to remain constant throughout the analysis
- Seasonal effects are not considered
