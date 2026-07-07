---
name: geo-audit
description: Measure how visible a brand is inside AI assistants (ChatGPT, Gemini, Claude, Perplexity) for its ICP's real questions. Runs a repeatable protocol of ~15 natural-language queries, reads whether and how the brand shows up, and reports Visibility, Rank, Sentiment, Recommendation rate, Share of Voice, and citation domains. Use when someone runs /growth-os:geo-audit, says "am I visible in ChatGPT," "AI visibility," "do LLMs recommend us," "GEO baseline," or when the growth audit needs the GEO section.
---

# geo-audit

Search is splitting. A growing share of buying research now happens inside an AI assistant that answers directly and never sends a click. `geo-audit` measures whether your brand exists in that layer: when someone asks an assistant the questions your ICP actually asks, do you get named, recommended, and cited — or does a competitor?

## What it does

Runs a **repeatable measurement protocol** and produces a scorecard you can re-run over time to see the trend:

- **Visibility** — in what share of the query set does the brand appear at all.
- **Rank** — when it appears, where in the answer (first named, mid-list, footnote).
- **Sentiment** — how it's framed (recommended, neutral mention, caveated, negative).
- **Recommendation rate** — how often the assistant actively suggests it, versus merely listing it.
- **Share of Voice** — brand mentions as a fraction of all brand mentions across the set (you vs the field).
- **Citation domains** — which sources the assistants pull from when they answer these questions (your owned domains, review sites, competitors, publications). This is the roadmap for `geo-content`.

## When to use

- As the GEO section of `/growth-os:audit`.
- Standalone, when someone specifically wants to know their standing in AI answers.
- On a repeating baseline (monthly) to measure whether GEO work is moving the needle.

## Inputs

- A written hub (`.agents/product-marketing.md`) — the **ICP and category drive the query set.** Without it, ask for the ICP or route to `context`.
- The brand name and its main alternatives (from the hub).

## The protocol

The whole point is repeatability. Same queries, same method, same read — so the numbers compare across runs. Design the run once, then keep it fixed.

1. **Derive ~15 queries from the ICP.** Turn the ICP's real jobs-to-be-done into the natural language a buyer would actually type — not brand-name lookups. Mix:
   - Category discovery: "best tools for <ICP job>," "how do teams handle <pain>."
   - Comparison: "<category> alternatives," "<competitor> vs others."
   - Recommendation: "recommend a <category> for <ICP context>, and cite your sources."
   Explicitly ask for sources where the assistant supports it — you want the citation domains.

2. **Reformulate to natural phrasing.** Rewrite each query the way a person speaks, not keyword-stuffed. Assistants reward natural questions; keyword strings skew the result.

3. **ASCII-fold and normalize.** Strip accents/diacritics and odd punctuation so the same string reproduces cleanly across engines and across runs. Keep a canonical list of the exact strings used — this *is* the test fixture.

4. **Run each query in a clean, signed-out session per engine.** Incognito / no logged-in history so personalization doesn't contaminate the read. Run the same set against ChatGPT, Gemini, Claude, and Perplexity.

5. **Record structured results.** For every query × engine: did the brand appear (Y/N), at what rank, with what sentiment, was it actively recommended, which domains were cited. Note competitor mentions in the same cells for Share of Voice.

6. **Aggregate the six metrics** across the set and write a compact scorecard plus the citation-domain list.

## Methods: UI-first, API optional

- **UI-first (default, free).** Drive the assistants through the browser (Claude-in-Chrome), one query at a time, reading the rendered answer. No API keys, no per-query cost — the sensible default for most users. Slower and manual, but zero setup.
- **API (optional).** Where an engine exposes an API and the user has a key, script the run for speed and consistency. Faster and more repeatable, but costs tokens and not every consumer assistant has a comparable API surface. Offer it; don't require it.

State which method a given run used, because results aren't perfectly comparable across methods — keep a run on one method for trend integrity.

## Output

A GEO scorecard: the six metrics, a per-engine breakdown, the ranked citation-domain list, and a short read of where the brand is weakest (invisible for which queries, out-cited by whom). Hand the scorecard back to `audit` when called as a sub-audit; write a standalone section when run directly.

## Which adapters / CLI it calls

- **Browser automation** (Claude-in-Chrome) for the default UI-first method — no Growth OS read-side adapters needed.
- Optionally, assistant APIs if the user has keys (their keys, their `.env`).
- Reads the hub for the ICP; writes no analytics calls.

## How it delegates

- **In:** called by `audit` for the GEO section.
- **Out:** the citation-domain list and the "invisible for these queries" gaps feed directly into `geo-content`, which turns them into a citability plan. `geo-audit` measures; `geo-content` fixes.

## Guardrails

- **Fixed fixture.** Don't quietly change the query set between runs, or the trend is meaningless. Version the query list.
- **Clean sessions.** Signed-out/incognito every time, or personalization poisons the baseline.
- **Honest small-N.** Fifteen queries is a directional read, not a census. Report it as a snapshot with a method note, not a precise market share.
- **Read-only.** Observes what assistants say; changes nothing.
