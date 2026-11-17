# /// script
# requires-python = ">=3.11"
# dependencies = ["xlsxwriter>=3.2"]
# ///
"""Writes the synthetic file pack of Dhilal Facilities Management Company (fictional).

  uv run labs/_tools/prepare_files.py

Fixed seed: the same bytes on every run. Everything is invented: the company, its people,
suppliers, customers, bank lines, invoices and payroll rows. The planted problems and the
reference figures go to labs/solutions/key.json for the trainer; labs/solutions/check.py
recomputes them from the files without this generator.
"""
from __future__ import annotations

import csv
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

import xlsxwriter

from texts import ANSWERS, NOTEBOOKS, TEXT_FILES

LABS = Path(__file__).resolve().parent.parent
FILES = LABS / "files"
SOL = LABS / "solutions"
SEED = 20261017
R = random.Random(SEED)
KEY: dict = {}


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip("\n") + "\n", encoding="utf-8", newline="\n")


def money(x: float) -> str:
    return f"{x:.2f}"


NAMES = ["الصانع", "بريق", "المنارة", "رواسي الخليج", "دانة", "السارية", "الفنار", "ريحانة", "المدار", "الوتد",
         "سما", "نبراس", "الركن الأخضر", "جسور", "الساحل", "المرجان", "طيبة", "الغدير", "أفق", "البيرق",
         "النخيل", "قمم", "الواحة", "سنابل", "الينابيع", "مسارات", "ضفاف", "الرواد", "إتقان الشرق", "الميزان"]
SUP_KIND = ["للمواد", "لمواد النظافة", "لقطع الغيار", "للتوريدات", "للمعدات", "للزي الموحد", "للوقود", "للأنظمة الأمنية"]
CUST_KIND = ["القابضة", "للعقارات", "الطبية", "التعليمية", "للتطوير", "التجارية"]
CC = [
    ("CC-101", "نظافة المباني الحكومية", "النظافة", 60, "G1", 420000, 0),
    ("CC-102", "نظافة المجمعات التجارية", "النظافة", 45, "G1", 310000, 25000),
    ("CC-103", "نظافة المرافق الصحية", "النظافة", 30, "G2", 280000, 0),
    ("CC-104", "الصيانة الميدانية", "الصيانة", 24, "G3", 520000, 60000),
    ("CC-105", "صيانة التكييف والتبريد", "الصيانة", 18, "G3", 400000, 40000),
    ("CC-106", "صيانة المصاعد والأنظمة", "الصيانة", 10, "G4", 260000, 0),
    ("CC-107", "الحراسات الأمنية", "الأمن", 80, "G1", 90000, 0),
    ("CC-108", "غرفة المراقبة والتحكم", "الأمن", 12, "G2", 150000, 0),
    ("CC-109", "المشتريات والمستودعات", "المساندة", 8, "G3", 60000, 0),
    ("CC-110", "أسطول المركبات", "المساندة", 6, "G2", 480000, 30000),
    ("CC-111", "الموارد البشرية والتدريب", "المساندة", 7, "G4", 120000, 0),
    ("CC-112", "الإدارة المالية وتقنية المعلومات", "المساندة", 9, "G5", 200000, 0),
]
DIVISIONS = ["النظافة", "الصيانة", "الأمن", "المساندة"]
RATES = [("G1", 4000, 5200), ("G2", 5500, 7100), ("G3", 7500, 9600), ("G4", 11000, 13800), ("G5", 15000, 18500)]
ASSUME = {"growth": 0.04, "contrib": 0.12, "inflation": 0.03}


def supplier(i: int) -> str:
    return f"{'مؤسسة' if i % 3 else 'شركة'} {NAMES[i % len(NAMES)]} {SUP_KIND[(i // len(NAMES) + i) % len(SUP_KIND)]}"


def customer(i: int) -> str:
    return f"شركة {NAMES[(i * 7 + 3) % len(NAMES)]} {CUST_KIND[i % len(CUST_KIND)]}"


# ---------------------------------------------------------------- lab 1.1: trial balance, six answers
def transpose(x: float) -> float:
    """The same total with two neighbouring digits swapped: what a prose sum gets wrong."""
    d = list(str(int(x)))
    i = next(k for k in range(2, len(d) - 1) if d[k] != d[k + 1])
    d[i], d[i + 1] = d[i + 1], d[i]
    return float("".join(d)) + round(x - int(x), 2)


