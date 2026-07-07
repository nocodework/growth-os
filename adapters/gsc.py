"""Growth OS adapter: Google Search Console (Search Analytics API).

v0.1 — untested against live API. Real implementation, read-only.

Auth (zero-approval, minutes to set up):
    The SAME service account you use for GA4 works here — add it as a user
    (Restricted / Full) on the Search Console property, then grant the
    `webmasters.readonly` scope.

        export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
        export GSC_SITE_URL="https://example.com/"   # or "sc-domain:example.com"

Dependencies:
    pip install google-api-python-client google-auth

Docs: docs/integrations/gsc.md
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any

_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def _site_url(explicit: str | None = None) -> str:
    site = explicit or os.environ.get("GSC_SITE_URL")
    if not site:
        raise RuntimeError(
            "GSC site url missing. Set GSC_SITE_URL or pass --site-url "
            '(e.g. "https://example.com/" or "sc-domain:example.com"). '
            "See docs/integrations/gsc.md"
        )
    return site.strip()


def _service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "google-api-python-client not installed. "
            "Run: pip install google-api-python-client google-auth"
        ) from exc

    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS not set. Point it at the service-account "
            "JSON added as a user on the Search Console property. See docs/integrations/gsc.md"
        )
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=_SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def _date_range(days: int) -> tuple[str, str]:
    end = _dt.date.today()
    start = end - _dt.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def query(
    days: int = 28,
    dimensions: list[str] | None = None,
    limit: int = 100,
    site_url: str | None = None,
) -> dict[str, Any]:
    """Search Analytics rows (default dimension: query) over the last N days."""
    site = _site_url(site_url)
    dims = dimensions or ["query"]
    start, end = _date_range(days)

    service = _service()
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": dims,
        "rowLimit": limit,
    }
    response = (
        service.searchanalytics()
        .query(siteUrl=site, body=body)
        .execute()
    )

    rows: list[dict[str, Any]] = []
    for row in response.get("rows", []):
        record = {name: value for name, value in zip(dims, row.get("keys", []))}
        record["clicks"] = row.get("clicks")
        record["impressions"] = row.get("impressions")
        record["ctr"] = row.get("ctr")
        record["position"] = row.get("position")
        rows.append(record)

    return {
        "adapter": "gsc",
        "command": "query",
        "site_url": site,
        "range_days": days,
        "dimensions": dims,
        "rows": rows,
    }


def top_queries(
    days: int = 28,
    limit: int = 50,
    site_url: str | None = None,
) -> dict[str, Any]:
    """Top search queries by clicks."""
    return {
        **query(days=days, dimensions=["query"], limit=limit, site_url=site_url),
        "command": "top_queries",
    }


def top_pages(
    days: int = 28,
    limit: int = 50,
    site_url: str | None = None,
) -> dict[str, Any]:
    """Top landing pages from organic search by clicks."""
    return {
        **query(days=days, dimensions=["page"], limit=limit, site_url=site_url),
        "command": "top_pages",
    }


COMMANDS = {
    "query": query,
    "top_queries": top_queries,
    "top_pages": top_pages,
}
