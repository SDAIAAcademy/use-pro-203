# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2", "openpyxl>=3.1", "formulas>=1.2"]
# ///
"""Runs the solution of every lab and prints PASS or the first difference.

  uv run labs/solutions/check.py            # every lab
  uv run labs/solutions/check.py 1.2 2.3    # some

It reads the participants' files in labs/files/, recomputes each reference figure with its own
code (not the generator's), and compares it with labs/solutions/key.json. It also runs, for real:
the code printed inside the scripted AI answers, the two scripted "generated" reconciliation
scripts (one faulty, one corrected), the three prepared notebooks, and both budget workbooks
through a formula engine. It calls no language model and leaves nothing in the course folder:
everything runs in a temporary folder.
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = HERE.parent / "files"
KEY = json.loads((HERE / "key.json").read_text(encoding="utf-8"))


def expect(name: str, got, want) -> None:
    if isinstance(got, float) or isinstance(want, float):
        ok = abs(float(got) - float(want)) < 0.005
    else:
        ok = got == want
    if not ok:
        print(f"FAIL  {name}: got {got!r}, expected {want!r}")
        raise SystemExit(1)
    print(f"ok    {name}: {got}")


def rows(path: Path) -> list[dict]:
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))


def cents(x) -> int:
    return round(float(x) * 100)


@contextlib.contextmanager
def workdir(*names: str):
    """A temporary folder holding copies of the named files; the course folder stays clean."""
    old = os.getcwd()
    tmp = tempfile.mkdtemp()
    try:
        for n in names:
            src = FILES / n if (FILES / n).exists() else HERE / n
            shutil.copy(src, Path(tmp) / Path(n).name)
        os.chdir(tmp)
        yield Path(tmp)
    finally:
        os.chdir(old)
        shutil.rmtree(tmp, ignore_errors=True)


def run_cells(code: str) -> tuple[dict, str]:
    ns: dict = {}
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(code, "<cells>", "exec"), ns)
    return ns, out.getvalue()


def notebook_code(name: str, replace: tuple[str, str] | None = None) -> str:
    nb = json.loads((FILES / "notebooks" / name).read_text(encoding="utf-8"))
    code = "\n\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    return code.replace(*replace) if replace else code


# ------------------------------------------------------------------ 1.1
def lab_1_1() -> None:
    k = KEY["answers"]
    tb = rows(FILES / "trial_balance_oct.csv")
    exp = [r for r in tb if r["group"] == "مصروفات"]
    rev = [r for r in tb if r["group"] == "إيرادات"]
    total = sum(cents(r["oct_2026"]) for r in exp) / 100
    expect("1.1 revenue, October", sum(cents(r["oct_2026"]) for r in rev) / 100, k["revenue_oct"])
    expect("1.1 expenses, October (the figure to recompute for A2)", total, k["expenses_oct"])
    a2 = (FILES / "ai_answers" / "A2.txt").read_text(encoding="utf-8")
    stated = float(re.search(r"إجمالي المصروفات ([\d,]+\.\d\d)", a2).group(1).replace(",", ""))
    expect("1.1 A2 states a different total", stated, k["a2_stated"])
    expect("1.1 A2 is wrong", stated != total, True)
    big = max(exp, key=lambda r: cents(r["oct_2026"]))
    expect("1.1 A4 largest expense account", big["account_name"], k["largest_expense"])
    expect("1.1 A4 share of expenses, percent", round(100 * float(big["oct_2026"]) / total, 1), k["largest_share_pct"])
    a4 = (FILES / "ai_answers" / "A4.txt").read_text(encoding="utf-8")
    expect("1.1 A4 states that share (right, yet generated)", f"{k['largest_share_pct']}%" in a4, True)
    sal = next(r for r in tb if r["account_code"] == "5010")
    expect("1.1 A3 salary change, percent", round(100 * (float(sal["oct_2026"]) / float(sal["sep_2026"]) - 1), 1), k["salary_change_pct"])
    expect("1.1 A3 formula points at row 5 (the salary account)", tb.index(sal) + 2, 5)
    staff = {"5010", "5020", "5030"}
    right6 = sum(cents(r["oct_2026"]) for r in exp if r["account_code"] not in staff) / 100
    expect("1.1 A6 right figure: expenses without staff costs", right6, k["non_payroll_expenses"])
    # run the code printed inside A1 and A6: the outputs they state are real outputs
    for name, want in (("A1.txt", (3, k["revenue_oct"])), ("A6.txt", (k["a6_accounts_included"], k["a6_stated"]))):
        text = (FILES / "ai_answers" / name).read_text(encoding="utf-8")
        code = "\n".join(l[4:] for l in text.splitlines() if l.startswith("    ") and not re.match(r"\s+[\d ,.]+$", l))
        with workdir("trial_balance_oct.csv"):
            _, out = run_cells(code)
        n, s = out.split()
        expect(f"1.1 {name} code runs and prints its stated count", int(n), want[0])
        expect(f"1.1 {name} code runs and prints its stated sum", float(s), want[1])
        expect(f"1.1 {name} states that sum", f"{want[1]:,.2f}" in text, True)
    expect("1.1 A6 computed, yet wrong: it kept two staff accounts", k["a6_stated"] != right6 and k["a6_accounts_included"] == 13, True)
    runs = rows(FILES / "ai_answers" / "A5_ai_function_runs.csv")
    changed = [int(r["row"]) for r in runs if r["ai_category_run_1"] != r["ai_category_run_2"]]
    expect("1.1 A5 rows that changed between two refreshes", changed, k["a5_changed_rows"])
    c = [sum(1 for r in runs if r[f"ai_category_run_{i}"] == "مواد نظافة") for i in (1, 2)]
    expect("1.1 A5 count of cleaning items, run 1 and run 2", c, [k["a5_cleaning_run_1"], k["a5_cleaning_run_2"]])
    expect("1.1 classification key: three computed, three generated", Counter(k["classification"].values()), Counter(computed=3, generated=3))


# ------------------------------------------------------------------ 1.2 and 1.3
def own_match():
    bank = rows(FILES / "bank_statement_oct.csv")
    ledger = rows(FILES / "ledger_cash_oct.csv")
    pool = defaultdict(list)
    for r in ledger:
        pool[(r["reference"].strip().upper(), cents(r["amount"]))].append(r)
    matched, bank_un = [], []
    for r in bank:
        k = (r["reference"].strip().upper(), cents(r["amount"]))
        if pool[k]:
            matched.append((r, pool[k].pop(0)))
        else:
            bank_un.append(r)
    ledger_un = [r for rs in pool.values() for r in rs]
    return bank, ledger, matched, bank_un, ledger_un


def lab_1_2() -> None:
    k = KEY["recon"]
    bank, ledger, matched, bank_un, ledger_un = own_match()
    expect("1.2 control total in: bank lines", len(bank), k["bank_lines"])
    expect("1.2 control total in: bank sum", sum(cents(r["amount"]) for r in bank) / 100, k["bank_sum"])
    expect("1.2 control total in: ledger lines", len(ledger), k["ledger_lines"])
    expect("1.2 control total in: ledger sum", sum(cents(r["amount"]) for r in ledger) / 100, k["ledger_sum"])
    expect("1.2 the two files hold 1,200 lines", len(bank) + len(ledger), 1200)
    expect("1.2 matched pairs", len(matched), k["matched_pairs"])
    expect("1.2 matched sum", sum(cents(b["amount"]) for b, _ in matched) / 100, k["matched_sum"])
    expect("1.2 unmatched bank lines", len(bank_un), 7)
    expect("1.2 unmatched ledger lines", len(ledger_un), 19)
    expect("1.2 control total out: matched + unmatched = lines", (len(matched) + len(bank_un), len(matched) + len(ledger_un)), (594, 606))
    messy = sum(1 for r in bank if r["reference"] != r["reference"].strip().upper())
    expect("1.2 bank references that need cleaning", messy, k["messy_references"])
    # the two scripted "generated" scripts, run for real
    with workdir("bank_statement_oct.csv", "ledger_cash_oct.csv") as tmp:
        res = {}
        for s in ("reconcile_first_try.py", "reconcile_second_try.py"):
            p = subprocess.run([sys.executable, str(FILES / "generated" / s), str(tmp)], capture_output=True, text=True, encoding="utf-8")
            if p.returncode:
                print(p.stderr)
                raise SystemExit(1)
            res[s] = json.loads(p.stdout.strip().splitlines()[-1])
    v1, v2 = res["reconcile_first_try.py"], res["reconcile_second_try.py"]
    print("      scripted first script reports:", v1)
    expect("1.2 scripted first script: ledger lines it accounts for (606 are in the file: the control total fails)",
           v1["matched_pairs"] + v1["ledger_unmatched"], 606 - k["duplicates"]["count"])
    expect("1.2 scripted first script: matched pairs (587 is right)", v1["matched_pairs"], k["matched_pairs"] - k["messy_references"])
    expect("1.2 scripted first script: bank lines unmatched (7 is right)", v1["bank_unmatched"], 7 + k["messy_references"])
    expect("1.2 scripted corrected script agrees with the reference",
           (v2["matched_pairs"], v2["bank_unmatched"], v2["ledger_unmatched"], v2["matched_sum"]), (587, 7, 19, k["matched_sum"]))
    # the prepared notebook, run for real
    with workdir("bank_statement_oct.csv", "ledger_cash_oct.csv") as tmp:
        ns, _ = run_cells(notebook_code("reconcile.ipynb"))
        log = rows(tmp / "run_log.csv")
    expect("1.2 notebook control totals", (ns["control_out"]["matched_pairs"], ns["control_out"]["bank_unmatched"], ns["control_out"]["ledger_unmatched"]), (587, 7, 19))
    expect("1.2 notebook adjusted balances", (ns["adjusted_bank"], ns["adjusted_ledger"]), (k["adjusted_balance"], k["adjusted_balance"]))
    expect("1.2 notebook wrote one run-log line with the totals", len(log) == 1 and "matched 587" in log[0]["control_totals"], True)


def lab_1_3() -> None:
    k = KEY["recon"]
    items = rows(FILES / "start" / "unmatched_items.csv")
    expect("1.3 start file lines", len(items), 26)
    bank, ledger, matched, _, _ = own_match()
    bank_refs = {r["reference"].strip().upper() for r in bank}
    ledger_refs = {r["reference"] for r in ledger}
    pairs = {(b["reference"].strip().upper(), cents(b["amount"])) for b, _ in matched}
    cls = defaultdict(list)
    for r in items:
        ref, h = r["reference"], cents(r["amount"])
        if r["side"] == "ledger":
            if ref not in bank_refs:
                cls["outstanding" if h < 0 else "in_transit"].append(h)
            elif (ref, h) in pairs:
                cls["duplicate"].append(h)
            else:
                cls["error_ledger"].append(h)
        else:
            cls["error_bank" if ref in ledger_refs else "bank_only"].append(h)
    n_items = sum(len(v) for v in cls.values()) - 1
    expect("1.3 unmatched items (the amount difference is one item)", n_items, 25)
    expect("1.3 payments not yet cleared: count, sum", (len(cls["outstanding"]), sum(cls["outstanding"]) / 100), (9, k["outstanding_payments"]["sum"]))
    expect("1.3 deposits in transit: count, sum", (len(cls["in_transit"]), sum(cls["in_transit"]) / 100), (4, k["deposits_in_transit"]["sum"]))
    expect("1.3 entries posted twice: count, sum", (len(cls["duplicate"]), sum(cls["duplicate"]) / 100), (5, k["duplicates"]["sum"]))
    expect("1.3 bank-only lines: count, sum", (len(cls["bank_only"]), sum(cls["bank_only"]) / 100), (6, k["bank_only"]["sum"]))
    expect("1.3 amount difference: bank, ledger", (cls["error_bank"][0] / 100, cls["error_ledger"][0] / 100), (-43500.0, -45300.0))
    opening = k["opening_balance"]
    expect("1.3 opening balance is in the file", f"{opening:,.2f}" in (FILES / "opening_balance.txt").read_text(encoding="utf-8"), True)
    bank_close = opening + sum(cents(r["amount"]) for r in bank) / 100
    ledger_close = opening + sum(cents(r["amount"]) for r in ledger) / 100
    expect("1.3 bank closing balance", bank_close, k["bank_closing"])
    expect("1.3 ledger closing balance", ledger_close, k["ledger_closing"])
    adj_bank = bank_close + (sum(cls["in_transit"]) + sum(cls["outstanding"])) / 100
    adj_ledger = ledger_close + (-sum(cls["duplicate"]) + sum(cls["bank_only"]) + cls["error_bank"][0] - cls["error_ledger"][0]) / 100
    expect("1.3 adjusted bank balance", round(adj_bank, 2), k["adjusted_balance"])
    expect("1.3 adjusted ledger balance", round(adj_ledger, 2), k["adjusted_balance"])
    tb = {r["account_code"]: r for r in rows(FILES / "trial_balance_oct.csv")}
    expect("1.3 trial balance carries the unadjusted ledger cash", float(tb["1010"]["oct_2026"]), k["ledger_closing"])


# ------------------------------------------------------------------ 1.4 and 2.1
def evaluate(path: Path) -> dict:
    import formulas
    model = formulas.ExcelModel().loads(str(path)).finish()
    out = {}
    for name, cell in model.calculate().items():
        m = re.match(r"'\[[^\]]+\]([A-Z]+)'!([A-Z]+\d+)$", name)
        if m:
            v = cell.value[0][0]
            out[f"{m.group(1).title()}!{m.group(2)}"] = v.item() if hasattr(v, "item") else v
    return out


def spec_values(path: Path) -> dict:
    """The specification applied to the workbook's inputs, in plain Python."""
    from openpyxl import load_workbook
    wb = load_workbook(path)
    a, r, b = wb["Assumptions"], wb["Rates"], wb["Budget"]
    growth, contrib, infl = a["B2"].value, a["B3"].value, a["B4"].value
    full = {r[f"A{i}"].value: r[f"C{i}"].value for i in range(2, 7)}
    out = {}
    for x in range(3, 15):
        g = b[f"D{x}"].value * full[b[f"E{x}"].value] * 12 * (1 + growth)
        h = g * contrib
        j = b[f"I{x}"].value * (1 + infl)
        out[b[f"A{x}"].value] = {"F": full[b[f"E{x}"].value], "G": g, "H": h, "J": j, "L": g + h + j - b[f"K{x}"].value}
    return out


