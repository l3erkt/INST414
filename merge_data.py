"""
merge_data.py — Merge FEC donation data with Congress.gov legislative data.

Produces a single dataset per (legislator × industry) with both donation totals
and legislative activity counts, ready for analysis.

Output: data/merged.csv
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DONATIONS_CSV = os.path.join(DATA_DIR, "donations.csv")
LEGISLATION_CSV = os.path.join(DATA_DIR, "legislation.csv")
MERGED_CSV = os.path.join(DATA_DIR, "merged.csv")


def merge_datasets() -> pd.DataFrame:
    """
    Join donations and legislation data on (bioguide_id, industry).
    """
    if os.path.exists(MERGED_CSV):
        print(f"✓ Cached merged data found at {MERGED_CSV}")
        return pd.read_csv(MERGED_CSV)

    # Load raw data
    print("Loading donations data...")
    donations = pd.read_csv(DONATIONS_CSV)
    print(f"  → {len(donations)} donation records")

    print("Loading legislation data...")
    legislation = pd.read_csv(LEGISLATION_CSV)
    print(f"  → {len(legislation)} legislation records")

    # ── Aggregate donations per (legislator, industry) ────────────────────
    donation_agg = (
        donations
        .groupby(["bioguide_id", "industry"])
        .agg(
            legislator_name=("legislator_name", "first"),
            candidate_id=("candidate_id", "first"),
            party=("party", "first"),
            state=("state", "first"),
            industry_donation_total=("amount", "sum"),
            num_pacs_donating=("amount", lambda x: (x > 0).sum()),
            total_pac_contributions=("total_pac_contributions", "first"),
            total_receipts=("total_receipts", "first"),
        )
        .reset_index()
    )

    print(f"  → {len(donation_agg)} aggregated donation records")

    # ── Select columns from legislation to avoid duplicates ───────────────
    leg_cols = [
        "bioguide_id", "industry",
        "committees", "policy_areas_checked",
        "bills_sponsored_relevant", "bills_cosponsored_relevant",
        "total_relevant_bills", "total_bills_sponsored",
        "total_bills_cosponsored", "on_relevant_committee",
    ]
    legislation_slim = legislation[leg_cols]

    # ── Merge on (bioguide_id, industry) ──────────────────────────────────
    merged = pd.merge(
        donation_agg,
        legislation_slim,
        on=["bioguide_id", "industry"],
        how="outer",
    )

    # Fill NaN donation amounts with 0
    merged["industry_donation_total"] = merged["industry_donation_total"].fillna(0)
    merged["num_pacs_donating"] = merged["num_pacs_donating"].fillna(0).astype(int)

    # Fill missing legislator info from legislation data if needed
    if merged["legislator_name"].isna().any():
        # Look up from the original legislation df
        name_map = legislation.set_index("bioguide_id")["legislator_name"].to_dict()
        party_map = legislation.set_index("bioguide_id")["party"].to_dict()
        state_map = legislation.set_index("bioguide_id")["state"].to_dict()
        merged["legislator_name"] = merged["legislator_name"].fillna(
            merged["bioguide_id"].map(name_map)
        )
        merged["party"] = merged["party"].fillna(merged["bioguide_id"].map(party_map))
        merged["state"] = merged["state"].fillna(merged["bioguide_id"].map(state_map))

    # ── Derived metrics ───────────────────────────────────────────────────
    merged["industry_donation_share"] = (
        merged["industry_donation_total"] /
        merged["total_pac_contributions"].replace(0, float("nan"))
    ).fillna(0)

    merged["sponsorship_rate"] = (
        merged["bills_sponsored_relevant"] /
        merged["total_bills_sponsored"].replace(0, float("nan"))
    ).fillna(0)

    # Sort for readability
    merged.sort_values(
        ["industry", "industry_donation_total"],
        ascending=[True, False],
        inplace=True,
    )

    merged.to_csv(MERGED_CSV, index=False)
    print(f"\n✓ Saved {len(merged)} merged records to {MERGED_CSV}")
    return merged


if __name__ == "__main__":
    df = merge_datasets()
    print(f"\nPreview:\n{df.head(10).to_string()}")
    print(f"\nColumns: {list(df.columns)}")
