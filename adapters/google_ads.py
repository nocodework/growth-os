"""Growth OS adapter: Google Ads — DOCUMENTED STUB (approval-gated).

Google Ads read access is not zero-approval. Before this adapter can run you
need, on the account owner's side:

    1. A Google Ads Manager (MCC) account.
    2. A developer token (Tools -> API Center). It starts in Test access; you
       apply for Basic/Standard access to hit production accounts.
    3. An OAuth2 client (Desktop or Web) + a refresh token for a user with
       access to the target account.

Because that has a real lead time, v0.1 ships signatures + docstrings only. Each
function raises NotImplementedError pointing at the setup doc. Fill in the body
once you hold a token — the shape of the returned dict is documented per method
so the orchestrator, tools.json manifest, and MCP server stay stable.

Expected env once implemented:
    GOOGLE_ADS_DEVELOPER_TOKEN
    GOOGLE_ADS_CLIENT_ID
    GOOGLE_ADS_CLIENT_SECRET
    GOOGLE_ADS_REFRESH_TOKEN
    GOOGLE_ADS_LOGIN_CUSTOMER_ID   # the MCC id, digits only
    GOOGLE_ADS_CUSTOMER_ID         # the account being read, digits only

Dependencies (once implemented):
    pip install google-ads

Docs: docs/integrations/google-ads.md
"""

from __future__ import annotations

from typing import Any

_NOT_READY = (
    "Google Ads is approval-gated (developer token + MCC). This adapter is a "
    "documented stub in v0.1 — see docs/integrations/google-ads.md to provision "
    "access, then implement the query body."
)


def campaigns(days: int = 30, customer_id: str | None = None) -> dict[str, Any]:
    """Return campaign-level performance for the last N days.

    Planned GAQL: SELECT campaign.name, campaign.status,
    metrics.impressions, metrics.clicks, metrics.cost_micros,
    metrics.conversions, metrics.average_cpc FROM campaign
    WHERE segments.date DURING LAST_{days}_DAYS.

    Returns:
        {
          "adapter": "google_ads", "command": "campaigns",
          "customer_id": "...", "range_days": days,
          "rows": [ { "name", "status", "impressions", "clicks",
                      "cost", "conversions", "cpc" }, ... ]
        }
    """
    raise NotImplementedError(_NOT_READY)


def spend(days: int = 30, customer_id: str | None = None) -> dict[str, Any]:
    """Return total ad spend + top-line efficiency for the last N days.

    Returns:
        { "adapter": "google_ads", "command": "spend",
          "range_days": days, "cost": float, "clicks": int,
          "conversions": float, "cpa": float | None, "roas": float | None }
    """
    raise NotImplementedError(_NOT_READY)


def keywords(days: int = 30, limit: int = 50, customer_id: str | None = None) -> dict[str, Any]:
    """Return top search keywords by cost for the last N days.

    Returns:
        { "adapter": "google_ads", "command": "keywords",
          "range_days": days,
          "rows": [ { "keyword", "match_type", "impressions",
                      "clicks", "cost", "conversions" }, ... ] }
    """
    raise NotImplementedError(_NOT_READY)


COMMANDS = {
    "campaigns": campaigns,
    "spend": spend,
    "keywords": keywords,
}