def lab_1_4() -> None:
    k = KEY["budget"]
    path = FILES / "budget_model_fy2027.xlsx"
    spec = spec_values(path)
    calc = evaluate(path)
    for code, c in k["hand_cases"].items():
        for col in "FGHJL":
            expect(f"1.4 hand case {code} {col}: the specification by hand", round(spec[code][col], 2), c["expected"][col])
            expect(f"1.4 model cell Budget!{col}{c['row']} as the formula engine computes it", round(calc[f"Budget!{col}{c['row']}"], 2), c["model_before"][col])
    expect("1.4 right company total by the specification", round(sum(v["L"] for v in spec.values()), 2), k["correct_total_L15"])
    expect("1.4 model total Budget!L15", round(calc["Budget!L15"], 2), k["faulty_total_L15"])
    expect("1.4 model sum of divisions Summary!B12 (differs from the total: a clue)", round(calc["Summary!B12"], 2), k["faulty_sum_of_divisions"])
    from openpyxl import load_workbook
    cached = load_workbook(path, data_only=True)["Budget"]["L15"].value
    expect("1.4 the workbook stores the value a spreadsheet would show", round(cached, 2), k["faulty_total_L15"])
    worked = rows(FILES / "start" / "hand_cases_worked.csv")
    expect("1.4 differences in the worked start file", sum(1 for r in worked if r["equal"] == "لا"), 14)
    expect("1.4 faults listed for lab 2.1", len(rows(FILES / "start" / "fault_list.csv")), 5)


