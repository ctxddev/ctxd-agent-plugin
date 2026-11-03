#!/bin/sh
set -eu

# Keep startup output separate from the MCP JSON-RPC stream.
ctxd backend set ctxfs >&2
ctxd folders add /sources --name Source >&2
python -m ctxd.tracker_service sync-once >&2
ctxd tracker start >&2
exec ctxd-mcp
