---
name: dashboard
description: Assemble a single text overview from the context hub — the live baseline (GA4/GSC), the latest audit findings, the GEO scorecard, and integration status — into one readable report. Use when someone runs /growth-os:dashboard, says "give me the overview," "where do things stand," "growth summary," "status report," or wants the whole picture in one place without re-running everything.
---

# dashboard

The read-out. After onboarding, connecting, and auditing, the pieces live in a few places — the hub, `.env`, the GEO scorecard. `dashboard` pulls them together into one plain-text report so the user can see, at a glance, where the business stands and what to do next. It composes; it doesn't re-run the heavy work.

## What it does

Assembles four things into one overview:

1. **Live baseline** — the current numbers from GA4 and Search Console, if connected: traffic, top pages, top queries, sources, conversions where available.
2. **Audit findings** — the ranked `## Audit Findings` from the hub, top items surfaced.
3. **GEO scorecard** — the latest `geo-audit` metrics: visibility, rank, sentiment, recommendation rate, share of voice, citation domains.
4. **Integration status** — what's connected (🟢), what's pending approval (🔴), and what that unlocks.

Then it closes with the single highest-leverage next action.

## When to use

- The user wants the state of play without kicking off a full audit.
- A weekly/monthly check-in on where growth stands.
- Right after `onboard` finishes, as the tidy summary of everything that just happened.

## Steps

1. **Read the hub.** Load `.agents/product-marketing.md` — positioning (one-line reminder of who this is for), the `## Audit Findings` section, and any stored GEO scorecard.

2. **Pull a fresh baseline if cheap.** If GA4/GSC are connected, run the light read-side commands for current numbers (`growth-os ga4 visitors 30`, `growth-os ga4 pages 30`, `growth-os gsc queries 30`). These are fast and give the report live data instead of stale audit numbers. If not connected, say so and show the last known state.

3. **Check integration status.** Scan `.env` (via `connect`'s detection) and list 🟢 live / 🔴 pending, noting what each pending item will unlock when it lands.

4. **Compose the report.** One clean text layout, top to bottom:
   - **Who** — one line: business + ICP.
   - **Baseline** — the live numbers, with the comparison window stated (last 30 days, etc.).
   - **Top findings** — the three-to-five highest-priority audit items, each with its fix owner.
   - **GEO** — the scorecard in a compact block.
   - **Integrations** — the 🟢/🔴 status list.
   - **Do next** — the one action worth taking now.

5. **Point onward.** Link the next moves: `/growth-os:audit` to refresh diagnosis, `/growth-os:connect` to unlock a pending source, `/growth-os:delegate` to act on a finding.

## Which adapters / CLI it calls

- `growth-os ga4 <cmd> [days]` and `growth-os gsc <cmd> [days]` for the fresh baseline (only if connected; both 🟢).
- Optionally `growth-os mailerlite …`, and — where approved — `growth-os google-ads …` / `growth-os meta …` for a fuller picture. All read-side.
- Reads the hub and `.env`; runs no new audit or GEO measurement of its own.

## How it delegates

`dashboard` is a **composer**, not a producer. It doesn't re-run `audit` or `geo-audit` — it reads what they already wrote. If a section is empty (no audit yet, GEO never measured), it says so and points the user to the skill that fills it, rather than faking the content. Keeps the read cheap and the source of truth single.

## Guardrails

- **Compose, don't fabricate.** Every number is either a fresh read-side call or a clearly-dated value from the hub. Empty sections are labeled empty, not invented.
- **State the window.** Always say what date range a metric covers.
- **Read-only.** Pulls current data; changes nothing.
- **One screen.** Keep it scannable — this is the glance view, not the deep report.
