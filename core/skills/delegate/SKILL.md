---
name: delegate
description: Route a growth task to the right skill. Maps a job (get more signups, reduce churn, rank a page, write ads) to Growth OS's native skills first, and — only if the user has a marketing skill pack installed — points to it by reference without copying any of its content. Uses core/knowledge/atomic-skills-map.md. Use when someone runs /growth-os:delegate, says "help me with X growth task," "what should I use for this," or when an audit finding needs an owner.
---

# delegate

The router. Growth OS does diagnosis and context extremely well, but "growth" is a huge surface — copywriting, paid ads, lifecycle email, pricing, referrals, retention. `delegate` takes a concrete task and points it at the right executor: a Growth OS native skill when one fits, or an external marketing skill pack **by reference** when the user has one installed and it's the better tool.

## What it does

- Interprets the growth task and locates it on the AARRR funnel (acquisition, activation, retention, revenue, referral).
- Looks up the task in `core/knowledge/atomic-skills-map.md`.
- Recommends the **native Growth OS skill** if one covers it.
- If the task falls outside Growth OS's native set and the user has an external marketing skill pack installed, notes that "a pack you have can handle this" and names the *category* of capability — never reproducing, quoting, or paraphrasing that pack's content.
- Passes along the relevant context from the hub so whatever executes the task starts informed.

## When to use

- An `audit` finding needs action and it's not obvious which skill owns it.
- The user has a specific growth job and wants the fastest right tool.
- Someone asks "can Growth OS do X?" — `delegate` answers honestly (native / via a pack / not covered).

## Steps

1. **Clarify the task in one line.** "Improve the pricing page's conversion," "get more email signups," "win back churned users." If it's fuzzy, ask one sharpening question.

2. **Place it on the funnel.** Which AARRR stage — and which sub-job. This is the lookup key into the skills map.

3. **Look it up in `atomic-skills-map.md`.** The map lists common growth jobs and, for each, the native Growth OS skill (if any) plus a neutral note about delegating to an installed pack.

4. **Recommend, in priority order:**
   - **a) Native Growth OS skill** — if `context`, `audit`, `geo-audit`, `geo-content`, `connect`, or `dashboard` covers it, route there. Growth OS's own house first.
   - **b) External marketing pack (by reference only)** — if it's a job Growth OS doesn't natively do (write ad variations, build a cold-email sequence, design a paywall, plan an A/B test) *and* the user has a compatible pack installed, tell them: "This is a job for a dedicated marketing skill pack — if you have one installed, it can take this, and Growth OS will feed it your context." Name the capability type, point to their pack, and **stop there.** Do not copy, summarize, or restate anything from that pack. Growth OS links; it never redistributes.
   - **c) Not covered** — if nothing fits, say so plainly rather than forcing a bad match.

5. **Hand off context.** Whatever executes the task, make sure it gets the positioning from `.agents/product-marketing.md` and any relevant audit findings, so it doesn't start cold.

## Which adapters / CLI it calls

None directly. `delegate` is pure routing. It reads `core/knowledge/atomic-skills-map.md` and the hub, then points at an executor. Any data pulls happen inside the skill it routes to.

## How it delegates

That's the whole job. Two lanes:
- **Native** — invoke the matching Growth OS skill.
- **External** — reference an installed pack without touching its content. Growth OS and marketing packs are designed to sit side by side: Growth OS owns context + diagnosis + GEO + data plumbing; a pack owns deep execution of a given marketing craft. `delegate` is the seam between them.

## Guardrails — licensing, non-negotiable

- **Reference, never redistribute.** When pointing at an external pack, Growth OS names the capability and defers to the user's own installed copy. It never bundles, copies, quotes, paraphrases, or reproduces any third-party pack's prompts, skill text, or structure. If a pack isn't installed, Growth OS does not supply its content as a substitute — it says "install a pack for that" or offers the native alternative.
- **Honest coverage.** Don't oversell. If Growth OS can't do something natively and the user has no pack, say it's out of scope rather than improvising a weak version.
- **Context flows one way.** Growth OS shares *the user's own* context with the executor; it never pulls content back from a pack into Growth OS's files.
