# Atomic Skills Map

The routing table `delegate` reads. It maps common growth jobs — organized by the AARRR funnel (Acquisition, Activation, Retention, Revenue, Referral) — to the **native Growth OS skill** that handles them, plus a neutral note about delegating to an external marketing skill pack when the user has one installed.

## How to read this

Each row is a growth job someone actually asks for. For each:

- **Native Growth OS** — the Growth OS skill to use, or "—" if Growth OS doesn't do this natively.
- **Delegate to a pack** — whether this is a job better suited to a dedicated marketing skill pack. When it says "yes (via installed pack)," it means: *if the user has a marketing pack installed, route there by reference.* Growth OS never supplies that pack's content — it points at the user's own copy or, if none is installed, tells them a pack is needed.

Growth OS's native lane is deliberately narrow and deep: **context, diagnosis (audit), AI visibility (GEO), and read-side data plumbing.** Broad marketing *execution* — writing ads, sequences, paywalls, pricing pages — is intentionally left to dedicated packs. This map is where the two lanes meet.

---

## Foundation (runs before everything)

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Capture positioning: USP / UVP / ICP | **context** | no — Growth OS owns this |
| Keep a durable, shared marketing context file | **context** | no — this is the hub every skill reads |
| Diagnose overall growth health | **audit** | no — Growth OS owns diagnosis |
| See the whole picture in one report | **dashboard** | no |
| Wire up data sources / analytics | **connect** | no — Growth OS owns the plumbing |

---

## Acquisition — get found, get visitors

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Technical/on-page SEO audit | **audit** (SEO pass) diagnoses; fix → | yes (via installed pack) for deep on-page rewrites |
| Am I visible in ChatGPT / Gemini / Claude / Perplexity? | **geo-audit** | no — Growth OS owns GEO measurement |
| Make a page quotable/citable by AI | **geo-content** | no — Growth OS owns GEO content patterns |
| Structured data beyond FAQPage (Product, Article, etc.) | geo-content adds FAQPage; broader → | yes (via installed pack) for full schema work |
| Competitor / alternative comparison pages | **audit** surfaces the gap; build → | yes (via installed pack) |
| Paid ads strategy (Google / Meta / LinkedIn) | **audit** can read spend (if connected); strategy → | yes (via installed pack) |
| Write / scale ad creative & headlines | — | yes (via installed pack) |
| Content strategy & editorial planning | **audit** finds gaps; plan → | yes (via installed pack) |
| Landing / homepage copywriting | — | yes (via installed pack) |
| Directory / listing submissions | — | yes (via installed pack) |

## Activation — turn visitors into users

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Which pages convert / where's the drop-off? | **audit** + **dashboard** (GA4/GSC baseline) | no — Growth OS reads the data |
| Conversion-rate optimization on a page/form | **audit** flags it; optimize → | yes (via installed pack) |
| Signup / onboarding flow design | — | yes (via installed pack) |
| Popups / modals / lead capture copy | — | yes (via installed pack) |
| Lead magnets / free tools | — | yes (via installed pack) |

## Retention — keep users coming back

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Read retention/return-visitor signals | **dashboard** (GA4 baseline) | no — Growth OS reads the data |
| Lifecycle / nurture email sequences | — | yes (via installed pack) |
| Churn prevention, save offers, win-backs | — | yes (via installed pack) |
| Community-led retention | — | yes (via installed pack) |

## Revenue — monetize

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Read revenue/conversion baseline | **dashboard** + **audit** (if conversions tracked) | no |
| Pricing strategy & pricing-page design | — | yes (via installed pack) |
| Paywalls / upgrade paths | — | yes (via installed pack) |
| Sales enablement / battle cards | **audit** competitor read informs it; build → | yes (via installed pack) |

## Referral — turn users into advocates

| Job | Native Growth OS | Delegate to a pack |
|-----|---------------|--------------------|
| Referral programs | — | yes (via installed pack) |
| Co-marketing / partnerships | — | yes (via installed pack) |
| Community & advocacy building | — | yes (via installed pack) |

---

## The rule of thumb

1. **Is it context, diagnosis, GEO, or data?** → a native Growth OS skill owns it. Use it.
2. **Is it broad marketing execution** (writing, ads, email, pricing, paywalls, referral mechanics)? → it's pack territory. If the user has a marketing skill pack installed, `delegate` routes there **by reference** — Growth OS feeds it the context from `.agents/product-marketing.md` and lets the pack do the craft. Growth OS never reproduces a pack's content.
3. **Nothing fits and no pack is installed?** → say so honestly. Don't force a weak native version of a job Growth OS wasn't built for.

Growth OS is the Growth OS: it holds the context, runs the diagnosis, owns AI visibility, and plumbs the data. Everything else it points at the right tool for — including tools it didn't write.
