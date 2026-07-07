---
name: connect
description: Guided wizard for wiring up data sources. Scans .env for what's already connected, splits sources into 🟢 start-now (GA4, Search Console, MailerLite, PageSpeed) versus 🔴 needs-approval (Google Ads, Meta), links to docs/integrations/*, and walks the user through it step by step — separating one-time developer approvals from per-user OAuth. Use when someone runs /growth-os:connect, says "connect my accounts," "hook up GA4," "wire up analytics," or when an audit is blocked because a data source is missing.
---

# connect

The integration wizard. Connecting analytics and ad accounts is where most tools lose people — the approval flows are confusing, some take weeks, and it's never clear what you can start *right now*. `connect` fixes that by telling you exactly what's fast, what's slow, and walking you through each one in the right order.

## What it does

- **Detects** which credentials are already present in `.env` and which sources are live.
- **Classifies** every source as 🟢 (zero-approval, minutes) or 🔴 (needs an owner-side approval with real lead time).
- **Sequences** the setup so the user gets value today: do all the 🟢 sources now, kick off the 🔴 approvals in parallel so their clock starts.
- **Guides** each connection step by step, linking to the matching `docs/integrations/*` page.
- **Separates** the two very different kinds of approval so nobody waits on the wrong thing.

## The two kinds of approval — this is the key distinction

- **Developer approval (once, ever).** A one-time setup the account *owner* does at the platform level — a developer token, a verified business, an app that passes review. Slow, but you do it once and it's done for the whole org. These are the 🔴 sources.
- **User OAuth (per person, fast).** An individual granting read access to their own data via a consent screen. Seconds to minutes. These are the 🟢 sources (plus, later, the read grant on the 🔴 platforms once the developer approval exists).

Conflating these is why integrations feel painful. `connect` keeps them apart and tells the user which clock they're on.

## The sources

### 🟢 Zero-approval — start now, minutes each
- **GA4 (Data API)** — service-account JSON added to the property, or OAuth with `analytics.readonly`. → `docs/integrations/ga4.md`
- **Google Search Console** — `webmasters.readonly`, the *same service account* added as a user on the property. → `docs/integrations/gsc.md`
- **MailerLite** — Bearer API key generated in the MailerLite UI. → `docs/integrations/mailerlite.md`
- **PageSpeed Insights** — an API key from a Google Cloud project. → `docs/integrations/pagespeed.md`

### 🔴 Needs approval — owner-side, real lead time, start in parallel
- **Google Ads** — a developer token on a Manager (MCC) account. Test/Explorer access works to start; Basic access needs Google's sign-off. → `docs/integrations/google-ads.md`
- **Meta Marketing / Graph (+ Instagram)** — **Business Verification first (~14+ days)**, then App Review for `ads_read` / `instagram_*` scopes. → `docs/integrations/meta.md`

## Steps

1. **Scan `.env`.** Report what's already wired: "GA4 ✅, PageSpeed ✅, MailerLite ❌, Search Console ❌…" so the user sees the current state at a glance.

2. **Explain the two clocks.** Briefly: the 🟢 sources take minutes and unlock most of the audit; the 🔴 sources need owner-side approvals that take days-to-weeks, so we start those in the background and don't wait on them.

3. **Do the 🟢 sources first, one at a time.** For each missing 🟢 source: open its `docs/integrations/*` page, walk the exact steps (create key / add service account / paste into `.env`), then verify the connection with a smoke call (`growth-os ga4 visitors 7`, `growth-os psi <url>`, etc.). Confirm it works before moving to the next. Don't dump all four at once — one clean win at a time.

4. **Kick off the 🔴 approvals.** For Google Ads and Meta, explain what the *owner* needs to start today so the lead-time clock begins — especially Meta Business Verification, which gates everything else and is the long pole. Point them at the docs, note it's a one-time developer approval, and mark the source "pending" in the current state. Make clear they don't need to finish this to keep going.

5. **Summarize the new state.** What's live, what's pending, and what that unlocks: "GA4 + GSC live → the audit now has a real baseline. Meta pending verification → ads reach data lands in ~2 weeks." Route back to `/growth-os:audit` (re-run with the new data) or `/growth-os:dashboard` (see integration status).

## Which adapters / CLI it calls

- Verifies each connection with the matching read-side smoke command: `growth-os ga4 …`, `growth-os gsc …`, `growth-os mailerlite …`, `growth-os psi …`, and (once approved) `growth-os google-ads …`, `growth-os meta …`.
- Reads and writes **`.env` only** for credentials — never the hub, never anywhere remote.
- References `docs/integrations/*` for the human steps.

## How it delegates

- **In:** called by `onboard` during first-run, and by `audit`/`dashboard` when a needed source is missing.
- **Out:** once a source connects, hands control back to whatever needed it (usually `audit`). Doesn't do analysis itself — it's plumbing.

## Guardrails

- **Keys stay local.** Everything goes in the user's `.env`. Growth OS stores no credentials and phones nothing home.
- **Never block on 🔴.** The fast sources always run first and independently; slow approvals proceed in parallel.
- **Verify, don't assume.** A source is only "connected" after a live smoke call succeeds.
- **Read scopes only.** Every scope Growth OS requests is read-only (`analytics.readonly`, `webmasters.readonly`, `ads_read`, etc.). It never asks for write access to a user's accounts.
