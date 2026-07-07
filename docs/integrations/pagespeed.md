# PageSpeed Insights

Growth OS reads this to score your site's **speed and Core Web Vitals** (Lighthouse performance, LCP, CLS, INP) during the growth audit — no account approval needed, just a free API key.

## Prerequisites
- A Google account.
- ~3 minutes.

## Step 1 — Create a Google Cloud API key
1. Open [Google Cloud Console](https://console.cloud.google.com/) and pick (or create) a project.
2. Go to **APIs & Services → Library**, search **PageSpeed Insights API**, click **Enable**.
3. Go to **APIs & Services → Credentials → Create credentials → API key**.
4. Copy the key. (Optional but recommended: **Restrict key** → restrict to *PageSpeed Insights API*.)

## Step 2 — Paste it into `.env`
```bash
PAGESPEED_API_KEY="AIza..."
```

## Verify
```bash
growth-os pagespeed audit --url https://your-site.com
```
You should get JSON with Lighthouse scores and Core Web Vitals.

## Troubleshooting
- **`403 / API key not valid`** — make sure the PageSpeed Insights API is *enabled* on the same project the key belongs to.
- **Empty field data** — CrUX field metrics only appear for URLs with enough real-user traffic; lab (Lighthouse) scores always return.
- **Rate limits** — the free tier allows ~25k requests/day; audits are one request per URL.