def trial_balance() -> None:
    rows = [
        ("4010", "إيرادات عقود النظافة", "إيرادات", 1184300.00, 1212750.00),
        ("4020", "إيرادات عقود الصيانة", "إيرادات", 968400.00, 1004880.00),
        ("4030", "إيرادات عقود الحراسات", "إيرادات", 702150.00, 731400.00),
        ("5010", "رواتب وأجور", "مصروفات", 1296400.00, 1337885.00),
        ("5020", "بدلات سكن ونقل", "مصروفات", 318200.00, 327746.00),
        ("5030", "تأمينات اجتماعية", "مصروفات", 151300.00, 156142.00),
        ("5110", "مواد نظافة", "مصروفات", 98450.00, 104310.00),
        ("5120", "قطع غيار", "مصروفات", 132700.00, 149865.00),
        ("5130", "وقود وزيوت", "مصروفات", 41980.00, 39470.00),
        ("5140", "إيجار مركبات", "مصروفات", 56000.00, 48000.00),
        ("5150", "زي موحد ومعدات سلامة", "مصروفات", 22300.00, 31790.00),
        ("5210", "إيجار مكاتب ومستودعات", "مصروفات", 87500.00, 87500.00),
        ("5220", "كهرباء ومياه واتصالات", "مصروفات", 19640.00, 18225.00),
        ("5230", "تأمين طبي", "مصروفات", 74200.00, 74200.00),
        ("5240", "تدريب وتأهيل", "مصروفات", 12800.00, 26450.00),
        ("5250", "رسوم حكومية وتراخيص", "مصروفات", 33150.00, 21900.00),
        ("5260", "استهلاك أصول", "مصروفات", 64300.00, 64300.00),
        ("1010", "النقد لدى البنك", "أصول", 2350000.00, 0.0),
        ("1100", "ذمم مدينة", "أصول", 3412600.00, 3586900.00),
        ("1200", "مخزون مواد وقطع غيار", "أصول", 486300.00, 471250.00),
        ("2010", "ذمم دائنة", "التزامات", 1274800.00, 1198450.00),
        ("2100", "مستحقات رواتب", "التزامات", 402300.00, 415700.00),
    ]
    KEY["tb_rows"] = rows  # the cash line is filled after the bank files exist
    exp = [r for r in rows if r[2] == "مصروفات"]
    rev = [r for r in rows if r[2] == "إيرادات"]
    exp_total = round(sum(r[4] for r in exp), 2)
    largest = max(exp, key=lambda r: r[4])
    payroll_codes = {"5010", "5020", "5030"}
    non_payroll = round(sum(r[4] for r in exp if r[0] not in payroll_codes), 2)
    a6_wrong = round(sum(r[4] for r in exp if "رواتب" not in r[1]), 2)
    salaries = next(r for r in rows if r[0] == "5010")
    KEY["answers"] = {
        "revenue_oct": round(sum(r[4] for r in rev), 2),
        "expenses_oct": exp_total,
        "expense_accounts": len(exp),
        "a2_stated": transpose(exp_total),
        "largest_expense": largest[1],
        "largest_share_pct": round(100 * largest[4] / exp_total, 1),
        "salary_change_pct": round(100 * (salaries[4] / salaries[3] - 1), 1),
        "non_payroll_expenses": non_payroll,
        "a6_stated": a6_wrong,
        "a6_accounts_included": sum(1 for r in exp if "رواتب" not in r[1]),
        "non_payroll_accounts": len(exp) - len(payroll_codes),
        "classification": {"A1": "computed", "A2": "generated", "A3": "computed", "A4": "generated",
                           "A5": "generated", "A6": "computed"},
        "figure_right": {"A1": True, "A2": False, "A3": True, "A4": True, "A5": False, "A6": False},
    }
    assert KEY["answers"]["a2_stated"] != exp_total and abs(KEY["answers"]["a2_stated"] - exp_total) < 400000

    # A5: an AI cell function classifies 20 expense descriptions; two refreshes differ
    desc = ["مطهرات أرضيات 20 لتر", "فلاتر مكيفات مركزية", "قفازات ومعدات وقاية", "منظف زجاج مركز", "ضاغط تكييف 5 طن",
            "أكياس نفايات صناعية", "سترات عاكسة للحراس", "زيت محركات للمولدات", "مناديل ومستلزمات دورات المياه", "أحذية سلامة",
            "حساسات مصاعد", "ملمع رخام", "كشافات يدوية للحراس", "غاز تبريد R410", "معقم أيدي عبوات", "خوذ سلامة",
            "سيور مراوح", "مكانس كهربائية صناعية", "أقفال وسلاسل بوابات", "صابون سائل براميل"]
    cat1 = ["مواد نظافة", "قطع غيار", "معدات سلامة", "مواد نظافة", "قطع غيار", "مواد نظافة", "معدات سلامة", "قطع غيار",
            "مواد نظافة", "معدات سلامة", "قطع غيار", "مواد نظافة", "معدات سلامة", "قطع غيار", "مواد نظافة",
            "معدات سلامة", "قطع غيار", "مواد نظافة", "معدات سلامة", "مواد نظافة"]
    cat2 = list(cat1)
    cat2[2], cat2[7], cat2[18] = "مواد نظافة", "مواد نظافة", "قطع غيار"
    write_csv(FILES / "ai_answers" / "A5_ai_function_runs.csv", ["row", "description", "ai_category_run_1", "ai_category_run_2"],
              [[i + 1, d, cat1[i], cat2[i]] for i, d in enumerate(desc)])
    KEY["answers"]["a5_changed_rows"] = [i + 1 for i in range(20) if cat1[i] != cat2[i]]
    KEY["answers"]["a5_cleaning_run_1"] = cat1.count("مواد نظافة")
    KEY["answers"]["a5_cleaning_run_2"] = cat2.count("مواد نظافة")


def write_trial_balance(cash_oct: float) -> None:
    rows = [list(r) for r in KEY.pop("tb_rows")]
    for r in rows:
        if r[0] == "1010":
            r[4] = cash_oct
    write_csv(FILES / "trial_balance_oct.csv", ["account_code", "account_name", "group", "sep_2026", "oct_2026"],
              [[r[0], r[1], r[2], money(r[3]), money(r[4])] for r in rows])
    a = KEY["answers"]
    fmt = {
        "REV": f"{a['revenue_oct']:,.2f}", "A2": f"{a['a2_stated']:,.2f}", "LARGEST": a["largest_expense"],
        "SHARE": f"{a['largest_share_pct']}", "SALPCT": f"{a['salary_change_pct']}", "A6": f"{a['a6_stated']:,.2f}",
        "N6": str(a["a6_accounts_included"]), "C1": str(a["a5_cleaning_run_1"]),
    }
    for name, text in ANSWERS.items():
        for k, v in fmt.items():
            text = text.replace("{" + k + "}", v)
        write_text(FILES / "ai_answers" / name, text)
    write_csv(FILES / "ai_answers" / "classification_sheet.csv",
              ["answer", "computed_or_generated", "what_shows_it", "check_it_needs", "figure_recomputed", "matches"],
              [[f"A{i}", "", "", "", "", ""] for i in range(1, 7)])


