"""Growth OS adapter: Google Analytics 4 (Data API).

v0.1 — untested against live API. Real implementation, read-only.

Auth (zero-approval, minutes to set up):
    Either a service account JSON granted Viewer on the GA4 property, or an
    OAuth client with the `analytics.readonly` scope. Point the standard Google
    env var at your key file and set the property id:

        export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
        export GA4_PROPERTY_ID=123456789

Dependencies:
    pip install google-analytics-data

Docs: docs/integrations/ga4.md
"""

from __future__ import annotations

import os
from typing import Any


def _property_id(explicit: str | None = None) -> str:
    prop = explicit or os.environ.get("GA4_PROPERTY_ID")
    if not prop:
        raise RuntimeError(
            "GA4 property id missing. Set GA4_PROPERTY_ID or pass --property-id. "
            "See docs/integrations/ga4.md"
        )
    return prop.replace("properties/", "").strip()


def _client():
    """Build a BetaAnalyticsDataClient using ADC / service account JSON."""
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "google-analytics-data not installed. Run: pip install google-analytics-data"
        ) from exc

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS not set. Point it at your service-account "
            "JSON granted Viewer on the GA4 property. See docs/integrations/ga4.md"
        )
    return BetaAnalyticsDataClient()


def _run_report(
    property_id: str,
    dimensions: list[str],
    metrics: list[str],
    start_date: str,
    end_date: str,
    limit: int = 100,
) -> list[dict[str, Any]]:
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )

    client = _client()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=limit,
    )
    response = client.run_report(request)

    dim_headers = [h.name for h in response.dimension_headers]
    met_headers = [h.name for h in response.metric_headers]

    rows: list[dict[str, Any]] = []
    for row in response.rows:
        record: dict[str, Any] = {}
        for name, cell in zip(dim_headers, row.dimension_values):
            record[name] = cell.value
        for name, cell in zip(met_headers, row.metric_values):
            record[name] = cell.value
        rows.append(record)
    return rows


def overview(
    days: int = 28,
    property_id: str | None = None,
) -> dict[str, Any]:
    """Traffic baseline: users, sessions, engagement over the last N days."""
    prop = _property_id(property_id)
    rows = _run_report(
        property_id=prop,
        dimensions=["date"],
        metrics=[
            "activeUsers",
            "sessions",
            "screenPageViews",
            "engagementRate",
            "averageSessionDuration",
        ],
        start_date=f"{days}daysAgo",
        end_date="today",
        limit=days,
    )
    return {
        "adapter": "ga4",
        "command": "overview",
        "property_id": prop,
        "range_days": days,
        "rows": rows,
    }


def top_pages(
    days: int = 28,
    limit: int = 25,
    property_id: str | None = None,
) -> dict[str, Any]:
    """Highest-traffic pages by views over the last N days."""
    prop = _property_id(property_id)
    rows = _run_report(
        property_id=prop,
        dimensions=["pagePath", "pageTitle"],
        metrics=["screenPageViews", "activeUsers", "engagementRate"],
        start_date=f"{days}daysAgo",
        end_date="today",
        limit=limit,
    )
    return {
        "adapter": "ga4",
        "command": "top_pages",
        "property_id": prop,
        "range_days": days,
        "rows": rows,
    }


def sources(
    days: int = 28,
    limit: int = 25,
    property_id: str | None = None,
) -> dict[str, Any]:
    """Acquisition channels / source-medium over the last N days."""
    prop = _property_id(property_id)
    rows = _run_report(
        property_id=prop,
        dimensions=["sessionSourceMedium", "sessionDefaultChannelGroup"],
        metrics=["sessions", "activeUsers", "conversions"],
        start_date=f"{days}daysAgo",
        end_date="today",
        limit=limit,
    )
    return {
        "adapter": "ga4",
        "command": "sources",
        "property_id": prop,
        "range_days": days,
        "rows": rows,
    }


COMMANDS = {
    "overview": overview,
    "top_pages": top_pages,
    "sources": sources,
}
