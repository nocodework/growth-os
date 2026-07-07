# Growth OS on Hermes (autonomous agents)

Growth OS is runtime-agnostic, so it drops into a long-running autonomous agent the
same way it drops into an interactive CLI. This guide targets a Nous Hermes-style
agent (a self-directed loop with a tool registry and a system prompt), but the
approach generalizes to any agent that can (a) run a shell command or call an MCP
tool and (b) read a Markdown file.

There are two ways to wire Growth OS in. Use whichever your agent supports; you can
use both.

## Option A — CLI as tools (simplest)

Register the Growth OS CLI as callable tools. Each read-side adapter command becomes
one tool the agent can invoke autonomously.

```
tool: growth-os_ga4         → runs `growth-os ga4 <cmd> [flags]`
tool: growth-os_gsc         → runs `growth-os gsc <cmd> [flags]`
tool: growth-os_pagespeed   → runs `growth-os pagespeed audit --url <url>`
tool: growth-os_mailerlite  → runs `growth-os mailerlite <cmd>`
tool: growth-os_meta        → runs `growth-os meta <cmd>`        (once approved)
tool: growth-os_googleads   → runs `growth-os googleads <cmd>`   (once approved)
```

Give each tool a one-line description matching the adapter (e.g. "GA4 traffic,
sources, and top pages for the connected property") so the agent's planner can
route to it. Credentials are read from `.env` in the Growth OS checkout — the agent
never sees the raw keys.

## Option B — MCP server (structured)

Growth OS ships an MCP scaffold. Point your agent's MCP client at it and the same
adapters are exposed as MCP tools, with the skills available as MCP resources the
agent can read on demand.

```jsonc
// mcp config (illustrative)
{
  "mcpServers": {
    "growth-os": {
      "command": "python",
      "args": ["-m", "core.mcp.server"],
      "cwd": "/path/to/growth-os"
    }
  }
}
```

> The MCP server is a v0.1.0 scaffold — see `CHANGELOG.md`. The CLI (Option A) is
> the more mature path today.

## System-prompt include

For an autonomous agent to *use* Growth OS well, it needs to know the operating
procedure, not just the tool list. Include this block in the agent's system
prompt (adapt paths to your deployment):

```
You have Growth OS, a Growth OS, available as tools.

Ground rules:
- The file .agents/product-marketing.md is the business context hub
  (USP / UVP / ICP / positioning). Read it before any marketing action.
  Keep it updated when you learn something durable about the business.
- For any decision that needs real numbers, call a growth-os_* tool. Never
  fabricate metrics; if an account isn't connected, say so.
- Growth playbooks live in core/skills/<name>/SKILL.md. Read the relevant
  one and follow it as your SOP. The verbs are: onboard, context, audit,
  geo-audit, geo-content, connect, delegate, dashboard.
- Keys live in .env and must never be printed or exfiltrated.
```

## A typical autonomous run

1. Read `.agents/product-marketing.md`. If missing, follow
   `core/skills/onboard/SKILL.md` to build it from the business URL.
2. On a schedule (say, weekly): follow `core/skills/audit/SKILL.md`, calling
   `growth-os_pagespeed`, `growth-os_gsc`, `growth-os_ga4`, and the GEO checks.
3. Diff against the last run stored in the context hub; surface material changes
   (traffic drop, ranking loss, AI-visibility gap) to its notification channel.
4. Where a gap is actionable, follow `core/skills/delegate/SKILL.md` to hand the
   work to the matching marketing skill.

Because the skills and adapters are identical across runtimes, an audit produced
by a Hermes agent overnight is directly comparable to one you run by hand in
Claude Code the next morning — same context hub, same numbers, same playbook.
