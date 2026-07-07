---
name: geo-content
description: Make a page more likely to be cited and quoted by AI assistants. Applies a 9-pattern citability checklist (answer-first, descriptive headings, standalone sections, tables, lists, fact density, entity naming, clean HTML) and adds llms.txt plus FAQPage schema. Use when someone runs /growth-os:geo-content, says "optimize for AI citations," "make this quotable," "GEO content," "help ChatGPT quote my page," or after geo-audit shows the brand is invisible or out-cited.
---

# geo-content

`geo-audit` tells you *whether* AI assistants cite you. `geo-content` is how you earn more of those citations — by restructuring content so an assistant can lift a clean, self-contained, factual answer straight from your page. It's not a growth hack; it's disciplined information design that happens to also help human readers and traditional SEO.

## What it does

Takes a page (or a content plan) and applies a concrete checklist that makes it more extractable and quotable, then adds the two machine-readable affordances assistants and their crawlers look for:

- A **9-pattern citability pass** on the content itself.
- An **llms.txt** file describing the site for AI crawlers.
- **FAQPage / structured data** where the content is genuinely Q&A shaped.

## When to use

- After `geo-audit` surfaces queries where the brand is invisible or losing citations to competitors.
- When writing or rewriting a cornerstone page that should become the quotable answer for a topic.
- As the content-side follow-through on a growth audit finding.

## The 9 citability patterns

Work through each. They compound — a page that does all nine is dramatically easier for an assistant to quote confidently.

1. **Answer-first.** Put the direct answer in the first sentence or two under the heading, before context or story. Assistants extract the top of a section; bury the answer and it gets skipped.
2. **Descriptive H2/H3.** Headings that state the question or the claim ("How much does X cost?" / "X reduces onboarding time by 40%"), not clever labels. The heading is the retrieval hook.
3. **Standalone sections.** Each section should make sense lifted out of the page with no surrounding context. No "as mentioned above," no dangling pronouns referring to earlier sections.
4. **Tables for structured comparisons.** Pricing, feature comparisons, specs — put them in real HTML tables. Assistants parse and reproduce tables cleanly.
5. **Lists for steps and enumerations.** Ordered lists for processes, unordered for sets. Extractable, scannable, quotable as-is.
6. **Fact density.** Concrete numbers, dates, named specifics over adjectives. "Ships in 3 business days" beats "fast shipping." Facts are what gets quoted; vibes get paraphrased away or dropped.
7. **Entity naming.** Name the product, company, people, and category explicitly and consistently — don't rely on "we," "our platform," "it." Assistants attribute to named entities; unnamed subjects lose the citation.
8. **Clean semantic HTML.** Proper heading hierarchy, real `<table>`/`<ul>`/`<ol>`, no critical content trapped in images or rendered only by client-side JS an crawler won't run. If it isn't in the served HTML, it can't be cited.
9. **Freshness signals.** Visible published/updated dates and current figures. Assistants prefer sources that look maintained.

## The two machine affordances

- **llms.txt.** Author a root `llms.txt` that gives AI crawlers a clean map: what the site is, the canonical pages worth reading, short descriptions. It's the AI-era analogue of a curated sitemap-for-reasoning. Keep it honest and concise.
- **FAQPage schema.** Where a section is genuinely a set of questions and answers, add valid FAQPage structured data. Don't fake it — schema that doesn't match visible content is a liability, not a lever. For other structured-data types, hand off to the `schema` capability.

## Steps

1. Take the target page(s) — often the gaps `geo-audit` flagged.
2. Run the 9-pattern checklist, producing specific, line-level edits (rewrite this heading, front-load this answer, convert this paragraph to a table). Show the before/after; don't just describe.
3. Draft or update `llms.txt` for the site.
4. Add FAQPage schema only where the content truly is Q&A.
5. Note what to re-measure: point the user back to `geo-audit` in a few weeks to see if citations moved.

## Which adapters / CLI it calls

None directly. It's a content + markup skill. It reads the page (web fetch), reads `geo-audit`'s gap list if available, and outputs edits, an `llms.txt`, and schema. It changes nothing on the live site — it produces the changes for the user to ship.

## How it delegates

- **In:** consumes `geo-audit`'s citation-domain gaps and invisible-query list to prioritize which pages to work on first.
- **Out:** deep structured-data work beyond FAQPage → `schema` capability; broader content planning → content-strategy skills; the actual publishing → the user's own workflow. Growth OS is read-side and advisory here — it hands over finished edits, it doesn't push them.

## Guardrails — read this

- **GEO is SEO's sibling, not its replacement.** These patterns help citations *and* traditional ranking. Never sell "AI visibility" as a magic channel that bypasses fundamentals — a page still needs to be good, indexable, and genuinely useful. Frame every recommendation as "this helps both."
- **No fabricated schema.** Structured data must match visible content, always.
- **No manipulation.** The goal is being genuinely the best, most quotable answer — not gaming assistants. Anything else gets unwound the moment models update.
- **Measure, don't promise.** Recommend re-running `geo-audit` to verify impact instead of claiming a guaranteed lift.