def lab_2_1() -> None:
    k = KEY["budget"]
    from openpyxl import load_workbook
    before = load_workbook(FILES / "budget_model_fy2027.xlsx")["Budget"]
    fixed_path = HERE / "budget_model_fy2027_repaired.xlsx"
    after = load_workbook(fixed_path)["Budget"]
    changed = sorted(c.coordinate for row in before["A1:L15"] for c in row if c.value != after[c.coordinate].value)
    want = sorted([f"{col}{x}" for col in "FHL" for x in range(3, 15)] + ["J7", "L15"])
    expect("2.1 cells that differ between the model and the repair", changed, want)
    calc = evaluate(fixed_path)
    spec = spec_values(fixed_path)
    for code, v in spec.items():
        row = next(x for x in range(3, 15) if after[f"A{x}"].value == code)
        expect(f"2.1 repaired {code} total equals the specification", round(calc[f"Budget!L{row}"], 2), round(v["L"], 2))
    expect("2.1 repaired company total", round(calc["Budget!L15"], 2), k["correct_total_L15"])
    expect("2.1 control: total minus sum of divisions", round(calc["Tests!D10"], 2), 0.0)
    expect("2.1 every test passes in the formula engine", [bool(calc[f"Tests!E{x}"]) for x in list(range(2, 9)) + [10]], [True] * 8)
    tests = load_workbook(fixed_path)["Tests"]
    for x, code in ((7, "CC-101"), (8, "CC-112")):
        expect(f"2.1 test row {x} expects the hand-worked value", round(tests[f"C{x}"].value, 2), k["hand_cases"][code]["expected"]["L"])
    expect("2.1 change log has a line per fix", load_workbook(fixed_path)["ChangeLog"].max_row - 1, 5)
    expect("2.1 the hand case fails on the model before the repair",
           round(evaluate(FILES / "budget_model_fy2027.xlsx")["Budget!L7"], 2) != k["hand_cases"]["CC-105"]["expected"]["L"], True)