# ---------------------------------------------------------------- labs 1.2 and 1.3: bank and ledger
def bank_and_ledger() -> None:
    opening = 2350000.00
    d0 = date(2026, 10, 1)
    base = []
    for i in range(587):
        pay = R.random() < 0.62
        day = R.randint(0, 27)
        if pay:
            kind = "CHQ" if R.random() < 0.3 else "TRF"
            ref = f"{kind}-{260000 + i * 3 + R.randint(0, 2):06d}"
            amt = -round(R.choice([R.uniform(350, 4800), R.uniform(4800, 38000), R.uniform(38000, 96000)]), 2)
            desc = f"سداد {supplier(R.randint(0, 139))}"
        else:
            ref = f"RCV-{410000 + i * 2 + R.randint(0, 1):06d}"
            amt = round(R.choice([R.uniform(5000, 40000), R.uniform(40000, 110000)]), 2)
            desc = f"تحصيل {customer(R.randint(0, 39))}"
        base.append({"ref": ref, "amt": amt, "desc": desc, "ldate": d0 + timedelta(days=day),
                     "bdate": d0 + timedelta(days=min(30, day + R.choice([0, 0, 1, 1, 2])))})
    # six pairs of different payments that share an amount: an amount-only match pairs them wrongly
    twins = R.sample([b for b in base if b["amt"] < 0], 12)
    for a, b in zip(twins[:6], twins[6:]):
        b["amt"] = a["amt"]
    bank, ledger = [], []
    for b in base:
        bank.append([b["bdate"], b["ref"], b["desc"], b["amt"]])
        ledger.append([b["ldate"], b["ref"], b["desc"], b["amt"]])
    # one transposed amount in the ledger: the bank is right
    err_ref = "TRF-299101"
    bank.append([date(2026, 10, 14), err_ref, f"سداد {supplier(17)}", -43500.00])
    ledger.append([date(2026, 10, 13), err_ref, f"سداد {supplier(17)}", -45300.00])
    # timing: in the ledger in the last days, not yet at the bank
    timing = []
    for j in range(9):
        row = [date(2026, 10, 28 + j % 4), f"CHQ-2995{j:02d}", f"سداد {supplier(40 + j)}", -round(R.uniform(2500, 61000), 2)]
        timing.append(row)
    for j in range(4):
        row = [date(2026, 10, 30 + j % 2), f"RCV-4995{j:02d}", f"تحصيل {customer(11 + j)}", round(R.uniform(15000, 120000), 2)]
        timing.append(row)
    ledger += [list(t) for t in timing]
    # five ledger entries posted twice
    dup_src = R.sample([b for b in base if b["amt"] < 0 and b not in twins], 5)
    dups = [[min(date(2026, 10, 31), b["ldate"] + timedelta(days=R.choice([0, 1]))), b["ref"], b["desc"], b["amt"]] for b in dup_src]
    ledger += [list(d) for d in dups]
    # six bank-only lines
    bank_only = [
        [date(2026, 10, 5), "FEE-100501", "رسوم خدمات مصرفية", -75.00],
        [date(2026, 10, 15), "FEE-101502", "رسوم تحويلات دولية", -120.00],
        [date(2026, 10, 31), "FEE-103103", "رسوم كشف حساب", -45.00],
        [date(2026, 10, 22), "DEP-102201", f"إيداع مباشر {customer(5)}", 86250.00],
        [date(2026, 10, 29), "DEP-102902", f"إيداع مباشر {customer(23)}", 41800.00],
        [date(2026, 10, 27), "RTN-102701", f"شيك مرتجع {customer(8)}", -27600.00],
    ]
    bank += [list(b) for b in bank_only]
    bank.sort(key=lambda r: (r[0], r[1]))
    ledger.sort(key=lambda r: (r[0], r[1], r[3]))
    # eight bank references typed differently (lower case, spaces): the key must be normalised
    messy = R.sample([i for i, r in enumerate(bank) if r[1].startswith(("TRF", "CHQ"))], 8)
    bank_out = []
    for i, r in enumerate(bank):
        ref = f" {r[1].lower()} " if i in messy else r[1]
        bank_out.append([f"B{i + 1:04d}", r[0].isoformat(), ref, r[2], money(r[3])])
    posted = ["yusra.b", "accountant2", "accountant3"]
    ledger_out = [[f"L{i + 1:04d}", r[0].isoformat(), r[1], r[2], money(r[3]), posted[(i * 5 + len(r[1])) % 3]] for i, r in enumerate(ledger)]
    assert len(bank_out) == 594 and len(ledger_out) == 606, (len(bank_out), len(ledger_out))
    write_csv(FILES / "bank_statement_oct.csv", ["line_no", "date", "reference", "description", "amount"], bank_out)
    write_csv(FILES / "ledger_cash_oct.csv", ["entry_no", "date", "reference", "description", "amount", "posted_by"], ledger_out)

    bank_sum = round(sum(r[3] for r in bank), 2)
    ledger_sum = round(sum(r[3] for r in ledger), 2)
    tim_pay = round(sum(t[3] for t in timing if t[3] < 0), 2)
    tim_rec = round(sum(t[3] for t in timing if t[3] > 0), 2)
    dup_sum = round(sum(d[3] for d in dups), 2)
    bo_sum = round(sum(b[3] for b in bank_only), 2)
    bank_close = round(opening + bank_sum, 2)
    ledger_close = round(opening + ledger_sum, 2)
    adj_bank = round(bank_close + tim_pay + tim_rec, 2)
    adj_ledger = round(ledger_close - dup_sum + bo_sum + (-43500.00 - -45300.00), 2)
    assert adj_bank == adj_ledger, (adj_bank, adj_ledger)
    KEY["recon"] = {
        "opening_balance": opening, "bank_lines": 594, "ledger_lines": 606, "bank_sum": bank_sum, "ledger_sum": ledger_sum,
        "matched_pairs": 587, "matched_sum": round(sum(b["amt"] for b in base), 2),
        "amount_difference": {"reference": err_ref, "bank": -43500.00, "ledger": -45300.00},
        "outstanding_payments": {"count": 9, "sum": tim_pay}, "deposits_in_transit": {"count": 4, "sum": tim_rec},
        "duplicates": {"count": 5, "sum": dup_sum, "references": sorted(d[1] for d in dups)},
        "bank_only": {"count": 6, "sum": bo_sum},
        "bank_closing": bank_close, "ledger_closing": ledger_close, "adjusted_balance": adj_bank,
        "messy_references": 8, "same_amount_pairs": 6,
    }
    write_text(FILES / "opening_balance.txt",
               f"شركة ظِلال لإدارة المرافق · الحساب الجاري الرئيسي · أكتوبر 2026\n"
               f"الرصيد الافتتاحي في 1 أكتوبر 2026 في كشف البنك وفي دفتر الأستاذ: {opening:,.2f} ريال.\n"
               f"مطابقة سبتمبر أُقفلت دون بنود معلقة.\n"
               f"المبالغ الموجبة مقبوضات والسالبة مدفوعات، في الملفين.")

    # start files for lab 1.3: the 25 unmatched items, unclassified
    ref_of = lambda s: s.strip().upper()
    led_refs = {}
    for r in ledger_out:
        led_refs.setdefault(r[2], []).append(r)
    bank_refs = {ref_of(r[2]): r for r in bank_out}
    items = []
    for r in bank_out:
        k = ref_of(r[2])
        if k not in led_refs:
            items.append(["bank", r[0], r[1], k, r[3], r[4]])
        elif k == err_ref:
            items.append(["bank", r[0], r[1], k, r[3], r[4]])
    for k, rs in led_refs.items():
        if k not in bank_refs:
            items += [["ledger", r[0], r[1], k, r[3], r[4]] for r in rs]
        elif k == err_ref:
            items.append(["ledger", rs[0][0], rs[0][1], k, rs[0][3], rs[0][4]])
        elif len(rs) > 1:
            items += [["ledger", r[0], r[1], k, r[3], r[4]] for r in rs[1:]]
    # the amount difference is one item with two lines
    assert len(items) == 26, len(items)
    items.sort(key=lambda r: (r[0], r[2], r[1]))
    write_csv(FILES / "start" / "unmatched_items.csv", ["side", "id", "date", "reference", "description", "amount", "class", "action"],
              [i + ["", ""] for i in items])
    write_text(FILES / "start" / "match_summary.txt", f"""
ملخص المطابقة المرجعي لأكتوبر 2026 (نقطة بداية المختبر 1.3)
المفتاح: المرجع بعد حذف المسافات وتوحيد الحروف، ثم المبلغ.

كشف البنك: 594 سطرًا، مجموعها {bank_sum:,.2f}
دفتر الأستاذ: 606 أسطر، مجموعها {ledger_sum:,.2f}
أزواج متطابقة مرجعًا ومبلغًا: 587 زوجًا، مجموعها {KEY['recon']['matched_sum']:,.2f}
بنود غير متطابقة: 25 بندًا في unmatched_items.csv (26 سطرًا: فرق المبلغ بند واحد له سطران)
الفحص: 587 + 7 = 594 سطرًا في البنك، و587 + 19 = 606 أسطر في الدفتر.
""")


