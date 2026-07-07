#!/usr/bin/env python3
"""Growth OS MCP server — expose the read-side adapters as MCP tools.

This lets any MCP-capable runtime (Claude Code, Codex, Hermes, a custom host)
call Growth OS adapters as first-class tools instead of shelling out to the CLI.
It reads the SAME adapter modules and the SAME `adapters/tools.json` manifest, so
there is one source of truth for what exists.

Run it (stdio transport):

    python -m mcp.server
    # or, if installed:  growth-os-mcp

Then register it with your host. For Claude Code, add to your MCP config:

    {
      "mcpServers": {
        "growth-os": { "command": "python", "args": ["-m", "mcp.server"] }
      }
    }

Dependencies:
    pip install "mcp"

Design:
    * Tools are generated dynamically from tools.json — add an adapter command
      to the manifest + the adapter's COMMANDS dict and it shows up here for free.
    * Each tool call maps its JSON arguments straight onto the adapter callable's
      keyword arguments (same contract the CLI uses).
    * Credentials are read from the server process's environment, exactly like the
      CLI. Never accept secrets as tool arguments.

Part of the NoCodeWork tools — https://nocodework.io  ·  License: MIT
"""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Manifest + adapter loading (shared source of truth with the CLI)
# ---------------------------------------------------------------------------

_MANIFEST_PATH = Path(__file__).resolve().parent.parent / "adapters" / "tools.json"

_ADAPTER_MODULES: dict[str, str] = {
    "ga4": "adapters.ga4",
    "gsc": "adapters.gsc",
    "google_ads": "adapters.google_ads",
    "meta": "adapters.meta",
    "mailerlite": "adapters.mailerlite",
    "pagespeed": "adapters.pagespeed",
    "geo": "adapters.geo",
}

# MCP tool names can't contain a space; we join adapter + command with "__".
_TOOL_SEP = "__"


def _load_manifest() -> dict[str, Any]:
    with _MANIFEST_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _json_type(t: str) -> str:
    return {
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "list": "array",
        "string": "string",
    }.get(t, "string")


def _input_schema(args: list[dict[str, Any]]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []
    for arg in args:
        name = arg["name"]
        schema: dict[str, Any] = {"type": _json_type(arg.get("type", "string"))}
        if schema["type"] == "array":
            schema["items"] = {"type": "string"}
        if "default" in arg:
            schema["default"] = arg["default"]
        if "enum" in arg:
            schema["enum"] = arg["enum"]
        properties[name] = schema
        if arg.get("required"):
            required.append(name)
    out: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        out["required"] = required
    return out


def _call_adapter(adapter: str, command: str, arguments: dict[str, Any]) -> dict[str, Any]:
    module = importlib.import_module(_ADAPTER_MODULES[adapter])
    commands = getattr(module, "COMMANDS", {})
    func = commands.get(command)
    if func is None:
        raise ValueError(f"unknown command '{command}' for adapter '{adapter}'")
    return func(**(arguments or {}))


# ---------------------------------------------------------------------------
# MCP wiring
# ---------------------------------------------------------------------------

def build_server():  # -> mcp.server.Server
    """Construct and return the MCP Server with all Growth OS tools registered.

    TODO(runtime): if you target a different MCP SDK surface (FastMCP, the
    low-level Server, or a hosted transport), this is the ONE function to adapt.
    Everything above is transport-agnostic.
    """
    try:
        from mcp.server import Server
        from mcp.types import TextContent, Tool
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('MCP SDK not installed. Run: pip install "mcp"') from exc

    manifest = _load_manifest()
    server = Server("growth-os")

    # Flatten manifest -> {tool_name: (adapter, command, arg_spec)}
    registry: dict[str, tuple[str, str, list[dict[str, Any]]]] = {}
    for adapter in manifest.get("adapters", []):
        a_name = adapter["name"]
        for cmd in adapter.get("commands", []):
            tool_name = f"{a_name}{_TOOL_SEP}{cmd['name']}"
            registry[tool_name] = (a_name, cmd["name"], cmd.get("args", []))

    @server.list_tools()
    async def list_tools() -> list[Tool]:  # type: ignore[valid-type]
        tools: list[Tool] = []
        for adapter in manifest.get("adapters", []):
            a_name = adapter["name"]
            status = adapter.get("status", "")
            access = adapter.get("access", "")
            for cmd in adapter.get("commands", []):
                tag = f" [{status}/{access}]" if status else ""
                tools.append(
                    Tool(
                        name=f"{a_name}{_TOOL_SEP}{cmd['name']}",
                        description=f"{adapter.get('title', a_name)}: {cmd['description']}{tag}",
                        inputSchema=_input_schema(cmd.get("args", [])),
                    )
                )
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:  # type: ignore[valid-type]
        entry = registry.get(name)
        if entry is None:
            payload = {"error": f"unknown tool '{name}'"}
        else:
            adapter, command, _args = entry
            try:
                payload = _call_adapter(adapter, command, arguments or {})
            except NotImplementedError as exc:
                payload = {"error": str(exc), "kind": "not_implemented"}
            except Exception as exc:  # noqa: BLE001 — MCP boundary
                payload = {"error": str(exc), "kind": type(exc).__name__}
        return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, default=str))]

    return server


async def _amain() -> None:
    # TODO(runtime): swap stdio_server for your transport (SSE / streamable HTTP)
    # if you host Growth OS remotely rather than as a local stdio subprocess.
    from mcp.server.stdio import stdio_server

    server = build_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    import asyncio

    # Ensure the package root is importable when run as a script.
    os.environ.setdefault("PYTHONPATH", str(Path(__file__).resolve().parent.parent))
    asyncio.run(_amain())


if __name__ == "__main__":
    main()