# ------------------------------------------------------------------ 2.2
TAG = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(%?)\s*(?:ريال)?\s*\[Variance!([A-F]\d+)\]")
LOOSE = re.compile(r"\d{1,3}(?:,\d{3})+(?![\d,])(?!\s*(?:ريال)?\s*\[Variance!)")


def read_commentary(text: str) -> dict:
    cells = KEY["variance"]["cells"]
    ok = bad = 0
    for num, pct, cell in TAG.findall(text):
        stated = float(num.replace(",", ""))
        shown = round(abs(cells[cell]) * 100, 1) if pct else round(abs(cells[cell]))
        ok, bad = ok + (stated == shown), bad + (stated != shown)
    return {"tags": ok + bad, "match": ok, "no_match": bad, "untagged": len(LOOSE.findall(text))}


def lab_2_2() -> None:
    k = KEY["variance"]
    from openpyxl import load_workbook
    ws = load_workbook(FILES / "variance_oct.xlsx")["Variance"]
    material = []
    for x in range(4, 16):
        bud, act = ws[f"C{x}"].value, ws[f"D{x}"].value
        expect(f"2.2 cell E{x} (actual minus budget)", act - bud, k["cells"][f"E{x}"])
        if abs(act - bud) >= 20000 and abs(act - bud) / bud >= 0.10:
            material.append(ws[f"A{x}"].value)
    expect("2.2 cost centres the rule asks a comment on", material, k["material"])
    calc = evaluate(FILES / "variance_oct.xlsx")
    expect("2.2 total variance in the formula engine", round(calc["Variance!E16"]), k["cells"]["E16"])
    draft = (FILES / "ai_draft_commentary.txt").read_text(encoding="utf-8")
    d = read_commentary(draft)
    expect("2.2 scripted draft: figures with a cell", d["tags"], k["draft"]["tagged_figures"])
    expect("2.2 scripted draft: figures that match their cell", d["match"], k["draft"]["tags_that_match"])
    expect("2.2 scripted draft: figures that do not", d["no_match"], k["draft"]["tags_that_do_not_match"])
    expect("2.2 scripted draft: figures with no cell", d["untagged"], k["draft"]["untagged_figures"])
    expect("2.2 scripted draft: material centres left out", [c for c in material if c not in draft], k["draft"]["material_centres_missing"])
    notes = (FILES / "cc_notes.txt").read_text(encoding="utf-8")
    evidenced = [c for c in material if re.search(rf"^{c} ", notes, re.M)]
    expect("2.2 material centres with a note from the owner", evidenced, k["with_evidence"])
    ref = (HERE / "commentary_reference.txt").read_text(encoding="utf-8")
    r = read_commentary(ref)
    expect("2.2 reference commentary: every figure has a cell and matches", (r["tags"], r["no_match"], r["untagged"]), (13, 0, 0))
    expect("2.2 reference commentary covers the material centres", all(c in ref for c in material), True)
    expect("2.2 reference commentary marks the undocumented causes", ref.count("غير موثق"), len(k["to_confirm"]))
    for name, want in (("ai_draft_commentary.txt", (10, 7, 1, ["CC-109"], ["CC-101"])), ("commentary_reference.txt", (13, 13, 0, [], []))):
        with workdir(name, "variance_oct.xlsx"):
            ns, _ = run_cells(notebook_code("commentary_check.ipynb", ('"ai_draft_commentary.txt"', f'"{name}"')))
        got = (len(ns["tags"]), int(ns["tags"]["match"].sum()), len(ns["untagged"]), ns["missing"], ns["extra"])
        expect(f"2.2 notebook on {name}", got, want)