# ---------------------------------------------------------------- labs 1.4 and 2.1: budget workbook
def budget_values(faulty: bool) -> dict:
    """The values each formula returns, computed here so the workbook carries cached results."""
    rate = {g: (b, t) for g, b, t in RATES}
    out = {"rows": []}
    for n, (code, name, div, hc, grade, sup, rec) in enumerate(CC):
        row = n + 3
        f = rate[grade][0 if faulty else 1]
        g = hc * f * 12 * (1 + ASSUME["growth"])
        if faulty:
            contrib = {3: ASSUME["contrib"], 4: ASSUME["inflation"]}.get(row, 0)
        else:
            contrib = ASSUME["contrib"]
        h = g * contrib
        j = sup if (faulty and row == 7) else sup * (1 + ASSUME["inflation"])
        l = g + h + j + rec if faulty else g + h + j - rec
        out["rows"].append({"F": f, "G": g, "H": h, "J": j, "L": l})
    rows = out["rows"]
    out["D15"] = sum(c[3] for c in CC)
    for col in "GHJ":
        out[col + "15"] = sum(r[col] for r in rows)
    out["K15"] = sum(c[6] for c in CC)
    out["L15"] = sum(r["L"] for r in (rows[:-1] if faulty else rows))
    out["div"] = {d: sum(r["L"] for r, c in zip(rows, CC) if c[2] == d) for d in DIVISIONS}
    return out


def budget_workbook(path: Path, faulty: bool) -> dict:
    v = budget_values(faulty)
    wb = xlsxwriter.Workbook(str(path))
    wb.set_properties({"title": "Dhilal FY2027 budget (synthetic)", "author": "SDAIA Academy", "created": datetime(2026, 10, 17)})
    h = wb.add_format({"bold": True, "bg_color": "#E7EEF5", "border": 1, "text_wrap": True, "valign": "top"})
    num = wb.add_format({"num_format": "#,##0"})
    pct = wb.add_format({"num_format": "0.0%"})
    bold = wb.add_format({"bold": True, "num_format": "#,##0"})
    title = wb.add_format({"bold": True, "font_size": 13})

    a = wb.add_worksheet("Assumptions"); a.right_to_left(); a.set_column("A:A", 44); a.set_column("B:B", 12)
    a.write("A1", "افتراضات موازنة 2027 · شركة ظِلال لإدارة المرافق (بيانات اصطناعية)", title)
    a.write("A2", "زيادة الرواتب السنوية"); a.write("B2", ASSUME["growth"], pct)
    a.write("A3", "اشتراكات وتأمينات على صاحب العمل، من الرواتب السنوية"); a.write("B3", ASSUME["contrib"], pct)
    a.write("A4", "تضخم عقود المواد والخدمات"); a.write("B4", ASSUME["inflation"], pct)

    r = wb.add_worksheet("Rates"); r.right_to_left(); r.set_column("A:C", 26)
    for c, t in enumerate(["الدرجة", "الراتب الأساسي الشهري", "الراتب الشهري الشامل (مع البدلات)"]):
        r.write(0, c, t, h)
    for i, (g, b, t) in enumerate(RATES):
        r.write(i + 1, 0, g); r.write(i + 1, 1, b, num); r.write(i + 1, 2, t, num)

    b = wb.add_worksheet("Budget"); b.right_to_left(); b.set_column("A:A", 9); b.set_column("B:B", 30); b.set_column("C:L", 15)
    b.write("A1", "موازنة 2027 حسب مركز التكلفة (ريال)", title)
    heads = ["الرمز", "مركز التكلفة", "القطاع", "عدد الموظفين", "الدرجة الغالبة", "الراتب الشهري الشامل", "الرواتب السنوية 2027",
             "اشتراكات صاحب العمل", "مواد وخدمات 2026", "مواد وخدمات 2027", "مبالغ مستردة من العملاء", "إجمالي الموازنة"]
    for c, t in enumerate(heads):
        b.write(1, c, t, h)
    for n, (code, name, div, hc, grade, sup, rec) in enumerate(CC):
        x = n + 3
        vals = v["rows"][n]
        b.write(f"A{x}", code); b.write(f"B{x}", name); b.write(f"C{x}", div); b.write(f"D{x}", hc, num); b.write(f"E{x}", grade)
        b.write_formula(f"F{x}", f"=VLOOKUP(E{x},Rates!$A$2:$C$6,{2 if faulty else 3},FALSE)", num, vals["F"])
        b.write_formula(f"G{x}", f"=D{x}*F{x}*12*(1+Assumptions!$B$2)", num, vals["G"])
        b.write_formula(f"H{x}", f"=G{x}*Assumptions!{'B' + str(x) if faulty else '$B$3'}", num, vals["H"])
        b.write(f"I{x}", sup, num)
        if faulty and x == 7:
            b.write(f"J{x}", sup, num)
        else:
            b.write_formula(f"J{x}", f"=I{x}*(1+Assumptions!$B$4)", num, vals["J"])
        b.write(f"K{x}", rec, num)
        b.write_formula(f"L{x}", f"=G{x}+H{x}+J{x}{'+' if faulty else '-'}K{x}", num, vals["L"])
    b.write("B15", "الإجمالي", bold)
    b.write_formula("D15", "=SUM(D3:D14)", bold, v["D15"])
    for col in "GHJK":
        b.write_formula(f"{col}15", f"=SUM({col}3:{col}14)", bold, v[col + "15"])
    b.write_formula("L15", f"=SUM(L3:L{13 if faulty else 14})", bold, v["L15"])

    s = wb.add_worksheet("Summary"); s.right_to_left(); s.set_column("A:A", 36); s.set_column("B:B", 18)
    s.write("A1", "ملخص موازنة 2027", title)
    s.write("A2", "إجمالي الموازنة"); s.write_formula("B2", "=Budget!L15", bold, v["L15"])
    s.write("A3", "الرواتب والاشتراكات"); s.write_formula("B3", "=Budget!G15+Budget!H15", num, v["G15"] + v["H15"])
    s.write("A4", "عدد الموظفين"); s.write_formula("B4", "=Budget!D15", num, v["D15"])
    s.write("A5", "تكلفة الموظف السنوية"); s.write_formula("B5", "=B3/B4", num, (v["G15"] + v["H15"]) / v["D15"])
    s.write("A7", "حسب القطاع", h); s.write("B7", "إجمالي الموازنة", h)
    for i, d in enumerate(DIVISIONS):
        s.write(7 + i, 0, d)
        s.write_formula(7 + i, 1, f"=SUMIF(Budget!$C$3:$C$14,A{8 + i},Budget!$L$3:$L$14)", num, v["div"][d])
    s.write("A12", "مجموع القطاعات"); s.write_formula("B12", "=SUM(B8:B11)", bold, sum(v["div"].values()))

    if not faulty:
        good = v
        t = wb.add_worksheet("Tests"); t.right_to_left(); t.set_column("A:A", 54); t.set_column("B:D", 16); t.set_column("E:E", 10)
        for c, x in enumerate(["الاختبار", "الخلية", "المتوقع (محسوب يدويًا)", "الفعلي", "ناجح؟"]):
            t.write(0, c, x, h)
        tests = [
            ("الإصلاح 1 · الراتب الشامل لمركز CC-101 من العمود الصحيح", "Budget!F3", 5200),
            ("الإصلاح 2 · اشتراكات CC-105 بنسبة 12% من الرواتب", "Budget!H7", good["rows"][4]["H"]),
            ("الإصلاح 3 · مواد وخدمات CC-105 بعد التضخم", "Budget!J7", good["rows"][4]["J"]),
            ("الإصلاح 4 · إجمالي CC-105 يطرح المبالغ المستردة", "Budget!L7", good["rows"][4]["L"]),
            ("الإصلاح 5 · الإجمالي يشمل CC-112: يساوي مجموع القطاعات", "Budget!L15", good["L15"]),
            ("حالة يدوية · إجمالي CC-101", "Budget!L3", good["rows"][0]["L"]),
            ("حالة يدوية · إجمالي CC-112", "Budget!L14", good["rows"][11]["L"]),
        ]
        for i, (name, cell, exp) in enumerate(tests):
            x = i + 2
            t.write(f"A{x}", name); t.write(f"B{x}", cell); t.write(f"C{x}", round(exp, 2), num)
            t.write_formula(f"D{x}", f"={cell}", num, exp)
            t.write_formula(f"E{x}", f"=ABS(D{x}-C{x})<0.5", None, True)
        t.write("A10", "فحص رقابي · إجمالي الموازنة ناقص مجموع القطاعات")
        t.write_formula("D10", "=Summary!B2-Summary!B12", num, 0)
        t.write_formula("E10", "=ABS(D10)<0.5", None, True)
        c = wb.add_worksheet("ChangeLog"); c.right_to_left(); c.set_column("A:A", 12); c.set_column("B:B", 14); c.set_column("C:F", 40)
        for k, x in enumerate(["التاريخ", "الخلية أو النطاق", "قبل", "بعد", "السبب", "الاختبار، ومن أصلح"]):
            c.write(0, k, x, h)
        log = [
            ("Budget!F3:F14", "VLOOKUP(...,2,FALSE)", "VLOOKUP(...,3,FALSE)", "المواصفة تطلب الراتب الشامل، والعمود 2 هو الأساسي", "الاختبار 1 · شاهين اللهيب"),
            ("Budget!H3:H14", "G*Assumptions!B3 بمرجع نسبي ينزلق", "G*Assumptions!$B$3", "النسبة في خلية واحدة، فيلزم مرجع مطلق", "الاختبار 2 · شاهين اللهيب"),
            ("Budget!J7", "رقم مكتوب باليد 400000", "=I7*(1+Assumptions!$B$4)", "رقم 2026 كُتب فوق الصيغة", "الاختبار 3 · شاهين اللهيب"),
            ("Budget!L3:L14", "G+H+J+K", "G+H+J-K", "المبالغ المستردة تخفض التكلفة", "الاختبار 4 · شاهين اللهيب"),
            ("Budget!L15", "SUM(L3:L13)", "SUM(L3:L14)", "النطاق لم يشمل CC-112", "الاختبار 5 والفحص الرقابي · شاهين اللهيب"),
        ]
        for i, row in enumerate(log):
            c.write(i + 1, 0, "2026-11-01")
            for k, x in enumerate(row):
                c.write(i + 1, k + 1, x)
    wb.close()
    return v


