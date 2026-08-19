"""
Generates CAMPAIGNS: the 9 defined travel campaigns, matching the columns
in docs/data-model/operational-data-model.dbml
"""

import pandas as pd
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "generated" / "campaigns.csv"

# One row per campaign, exactly as defined in the business brief.
# start_date/end_date reflect the working months already established in
# data-generation-rules.md §2.3 (which months each campaign is active)
CAMPAIGNS = [
    {"campaign_id": "466CRURIO", "campaign_name": "Rio de Janeiro and Búzios", "destination": "Rio de Janeiro, Búzios", "country": "Brazil",
     "product_type": "Cruise", "list_price": 1200, "discount": 0.175, "monthly_target": 85000,
     "start_date": "2026-07-01", "end_date": "2026-09-30"},

    {"campaign_id": "456CRUCAR", "campaign_name": "Southern Caribbean and the Antilles", "destination": "Southern Caribbean, the Antilles", "country": "United States, Antilles",
     "product_type": "Cruise", "list_price": 3200, "discount": 0.0, "monthly_target": 75000,
     "start_date": "2026-08-01", "end_date": "2026-09-30"},

    {"campaign_id": "263EURMAD", "campaign_name": "Madrid and Andalusia", "destination": "Madrid, Andalusia", "country": "Spain",
     "product_type": "Europe", "list_price": 2300, "discount": 0.065, "monthly_target": 70000,
     "start_date": "2026-08-01", "end_date": "2026-09-30"},

    {"campaign_id": "267EURITA", "campaign_name": "French Riviera and Classic Italy", "destination": "French Riviera, Classic Italy", "country": "France, Italy",
     "product_type": "Europe", "list_price": 4800, "discount": 0.0, "monthly_target": 60000,
     "start_date": "2026-07-01", "end_date": "2026-07-31"},

    {"campaign_id": "197CARPUN", "campaign_name": "Punta Cana", "destination": "Punta Cana", "country": "Dominican Republic",
     "product_type": "Caribbean", "list_price": 1500, "discount": 0.125, "monthly_target": 100000,
     "start_date": "2026-07-01", "end_date": "2026-09-30"},

    {"campaign_id": "175CARRIV", "campaign_name": "Riviera Maya", "destination": "Riviera Maya", "country": "Mexico",
     "product_type": "Caribbean", "list_price": 3000, "discount": 0.0, "monthly_target": 75000,
     "start_date": "2026-07-01", "end_date": "2026-08-31"},

    {"campaign_id": "587ARGBAR", "campaign_name": "Bariloche", "destination": "Bariloche", "country": "Argentina",
     "product_type": "Vacation Package", "list_price": 700, "discount": 0.20, "monthly_target": 65000,
     "start_date": "2026-07-01", "end_date": "2026-08-15"},

    {"campaign_id": "521ARGPUE", "campaign_name": "Puerto Iguazú", "destination": "Puerto Iguazú", "country": "Argentina",
     "product_type": "Vacation Package", "list_price": 450, "discount": 0.10, "monthly_target": 80000,
     "start_date": "2026-07-01", "end_date": "2026-09-30"},

    {"campaign_id": "502ARGUSH", "campaign_name": "Ushuaia and Los Cauquenes", "destination": "Ushuaia, Los Cauquenes", "country": "Argentina",
     "product_type": "Vacation Package", "list_price": 1700, "discount": 0.0, "monthly_target": 70000,
     "start_date": "2026-08-01", "end_date": "2026-09-30"},
]

def generate_campaigns() -> pd.DataFrame:
    df = pd.DataFrame(CAMPAIGNS)
    return df


def main():
    df = generate_campaigns()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df)} campaigns -> {OUTPUT_PATH}")
    print(df[["campaign_id", "campaign_name", "product_type", "list_price"]])


if __name__ == "__main__":
    main()