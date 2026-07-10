---
name: geo-report
description: Generate a GEO (Generative Engine Optimization) answer-engine visibility baseline report in The Prompting Company two-page template. Use when the user provides a promptingco "prompts" export CSV and a "cited-sources" export CSV for a product and wants a client-facing report covering share of voice, per-engine and per-topic breakdowns, the competitive set, citations, and recommended next steps.
---

# GEO Baseline Report

Builds a polished two-page PDF (from HTML) measuring how often a product is
recommended across AI answer engines, plus where it wins/loses and what the
models cite. This is the same format used for Postmark, PlanetScale, Vercel,
Telnyx and Extend.

## Inputs to collect

1. **prompts export CSV** — columns: `ID, Prompt, Platforms, Product Mentions, Total Runs, Prompt SOV, Persona, View, Topic`.
2. **cited-sources export CSV** — columns: `Hostname, Path, Search, URL, Citation Count, Citation Share, Unique Conversations, Models (Answer Engine)`.
3. From the **dashboard** (ask the user for screenshots or the values):
   - Product name.
   - The Share-of-voice chart **tooltip**: per-engine SoV and "Sum of last 30 days" mentions/runs for each engine (this is the authoritative live SoV; the CSV can lag).
   - **Industry ranking** and/or **Pinned competitors** with SoV, plus the product's own rank number.

## Steps

1. **Analyze.** Run `python3 analyze.py <prompts.csv> <cited-sources.csv>`. It prints blended SoV, per-topic SoV, total citations, top domains, engine citations, and the owned/competitor/third-party citation mix. Before trusting the mix, open `analyze.py` and edit `OWNED` and `COMPETITOR` for this client's domains.
2. **Reconcile with the dashboard.** Use the live tooltip for the headline SoV and per-engine numbers (they are fresher than the export). Use the CSV for topics and citations. Note if the two snapshots differ.
3. **Build.** Copy `template.html`, fill every `{{PLACEHOLDER}}` and the tables, following the house rules below.
4. **Render.** `python3 -m weasyprint report.html report.pdf` (install with `pip install weasyprint --break-system-packages` if needed).
5. **Verify.** Re-read the PDF. Recompute every figure from the CSVs and confirm it matches. Confirm exactly **2 pages** and **zero em/en dashes**.

## House rules (do not skip)

- **Exactly two pages.** If it spills to a third, tighten padding/wording until it fits.
- **No em dashes or en dashes** anywhere. Use commas, colons, semicolons, or parentheses. Grep the file for `—` and `–` and confirm zero.
- **Competitive set = pinned competitors**, listed by share of voice, with the product's row highlighted and showing its true industry rank (e.g. `#21`). Do not invent ranks for the competitors; if you only have their SoV, show SoV without rank numbers.
- **Insight table** uses columns **"Highlight"** and **"Data from TPC runs"**, with rows **Winning / Losing / Competition / What's cited?**
- **Recommended next steps**: 3 short, plain (non-bold) one-liners aligned to what the agency can deliver (own-domain content, third-party listicle outreach, coding-agent analysis). No verbose AI-sounding prose.
- **Owned content** includes all of the product's domains (e.g. `extend.ai` AND `docs.extend.ai`).
- **Every number must be verifiable** from the two CSVs or a dashboard screenshot. Never estimate a figure without labeling it.

## Layout reference

Page 1: eyebrow + title + brandmark, lede, baseline-assessment callout, section
"1 GEO baseline", headline sentence, four stat cards (blended SoV, competitor
gap/rank, strongest topic, weakest engine), By engine table, By topic + Competitive
set (two columns), Insight table.
Page 2: "What the models cite: top domains" + "Citation mix & engines" (two columns),
section "2 Recommended next steps", Sources line.
