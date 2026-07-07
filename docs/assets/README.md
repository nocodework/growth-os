# Growth OS brand assets

Everything here is hand-written SVG. No exported bitmaps, no clipart, no screenshots.
Keep new assets in the same visual language so the repo reads as one system.

## Files

| File | What it is | Where it's used |
|------|------------|-----------------|
| `growth-os-mark.svg` | The logo-mark — a harbour gate over water in a rounded tile. Square, scales down to a favicon. | avatar, favicon, social card, inline badge |
| `growth-os-hero.svg` | The hero diagram — data sources flow into the Growth OS gate, which drives the audit → context → act growth loop. ~1200 wide. | top of the root `README.md` |

Embed SVGs as standalone images — GitHub only renders `.svg` when it's referenced as a file:

```markdown
![Growth OS](docs/assets/growth-os-hero.svg)
```

Inline `<svg>` markup inside Markdown is stripped by GitHub, so don't paste SVG source into a `.md` file.

## Palette (NoCodeWork)

The brand runs on a pink→violet gradient over ink, with a light surface. Copy these hex tokens exactly.

### Core

| Token | Hex | Use |
|-------|-----|-----|
| pink | `#fd43be` | gradient start, primary accent |
| violet | `#7c3aed` | gradient end, links, arrows |
| deep-violet | `#2a2440` | solid dark fills (nodes, gate) |
| ink | `#1a1a2e` | darkest text / backgrounds |
| off-white | `#ffffff` | light surface, card fills |
| soft | `#f4f5f6` | muted panels, gate opening |

### Semantic (source dots, status)

| Token | Hex | Use |
|-------|-----|-----|
| green | `#16863d` | Google Ads / success |
| amber | `#ffd400` | GA4 / warning |
| blue | `#3b82f6` | Search Console / info |

### Support neutrals

| Token | Hex | Use |
|-------|-----|-----|
| border | `#e7e3ee` | 1px card outlines |
| muted-text | `#9a94ad` | captions, section labels |
| body-text | `#55506a` | secondary copy |

### The gradient

Always **pink → violet**, left-to-right for horizontal accents, top-to-bottom for vertical ones:

```xml
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fd43be"/>
  <stop offset="1" stop-color="#7c3aed"/>
</linearGradient>
```

## SVG conventions

- **Root element:** always set `width`, `height` *and* `viewBox`. Add `role="img"` + `<title>`/`<desc>` for accessibility.
- **Fonts:** `font-family="system-ui,-apple-system,Segoe UI,sans-serif"`. Never rely on a web font — GitHub won't load it.
- **Corners:** rounded, `rx` 12–16 on cards, larger (`rx` ~56) on the app tile.
- **Strokes:** thin (1–3px) for structure, `stroke-linecap="round"` / `stroke-linejoin="round"` everywhere.
- **Accents:** the pink→violet gradient carries the brand — use it on lines, keys and the primary node, not on everything.
- **Backgrounds:** light (`#ffffff` / `#f4f5f6`) for diagrams, `ink` for standalone dark marks.
- **No emoji** inside SVG, no drop-shadow soup, no gratuitous glows — one soft radial accent behind a focal point at most.

## Badges

Shields.io, in-palette:

```markdown
![License: MIT](https://img.shields.io/badge/License-MIT-7c3aed)
![Growth OS](https://img.shields.io/badge/Growth-OS-fd43be)
```