# ------------------------------------------------------------------ 2.3
def lab_2_3() -> None:
    k = KEY["sample"]
    inv = rows(FILES / "invoices_fy2026.csv")
    expect("2.3 population: count", len(inv), k["population"]["count"])
    expect("2.3 population: sum", sum(cents(r["amount"]) for r in inv) / 100, k["population"]["sum"])
    key_items = [r for r in inv if cents(r["amount"]) >= 100000 * 100]
    rest = sorted((r for r in inv if cents(r["amount"]) < 100000 * 100), key=lambda r: r["invoice_id"])
    expect("2.3 key items: count", len(key_items), k["key_items"]["count"])
    expect("2.3 key items: sum", sum(cents(r["amount"]) for r in key_items) / 100, k["key_items"]["sum"])
    expect("2.3 remainder: count", len(rest), k["remainder"]["count"])
    interval = len(rest) // 60
    start = int(random.Random(20261031).random() * interval) + 1
    expect("2.3 interval", interval, k["interval"])
    expect("2.3 random start from seed 20261031", start, k["start"])
    sample = [rest[start - 1 + interval * i] for i in range(60)]
    expect("2.3 sample invoices", [r["invoice_id"] for r in sample], k["sample_ids"])
    expect("2.3 sample sum", sum(cents(r["amount"]) for r in sample) / 100, k["sample_sum"])
    twins = Counter((r["supplier_id"], r["supplier_invoice_no"], cents(r["amount"])) for r in inv)
    day = defaultdict(list)
    for r in inv:
        if cents(r["amount"]) < 50000 * 100:
            day[(r["supplier_id"], r["invoice_date"])].append(cents(r["amount"]))

    def flags(r):
        f = []
        if not r["po_number"]:
            f.append("missing_po")
        if twins[(r["supplier_id"], r["supplier_invoice_no"], cents(r["amount"]))] > 1:
            f.append("duplicate")
        if r["invoice_date"][:7] > r["posting_period"]:
            f.append("cut_off")
        d = day[(r["supplier_id"], r["invoice_date"])]
        if cents(r["amount"]) < 50000 * 100 and len(d) > 1 and sum(d) >= 50000 * 100:
            f.append("split_under_limit")
        return f

    found = defaultdict(list)
    for r in key_items + sample:
        for f in flags(r):
            found[f].append(r["invoice_id"])
    expect("2.3 items to look at among the 98 tested", {a: sorted(b) for a, b in sorted(found.items())},
           {a: sorted(b) for a, b in sorted(k["flags_in_tested_items"].items())})
    pop = defaultdict(int)
    for r in inv:
        for f in flags(r):
            pop[f] += 1
    expect("2.3 the same tests over the whole population (the stretch)", dict(sorted(pop.items())),
           {"cut_off": 5, "duplicate": 12, "missing_po": 9, "split_under_limit": 9})
    text = (FILES / "ai_sample_answer.txt").read_text(encoding="utf-8")
    first, second = text.split("حين أُعيد الطلب")
    ids = re.findall(r"INV-\d{6}", first)
    known = {r["invoice_id"] for r in inv}
    p = k["prose_answer"]
    expect("2.3 scripted prose answer: invoices listed", len(ids), p["listed"])
    expect("2.3 scripted prose answer: not in the population", sum(1 for i in ids if i not in known), p["not_in_population"])
    expect("2.3 scripted prose answer: among the first 1,000 numbers", sum(1 for i in ids if int(i[4:]) <= 1000), p["in_first_1000"])
    expect("2.3 scripted prose answer: a second request gives another list", set(re.findall(r"INV-\d{6}", second)) <= set(ids), False)
    with workdir("invoices_fy2026.csv") as tmp:
        ns, _ = run_cells(notebook_code("audit_sample.ipynb"))
        again, _ = run_cells(notebook_code("audit_sample.ipynb"))
        file_rows = (tmp / "sampling_file.csv").read_text(encoding="utf-8-sig").splitlines()
        log = rows(tmp / "run_log.csv")
    expect("2.3 notebook draws the same sample", ns["sample"]["invoice_id"].tolist(), k["sample_ids"])
    expect("2.3 a second run of the notebook draws it again", again["sample"]["invoice_id"].tolist(), k["sample_ids"])
    expect("2.3 notebook items to look at", sorted(ns["look"]["invoice_id"]), sorted(i for v in k["flags_in_tested_items"].values() for i in v))
    expect("2.3 sampling file: 98 tested invoices and a method line",
           (len(file_rows) - 2, "seed=20261031" in file_rows[-1], f"start={k['start']}" in file_rows[-1]), (98, True, True))
    expect("2.3 run log has a line per run", len(log), 2)


