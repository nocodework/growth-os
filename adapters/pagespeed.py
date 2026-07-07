"""Growth OS adapter: PageSpeed Insights (Lighthouse + CrUX field data).

v0.1 — untested against live API. Real implementation, read-only.

Auth (zero-approval, minutes to set up):
    Create an API key in Google Cloud Console (enable "PageSpeed Insights API"),
    then export it. The endpoint also works keyless at a low rate limit, so the
    key is optional but strongly recommended.

        export PAGESPEED_API_KEY="AIza...."

Dependencies:
    pip install requests

Docs: docs/integrations/pagespeed.md
"""

from __future__ import annotations

import os
from typing import Any

_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def _key(explicit: str | None = None) -> str | None:
    # Key is optional — return None to run keyless (rate-limited).
    return explicit or os.environ.get("PAGESPEED_API_KEY")


def audit(
    url: str,
    strategy: str = "mobile",
    key: str | None = None,
) -> dict[str, Any]:
    """Run Lighthouse on a URL and return core scores + Core Web Vitals.

    strategy: "mobile" (default) or "desktop".
    """
    if not url:
        raise RuntimeError("pagespeed audit requires --url. See docs/integrations/pagespeed.md")

    try:
        import requests
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("requests not installed. Run: pip install requests") from exc

    params: dict[str, Any] = {
        "url": url,
        "strategy": strategy,
    }
    # Request all Lighthouse categories.
    categories = ["performance", "accessibility", "best-practices", "seo"]
    api_key = _key(key)
    if api_key:
        params["key"] = api_key

    resp = requests.get(
        _ENDPOINT,
        params=[("url", url), ("strategy", strategy)]
        + [("category", c) for c in categories]
        + ([("key", api_key)] if api_key else []),
        timeout=90,
    )
    resp.raise_for_status()
    data = resp.json()

    lighthouse = data.get("lighthouseResult", {})
    cats = lighthouse.get("categories", {})
    scores = {
        name: (cats.get(name, {}).get("score") if cats.get(name) else None)
        for name in ["performance", "accessibility", "best-practices", "seo"]
    }

    audits = lighthouse.get("audits", {})

    def _metric(audit_id: str) -> Any:
        node = audits.get(audit_id, {})
        return {
            "value": node.get("numericValue"),
            "display": node.get("displayValue"),
            "score": node.get("score"),
        }

    lab_metrics = {
        "first-contentful-paint": _metric("first-contentful-paint"),
        "largest-contentful-paint": _metric("largest-contentful-paint"),
        "cumulative-layout-shift": _metric("cumulative-layout-shift"),
        "total-blocking-time": _metric("total-blocking-time"),
        "speed-index": _metric("speed-index"),
    }

    # Field data (CrUX), when available for the URL/origin.
    loading_experience = data.get("loadingExperience", {}).get("metrics", {})

    return {
        "adapter": "pagespeed",
        "command": "audit",
        "url": url,
        "strategy": strategy,
        "scores": scores,
        "lab_metrics": lab_metrics,
        "field_metrics": loading_experience,
        "keyless": api_key is None,
    }


COMMANDS = {
    "audit": audit,
}
