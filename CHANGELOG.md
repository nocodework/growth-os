# Changelog

All notable changes to Growth OS are documented here. The format is loosely based on
[Keep a Changelog](https://keepachangelog.com/), and the project aims to follow
[Semantic Versioning](https://semver.org/).

## [0.1.0] — Unreleased

First public scaffold. This is an early, honest cut: the architecture is in
place, the docs are real, and the read-side adapters are written against the real
APIs — but most of them have **not yet been verified against live accounts.**
Treat v0.1.0 as a foundation to build and test on, not a finished product.

### Added

- **Project scaffold** — plugin + marketplace manifests
  (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`), MIT license,
  contributing guide, and this changelog.
- **Six-layer architecture** wired up: orchestrator commands, atomic skill
  composition, read-side adapters, the GEO module, account onboarding wizards,
  and the context hub (`.agents/product-marketing.md`).
- **Skills (skeleton)** in `core/skills/`: `onboard`, `context`, `audit`,
  `geo-audit`, `geo-content`, `connect`, `delegate`, `dashboard`. Bodies are in
  place and follow the portable-SOP format; they will be hardened as the adapters
  are validated.
- **Integration docs** in `docs/integrations/` for GA4, Google Search Console,
  Google Ads, Meta Marketing/Graph (+ Instagram), MailerLite, and PageSpeed
  Insights — each marked zero-approval or approval-gated with the exact steps to
  obtain access.
- **Runtime notes** for three runtimes: Claude Code (plugin, `/growth-os:*`
  commands), OpenAI Codex (`AGENTS.md`, portable core), and Hermes (autonomous
  agent via CLI-as-tools or MCP).
- **MCP scaffold** (`core/mcp/`) exposing adapters as tools and skills as
  resources for autonomous/MCP-based agents.

### Read-side adapters

v1 is intentionally **read-only** — Growth OS reports and audits, it does not push
changes to your accounts.

- `ga4` (GA4 Data API), `gsc` (Search Console), `mailerlite` (MailerLite API),
  `pagespeed` (PageSpeed Insights) — **written against the live APIs but not yet
  tested end-to-end against real accounts.** Expect rough edges; bug reports with
  redacted command output are very welcome.
- `googleads` (Google Ads) and `meta` (Meta Marketing/Graph + Instagram) —
  **stubs only.** These sit behind owner-side approval (Google Ads developer
  token + MCC; Meta Business Verification, which takes ~14+ days, then App
  Review). The command surface exists; the implementations land once test access
  is available.

### Known limitations

- No adapter has a passing live-API integration test yet. "Works" here means
  "written correctly per the docs," not "verified in production."
- `googleads` and `meta` return stub responses until approval and implementation.
- The MCP server is a scaffold; the CLI is the more complete path today.
- No telemetry, by design — so there is no usage data to draw on. Please file
  issues.

### Notes

- All content in this repo is original to Growth OS. No third-party or commercial
  skill/prompt pack text is copied or redistributed; interop with other marketing
  packs is by reference only. See [CONTRIBUTING.md](CONTRIBUTING.md).

[0.1.0]: https://github.com/nocodework/growth-os/releases/tag/v0.1.0