def budget() -> None:
    faulty = budget_workbook(FILES / "budget_model_fy2027.xlsx", True)
    good = budget_workbook(SOL / "budget_model_fy2027_repaired.xlsx", False)
    cases = {}
    for idx in (0, 4, 11):
        c = CC[idx]
        cases[c[0]] = {
            "row": idx + 3,
            "expected": {k: round(good["rows"][idx][k], 2) for k in "FGHJL"},
            "model_before": {k: round(faulty["rows"][idx][k], 2) for k in "FGHJL"},
        }
    KEY["budget"] = {
        "faulty_total_L15": round(faulty["L15"], 2), "correct_total_L15": round(good["L15"], 2),
        "faulty_sum_of_divisions": round(sum(faulty["div"].values()), 2),
        "hand_cases": cases,
        "faults": [
            {"n": 1, "where": "Budget!F3:F14", "what": "lookup returns column 2 (basic salary), the specification asks for column 3"},
            {"n": 2, "where": "Budget!H4:H14", "what": "relative reference Assumptions!B3 drifts when copied down"},
            {"n": 3, "where": "Budget!J7", "what": "a typed number over the formula"},
            {"n": 4, "where": "Budget!L3:L14", "what": "recoveries are added, the specification subtracts them"},
            {"n": 5, "where": "Budget!L15", "what": "SUM(L3:L13) leaves CC-112 out"},
        ],
    }
    rows = [["cost_centre", "item", "inputs", "your_hand_result", "model_cell", "model_value", "equal"]]
    for code, c in cases.items():
        for k, label in (("F", "الراتب الشهري الشامل"), ("G", "الرواتب السنوية 2027"), ("H", "اشتراكات صاحب العمل"),
                         ("J", "مواد وخدمات 2027"), ("L", "إجمالي الموازنة")):
            rows.append([code, label, "", "", f"Budget!{k}{c['row']}", "", ""])
    rows.append(["الكل", "إجمالي الموازنة لكل المراكز", "", "", "Budget!L15", "", ""])
    write_csv(FILES / "hand_cases.csv", rows[0], rows[1:])
    done = [["cost_centre", "item", "hand_result", "model_cell", "model_value", "equal"]]
    names = {"F": "الراتب الشهري الشامل", "G": "الرواتب السنوية 2027", "H": "اشتراكات صاحب العمل", "J": "مواد وخدمات 2027", "L": "إجمالي الموازنة"}
    for code, c in cases.items():
        for k in "FGHJL":
            e, m = c["expected"][k], c["model_before"][k]
            done.append([code, names[k], money(e), f"Budget!{k}{c['row']}", money(m), "نعم" if abs(e - m) < 0.5 else "لا"])
    done.append(["الكل", "إجمالي الموازنة لكل المراكز", money(good["L15"]), "Budget!L15", money(faulty["L15"]), "لا"])
    write_csv(FILES / "start" / "hand_cases_worked.csv", done[0], done[1:])
    write_csv(FILES / "start" / "fault_list.csv", ["fault", "cell_or_range", "what_is_wrong", "found_by", "fix", "test", "done"],
              [[1, "Budget!F3:F14", "دالة البحث تعيد العمود 2 (الراتب الأساسي) والمواصفة تطلب الراتب الشامل", "الحالات اليدوية الثلاث", "", "", ""],
               [2, "Budget!H4:H14", "مرجع النسبة Assumptions!B3 نسبي فانزلق عند النسخ إلى أسفل", "حالتا CC-105 وCC-112", "", "", ""],
               [3, "Budget!J7", "رقم مكتوب باليد فوق الصيغة", "حالة CC-105", "", "", ""],
               [4, "Budget!L3:L14", "المبالغ المستردة تُجمع والمواصفة تطرحها", "حالة CC-105", "", "", ""],
               [5, "Budget!L15", "نطاق الجمع ينتهي عند الصف 13 ويترك CC-112", "الإجمالي، ومجموع القطاعات في ورقة Summary", "", "", ""]])