# ------------------------------------------------------------------ 2.4
def lab_2_4() -> None:
    cards = rows(FILES / "data_cards.csv")
    rule = {}
    for c in cards:
        public = c["classification"] == "عام"
        rule[c["card"]] = {"public_assistant": public, "raqeem": c["classification"] in ("عام", "مقيد") and c["personal_data"] == "لا", "local_tools": True}
    expect("2.4 tools each file may enter, by the register's rule", rule, KEY["data_rules"])
    expect("2.4 files a public assistant may hold", [c for c, v in rule.items() if v["public_assistant"]], ["F6"])
    expect("2.4 files the approved assistant may not hold", [c for c, v in rule.items() if not v["raqeem"]], ["F3", "F7"])
    pay = rows(FILES / "payroll_oct_extract.csv")
    expect("2.4 payroll extract is marked synthetic", all(r["national_id"].startswith("TEST-ID-") and "TEST" in r["iban"] for r in pay), True)
    k = KEY["redesign"]
    st = rows(FILES / "redesign" / "supplier_statement.csv")
    le = rows(FILES / "redesign" / "ap_ledger_supplier.csv")
    expect("2.4 control totals in: statement lines, balance", (len(st), sum(cents(r["amount"]) for r in st) / 100), (k["statement"]["lines"], k["statement"]["balance"]))
    expect("2.4 control totals in: ledger lines, balance", (len(le), sum(cents(r["amount"]) for r in le) / 100), (k["ledger"]["lines"], k["ledger"]["balance"]))
    pool = defaultdict(list)
    for r in le:
        pool[r["document"]].append(cents(r["amount"]))
    diffs, effect = {}, 0
    for r in st:
        h = cents(r["amount"])
        if not pool[r["document"]]:
            diffs[r["document"]] = "not booked"
            effect += h
        else:
            led = pool[r["document"]].pop(0)
            if led != h:
                diffs[r["document"]] = "amount"
                effect += h - led
    for doc, left in pool.items():
        for led in left:
            diffs[doc] = "booked twice"
            effect -= led
    i = k["items"]
    expect("2.4 the four differences", dict(sorted(diffs.items())), dict(sorted({
        i["not_booked_invoice"]: "not booked", i["not_booked_credit_note"]: "not booked",
        i["amount_difference"]["document"]: "amount", i["payment_booked_twice"]: "booked twice"}.items())))
    expect("2.4 control total out: the differences explain the gap between the balances", effect / 100, k["difference"])
    base = rows(FILES / "redesign" / "baseline_log_dhilal.csv")
    expect("2.4 baseline: mean minutes (rounded), mean errors", (round(sum(int(r["minutes"]) for r in base) / 3), sum(int(r["errors"]) for r in base) / 3), (46, 2.0))
    expect("2.4 baseline: errors are missed plus wrongly flagged", all(int(r["errors"]) == int(r["missed"]) + int(r["wrongly_flagged"]) for r in base), True)


LABS = {"1.1": lab_1_1, "1.2": lab_1_2, "1.3": lab_1_3, "1.4": lab_1_4, "2.1": lab_2_1, "2.2": lab_2_2, "2.3": lab_2_3, "2.4": lab_2_4}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    wanted = sys.argv[1:] or list(LABS)
    for lab in wanted:
        LABS[lab]()
        print(f"PASS  lab {lab}")
    print(f"{len(wanted)} of {len(wanted)} labs pass")
