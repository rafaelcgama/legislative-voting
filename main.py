import os
import pandas as pd

# Transform CSV files into DataFrames
bills = pd.read_csv('data/bills.csv')
legislators = pd.read_csv('data/legislators.csv')
vote_results = pd.read_csv('data/vote_results.csv')
votes = pd.read_csv('data/votes.csv')

# ===================== Deliverable 1 ===================== #

votes = votes.rename(columns={"id": "vote_id"})  # normalize key
vr = vote_results.merge(votes[["vote_id", "bill_id"]], on="vote_id")  # attach bill_id

# For each legislator how many bills he voted "yes"
supported = vr[vr["vote_type"] == 1].groupby("legislator_id")["bill_id"].nunique()

# For each legislator how many bills he voted "no"
opposed = vr[vr["vote_type"] == 2].groupby("legislator_id")["bill_id"].nunique()

voters = vr["legislator_id"].unique()

# Finds which legislators were voters on the proposed bills
l = legislators[legislators["id"].isin(voters)].copy()

# fillna(0) is used in case a legislator voted for "yes" or "no" for the 2 bills
l["num_supported_bills"] = l["id"].map(supported).fillna(0).astype(int)
l["num_opposed_bills"] = l["id"].map(opposed).fillna(0).astype(int)

os.makedirs("output", exist_ok=True)
l.to_csv("output/legislators-support-oppose-count.csv", index=False)

# ===================== Deliverable 2 ===================== #

# For each bill, how many legislators voted "yes"
supporters = vr[vr["vote_type"] == 1].groupby("bill_id")["legislator_id"].nunique()

# For each bill, how many legislators voted "no"
opposers = vr[vr["vote_type"] == 2].groupby("bill_id")["legislator_id"].nunique()

b = bills.copy()
b["supporter_count"] = b["id"].map(supporters).fillna(0).astype(int)
b["opposer_count"] = b["id"].map(opposers).fillna(0).astype(int)
b["primary_sponsor"] = b["sponsor_id"].map(legislators.set_index("id")["name"]).fillna("Unknown")

b[["id", "title", "supporter_count", "opposer_count", "primary_sponsor"]].to_csv("output/bills.csv", index=False)
