"""Growth OS adapters — read-side integrations for the Growth OS.

Each adapter is a thin, read-only wrapper over a marketing/analytics API.
Adapters never write to external systems in v0.1. They read credentials from
environment variables, call the vendor API, and return plain Python dicts that
serialise cleanly to JSON.

Adapters:
    ga4         Google Analytics 4 (Data API) — real impl
    gsc         Google Search Console (Search Analytics) — real impl
    mailerlite  MailerLite (subscribers, campaigns, stats) — real impl
    pagespeed   PageSpeed Insights / Lighthouse — real impl
    google_ads  Google Ads — documented stub (approval-gated)
    meta        Meta Marketing / Graph (+ Instagram) — documented stub (approval-gated)
    geo         Generative Engine Optimization prober — protocol stub

Growth OS is part of the NoCodeWork tools — https://nocodework.io
License: MIT
"""

__all__ = [
    "ga4",
    "gsc",
    "mailerlite",
    "pagespeed",
    "google_ads",
    "meta",
    "geo",
]

__version__ = "0.1.0"
