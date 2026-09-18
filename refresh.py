"""Pulls my live GitHub contribution calendar and rewrites data.json, then rebuilds
every SVG in this repo. Run by .github/workflows/refresh.yml once a day.

Standard library only, no token needed: the calendar fragment is public.
"""
import json
import re
import subprocess
import sys
import urllib.request
from datetime import date, datetime

USER = "Parsa-Mansouri"
URL = f"https://github.com/users/{USER}/contributions"
HERE = __import__("pathlib").Path(__file__).parent


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "profile-readme-refresh",
        "Accept": "text/html",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    # every day cell: <td ... data-date="YYYY-MM-DD" id="contribution-day-component-r-c" data-level="N">
    days = {}
    for cell in re.findall(r"<td[^>]*data-level[^>]*>", html):
        d = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', cell)
        lvl = re.search(r'data-level="(\d)"', cell)
        cid = re.search(r'id="(contribution-day-component-[\d-]+)"', cell)
        if d and lvl:
            days[d.group(1)] = {"level": int(lvl.group(1)), "id": cid.group(1) if cid else None, "count": 0}

    # exact counts live in the matching tooltip: "8 contributions on August 10th."
    tips = {}
    for m in re.finditer(r'<tool-tip[^>]*for="(contribution-day-component-[\d-]+)"[^>]*>(.*?)</tool-tip>',
                         html, re.S):
        n = re.match(r"\s*(?:(\d+)|No)\b", m.group(2))
        tips[m.group(1)] = int(n.group(1)) if (n and n.group(1)) else 0
    for v in days.values():
        if v["id"] in tips:
            v["count"] = tips[v["id"]]

    total = re.search(r"([\d,]+)\s*\n?\s*contributions? in the last year", html)
    return days, (total.group(1) if total else None)


def main():
    days, total = parse(fetch(URL))
    if len(days) < 300:
        print(f"only {len(days)} day cells parsed, refusing to write", file=sys.stderr)
        return 1

    keys = sorted(days)
    levels = "".join(str(days[k]["level"]) for k in keys)
    counts = [days[k]["count"] for k in keys]

    streak = cur = 0
    for c in levels:
        cur = cur + 1 if c != "0" else 0
        streak = max(streak, cur)
    active = sum(1 for c in levels if c != "0")

    today = date.today()
    this_month = sum(
        days[k]["count"] for k in keys
        if datetime.strptime(k, "%Y-%m-%d").date().replace(day=1) == today.replace(day=1)
    )

    data = {
        "generated": today.isoformat(),
        "first_date": keys[0],
        "last_date": keys[-1],
        "levels": levels,
        "total_year": total or f"{sum(counts):,}",
        "this_month": this_month,
        "streak": streak,
        "active": active,
        "busiest_day": max(counts),
    }
    (HERE / "data.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({k: v for k, v in data.items() if k != "levels"}, indent=2))

    subprocess.run([sys.executable, str(HERE / "build.py")], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
