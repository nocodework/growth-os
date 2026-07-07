"""Growth OS adapter: Meta Marketing / Graph API (+ Instagram) — DOCUMENTED STUB.

Meta read access is the slowest to provision:

    1. Business Verification on your Meta Business account FIRST. This alone
       takes ~14+ days and must clear before advanced permissions unlock.
    2. A Meta app + App Review for the permissions you need:
         - ads_read              (Marketing API: campaign/ad insights)
         - instagram_basic       (IG account + media)
         - instagram_manage_insights (IG reach/impressions/engagement)
    3. A long-lived access token for a System User (recommended) or user token.

Because of the verification lead time this adapter ships as signatures +
docstrings only in v0.1. Each function raises NotImplementedError pointing at
the setup doc. Return shapes are documented so the rest of Growth OS stays stable
until you drop in the Graph calls.

Expected env once implemented:
    META_ACCESS_TOKEN
    META_AD_ACCOUNT_ID      # e.g. act_1234567890
    META_IG_USER_ID         # numeric IG business account id

Dependencies (once implemented):
    pip install requests            # Graph API is plain HTTPS/JSON

Docs: docs/integrations/meta.md
"""

from __future__ import annotations

from typing import Any

_GRAPH = "https://graph.facebook.com/v20.0"  # pin the version you review against

_NOT_READY = (
    "Meta is approval-gated (Business Verification ~14+ days, then App Review for "
    "ads_read / instagram_*). This adapter is a documented stub in v0.1 — see "
    "docs/integrations/meta.md to provision access, then implement the Graph calls."
)


def ad_insights(days: int = 30, ad_account_id: str | None = None) -> dict[str, Any]:
    """Return ad-account insights for the last N days (Marketing API).

    Planned: GET {_GRAPH}/{act_id}/insights with fields=spend,impressions,
    clicks,ctr,cpc,actions and date_preset / time_range.

    Returns:
        { "adapter": "meta", "command": "ad_insights",
          "range_days": days,
          "rows": [ { "date_start", "date_stop", "spend", "impressions",
                      "clicks", "ctr", "cpc", "results" }, ... ] }
    """
    raise NotImplementedError(_NOT_READY)


def instagram_profile(ig_user_id: str | None = None) -> dict[str, Any]:
    """Return the Instagram business profile snapshot.

    Planned: GET {_GRAPH}/{ig_user_id}?fields=username,followers_count,
    media_count,biography.

    Returns:
        { "adapter": "meta", "command": "instagram_profile",
          "username": str, "followers_count": int, "media_count": int }
    """
    raise NotImplementedError(_NOT_READY)


def instagram_insights(days: int = 30, ig_user_id: str | None = None) -> dict[str, Any]:
    """Return Instagram account insights for the last N days.

    Planned: GET {_GRAPH}/{ig_user_id}/insights with
    metric=reach,impressions,profile_views and period=day.

    Returns:
        { "adapter": "meta", "command": "instagram_insights",
          "range_days": days,
          "rows": [ { "metric", "date", "value" }, ... ] }
    """
    raise NotImplementedError(_NOT_READY)


COMMANDS = {
    "ad_insights": ad_insights,
    "instagram_profile": instagram_profile,
    "instagram_insights": instagram_insights,
}
