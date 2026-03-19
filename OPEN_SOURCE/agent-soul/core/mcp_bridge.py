#!/usr/bin/env python3
"""
MCP Bridge -- Expose sovrun agents as MCP tool servers.

External tools (n8n, Claude, other agents) can call sovrun agents
via the Model Context Protocol stdio transport. Also manages connections
to external MCP servers for consuming their tools.

Usage:
    from sovrun.core.mcp_bridge import MCPServerBridge
    from sovrun.core.handoff import HandoffRouter, handoff_target

    router = HandoffRouter()

    @handoff_target("summarizer")
    def summarize(context):
        return {"summary": context["text"][:100]}

    router.register(summarize)

    bridge = MCPServerBridge(router)
    bridge.serve_stdio()  # Blocks, serves MCP over stdin/stdout

CLI:
    sovrun-mcp --serve         # Start MCP server (stdio)
    sovrun-mcp --list          # Show available external MCPs
    sovrun-mcp --test TOOL     # Test an MCP tool call
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("SOVRUN_ROOT", Path.cwd()))
LOGS_DIR = Path(os.environ.get("SOVRUN_LOGS_DIR", PROJECT_ROOT / "logs"))
MCP_REGISTRY = Path(os.environ.get(
    "SOVRUN_MCP_REGISTRY", PROJECT_ROOT / "config" / "mcp_servers.json"))
MCP_LOG = LOGS_DIR / "mcp_bridge.jsonl"

logger = logging.getLogger("sovrun.mcp_bridge")


def safe_path(target: str | Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    root = PROJECT_ROOT.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"BLOCKED: {resolved} outside {root}")
    return resolved


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


# ---------------------------------------------------------------------------
# Tool annotations (per MCP spec)
# ---------------------------------------------------------------------------

@dataclass
class ToolAnnotation:
    """MCP tool annotations marking behavior characteristics."""
    read_only: bool = False
    destructive: bool = False
    idempotent: bool = False
    open_world: bool = False
    title: str = ""
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        # Include bool fields even when False (False is a valid annotation).
        # Only exclude empty strings and None.
        return {k: v for k, v in asdict(self).items()
                if v is not None and v != ""}


# ---------------------------------------------------------------------------
# Schema generation
# ---------------------------------------------------------------------------

def generate_tool_schema(agent_name: str,
                         description: str = "",
                         annotations: ToolAnnotation | None = None,
                         input_properties: dict[str, Any] | None = None,
                         required_fields: list[str] | None = None) -> dict[str, Any]:
    """Create MCP-compatible JSON schema for an agent's capabilities.

    Returns a tool definition following the MCP tools/list response format.
    """
    props = input_properties or {
        "task_description": {
            "type": "string",
            "description": "What to ask the agent to do",
        },
        "context": {
            "type": "object",
            "description": "Additional context passed to the agent",
            "additionalProperties": True,
        },
    }

    schema: dict[str, Any] = {
        "name": f"sovrun_{agent_name}",
        "description": description or f"Execute the {agent_name} agent",
        "inputSchema": {
            "type": "object",
            "properties": props,
            "required": required_fields or ["task_description"],
        },
    }

    if annotations:
        schema["annotations"] = annotations.to_dict()

    return schema


# ---------------------------------------------------------------------------
# MCP JSON-RPC helpers
# ---------------------------------------------------------------------------

def _jsonrpc_response(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _jsonrpc_error(req_id: Any, code: int, message: str,
                   data: Any = None) -> dict[str, Any]:
    err: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": req_id, "error": err}


# ---------------------------------------------------------------------------
# MCPServerBridge
# ---------------------------------------------------------------------------

class MCPServerBridge:
    """Exposes registered handoff targets as MCP tools over stdio.

    Takes a HandoffRouter and creates MCP tool definitions for each
    registered agent. Handles the MCP JSON-RPC protocol over stdin/stdout.

    Args:
        router: HandoffRouter with registered agent endpoints.
        annotations: optional per-agent annotation overrides.
    """

    def __init__(self, router: Any = None,
                 annotations: dict[str, ToolAnnotation] | None = None) -> None:
        self._router = router
        self._annotations = annotations or {}
        self._tool_schemas: dict[str, dict[str, Any]] = {}
        _ensure_dir(LOGS_DIR)

        if router is not None:
            self._build_schemas()

    def _build_schemas(self) -> None:
        """Generate MCP tool schemas from registered handoff agents."""
        if self._router is None:
            return

        for agent_name in self._router.list_agents():
            ann = self._annotations.get(agent_name, ToolAnnotation())
            schema = generate_tool_schema(
                agent_name=agent_name,
                description=f"Invoke the {agent_name} agent via sovrun handoff",
                annotations=ann,
            )
            self._tool_schemas[f"sovrun_{agent_name}"] = schema

    def _log_call(self, method: str, tool_name: str = "",
                  success: bool = True, error: str = "") -> None:
        """Append MCP call to audit log."""
        entry = {
            "ts": _now_iso(),
            "method": method,
            "tool": tool_name,
            "success": success,
            "error": error,
        }
        try:
            with open(MCP_LOG, "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except OSError:
            pass

    # -- Protocol handlers --------------------------------------------------

    def _handle_initialize(self, req_id: Any, params: dict) -> dict:
        """Handle MCP initialize request."""
        return _jsonrpc_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"listChanged": False},
            },
            "serverInfo": {
                "name": "sovrun-mcp-bridge",
                "version": "0.1.0",
            },
        })

    def _handle_tools_list(self, req_id: Any, params: dict) -> dict:
        """Handle tools/list request."""
        tools = list(self._tool_schemas.values())
        self._log_call("tools/list")
        return _jsonrpc_response(req_id, {"tools": tools})

    def _handle_tools_call(self, req_id: Any, params: dict) -> dict:
        """Handle tools/call request by routing to the appropriate agent."""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name not in self._tool_schemas:
            self._log_call("tools/call", tool_name, success=False,
                           error="unknown tool")
            return _jsonrpc_error(
                req_id, -32602, f"Unknown tool: {tool_name}")

        # Extract agent name from tool name (strip "sovrun_" prefix)
        agent_name = tool_name.removeprefix("sovrun_")

        if self._router is None:
            self._log_call("tools/call", tool_name, success=False,
                           error="no router")
            return _jsonrpc_error(req_id, -32603, "No router configured")

        # Import here to avoid circular dependency at module level
        from .handoff import HandoffRequest, GuardrailScope

        task_desc = arguments.get("task_description", "")
        context = arguments.get("context", {})

        request = HandoffRequest(
            source_agent="mcp_bridge",
            target_agent=agent_name,
            context=context,
            task_description=task_desc,
            guardrail_scope=GuardrailScope.READ_ONLY,
        )

        try:
            result = self._router.send(request)
        except Exception as exc:
            self._log_call("tools/call", tool_name, success=False,
                           error=str(exc))
            return _jsonrpc_error(req_id, -32603, f"Agent execution failed: {exc}")

        if result.success:
            self._log_call("tools/call", tool_name, success=True)
            return _jsonrpc_response(req_id, {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result.result_data, default=str),
                }],
            })
        else:
            self._log_call("tools/call", tool_name, success=False,
                           error=result.error or "")
            return _jsonrpc_response(req_id, {
                "content": [{
                    "type": "text",
                    "text": json.dumps({
                        "error": result.error,
                        "success": False,
                    }),
                }],
                "isError": True,
            })

    def _handle_request(self, request: dict) -> dict | None:
        """Route a JSON-RPC request to the appropriate handler."""
        method = request.get("method", "")
        req_id = request.get("id")
        params = request.get("params", {})

        handlers = {
            "initialize": self._handle_initialize,
            "tools/list": self._handle_tools_list,
            "tools/call": self._handle_tools_call,
        }

        handler = handlers.get(method)
        if handler:
            return handler(req_id, params)

        # Notifications (no id) are ignored
        if req_id is None:
            return None

        return _jsonrpc_error(req_id, -32601, f"Method not found: {method}")

    def serve_stdio(self) -> None:
        """Run as stdio MCP server using newline-delimited JSON-RPC.

        Reads one JSON object per line from stdin, writes responses
        as one JSON object per line to stdout. Blocks until stdin closes.
        Does not use Content-Length framing.
        """
        logger.info("MCP server starting on stdio")
        self._log_call("server_start")

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                response = _jsonrpc_error(None, -32700, "Parse error")
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                continue

            response = self._handle_request(request)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

        self._log_call("server_stop")
        logger.info("MCP server stopped")


# ---------------------------------------------------------------------------
# MCPClientPool
# ---------------------------------------------------------------------------

@dataclass
class MCPServerEntry:
    """Registry entry for an external MCP server."""
    name: str
    transport: str = "stdio"  # stdio, sse, streamable-http
    command: str = ""
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MCPServerEntry:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class MCPClientPool:
    """Manage connections to external MCP servers.

    Reads a registry JSON of known MCP servers and their capabilities.
    Does NOT manage live connections (stdlib only, no async transport),
    but provides the registry and tool lookup needed to integrate with
    external MCP orchestrators.

    Args:
        registry_path: path to mcp_servers.json registry file.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        self._registry_path = registry_path or MCP_REGISTRY
        self._servers: dict[str, MCPServerEntry] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Load server registry from JSON file."""
        if not self._registry_path.exists():
            return
        try:
            data = json.loads(self._registry_path.read_text())
            servers = data if isinstance(data, list) else data.get("servers", [])
            for entry in servers:
                server = MCPServerEntry.from_dict(entry)
                self._servers[server.name] = server
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("failed to load MCP registry: %s", exc)

    def list_available(self) -> list[dict[str, Any]]:
        """List all registered external MCP servers."""
        return [s.to_dict() for s in self._servers.values()]

    def get_server(self, name: str) -> MCPServerEntry | None:
        """Get a server entry by name."""
        return self._servers.get(name)

    def find_by_capability(self, capability: str) -> list[MCPServerEntry]:
        """Find servers that advertise a given capability."""
        return [
            s for s in self._servers.values()
            if capability in s.capabilities
        ]

    def register_server(self, entry: MCPServerEntry) -> None:
        """Add or update a server in the registry."""
        self._servers[entry.name] = entry
        self._save_registry()

    def remove_server(self, name: str) -> bool:
        """Remove a server from the registry."""
        if name in self._servers:
            del self._servers[name]
            self._save_registry()
            return True
        return False

    def _save_registry(self) -> None:
        """Persist registry to disk."""
        _ensure_dir(self._registry_path.parent)
        path = safe_path(self._registry_path)
        data = {"servers": [s.to_dict() for s in self._servers.values()]}
        path.write_text(json.dumps(data, indent=2))


def list_available_mcps(registry_path: Path | None = None) -> list[dict[str, Any]]:
    """Read the MCP registry and return available servers."""
    pool = MCPClientPool(registry_path)
    return pool.list_available()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="MCP Bridge -- expose sovrun agents as MCP tool servers")
    parser.add_argument("--serve", action="store_true",
                        help="Start MCP server (stdio transport)")
    parser.add_argument("--list", action="store_true",
                        help="Show available external MCPs from registry")
    parser.add_argument("--test", type=str, metavar="TOOL",
                        help="Test an MCP tool call (dry run)")
    args = parser.parse_args()

    if not any([args.serve, args.list, args.test]):
        parser.print_help()
        return

    if args.list:
        servers = list_available_mcps()
        print(f"\n=== External MCP Servers ({len(servers)}) ===\n")
        if not servers:
            print(f"  No servers registered.")
            print(f"  Add servers to: {MCP_REGISTRY}")
        for s in servers:
            print(f"  {s['name']}")
            print(f"    Transport: {s.get('transport', 'stdio')}")
            if s.get("command"):
                print(f"    Command: {s['command']}")
            if s.get("capabilities"):
                print(f"    Capabilities: {', '.join(s['capabilities'])}")
            if s.get("description"):
                print(f"    Description: {s['description']}")
            print()

    if args.test:
        tool_name = args.test
        print(f"\n=== Test Tool Call: {tool_name} ===\n")

        # Build a test request
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": {
                    "task_description": "test invocation",
                    "context": {"test": True},
                },
            },
        }
        print(f"Request:")
        print(json.dumps(test_request, indent=2))
        print()

        # Try to execute against local bridge
        try:
            from .handoff import HandoffRouter
            router = HandoffRouter()
            bridge = MCPServerBridge(router)
            response = bridge._handle_request(test_request)
            print(f"Response:")
            print(json.dumps(response, indent=2))
        except Exception as exc:
            print(f"Test failed: {exc}")
            print("(This is expected if no agents are registered)")
        print()

    if args.serve:
        print("Starting MCP server on stdio...", file=sys.stderr)
        try:
            from .handoff import HandoffRouter
            router = HandoffRouter()
            bridge = MCPServerBridge(router)
            bridge.serve_stdio()
        except ImportError:
            # Serve without router if handoff not available
            bridge = MCPServerBridge()
            bridge.serve_stdio()


if __name__ == "__main__":
    main()
