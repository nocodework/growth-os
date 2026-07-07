---
name: context
description: Build or update the Growth OS context hub — .agents/product-marketing.md — the single source of truth for the business's USP, UVP, ICP, positioning, and voice. Pre-fills from a business URL, confirms with the user through short batched questions, and writes idempotently. Use when someone runs /growth-os:context, says "set up my context," "update positioning," "who's my ICP," or before any other growth work so downstream skills have something to read.
---

# context

Every other Growth OS skill reads one file: `.agents/product-marketing.md`. `context` is the skill that creates and maintains it. Get this right and the audit, GEO work, and any delegated marketing task all speak in the business's actual language instead of guessing.

## What it does

Turns a URL and a short interview into a durable, structured positioning document:

- **USP** — what makes this business different, in one sentence.
- **UVP** — the value promise to the customer (outcome, not features).
- **ICP** — who it's for: segment, role, company shape, the pain that sends them looking.
- **Positioning** — category, main alternatives, the wedge.
- **Voice & proof** — tone, words to use and avoid, credible proof points (numbers, names, guarantees).

It writes this to `.agents/product-marketing.md` in the project root and keeps it current across sessions.

## When to use

- Before any other Growth OS growth work, on a fresh project.
- When positioning shifts — new segment, new pricing, a pivot, a rebrand.
- When the audit or a delegated skill produces a vague result and the root cause is thin context.

## Inputs

- A **business URL** (strongly preferred — it's the pre-fill source).
- Whatever the user already knows about their audience. If they know a lot, the interview is a confirmation. If they know little, it's discovery.

## Steps

1. **Read the URL.** Pull the homepage and one or two key pages (pricing, product, about). Extract a first draft of USP/UVP/ICP and voice from what's actually on the site. This draft is a starting point, not the answer.

2. **Present the pre-fill for confirmation.** Show the user what you inferred, section by section, in plain language: "Here's what your site says you do and who it's for — is this right?" People correct a draft far faster than they fill a blank form. Never treat the inference as final; it's a prompt for correction.

3. **Interview in small batches.** Ask **3–5 questions at a time**, never a wall of twenty. Group by theme:
   - Batch 1 — the customer: who buys, what job they're hiring the product for, what they'd Google at 2am.
   - Batch 2 — the difference: why they pick you over the obvious alternative, what you refuse to be.
   - Batch 3 — proof and voice: hard numbers, named customers, guarantees; the tone and the words to avoid.
   Wait for answers before the next batch. Stop early if the picture is already complete — don't pad.

4. **Synthesize.** Fold the confirmed pre-fill and the interview answers into clean, specific prose. No filler, no generic marketing adjectives. If the user gave a concrete number or a real customer name, use it verbatim.

5. **Write idempotently.**
   - If `.agents/product-marketing.md` **doesn't exist** → create it with the full structure.
   - If it **exists** → read it first, merge the new information, and **show a diff of what changes before writing.** Never blow away sections the user already curated. Preserve any `## Audit Findings` or other appended sections written by other skills — update the positioning sections only.
   - Confirm before overwriting anything non-trivial.

6. **Close the loop.** Tell the user the hub is written and that every other Growth OS skill now reads from it. Point them to `/growth-os:connect` (wire up data) or `/growth-os:audit` (run the growth audit) as the next step.

## File structure it maintains

```
# Product Marketing Context

## Business
<one-paragraph what-it-is>

## USP
## UVP
## ICP
- Primary segment:
- Role / buyer:
- Trigger / pain:

## Positioning
- Category:
- Main alternatives:
- Wedge:

## Voice
- Tone:
- Use these words:
- Avoid:

## Proof
- <numbers, named customers, guarantees>

<-- other skills append below, e.g. ## Audit Findings -->
```

## Which adapters / CLI it calls

None. `context` is a reasoning + file skill. It reads the web (URL) and writes one markdown file. No credentials, no API calls.

## How it delegates

`context` is usually delegated *to* (by `onboard`) rather than delegating out. It's a leaf. Its one downstream signal: when it finishes, the ICP it captured becomes the seed for `geo-audit`'s query set, so a clean ICP directly improves GEO measurement quality.

## Guardrails

- **Never overwrite silently.** Diff-and-confirm on any existing file.
- **Specific over generic.** "Ops leads at 20–50 person agencies drowning in client reporting" beats "small businesses that want to grow."
- **User's words win.** The pre-fill is a hypothesis; the user's correction is the truth.
- **One file, project-local.** The hub lives in the repo, in version control if the user wants it, never phoned home.
