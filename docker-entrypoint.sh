#!/bin/sh
set -eu

# Keep startup output separate from the MCP JSON-RPC stream.
ctxd backend set ctxfs >&2
python - <<'PY'
import os
from ctxd.config import load_config, save_config
from ctxd.folders import FolderConfig

if not os.access('/sources', os.R_OK | os.X_OK):
    raise RuntimeError('The source folder must be readable by container UID 10001')
config = load_config()
# Gateways may start a new container for each call. Keep returned paths stable.
config['folders'] = {
    'Source': FolderConfig(name='Source', path='/sources', prefix='local-files/source').model_dump()
}
save_config(config)
PY
python -m ctxd.tracker_service sync-once >&2
ctxd tracker start >&2
exec ctxd-mcp
