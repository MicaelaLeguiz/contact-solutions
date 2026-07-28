# Data Dictionary

## Purpose

This document describes the dimensional data model used throughout the project. It defines the business meaning of each table and field, ensuring a consistent interpretation of the data across the ETL process, analytical model, and Power BI dashboards

The dictionary includes table descriptions, source systems, grain definitions, and field-level documentation to facilitate data understanding and maintenance

---

# FactCalls

Stores one record for every customer interaction handled by Contact Solutions

- Source system: Contact Solutions

- Refresh frequency: Every 15 minutes. Simulates near real-time operational reporting

- Grain: One row represents one customer interaction (one call)

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `call_id` | Integer | No | Unique identifier for each customer interaction | Primary key |
| `customer_id` | Integer | No | Identifier of the customer associated with the call | Foreign key referencing `DimCustomer` |
| `agent_id` | Integer | No | Identifier of the agent who handled the interaction | Foreign key referencing `DimAgent` |
| `campaign_id` | Integer | No | Identifier of the campaign associated with the call | Foreign key referencing `DimCampaign` |
| `call_date` | Date | No | Date on which the interaction took place | Foreign key referencing `DimDate` |
| `start_time` | Time | No | Time when the interaction started | Used to calculate call duration |
| `end_time` | Time | No | Time when the interaction ended | Must be greater than or equal to `start_time` |
| `call_direction` | Varchar | No | Indicates whether the interaction was inbound or outbound | Allowed values are defined in the data model |
| `channel` | Varchar | No | Communication channel used for the interaction | Allowed values are defined in the data model |
| `call_reason` | Varchar | No | Business purpose of the interaction | Allowed values are defined in the data model |
| `call_result` | Varchar | No | Final outcome of the interaction | Allowed values are defined in the data model |
| `acd_time_seconds` | Integer | No | Time spent in active conversation with the customer | Used in the AHT calculation |
| `hold_time_seconds` | Integer | No | Time the customer spent on hold during the interaction | Used in the AHT calculation |
| `acw_time_seconds` | Integer | No | Time spent completing after-call work once the interaction ended | Used in the AHT calculation |
| `available_time_seconds` | Integer | No | Time the agent remained available before receiving this interaction | Used to calculate agent utilization |
| `abandon_time_seconds` | Integer | Yes | Time elapsed before the customer abandoned the interaction | Null when the interaction was successfully answered |
| `call_duration_seconds` | Integer | No | Total duration of the interaction | Used for operational reporting |
| `csat_score` | Integer | Yes | Customer Satisfaction score collected after the interaction | Null when no survey response is available |

---

# FactSales

Stores one record for every confirmed sale reported by Global Experience

- Source system: Global Experience

- Refresh frequency: Daily (end of day). Global Experience confirms sales and payments at the end of each business day

- Grain: One row represents one confirmed sale

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `sale_id` | Integer | No | Unique identifier for each sale | Primary key |
| `customer_id` | Integer | No | Identifier of the customer who completed the purchase | Foreign key referencing `DimCustomer` |
| `campaign_id` | Integer | No | Identifier of the purchased campaign | Foreign key referencing `DimCampaign` |
| `sale_date` | Date | No | Date when the sale was confirmed | Foreign key referencing `DimDate` |
| `payment_date` | Date | Yes | Date when the payment was completed | Foreign key referencing `DimDate` |
| `payment_status` | Varchar | No | Current payment status of the sale | Allowed values are defined in the data model |
| `passenger_count` | Integer | No | Number of passengers included in the booking | Must be greater than zero |
| `sale_amount` | Decimal | No | Contracted value of the sale | May differ from the campaign list price due to negotiated discounts |
| `paid_amount` | Decimal | Yes | Amount effectively collected from the customer | Must be less than or equal to `sale_amount` |
| `commission_rate` | Decimal | No | Commission percentage paid by Global Experience to Contact Solutions | Expressed as a percentage of the collected revenue |
| `commission_amount` | Decimal | Yes | Commission amount calculated from the collected revenue | Derived from `paid_amount × commission_rate` |

---

# FactCosts

Stores monthly operating costs associated with the contact center operation

- Source system: Contact Solutions

- Refresh frequency: monthly. 10th day of the following month, after the accounting close
  
- Grain: One row represents one monthly cost record by cost category

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `cost_id` | Integer | No | Unique identifier for each cost record | Primary key |
| `date` | Date | No | Reporting month associated with the operating cost | Foreign key referencing `DimDate`. Monthly costs are recorded using the first day of the reporting month |
| `agent_type` | Varchar | No | Type of workforce associated with the cost | Allowed values are defined in the data model |
| `cost_category` | Varchar | No | Operating cost category | Allowed values are defined in the data model |
| `cost_type` | Varchar | No | Classification of the operating cost | Allowed values are defined in the data model |
| `amount` | Decimal | No | Monetary value of the operating cost | Expressed in USD and recorded after the monthly accounting close |

