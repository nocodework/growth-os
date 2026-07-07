# Growth OS on Claude Code

This is the reference runtime. Growth OS ships as a Claude Code plugin, so every
`/growth-os:*` command maps 1:1 to a skill in `core/skills/`. Nothing here is
Claude-specific in spirit — the same skills run on Codex and Hermes (see the
sibling folders) — but Claude Code is where the slash commands, the plugin
marketplace install, and the skill auto-discovery all work out of the box.

## Install

```
/plugin marketplace add nocodework/growth-os
/plugin install growth-os
```

The plugin manifest (`.claude-plugin/plugin.json`) points at `./core/skills`,
so all eight skills load automatically. Restart the session if the commands
don't show up on first install.

## The commands

Growth OS exposes six orchestrator commands. Each one is a thin conductor — it
reads/writes the context hub (`.agents/product-marketing.md`) and calls the
atomic skills underneath.

| Command | Skill(s) it runs | What happens |
|---------|------------------|--------------|
| `/growth-os:onboard <url>` | `onboard` → `context` | Fetches the business URL, extracts USP / UVP / ICP / positioning, writes the first version of `.agents/product-marketing.md`, then walks you through what to connect next. |
| `/growth-os:context` | `context` | Opens, reviews, or patches the context hub by hand. Run it any time your positioning changes so every downstream skill stays current. |
| `/growth-os:audit` | `audit` (+ `geo-audit`) | Full growth audit: on-page + technical SEO, PageSpeed/Core Web Vitals, competitor snapshot, and — if any accounts are connected — a live GA4/GSC baseline. Pulls GEO results in via `geo-audit`. |
| `/growth-os:connect [service]` | `connect` | The onboarding wizard for accounts and API keys. Handles the zero-approval integrations end-to-end and hands you a checklist for the approval-gated ones. |
| `/growth-os:delegate <goal>` | `delegate` | Reads the context hub, decides which marketing skill(s) fit the goal, and hands off with full context pre-loaded (works with your existing marketing skill packs). |
| `/growth-os:dashboard` | `dashboard` | Assembles the connected read-side adapters into one plain-English status view: traffic, top queries, ad spend, list growth, speed. |

GEO has two skills of its own that the orchestrator calls, and you can also run
them directly:

- `/growth-os:geo-audit` → `geo-audit` — measures whether ChatGPT, Gemini, Claude,
  and Perplexity mention/cite you for your core prompts, and where you rank
  against competitors in AI answers.
- `/growth-os:geo-content` → `geo-content` — turns those gaps into concrete
  content and structured-data work so AI engines start citing you.

## How a command actually runs

1. The command loads its skill from `core/skills/<name>/SKILL.md`.
2. The skill reads `.agents/product-marketing.md` for product, audience, and
   positioning context (so you never re-explain your business).
3. For anything that needs live data, the skill shells out to the Python CLI:
   `growth-os <adapter> <cmd>` (e.g. `growth-os ga4 traffic --days 28`). Adapters read
   credentials from your local `.env` — see `docs/integrations/`.
4. Results are summarized back into the conversation and, where useful, appended
   to the context hub so the next skill inherits them.

## Where things live

```
core/skills/            portable skill bodies (SKILL.md each)
core/adapters/          Python read-side CLI (growth-os <adapter> <cmd>)
docs/integrations/      per-service connect guides
.agents/                product-marketing.md — the context hub (created on onboard)
.env                    your own API keys (gitignored, never committed)
```

## Start here

```
/growth-os:onboard https://your-business.com
/growth-os:connect          # wire up GA4, GSC, MailerLite, PageSpeed — minutes, no approvals
/growth-os:audit            # first full growth read
```
