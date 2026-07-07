"""Growth OS adapter: MailerLite (new API v2).

v0.1 — untested against live API. Real implementation, read-only.

Auth (zero-approval, minutes to set up):
    Create an API token in the MailerLite UI (Integrations -> API) and export it.

        export MAILERLITE_API_KEY="ml-xxxxxxxxxxxxxxxx"

Dependencies:
    pip install requests

Docs: docs/integrations/mailerlite.md
"""

from __future__ import annotations

import os
from typing import Any

_BASE = "https://connect.mailerlite.com/api"


def _token(explicit: str | None = None) -> str:
    token = explicit or os.environ.get("MAILERLITE_API_KEY")
    if not token:
        raise RuntimeError(
            "MailerLite token missing. Set MAILERLITE_API_KEY "
            "(Integrations -> API in the MailerLite UI). See docs/integrations/mailerlite.md"
        )
    return token.strip()


def _get(path: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        import requests
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("requests not installed. Run: pip install requests") from exc

    resp = requests.get(
        f"{_BASE}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        params=params or {},
        timeout=30,
    )
    if resp.status_code == 401:
        raise RuntimeError("MailerLite returned 401 — check MAILERLITE_API_KEY.")
    resp.raise_for_status()
    return resp.json()


def account(token: str | None = None) -> dict[str, Any]:
    """Account-level totals: subscriber count, plan, timezone."""
    tok = _token(token)
    data = _get("/subscribers", tok, params={"limit": 1})
    total = data.get("total") if isinstance(data, dict) else None
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    return {
        "adapter": "mailerlite",
        "command": "account",
        "subscriber_total": total if total is not None else meta.get("total"),
        "raw_meta": meta,
    }


def subscribers(limit: int = 25, token: str | None = None) -> dict[str, Any]:
    """Recent subscribers (email, status, created_at)."""
    tok = _token(token)
    data = _get("/subscribers", tok, params={"limit": limit})
    items = data.get("data", []) if isinstance(data, dict) else []
    rows = [
        {
            "email": s.get("email"),
            "status": s.get("status"),
            "created_at": s.get("created_at"),
            "opted_in_at": s.get("opted_in_at"),
        }
        for s in items
    ]
    return {
        "adapter": "mailerlite",
        "command": "subscribers",
        "count": len(rows),
        "rows": rows,
    }


def campaigns(limit: int = 25, token: str | None = None) -> dict[str, Any]:
    """Recent campaigns with headline delivery stats (opens, clicks)."""
    tok = _token(token)
    data = _get("/campaigns", tok, params={"limit": limit})
    items = data.get("data", []) if isinstance(data, dict) else []
    rows = []
    for c in items:
        stats = c.get("stats", {}) or {}
        rows.append(
            {
                "name": c.get("name"),
                "status": c.get("status"),
                "type": c.get("type"),
                "sent_at": c.get("finished_at") or c.get("scheduled_for"),
                "sent": stats.get("sent"),
                "opens_count": stats.get("opens_count"),
                "clicks_count": stats.get("clicks_count"),
                "open_rate": (stats.get("open_rate") or {}).get("float")
                if isinstance(stats.get("open_rate"), dict)
                else stats.get("open_rate"),
            }
        )
    return {
        "adapter": "mailerlite",
        "command": "campaigns",
        "count": len(rows),
        "rows": rows,
    }


COMMANDS = {
    "account": account,
    "subscribers": subscribers,
    "campaigns": campaigns,
}