---

# DimCustomer

Stores customer master data received from Global Experience

- Source system: Global Experience

- Refresh frequency: Monthly (beginning of month). Global Experience provides a refreshed customer master file at the beginning of each month

- Grain: One row represents one customer

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `customer_id` | Integer | No | Unique identifier for each customer | Primary key |
| `full_name` | Varchar | No | Customer full name | Free-text value provided by Global Experience |
| `age` | Integer | No | Customer age | Must be greater than or equal to 18 |
| `province` | Varchar | No | Customer province or state | Free-text value provided by Global Experience |
| `country` | Varchar | No | Customer country | Free-text value provided by Global Experience |
| `registration_date` | Date | No | Date when the customer registered with Global Experience | Foreign key referencing `DimDate` |
| `is_new_customer` | Boolean | No | Indicates whether the customer is new during the current reporting period | True if the customer registered during the current reporting period |
| `trip_count` | Integer | No | Number of trips previously completed by the customer | Must be greater than or equal to zero |
| `customer_tier` | Varchar | No | Customer loyalty segment | Allowed values are defined in the data model |
| `primary_campaign_id` | Integer | No | Campaign recommended as the primary offer for the customer | Foreign key referencing `DimCampaign`. Recommendation provided by Global Experience |
| `secondary_campaign_id` | Integer | Yes | Alternative campaign recommended for the customer | Foreign key referencing `DimCampaign`. Recommendation provided by Global Experience |
| `opportunity_status` | Varchar | No | Current commercial status of the customer | Stores the latest available status only. Allowed values are defined in the data model |

---

# DimCampaign

Stores information about tourism campaigns and products offered by Global Experience

- Source system: Global Experience
  
- Refresh frequency: Monthly (beginning of month). Campaign definitions are updated and shared before the monthly operation begins

- Grain: One row represents one campaign

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `campaign_id` | Integer | No | Unique identifier for each campaign | Primary key |
| `campaign_name` | Varchar | No | Commercial name of the campaign | Free-text value provided by Global Experience |
| `destination` | Varchar | No | Destination associated with the travel package | Free-text value provided by Global Experience |
| `country` | Varchar | No | Country where the destination is located | Free-text value provided by Global Experience |
| `product_type` | Varchar | No | Category of the tourism product | Allowed values are defined in the data model |
| `list_price` | Decimal | No | Standard catalog price before discounts | Expressed in USD |
| `discount` | Decimal | No | Standard discount applied to the campaign | Expressed as a percentage |
| `monthly_target` | Integer | No | Monthly sales target established for the campaign | Defined by Global Experience |
| `start_date` | Date | No | Date when the campaign becomes available | Foreign key referencing `DimDate` |
| `end_date` | Date | No | Date when the campaign ends | Foreign key referencing `DimDate`. Must be greater than or equal to `start_date` |

---

# DimAgent

Stores agent master data, including both human and AI agents

- Source system: Contact Solutions

- Refresh frequency: Every 15 days. Simulates periodic synchronization of HR records, including new hires and terminations

- Grain: One row represents one agent

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `agent_id` | Integer | No | Unique identifier for each agent | Primary key |
| `full_name` | Varchar | No | Full name of the agent | Free-text value provided by Contact Solutions |
| `agent_type` | Varchar | No | Type of agent handling customer interactions | Allowed values are defined in the data model |
| `supervisor` | Varchar | No | Name of the supervisor responsible for the agent | Free-text value provided by Contact Solutions |
| `account` | Varchar | No | Client account assigned to the agent | Free-text value provided by Contact Solutions |
| `employment_type` | Varchar | No | Employment arrangement of the agent | Allowed values are defined in the data model |
| `hire_date` | Date | No | Date when the agent joined Contact Solutions | Foreign key referencing `DimDate` |
| `termination_date` | Date | Yes | Date when the agent left Contact Solutions | Foreign key referencing `DimDate`. Null if the agent is still active |

---

# DimDate

Calendar dimension used for time-based analysis

- Source system: Generated during the ETL process

- Refresh frequency: Generated once during the initial ETL setup

- Grain: One row represents one calendar date

## Columns

| Field | Data Type | Nullable | Description | Business Rule |
|--------|-----------|----------|-------------|---------------|
| `date` | Date | No | Calendar date | Primary key |
| `day` | Integer | No | Day of the month | Value between 1 and 31 |
| `week` | Integer | No | Week number within the year | Generated during the ETL process |
| `month` | Integer | No | Month number | Value between 1 and 12 |
| `quarter` | Integer | No | Quarter of the year | Value between 1 and 4 |
| `year` | Integer | No | Calendar year | Four-digit year |
