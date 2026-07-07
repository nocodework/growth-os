#!/usr/bin/env python3
"""Growth OS CLI — read-side adapter dispatcher.

    growth-os <adapter> <command> [flags]

Every adapter exposes a COMMANDS dict mapping command name -> callable. The CLI
resolves the callable, maps --flags onto its keyword arguments, invokes it, and
prints the returned dict as JSON on stdout. Credentials always come from the
environment (see each adapter's module docstring and docs/integrations/*).

Examples:
    growth-os ga4 overview --days 28
    growth-os gsc top_queries --days 28 --limit 50
    growth-os pagespeed audit --url https://example.com --strategy mobile
    growth-os mailerlite campaigns --limit 10
    growth-os geo generate_queries --brand Growth OS --category "growth tooling"
    growth-os --list

Design notes:
    * Adapters are imported lazily so a missing optional dependency for one
      vendor never breaks the whole CLI.
    * Errors are printed as JSON ({"error": ...}) with a non-zero exit code, so
      any calling runtime can parse failures the same way it parses results.

Part of the NoCodeWork tools — https://nocodework.io  ·  License: MIT
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from typing import Any, Callable

# adapter name -> module path (lazy import).
ADAPTERS: dict[str, str] = {
    "ga4": "adapters.ga4",
    "gsc": "adapters.gsc",
    "google_ads": "adapters.google_ads",
    "meta": "adapters.meta",
    "mailerlite": "adapters.mailerlite",
    "pagespeed": "adapters.pagespeed",
    "geo": "adapters.geo",
}


def _load_commands(adapter: str) -> dict[str, Callable[..., dict[str, Any]]]:
    module = importlib.import_module(ADAPTERS[adapter])
    commands = getattr(module, "COMMANDS", None)
    if not isinstance(commands, dict):
        raise RuntimeError(f"adapter '{adapter}' does not expose a COMMANDS dict")
    return commands


def _coerce(value: str) -> Any:
    """Best-effort scalar coercion for --flag values (int, float, bool, csv, str)."""
    low = value.lower()
    if low in ("true", "false"):
        return low == "true"
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]
    return value


def _parse_flags(tokens: list[str]) -> dict[str, Any]:
    """Turn ['--days', '28', '--limit', '10'] into {'days': 28, 'limit': 10}.

    Supports --key value, --key=value, and bare --flag (=> True).
    """
    kwargs: dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if not tok.startswith("--"):
            raise SystemExit(f"unexpected argument: {tok!r} (flags must start with --)")
        key = tok[2:]
        if "=" in key:
            key, raw = key.split("=", 1)
            kwargs[key.replace("-", "_")] = _coerce(raw)
            i += 1
            continue
        # Look ahead for a value.
        if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
            kwargs[key.replace("-", "_")] = _coerce(tokens[i + 1])
            i += 2
        else:
            kwargs[key.replace("-", "_")] = True
            i += 1
    return kwargs


def _print_manifest() -> int:
    listing: dict[str, list[str]] = {}
    for name in ADAPTERS:
        try:
            listing[name] = sorted(_load_commands(name).keys())
        except Exception as exc:  # noqa: BLE001 — surface import issues per-adapter
            listing[name] = [f"<unavailable: {exc}>"]
    print(json.dumps({"growth-os": "0.1.0", "adapters": listing}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    parser = argparse.ArgumentParser(
        prog="growth-os",
        description="Growth OS — the open-source Growth OS for any AI agent. "
        "Read-side adapter dispatcher.",
        add_help=True,
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List every adapter and its commands as JSON, then exit.",
    )
    parser.add_argument("adapter", nargs="?", choices=sorted(ADAPTERS), help="Adapter to call.")
    parser.add_argument("command", nargs="?", help="Command exposed by the adapter.")
    parser.add_argument(
        "rest",
        nargs=argparse.REMAINDER,
        help="Adapter flags, e.g. --days 28 --limit 10.",
    )

    args = parser.parse_args(argv)

    if args.list or (not args.adapter):
        return _print_manifest()

    if not args.command:
        cmds = ", ".join(sorted(_load_commands(args.adapter)))
        print(json.dumps({"error": f"missing command for '{args.adapter}'. available: {cmds}"}))
        return 2

    try:
        commands = _load_commands(args.adapter)
        func = commands.get(args.command)
        if func is None:
            avail = ", ".join(sorted(commands))
            print(json.dumps({"error": f"unknown command '{args.command}'. available: {avail}"}))
            return 2

        kwargs = _parse_flags(args.rest)
        result = func(**kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        return 0

    except NotImplementedError as exc:
        print(json.dumps({"error": str(exc), "kind": "not_implemented"}))
        return 3
    except TypeError as exc:
        # Usually a bad/unknown --flag for this command.
        print(json.dumps({"error": f"bad arguments: {exc}", "kind": "usage"}))
        return 2
    except Exception as exc:  # noqa: BLE001 — CLI boundary: report, don't traceback
        print(json.dumps({"error": str(exc), "kind": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
