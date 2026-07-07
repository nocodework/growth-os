---
name: audit
description: Run the Growth OS growth audit — SEO, page speed / Core Web Vitals, GEO (AI visibility), competitors, and a live GA4/GSC baseline — and write the results as an "## Audit Findings" section in the context hub. Use when someone runs /growth-os:audit, says "audit my growth," "how's my SEO," "give me a growth report," "what should I fix," or after onboarding to get a first read on the business.
---

# audit

The diagnostic pass. `audit` looks at a business from every angle Growth OS can measure — how it's found (SEO), how fast it loads (page speed), whether AI assistants know it exists (GEO), who it's up against (competitors), and what the live analytics actually say (GA4/GSC) — then writes a prioritized findings section back to the hub so the whole picture lives in one place.

## What it does

Orchestrates five sub-audits and merges them into one ranked report:

1. **SEO** — crawl the site's key pages. Titles, meta descriptions, heading structure, indexability, internal linking, structured data presence, thin/duplicate content, obvious on-page gaps.
2. **Page speed / Core Web Vitals** — pull PageSpeed Insights for the main templates (home, a key landing page, a blog post). LCP, CLS, INP, and the top opportunities.
3. **GEO** — delegate to `geo-audit` for a snapshot of how visible the brand is inside ChatGPT / Gemini / Claude / Perplexity for its ICP's questions.
4. **Competitors** — from the positioning in the hub, identify the main alternatives and note where they out-rank or out-answer the business (search presence, AI citations, obvious content coverage gaps).
5. **Live baseline** — if GA4 and Search Console are connected, pull the real numbers: traffic, top pages, top queries, sources, conversions where available. This grounds every other finding in reality instead of guesswork.

Then it ranks: what's costing the most growth for the least effort to fix goes first.

## When to use

- Right after `onboard`, as the first real read on the business.
- On a cadence (monthly/quarterly) to re-baseline.
- When the user asks an open "what should I work on?" question and there's no fresh audit to point at.

## Inputs

- A written `.agents/product-marketing.md` (required — the audit reasons from the positioning and ICP). If it's missing, stop and route the user to `/growth-os:context` first.
- Whatever accounts are connected. More connections = deeper audit. The audit degrades gracefully: with nothing connected it still does SEO + PageSpeed + GEO; with GA4/GSC it adds the live baseline.

## Steps

1. **Read the hub.** Load `.agents/product-marketing.md` for the URL, ICP, and competitor list. If absent, route to `context` and stop.

2. **SEO crawl.** Fetch the site's primary pages. Check the on-page fundamentals listed above. Flag anything that blocks indexing or wastes ranking potential. Note where structured data is missing (hand-off candidate for the `schema` capability).

3. **Page speed.** Run `growth-os psi <url>` for two or three representative pages. Record CWV field/lab data and the highest-impact opportunities. Call out mobile separately from desktop — mobile is usually where the pain is.

4. **GEO snapshot.** Delegate to `geo-audit`. Pull back the visibility/rank/sentiment/share-of-voice numbers and the citation domains. Don't re-implement it here — `audit` consumes its summary.

5. **Competitor read.** From the hub's alternatives (or infer them if none are listed), compare presence: who ranks for the category terms, whose domains show up as citations in the GEO results, what content the business is missing that competitors cover. Keep it factual — no speculation about their internals.

6. **Live baseline.** If `.env` has GA4 and GSC credentials:
   - `growth-os ga4 visitors|pages|sources|conversions [days]` — traffic shape and where it comes from.
   - `growth-os gsc queries|pages|ctr [days]` — what people actually search to find them, and where impressions aren't converting to clicks.
   Cross-reference: a query with high impressions and low CTR is a title/meta fix; a top landing page with slow CWV is a speed fix that's costing real sessions.

7. **Rank and write.** Merge everything into a single prioritized list. Each finding: what's wrong, the evidence (a number, a crawled fact), the impact, and the fix — ideally naming the Growth OS skill or delegated capability that handles it. Append as `## Audit Findings` in the hub (replace a prior audit block, don't stack duplicates; date-stamp it).

8. **Summarize.** Give the user the top three to five findings in plain language and the single highest-leverage next move. Point them at `/growth-os:dashboard` for the full picture and `/growth-os:delegate` to act.

## Which adapters / CLI it calls

- `growth-os psi <url>` — PageSpeed Insights (works with just the PSI key; 🟢 zero-approval).
- `growth-os ga4 <cmd> [days]` — GA4 Data API baseline (needs the service-account/OAuth connection; 🟢).
- `growth-os gsc <cmd> [days]` — Search Console (same service account; 🟢).
- **geo-audit** skill — for the AI-visibility snapshot.
- Web fetch — for the SEO crawl and competitor read (no keys needed).

Google Ads and Meta baselines are *not* required for a useful audit; if their credentials are present the audit can fold in spend/reach context, but they're 🔴 approval-gated and the audit never blocks on them.

## How it delegates

- **In:** consumes `geo-audit`'s output rather than duplicating GEO logic.
- **Out:** every finding names the fix owner. SEO on-page → the `seo`/`schema` capabilities; speed → the site/perf work; content gaps vs competitors → `geo-content` or content skills; low-CTR queries → copy/title work. `audit` diagnoses; `delegate` routes the fixes.

## Guardrails

- **Evidence, not vibes.** Every finding carries a crawled fact or a live number. If a check couldn't run (account not connected), say so explicitly rather than inventing a result.
- **Graceful degradation.** Missing connections shrink scope; they never fake data.
- **Read-only.** The audit reads the site and the analytics. It changes nothing on the site or in any account.
- **One findings block.** Re-running replaces the dated `## Audit Findings` section; it doesn't accumulate stale copies.
