# Project methodology

## Purpose

This document outlines the methodology used throughout the project

---

## Methodology

### 1. Business understanding

Define the business problem, stakeholders, objectives, research questions, hypotheses, and KPIs

### 2. Data design

Design the operational and dimensional data models and document the business rules through the KPI Dictionary and Data Dictionary

### 3. Data architecture

The ETL pipeline generates two analytical repositories from the same transformed dataset.

- **SQLite** serves as the local analytical database for SQL querying and Power BI reporting
- **BigQuery** stores the same analytical model in a cloud data warehouse to support Looker Studio reporting

This approach demonstrates both traditional relational database workflows and modern cloud analytics practices while maintaining a single source of truth for the transformed data

### 4. Data analysis

Perform SQL analysis, exploratory analysis in Python, and statistical validation of the proposed hypotheses

### 5. Decision support

Develop executive and operational dashboards and build a simplified optimization model to support business decisions

### 6. Communication

Develop executive and operational dashboards and build a simplified optimization model to support business decisions
