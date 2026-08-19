"""
Generates AGENTS: the Contact Solutions agent roster across all client accounts,
matching the columns defined in docs/data-model/operational-data-model.dbml

Global Experience includes the 141-agent operational baseline plus a small
replacement pool to simulate turnover during the pilot period
"""

import numpy as np
import pandas as pd
from pathlib import Path
from faker import Faker

# --- Config ---
SEED = 42

ACCOUNT_GLOBAL = "Global Experience"
ACCOUNT_AURA = "Aura Travel"
ACCOUNT_VANGUARD = "Vanguard Bank"

N_GLOBAL_HUMAN_BASE = 141
N_GLOBAL_REPLACEMENTS = 14
N_GLOBAL_AI = 9

N_AURA_HUMAN = 65
N_VANGUARD_HUMAN = 35

N_GLOBAL_HUMAN_SUPERVISORS = 10
N_AURA_SUPERVISORS = 7
N_VANGUARD_SUPERVISORS = 4

PILOT_START = pd.Timestamp("2026-07-01")
PILOT_END = pd.Timestamp("2026-09-30")

OUTPUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "generated"
    / "agents.csv"
)

rng = np.random.default_rng(SEED)
fake = Faker()
Faker.seed(SEED)


def generate_supervisors(n: int) -> list[str]:
    """Generates a unique supervisor pool"""
    return [fake.name() for _ in range(n)]


def assign_supervisors(n_agents: int, supervisors: list[str]) -> list[str]:
    """Distributes agents as evenly as possible across supervisors"""
    return [supervisors[i % len(supervisors)] for i in range(n_agents)]


def generate_hire_dates(
    n: int,
    start_date: pd.Timestamp,
    min_years: int = 0,
    max_years: int = 4,
) -> list[pd.Timestamp]:
    """Generates hire dates within a configurable historical range"""
    min_days = int(min_years * 365)
    max_days = int(max_years * 365)

    return [
        start_date - pd.Timedelta(
            days=int(rng.integers(min_days, max_days + 1))
        )
        for _ in range(n)
    ]


