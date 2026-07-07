# Contributing to Growth OS

Thanks for wanting to help. Growth OS is a small, opinionated Growth OS, and it
stays useful by staying coherent. This guide covers how to add skills, adapters,
and docs — and the one rule we will not bend on.

## The one non-negotiable rule: original content only

Everything in this repo must be **written by you, for this repo.** Do not copy,
paste, quote, transcribe, lightly reword, or "port" text from any commercial or
third-party skill/prompt pack (marketing.dev, Corey Haines' packs, or anyone
else). That includes skill bodies, prompt text, taxonomies, and doc copy.

Interoperability is fine and encouraged — Growth OS is *designed* to run alongside
other marketing skill packs. But interop means **calling** or **referring to**
those packs, never redistributing their files or their wording. If you're not
sure whether a contribution crosses the line, assume it does and rewrite it in
your own words from first principles. PRs that include copied third-party text
will be closed.

By opening a PR you confirm the content is your original work (or already MIT/
public-domain compatible) and you license it under this repo's MIT license.

## Repo layout

```
.claude-plugin/     plugin + marketplace manifests
core/skills/        the skills (one folder each, SKILL.md inside)
core/adapters/      Python read-side CLI (growth-os <adapter> <cmd>)
core/mcp/           MCP server scaffold
docs/integrations/  per-service connect guides
runtimes/           runtime notes: claude-code, codex, hermes
```

## Adding or editing a skill

A skill is a Markdown playbook an agent follows as a standard operating
procedure. Keep them portable — they must read the same on Claude Code, Codex,
and Hermes.

- One folder per skill under `core/skills/<name>/` with a `SKILL.md`.
- Start with frontmatter: `name`, a crisp `description` (what it does + when to
  use it), and any trigger phrases.
- Write imperative, numbered steps. Say what to read, what to run, what to write.
- Always read `.agents/product-marketing.md` first; never re-ask the user for
  positioning that already lives there. Persist durable findings back to it.
- For live data, call the CLI (`growth-os <adapter> <cmd>`) rather than hardcoding
  API calls inside the skill.
- No fabricated metrics. If an account isn't connected, the skill must say so.
- No emoji in skill bodies; keep the tone plain and direct.

## Adding an adapter

Adapters are the read-side data layer. v1 is deliberately read-only.

- Add a subcommand under `core/adapters/` so it's reachable as
  `growth-os <adapter> <cmd>`.
- Read credentials from `.env` only. Never hardcode keys; never print secrets.
- Keep output both human-readable and machine-parseable (a `--json` flag is
  ideal) so skills and dashboards can consume it.
- Ship a matching guide in `docs/integrations/<service>.md` covering: what scope/
  key is needed, whether it's zero-approval or approval-gated, and the exact
  steps to obtain it.
- Mark clearly in the PR whether the adapter has been tested against the live API
  or is still untested. Honesty here matters more than polish.

## Docs

Connect guides live in `docs/integrations/`. Write them for someone who has never
touched the platform's developer console. State the approval status up front
(zero-approval vs. lead-time), list required scopes, and give copy-pasteable
steps.

## Style and tone

- English, first person, honest, zero corporate filler.
- Prefer concrete nouns and real numbers over adjectives.
- Diagrams are hand-written standalone `.svg` files (GitHub only renders SVG when
  referenced as its own file, e.g. `![](path.svg)` — never inline in Markdown).
  Use the NoCodeWork palette: pink `#fd43be` → violet `#7c3aed` on accents.

## Workflow

1. Fork and branch from `main`.
2. Make the change; keep PRs focused (one skill, one adapter, one doc).
3. If you added an adapter, note tested vs. untested in the PR description.
4. Open the PR with a plain-language summary of what and why.

## Bugs and ideas

Open an issue. For adapter bugs, include the command you ran (with secrets
redacted) and what you expected vs. what happened.

## License

By contributing, you agree your work is released under the [MIT license](LICENSE).
