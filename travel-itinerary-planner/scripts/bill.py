#!/usr/bin/env python3
"""Turn an itemised trip bill (CSV) into Markdown tables with totals.

Usage:
  python bill.py bill.csv --home GBP --rate EUR:GBP=0.84 [--rate CHF:GBP=0.89] [-o bill.md]

CSV columns (header row required):
  date,item,category,where,amount,currency,status
  - amount: a number, or a range "low-high" (e.g. 30-45)
  - status: paid | to book | on the spot   (free text is fine)

Output: the bill table, totals per category (low/high, in the home currency),
totals per status, and the grand total. Rates convert 1 unit of the first
currency into the home currency.
"""
import argparse
import csv
import sys
from collections import OrderedDict


def parse_amount(text):
    text = str(text).replace(",", "").strip()
    if "-" in text.lstrip("-"):
        lo, hi = text.split("-", 1)
        return float(lo), float(hi)
    value = float(text)
    return value, value


def fmt(x):
    return f"{x:,.0f}" if abs(x) >= 100 else f"{x:,.2f}".rstrip("0").rstrip(".")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("--home", required=True, help="home currency code, e.g. GBP, CNY")
    ap.add_argument("--rate", action="append", default=[],
                    help="conversion like EUR:GBP=0.84 (repeatable)")
    ap.add_argument("-o", "--output", help="write Markdown here instead of stdout")
    args = ap.parse_args()

    rates = {args.home.upper(): 1.0}
    for r in args.rate:
        pair, value = r.split("=")
        src, dst = pair.upper().split(":")
        if dst != args.home.upper():
            sys.exit(f"rate {r}: target must be the home currency {args.home}")
        rates[src] = float(value)

    rows, by_cat, by_status = [], OrderedDict(), OrderedDict()
    total_lo = total_hi = 0.0
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            cur = row["currency"].strip().upper()
            if cur not in rates:
                sys.exit(f"no --rate given for {cur} (row: {row['item']})")
            lo, hi = parse_amount(row["amount"])
            lo_h, hi_h = lo * rates[cur], hi * rates[cur]
            rows.append((row, lo, hi, cur, lo_h, hi_h))
            for key, bucket in ((row["category"].strip(), by_cat),
                                (row["status"].strip(), by_status)):
                a, b = bucket.get(key, (0.0, 0.0))
                bucket[key] = (a + lo_h, b + hi_h)
            total_lo += lo_h
            total_hi += hi_h

    h = args.home.upper()
    out = ["| Date | Item | Category | Where / how to pay | Amount | Status |",
           "| --- | --- | --- | --- | --- | --- |"]
    for row, lo, hi, cur, _, _ in rows:
        amt = f"{fmt(lo)} {cur}" if lo == hi else f"{fmt(lo)}–{fmt(hi)} {cur}"
        out.append(f"| {row['date']} | {row['item']} | {row['category']} | "
                   f"{row['where']} | {amt} | {row['status']} |")
    out += ["", f"| Category | Low ({h}) | High ({h}) |", "| --- | --- | --- |"]
    for k, (a, b) in by_cat.items():
        out.append(f"| {k} | {fmt(a)} | {fmt(b)} |")
    out.append(f"| **Total** | **{fmt(total_lo)}** | **{fmt(total_hi)}** |")
    out += ["", f"| Status | Low ({h}) | High ({h}) |", "| --- | --- | --- |"]
    for k, (a, b) in by_status.items():
        out.append(f"| {k} | {fmt(a)} | {fmt(b)} |")
    rate_note = ", ".join(f"1 {c} = {v} {h}" for c, v in rates.items() if c != h)
    if rate_note:
        out += ["", f"Rates used: {rate_note}."]
    text = "\n".join(out) + "\n"
    if args.output:
        open(args.output, "w", encoding="utf-8").write(text)
        print(f"Wrote {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
