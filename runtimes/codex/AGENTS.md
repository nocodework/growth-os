# Growth OS on OpenAI Codex

Growth OS has no runtime lock-in. The skills in `core/skills/` are plain Markdown
playbooks, and the data layer is a plain Python CLI. That's everything Codex
needs — there are no Claude-only APIs in the core. This file tells a Codex agent
how to drive Growth OS.

## Mental model

Growth OS = **portable skills** (what to do) + **read-side adapters** (how to get
the numbers) + **a context hub** (what the business is).

- Skills live in `core/skills/<name>/SKILL.md`. Read the relevant one before you
  act. Treat it as your standard operating procedure, not as background reading.
- The context hub is `.agents/product-marketing.md`. It holds USP / UVP / ICP /
  positioning. Read it first on every task; write to it when you learn something
  durable about the business.
- Live data comes from the CLI: `growth-os <adapter> <cmd> [flags]`. Adapters read
  credentials from `.env` in the repo root.

There are no slash commands on Codex. You invoke a "command" by reading its skill
and following it. The mapping is one skill per orchestrator verb:
`onboard`, `context`, `audit`, `geo-audit`, `geo-content`, `connect`,
`delegate`, `dashboard`.

## Setup

```bash
# from the repo root
pip install -r core/adapters/requirements.txt
cp .env.example .env          # then fill in your own keys
growth-os --help                 # confirm the CLI resolves
```

If `growth-os` isn't on your PATH, call the module directly:
`python -m core.adapters.cli <adapter> <cmd>`.

## The core loop for any task

1. **Read context.** Open `.agents/product-marketing.md`. If it doesn't exist,
   run the onboard flow first (below).
2. **Read the skill.** Open `core/skills/<name>/SKILL.md` for the job at hand and
   follow its steps.
3. **Pull data when needed.** Shell out to `growth-os <adapter> <cmd>`.
4. **Summarize + persist.** Report back in plain language; append durable
   findings to the context hub so the next task inherits them.

## Worked examples

**Onboard a new business (the `onboard` skill):**

```bash
# 1. read core/skills/onboard/SKILL.md
# 2. fetch and read the target site, extract USP/UVP/ICP/positioning
# 3. write the first version of the context hub:
#    .agents/product-marketing.md
# 4. tell the user what to connect next (see the connect skill)
```

**Run a growth audit (the `audit` + `geo-audit` skills):**

```bash
growth-os pagespeed audit --url https://your-business.com --strategy mobile
growth-os gsc queries --days 28          # if Search Console is connected
growth-os ga4 traffic --days 28          # if GA4 is connected
# then follow geo-audit/SKILL.md to test ChatGPT/Gemini/Claude/Perplexity visibility
```

**Read the dashboard (the `dashboard` skill):**

```bash
growth-os ga4 traffic --days 28
growth-os gsc queries --days 28
growth-os mailerlite subscribers
growth-os meta insights --days 28        # once Meta is approved & connected
growth-os googleads spend --days 28      # once Google Ads is approved & connected
```

**Delegate to a marketing skill (the `delegate` skill):** read the context hub,
pick the matching marketing skill from your environment, and hand off with the
positioning already loaded. Growth OS is designed to run *alongside* existing
marketing skill packs, not replace them — it does the research, wiring, and
context; they do the craft.

## Adapters available in v1 (read-side)

`ga4`, `gsc`, `mailerlite`, `pagespeed` are ready to run once keys are set.
`googleads` and `meta` are stubs pending owner-side approval (developer token /
Business Verification). See `docs/integrations/` for each connect guide and
`CHANGELOG.md` for exactly what is untested against live APIs.

## Rules of the road

- Never invent metrics. If an adapter isn't connected, say so — don't fabricate a
  baseline.
- Keys stay in `.env`. Never print secrets, never commit them.
- The context hub is the source of truth. Keep it current; downstream tasks
  depend on it.