# ---------------------------------------------------------------- lab 2.2: variance and commentary
VAR = [("CC-101", 310000, 334800), ("CC-102", 228000, 262900), ("CC-103", 196000, 191300), ("CC-104", 236000, 277300),
       ("CC-105", 181000, 189500), ("CC-106", 143000, 139800), ("CC-107", 402000, 455600), ("CC-108", 97000, 99100),
       ("CC-109", 71000, 93400), ("CC-110", 118000, 89700), ("CC-111", 84000, 80200), ("CC-112", 152000, 154900)]


def variance() -> None:
    wb = xlsxwriter.Workbook(str(FILES / "variance_oct.xlsx"))
    wb.set_properties({"title": "Dhilal October 2026 variance (synthetic)", "author": "SDAIA Academy", "created": datetime(2026, 10, 17)})
    h = wb.add_format({"bold": True, "bg_color": "#E7EEF5", "border": 1, "text_wrap": True})
    num = wb.add_format({"num_format": "#,##0"}); pct = wb.add_format({"num_format": "0.0%"})
    bold = wb.add_format({"bold": True, "num_format": "#,##0"}); bpct = wb.add_format({"bold": True, "num_format": "0.0%"})
    w = wb.add_worksheet("Variance"); w.right_to_left(); w.set_column("A:A", 9); w.set_column("B:B", 32); w.set_column("C:F", 15)
    w.write("A1", "الانحراف عن الموازنة · أكتوبر 2026 · شركة ظِلال لإدارة المرافق (بيانات اصطناعية)", wb.add_format({"bold": True, "font_size": 13}))
    w.write("A2", "قاعدة التعليق: يُعلَّق على المركز حين يبلغ الانحراف 20,000 ريال و10% من موازنته معًا")
    for c, t in enumerate(["الرمز", "مركز التكلفة", "الموازنة", "الفعلي", "الانحراف (الفعلي ناقص الموازنة)", "الانحراف %"]):
        w.write(2, c, t, h)
    names = {c[0]: c[1] for c in CC}
    cells = {}
    for i, (code, bud, act) in enumerate(VAR):
        x = i + 4
        w.write(f"A{x}", code); w.write(f"B{x}", names[code]); w.write(f"C{x}", bud, num); w.write(f"D{x}", act, num)
        w.write_formula(f"E{x}", f"=D{x}-C{x}", num, act - bud)
        w.write_formula(f"F{x}", f"=E{x}/C{x}", pct, (act - bud) / bud)
        cells.update({f"C{x}": bud, f"D{x}": act, f"E{x}": act - bud, f"F{x}": (act - bud) / bud})
    tb, ta = sum(v[1] for v in VAR), sum(v[2] for v in VAR)
    w.write("B16", "الإجمالي", bold)
    w.write_formula("C16", "=SUM(C4:C15)", bold, tb); w.write_formula("D16", "=SUM(D4:D15)", bold, ta)
    w.write_formula("E16", "=D16-C16", bold, ta - tb); w.write_formula("F16", "=E16/C16", bpct, (ta - tb) / tb)
    cells.update({"C16": tb, "D16": ta, "E16": ta - tb, "F16": (ta - tb) / tb})
    wb.close()
    material = [v[0] for v in VAR if abs(v[2] - v[1]) >= 20000 and abs(v[2] - v[1]) / v[1] >= 0.10]
    KEY["variance"] = {
        "cells": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in cells.items()},
        "material": material, "with_evidence": ["CC-104", "CC-107", "CC-110"], "to_confirm": ["CC-102", "CC-109"],
        "above_amount_below_percent": ["CC-101"],
        "draft": {"tagged_figures": 10, "tags_that_match": 7, "tags_that_do_not_match": 3, "untagged_figures": 1,
                  "commented_below_rule": ["CC-101"],
                  "material_centres_missing": ["CC-109"], "causes_without_evidence": ["CC-102"]},
    }
    assert material == ["CC-102", "CC-104", "CC-107", "CC-109", "CC-110"], material


