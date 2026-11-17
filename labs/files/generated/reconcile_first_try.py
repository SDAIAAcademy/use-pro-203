"""A scripted stand-in for the first script an assistant writes when asked to reconcile the two
files. Written by the course author, not by a model. It runs, prints tidy numbers, and is wrong
in two ways that only control totals and a read of the join key show:
it drops "duplicate" ledger rows before matching, and it joins on the raw reference text.

  python reconcile_first_try.py <folder with the two csv files>
"""
import json
import sys
from pathlib import Path

import pandas as pd

data = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
bank = pd.read_csv(data / "bank_statement_oct.csv")
ledger = pd.read_csv(data / "ledger_cash_oct.csv")

ledger = ledger.drop_duplicates(subset=["reference", "amount"])  # "clean the data first"
merged = bank.merge(ledger, on=["reference", "amount"], how="outer", indicator=True)

result = {
    "matched_pairs": int((merged["_merge"] == "both").sum()),
    "bank_unmatched": int((merged["_merge"] == "left_only").sum()),
    "ledger_unmatched": int((merged["_merge"] == "right_only").sum()),
}
print("Reconciliation complete.")
print(json.dumps(result))
