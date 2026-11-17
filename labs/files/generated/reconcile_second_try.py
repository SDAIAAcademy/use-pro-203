"""A scripted stand-in for the corrected script, after the participant asked for control totals,
a cleaned join key and one use per line. Written by the course author, not by a model.

  python reconcile_second_try.py <folder with the two csv files>
"""
import json
import sys
from pathlib import Path

import pandas as pd

data = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
bank = pd.read_csv(data / "bank_statement_oct.csv", dtype={"reference": str})
ledger = pd.read_csv(data / "ledger_cash_oct.csv", dtype={"reference": str})

for df in (bank, ledger):
    df["h"] = (df["amount"] * 100).round().astype("int64")
    df["key"] = df["reference"].str.strip().str.upper()
    df["n"] = df.groupby(["key", "h"]).cumcount()

merged = bank.merge(ledger, on=["key", "h", "n"], how="outer", indicator=True)
both = merged[merged["_merge"] == "both"]
left = merged[merged["_merge"] == "left_only"]
right = merged[merged["_merge"] == "right_only"]

assert len(both) + len(left) == len(bank)
assert len(both) + len(right) == len(ledger)
assert both["h"].sum() + left["h"].sum() == bank["h"].sum()
assert both["h"].sum() + right["h"].sum() == ledger["h"].sum()

result = {
    "bank_lines": len(bank), "bank_sum": bank["h"].sum() / 100,
    "ledger_lines": len(ledger), "ledger_sum": ledger["h"].sum() / 100,
    "matched_pairs": len(both), "matched_sum": both["h"].sum() / 100,
    "bank_unmatched": len(left), "ledger_unmatched": len(right),
}
print(json.dumps(result))