# ---------------------------------------------------------------- lab 2.3: invoices and the sample
def invoices() -> None:
    n = 5000
    sup = [(f"S-{i + 1:03d}", supplier(i)) for i in range(140)]
    d0 = date(2026, 1, 1)
    rows = []
    key_idx = set(R.sample(range(n), 38))
    for i in range(n):
        s = sup[min(139, int(R.expovariate(1 / 28)))]
        day = int(i / n * 303) + R.randint(-3, 3)
        dt = d0 + timedelta(days=max(0, min(303, day)))
        if i in key_idx:
            amt = round(R.uniform(100000, 460000), 2)
        else:
            amt = round(min(16000 + R.uniform(0, 900), R.lognormvariate(8.3, 1.05) + 120), 2)
        rows.append({"id": f"INV-{i + 1:06d}", "sid": s[0], "sname": s[1], "no": f"{s[0][2:]}/{R.randint(1000, 99999)}",
                     "date": dt, "period": dt.strftime("%Y-%m"), "amt": amt, "po": f"PO-26-{R.randint(1, 4200):05d}",
                     "cc": CC[R.randint(0, 11)][0], "by": R.choice(["m.manager1", "m.manager2", "m.manager3", "f.controller"])})
    rest = [i for i in range(n) if i not in key_idx]
    seed, size = 20261031, 60
    interval = len(rest) // size
    start = int(random.Random(seed).random() * interval) + 1
    sample_pos = [start + interval * k for k in range(size)]
    sample_idx = [rest[p - 1] for p in sample_pos]
    in_sample = set(sample_idx)
    free = [i for i in rest if i not in in_sample and i > 50]
    taken: set[int] = set()

    def pick(pool):
        while True:
            i = R.choice(pool)
            if i not in taken and i - 1 not in taken and i + 1 not in taken:
                taken.add(i)
                return i

    planted = {"duplicate": [], "missing_po": [], "split": [], "cut_off": []}
    s_dup, s_po1, s_po2, s_split = sample_idx[7], sample_idx[19], sample_idx[41], sample_idx[52]
    taken.update({s_dup, s_po1, s_po2, s_split})

    def make_dup(j):
        i = j - R.randint(15, 40)
        while i in taken or i in key_idx or i in in_sample:
            i -= 1
        taken.add(i)
        for k in ("sid", "sname", "no", "amt"):
            rows[j][k] = rows[i][k]
        planted["duplicate"].append([rows[i]["id"], rows[j]["id"]])

    make_dup(s_dup)
    for _ in range(5):
        make_dup(pick(free))
    for j in [s_po1, s_po2] + [pick(free) for _ in range(7)]:
        rows[j]["po"] = ""
        planted["missing_po"].append(rows[j]["id"])

    def make_split(j, other):
        taken.add(other)
        a, b = sorted((j, other))
        for k in ("sid", "sname", "date", "period", "by"):
            rows[b][k] = rows[a][k]
        rows[a]["amt"], rows[b]["amt"] = round(R.uniform(46000, 49950), 2), round(R.uniform(45000, 49900), 2)
        planted["split"].append([rows[a]["id"], rows[b]["id"]])

    nb = s_split + 1 if (s_split + 1 not in key_idx and s_split + 1 not in in_sample) else s_split - 1
    assert nb not in key_idx and nb not in in_sample
    make_split(s_split, nb)
    for _ in range(3):
        j = pick([i for i in free if i + 1 in free])
        make_split(j, j + 1)
    late_key = sorted(key_idx)[-2]
    late = [late_key] + [pick([i for i in free if i > 4700]) for _ in range(4)]
    for k, j in enumerate(late):
        rows[j]["date"] = date(2026, 11, 2 + k)
        rows[j]["period"] = "2026-10"
        planted["cut_off"].append(rows[j]["id"])
    for r in rows:
        if r["date"] <= date(2026, 10, 31):
            r["period"] = r["date"].strftime("%Y-%m")
    out = [[r["id"], r["sid"], r["sname"], r["no"], r["date"].isoformat(), r["period"], money(r["amt"]), r["po"], r["cc"], r["by"]] for r in rows]
    write_csv(FILES / "invoices_fy2026.csv",
              ["invoice_id", "supplier_id", "supplier_name", "supplier_invoice_no", "invoice_date", "posting_period", "amount",
               "po_number", "cost_centre", "approved_by"], out)
    key_rows = [rows[i] for i in sorted(key_idx)]
    sample_rows = [rows[i] for i in sample_idx]
    assert all(r["amt"] < 100000 for i, r in enumerate(rows) if i not in key_idx)
    KEY["sample"] = {
        "population": {"count": n, "sum": round(sum(r["amt"] for r in rows), 2)},
        "key_items": {"threshold": 100000, "count": 38, "sum": round(sum(r["amt"] for r in key_rows), 2)},
        "remainder": {"count": len(rest), "sum": round(sum(rows[i]["amt"] for i in rest), 2)},
        "seed": seed, "size": size, "interval": interval, "start": start,
        "sample_ids": [r["id"] for r in sample_rows], "sample_sum": round(sum(r["amt"] for r in sample_rows), 2),
        "planted": planted,
        "flags_in_tested_items": {
            "duplicate": [rows[s_dup]["id"]], "missing_po": [rows[s_po1]["id"], rows[s_po2]["id"]],
            "split_under_limit": [rows[s_split]["id"]], "cut_off": [rows[late_key]["id"]]},
    }
    # the scripted prose answer: 60 "random" invoices, no seed, skewed, three that do not exist
    rr = random.Random(77)
    fake = sorted(rr.sample(range(1, 1001), 41) + rr.sample(range(1001, 5001), 16)) + [5012, 5148, 5630]
    ids = [f"INV-{i:06d}" for i in fake]
    second = [f"INV-{i:06d}" for i in sorted(random.Random(78).sample(range(1, 1500), 10))]
    text = TEXT_FILES["ai_sample_answer.txt"].replace("{IDS}", "\n".join("، ".join(ids[i:i + 6]) for i in range(0, 60, 6)))
    write_text(FILES / "ai_sample_answer.txt", text.replace("{SECOND}", "، ".join(second)))
    KEY["sample"]["prose_answer"] = {"listed": 60, "not_in_population": 3, "in_first_1000": 41, "seed_stated": False}


