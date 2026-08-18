"""
Generates DATE_DIM: one row per calendar day across the 3-month pilot period
(July 1 - September 30), matching the grain and columns defined in
docs/data-model/operational-data-model.dbml
"""

import pandas as pd
from pathlib import Path

# --- Config ---
START_DATE = "2026-07-01"
END_DATE = "2026-09-30"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "generated" / "date_dim.csv"


def generate_date_dim(start_date: str, end_date: str) -> pd.DataFrame:
    """Builds one row per calendar day, with day/week/month/quarter/year and is_business_day columns."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({"date": dates})
    df["day"] = df["date"].dt.day
    df["week"] = df["date"].dt.isocalendar().week
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["year"] = df["date"].dt.year
    
    # Evaluate if the day of the week is between Monday (0) and Friday (4)
    df["is_business_day"] = (df["date"].dt.dayofweek < 5).astype(int)

    # Store the date as a plain string (YYYY-MM-DD), not a pandas Timestamp,
    # so the CSV output matches how a real date column would be exported.
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df


def main():
    df = generate_date_dim(START_DATE, END_DATE)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df)} rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()