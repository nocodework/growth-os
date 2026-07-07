---
name: onboard
description: First-run flow for Growth OS. Takes a business URL and walks the user through the full setup — build the context hub, connect accounts, run the growth audit — then explains what to do next. Use when someone runs /growth-os:onboard, says "set up Growth OS", "get started", "onboard my business", or just drops a URL and asks Growth OS to take it from there.
---

# onboard

The front door to Growth OS. One command turns a raw business URL into a working Growth OS: a persistent context hub, a set of connected data sources, and a first growth audit — with a plain-language explanation of what each step found and what to do about it.

## What it does

`onboard` is an orchestrator. It doesn't do the heavy lifting itself — it sequences the three foundational skills in the right order and keeps the user oriented between them:

1. **context** — read the URL, draft a first-pass positioning (USP/UVP/ICP), and confirm it with the user. Writes `.agents/product-marketing.md`.
2. **connect** — figure out which data sources the user can wire up right now (zero-approval) versus which need a lead-time approval, and walk them through the fast ones first.
3. **audit** — run the growth audit against whatever is connected, plus the always-available checks (SEO, page speed, GEO), and write findings back to the hub.

Then it hands off: a short "here's what I found, here's what's worth doing first" summary.

## When to use

- The user is running Growth OS for the first time in a repo/project.
- Someone gives you a business URL and expects Growth OS to "take it from here."
- A returning user wants to re-baseline a business (new site, new positioning, new quarter).

If the hub already exists and the user only wants one piece (just re-run the audit, just connect one account), skip straight to that skill instead of the full flow.

## Inputs

- **Business URL** (required). The homepage is enough. If the user gives a deeper page (pricing, product), use it — more signal.
- Optional: a one-line description of the business, if the site is thin or gated.

If no URL is provided, ask for one before doing anything. Everything downstream keys off it.

## Steps

1. **Confirm the target.** Echo the URL back and state what you're about to do: build a context file, connect data sources, run an audit. Set the expectation that this takes a few passes and that nothing gets published or changed on their site — Growth OS is read-side.

2. **Check for an existing hub.** Look for `.agents/product-marketing.md`.
   - If missing → this is a true first run. Continue to step 3.
   - If present → tell the user Growth OS is already set up here. Offer: refresh context, re-run the audit, or connect more accounts. Don't silently overwrite anything.

3. **Delegate to `context`.** Hand off the URL. `context` runs its batched interview (pre-filled from the URL, user confirms), and writes the hub. Wait for it to finish and confirm the positioning is captured before moving on — the audit and every downstream skill reads from this file.

4. **Delegate to `connect`.** Now that we know the business, wire up data. `connect` scans `.env` for existing keys, splits sources into 🟢 start-now versus 🔴 needs-approval, and walks the user through the fast ones (GA4, Search Console, MailerLite, PageSpeed) first. Make it clear the 🔴 sources (Google Ads, Meta) can be started in parallel because the approvals sit with the account owner and take real calendar time — the user shouldn't wait on them to get value today.

5. **Delegate to `audit`.** Run the growth audit. It uses whatever `connect` managed to wire up for the live baseline, and always runs the checks that need no accounts (SEO crawl, PageSpeed if the key is set, GEO visibility). It appends an `## Audit Findings` section to the hub.

6. **Explain and hand off.** Summarize in plain language:
   - What Growth OS now knows about the business (one or two lines from the context).
   - What's connected and what's still pending approval.
   - The three or four highest-leverage findings from the audit.
   - The single next action worth taking — usually either "connect X to unlock Y" or "fix Z on the site."

   Point the user at `/growth-os:dashboard` for the assembled overview and `/growth-os:delegate` when they want to act on a specific finding.

## Which adapters / CLI it calls

`onboard` itself calls no adapters directly. It delegates:

- Positioning → **context** skill
- Data wiring → **connect** skill (which references `docs/integrations/*`)
- Audit → **audit** skill (which invokes the read-side CLI: `growth-os ga4 …`, `growth-os gsc …`, `growth-os psi …`, plus the GEO module)

## How it delegates

Sequential, gated hand-offs. Each step must land before the next starts, because each one depends on the previous:

- `context` must write the hub before `audit` can reason about the business or run GEO (GEO queries are derived from the ICP).
- `connect` should run before `audit` so the audit has live GA4/GSC data for the baseline — but the audit still runs (with a smaller scope) if the user skips connecting.

Never block the whole flow on a 🔴 approval. If Google Ads or Meta aren't ready, note them as pending and finish onboarding with everything else. The user gets value on day one and the slow approvals catch up later.

## Guardrails

- Read-side only. `onboard` never publishes, edits the user's site, or writes to any connected account.
- Idempotent. Running it again on an already-onboarded project offers a refresh, never a silent wipe.
- Own keys. Every credential the user provides during `connect` lives in their `.env`, never in the hub and never sent anywhere but the source API.