# ---------------------------------------------------------------- lab 2.4: payroll, data cards, redesign task
def payroll_and_redesign() -> None:
    first = ["سالم", "نورة", "خالد", "هيفاء", "ماجد", "ريم", "فهد", "أمل", "ناصر", "دانة", "عادل", "سارة", "بدر", "منى", "راشد", "لينا"]
    last = ["العتيق", "الصقير", "المحيميد", "الخضير", "الدبيان", "السحيم", "الرميح", "الفريح", "العجلان", "الجريس"]
    rate = {g: (b, t) for g, b, t in RATES}
    rows = []
    for i in range(40):
        g = R.choice(["G1", "G1", "G1", "G2", "G2", "G3", "G4"])
        basic, total = rate[g]
        ded = round(basic * 0.0975, 2)
        rows.append([f"E-{1001 + i}", f"{first[i % 16]} {last[(i * 3) % 10]}", f"TEST-ID-{R.randint(100000, 999999)}",
                     f"SA00 TEST {R.randint(1000, 9999)} {R.randint(1000, 9999)}", CC[R.randint(0, 11)][0], g,
                     money(basic), money(total - basic), money(ded), money(total - ded)])
    write_csv(FILES / "payroll_oct_extract.csv",
              ["employee_id", "employee_name", "national_id", "iban", "cost_centre", "grade", "basic", "allowances", "deductions", "net_pay"], rows)
    cards = [
        ("F1", "trial_balance_oct.csv", "ميزان مراجعة أكتوبر: أرصدة الحسابات", "مقيد", "لا"),
        ("F2", "bank_statement_oct.csv", "كشف الحساب الجاري: حركات وأسماء أطراف تجارية", "مقيد", "لا"),
        ("F3", "payroll_oct_extract.csv", "مسير رواتب: أسماء وهويات وحسابات بنكية ورواتب", "سري", "نعم"),
        ("F4", "invoices_fy2026.csv", "فواتير الموردين: أسماء منشآت ومبالغ وأوامر شراء", "مقيد", "لا"),
        ("F5", "budget_model_fy2027.xlsx", "نموذج موازنة 2027 قبل اعتماده", "مقيد", "لا"),
        ("F6", "تقرير سنوي منشور 2025", "القوائم المالية المنشورة على موقع الشركة", "عام", "لا"),
        ("F7", "ملف تحقيق المراجعة الداخلية 2026-07", "ورقة عمل تحقيق في اشتباه احتيال، فيها أسماء موظفين", "سري", "نعم"),
        ("F8", "مسير رواتب مجمَّع حسب مركز التكلفة", "مجاميع الرواتب لكل مركز تكلفة دون أسماء ولا هويات", "مقيد", "لا"),
    ]
    write_csv(FILES / "data_cards.csv", ["card", "file", "what_it_holds", "classification", "personal_data", "public_assistant", "raqeem", "local_tools"],
              [list(c) + ["", "", ""] for c in cards])
    allowed = {}
    for cid, _, _, level, personal in cards:
        allowed[cid] = {"public_assistant": level == "عام", "raqeem": level in ("عام", "مقيد") and personal == "لا", "local_tools": True}
    KEY["data_rules"] = allowed

    # the supplier-statement task for the redesign
    s_rows, l_rows = [], []
    bal = 0.0
    d0 = date(2026, 8, 1)
    for i in range(56):
        dt = d0 + timedelta(days=int(i * 1.6))
        if i % 4 == 3:
            amt = -round(R.uniform(9000, 42000), 2); doc = f"PAY-{7000 + i}"; kind = "سداد"
        else:
            amt = round(R.uniform(1800, 21000), 2); doc = f"SI-{31000 + i * 3}"; kind = "فاتورة"
        s_rows.append([dt.isoformat(), doc, kind, amt]); l_rows.append([dt.isoformat(), doc, kind, amt])
    # four planted differences
    s_rows.append(["2026-10-21", "SI-31990", "فاتورة", 6480.00])                    # on the statement, not booked
    s_rows.append(["2026-10-26", "CN-00412", "إشعار دائن", -2150.00])               # credit note not booked
    pay = next(r for r in l_rows if r[2] == "سداد" and r[0] > "2026-09-15")
    l_rows.append([pay[0], pay[1], pay[2], pay[3]])                                  # payment booked twice
    tgt = next(r for r in l_rows if r[2] == "فاتورة" and r[0] > "2026-10-01")
    stm = next(r for r in s_rows if r[1] == tgt[1])
    tgt[3] = round(stm[3] + 900.00, 2)                                               # amount keyed 900 too high
    s_rows.sort(key=lambda r: (r[0], r[1])); l_rows.sort(key=lambda r: (r[0], r[1]))
    write_csv(FILES / "redesign" / "supplier_statement.csv", ["date", "document", "type", "amount"], [[a, b, c, money(d)] for a, b, c, d in s_rows])
    write_csv(FILES / "redesign" / "ap_ledger_supplier.csv", ["date", "document", "type", "amount"], [[a, b, c, money(d)] for a, b, c, d in l_rows])
    s_sum, l_sum = round(sum(r[3] for r in s_rows), 2), round(sum(r[3] for r in l_rows), 2)
    KEY["redesign"] = {
        "statement": {"lines": len(s_rows), "balance": s_sum}, "ledger": {"lines": len(l_rows), "balance": l_sum},
        "difference": round(s_sum - l_sum, 2),
        "items": {"not_booked_invoice": "SI-31990", "not_booked_credit_note": "CN-00412", "payment_booked_twice": pay[1],
                  "amount_difference": {"document": tgt[1], "statement": stm[3], "ledger": tgt[3]}},
        "baseline_minutes": [44, 49, 46], "baseline_errors": [2, 1, 3],
    }
    write_csv(FILES / "redesign" / "baseline_log_dhilal.csv",
              ["run", "date", "who", "method", "minutes", "differences_in_key", "found_correctly", "missed", "wrongly_flagged", "errors"],
              [[1, "2026-08-31", "يسرى البواردي", "يدوي: تأشير سطرًا بسطر", 44, 4, 3, 1, 1, 2],
               [2, "2026-09-30", "يسرى البواردي", "يدوي: تأشير سطرًا بسطر", 49, 4, 3, 1, 0, 1],
               [3, "2026-10-31", "يسرى البواردي", "يدوي: تأشير سطرًا بسطر", 46, 4, 2, 2, 1, 3]])
    write_csv(FILES / "redesign" / "measurement_table.csv",
              ["run", "method", "minutes", "errors", "control_total_agrees", "note"],
              [["خط الأساس 1", "يدوي", "", "", "", ""], ["خط الأساس 2", "يدوي", "", "", "", ""], ["خط الأساس 3", "يدوي", "", "", "", ""],
               ["التنفيذ 1 بعد إعادة التصميم", "", "", "", "", ""], ["التنفيذ 2 بعد إعادة التصميم", "", "", "", "", ""]])


def notebooks_and_texts() -> None:
    for name, cells in NOTEBOOKS.items():
        nb = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
        for i, (kind, src) in enumerate(cells):
            src = src.strip("\n")
            cell = {"cell_type": kind, "id": f"c{i:02d}", "metadata": {}, "source": src.splitlines(keepends=True)}
            if kind == "code":
                cell.update({"execution_count": None, "outputs": []})
            nb["cells"].append(cell)
        p = FILES / "notebooks" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for name, text in TEXT_FILES.items():
        if name != "ai_sample_answer.txt":
            write_text(FILES / name, text)


def main() -> None:
    SOL.mkdir(parents=True, exist_ok=True)
    trial_balance()
    bank_and_ledger()
    write_trial_balance(KEY["recon"]["ledger_closing"])
    budget()
    variance()
    invoices()
    payroll_and_redesign()
    notebooks_and_texts()
    SOL.mkdir(parents=True, exist_ok=True)
    (SOL / "key.json").write_text(json.dumps(KEY, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("files written:", sum(1 for p in FILES.rglob("*") if p.is_file()))
    print(json.dumps({k: KEY[k] for k in ("recon",)}, ensure_ascii=False)[:900])


if __name__ == "__main__":
    main()