def generate_termination_dates(
    n: int,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> list[pd.Timestamp]:
    """Generates termination dates within the pilot period"""
    days = (end_date - start_date).days

    return [
        start_date + pd.Timedelta(days=int(rng.integers(0, days + 1)))
        for _ in range(n)
    ]


def generate_global_agents(
    n_base: int,
    n_replacements: int,
    supervisors: list[str],
    start_id: int,
) -> pd.DataFrame:
    """Generates Global Experience human agents and replacement agents"""

    total_humans = n_base + n_replacements
    
    df = pd.DataFrame({
        "agent_id": range(start_id, start_id + total_humans),
        "full_name": [fake.name() for _ in range(total_humans)],
        "agent_type": "Human",
        "supervisor": assign_supervisors(total_humans, supervisors),
        "account": ACCOUNT_GLOBAL,
        "employment_type": "Full-time",
        "hire_date": pd.NaT,
        "termination_date": pd.NaT,
    })

    # Original agents were already employed before the pilot
    df.loc[:n_base - 1, "hire_date"] = generate_hire_dates(
        n_base,
        PILOT_START,
        min_years=1,
        max_years=4,
    )

    # Replacement agents enter during the pilot
    replacement_hires = [
        PILOT_START
        + pd.Timedelta(
            days=int(
                rng.integers(
                    0,
                    (PILOT_END - PILOT_START).days + 1,
                )
            )
        )
        for _ in range(n_replacements)
    ]

    df.loc[n_base:, "hire_date"] = replacement_hires


    # Replacement agents represent temporary turnover/replacement activity
    df.loc[n_base:, "termination_date"] = [
        hire_date
        + pd.Timedelta(
            days=int(
                rng.integers(
                    7,
                    max(
                        8,
                        (PILOT_END - hire_date).days + 1,
                    ),
                )
            )
        )
        for hire_date in replacement_hires
    ]

    # Keep replacement termination dates within the pilot period
    df["termination_date"] = df.apply(
        lambda row: (
            min(row["termination_date"], PILOT_END)
            if pd.notna(row["termination_date"])
            else pd.NaT
        ),
        axis=1,
    )

    return df


def generate_client_agents(
    n: int,
    start_id: int,
    account: str,
    n_supervisors: int,
) -> pd.DataFrame:
    """Generates human agents for non-Global Experience accounts"""

    supervisors = generate_supervisors(n_supervisors)

    n_part_time = round(n * 0.20)
    n_terminated = round(n * 0.05)

    employment_types = np.array(["Full-time"] * n)
    part_time_idx = rng.choice(n, size=n_part_time, replace=False)
    employment_types[part_time_idx] = "Part-time"

    termination_idx = rng.choice(n, size=n_terminated, replace=False)
    termination_dates = [pd.NaT] * n

    generated_termination_dates = generate_termination_dates(
        n_terminated,
        PILOT_START,
        PILOT_END,
    )

    for idx, termination_date in zip(
        termination_idx,
        generated_termination_dates,
    ):
        termination_dates[idx] = termination_date

    return pd.DataFrame({
        "agent_id": range(start_id, start_id + n),
        "full_name": [fake.name() for _ in range(n)],
        "agent_type": "Human",
        "supervisor": assign_supervisors(n, supervisors),
        "account": account,
        "employment_type": employment_types,
        "hire_date": generate_hire_dates(
            n,
            PILOT_START,
            min_years=1,
            max_years=4,
        ),
        "termination_date": termination_dates,
    })


def generate_ai_agents(
    n: int,
    start_id: int,
) -> pd.DataFrame:
    """Generates AI agents for Global Experience"""

    return pd.DataFrame({
        "agent_id": range(start_id, start_id + n),
        "full_name": [f"AI Agent {i + 1}" for i in range(n)],
        "agent_type": "AI",
        "supervisor": "AI Operations",
        "account": ACCOUNT_GLOBAL,
        "employment_type": "N/A",
        "hire_date": PILOT_START,
        "termination_date": pd.NaT,
    })


def main():
    global_supervisors = generate_supervisors(N_GLOBAL_HUMAN_SUPERVISORS)

    current_id = 2497

    global_humans = generate_global_agents(
        N_GLOBAL_HUMAN_BASE,
        N_GLOBAL_REPLACEMENTS,
        global_supervisors,
        start_id=current_id,
    )
    current_id += len(global_humans)

    aura_agents = generate_client_agents(
        N_AURA_HUMAN,
        start_id=current_id,
        account=ACCOUNT_AURA,
        n_supervisors=N_AURA_SUPERVISORS,
    )
    current_id += len(aura_agents)

    vanguard_agents = generate_client_agents(
        N_VANGUARD_HUMAN,
        start_id=current_id,
        account=ACCOUNT_VANGUARD,
        n_supervisors=N_VANGUARD_SUPERVISORS,
    )
    current_id += len(vanguard_agents)

    ai_agents = generate_ai_agents(
        N_GLOBAL_AI,
        start_id=current_id,
    )

    df = pd.concat(
        [
            global_humans,
            aura_agents,
            vanguard_agents,
            ai_agents,
        ],
        ignore_index=True,
    )

    df["hire_date"] = pd.to_datetime(df["hire_date"]).dt.strftime("%Y-%m-%d")
    df["termination_date"] = pd.to_datetime(df["termination_date"]).dt.strftime("%Y-%m-%d")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(df)} agents -> {OUTPUT_PATH}")
    print("\nAgents by account:")
    print(df["account"].value_counts())

    print("\nAgents by type:")
    print(df["agent_type"].value_counts())

    print("\nEmployment type by account:")
    print(df.groupby(["account", "employment_type"]).size())

    print("\nTerminations by account:")
    print(df.groupby("account")["termination_date"].apply(lambda x: x.notna().sum()))


if __name__ == "__main__":
    main()