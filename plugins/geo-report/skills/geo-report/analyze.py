#!/usr/bin/env python3
"""
GEO report analyzer.
Usage: python3 analyze.py <prompts_export.csv> <cited_sources_export.csv>

Prints every figure needed to fill the GEO baseline template:
blended SoV, per-topic SoV, total citations, top domains, engine citations,
and the owned / competitor / third-party citation mix.

EDIT the OWNED and COMPETITOR lists below for each client before trusting
the citation mix. Matching is substring-based on the hostname.
"""
import csv
import sys
from collections import defaultdict

# ---- EDIT PER CLIENT ---------------------------------------------------------
# Substrings that mark a hostname as the product's own property.
OWNED = ["extend.ai"]            # e.g. ["vercel.com", "nextjs.org", "sdk.vercel.ai"]
# Substrings that mark a hostname as a tracked competitor's property.
COMPETITOR = [
    "llamaindex.ai", "firecrawl.dev", "docsumo.com", "lido.app", "parseur.com",
    "v7labs.com", "reducto.ai", "landing.ai", "unstract.com", "scryai.com",
    "meibel.ai", "aws.amazon.com", "cloud.google.com", "microsoft.com",
]
# ------------------------------------------------------------------------------


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def analyze_prompts(rows):
    tm = sum(int(r["Product Mentions"]) for r in rows)
    tr = sum(int(r["Total Runs"]) for r in rows)
    plats = set()
    for r in rows:
        plats.update(p.strip() for p in r["Platforms"].split(";") if p.strip())
    topic_m, topic_r, topic_n = defaultdict(int), defaultdict(int), defaultdict(int)
    for r in rows:
        t = r["Topic"]
        topic_m[t] += int(r["Product Mentions"])
        topic_r[t] += int(r["Total Runs"])
        topic_n[t] += 1

    print("=" * 60)
    print("PROMPTS / SHARE OF VOICE")
    print("=" * 60)
    print(f"Prompts: {len(rows)}   Engines tracked: {sorted(plats)}")
    print(f"Blended SoV: {tm}/{tr} = {round(100*tm/tr, 1) if tr else 0}%")
    print("\nBy topic (sorted by SoV):")
    for t in sorted(topic_m, key=lambda k: -(100 * topic_m[k] / topic_r[k]) if topic_r[k] else 0):
        sov = round(100 * topic_m[t] / topic_r[t], 1) if topic_r[t] else 0
        print(f"  {t}: {topic_n[t]} prompts, {topic_m[t]}/{topic_r[t]} = {sov}%")
    print("\nNOTE: dashboard 'Topics' view prompt counts can differ from the CSV")
    print("      topic field (a prompt can sit in multiple topic groupings).")
    print("      Use the dashboard counts in the report if the client asks.")


def classify(host):
    if any(s in host for s in OWNED):
        return "owned"
    if any(s in host for s in COMPETITOR):
        return "competitor"
    return "third"


def analyze_citations(rows):
    total = sum(int(x["Citation Count"]) for x in rows)
    urls = len(set(x["URL"] for x in rows))
    dom = defaultdict(int)
    for x in rows:
        dom[x["Hostname"]] += int(x["Citation Count"])

    print("\n" + "=" * 60)
    print("CITATIONS")
    print("=" * 60)
    print(f"Total citations: {total}   Unique URLs: {urls}")
    print("\nTop 12 domains:")
    for h, c in sorted(dom.items(), key=lambda kv: -kv[1])[:12]:
        print(f"  {c:5d}  {round(100*c/total,1):4}%  {classify(h):10s}  {h}")

    eng = defaultdict(int)
    for x in rows:
        for m in (m.strip() for m in x["Models (Answer Engine)"].split(",")):
            if m:
                eng[m] += int(x["Citation Count"])
    print("\nEngine citations (a cite counts once per engine listed):")
    for m, c in sorted(eng.items(), key=lambda kv: -kv[1]):
        print(f"  {m}: {c}")

    mix = defaultdict(int)
    for h, c in dom.items():
        mix[classify(h)] += c
    print("\nCitation mix (edit OWNED / COMPETITOR at top of this file to tune):")
    for k in ("third", "competitor", "owned"):
        print(f"  {k}: {mix[k]} ({round(100*mix[k]/total,1)}%)")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 analyze.py <prompts.csv> <cited-sources.csv>")
        sys.exit(1)
    analyze_prompts(read_csv(sys.argv[1]))
    analyze_citations(read_csv(sys.argv[2]))


if __name__ == "__main__":
    main()
