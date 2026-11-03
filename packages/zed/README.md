# ctxd MCP Server for Zed

Connect Zed to open-source [ctxd](https://github.com/ctxd-dev/ctxd), context
infrastructure between agents and data. The local tracker synchronizes source
content into ctxfs. Zed can inspect paths and read source content through Model
Context Protocol (MCP).

## Setup

On your Linux workstation as your normal user, install
[uv](https://docs.astral.sh/uv/getting-started/installation/) and use a Python
3.11 or 3.12 environment. The system `ps` command must be available.

```sh
pip install ctxd
ctxd backend set ctxfs
ctxd folders add /path/to/your/source --name Source
python -m ctxd.tracker_service sync-once
ctxd tracker start
```

Replace the source path with material you want your agent to access. Run Zed as
the same user, install this extension and enable **ctxd MCP Server** in the
Agent Panel's MCP settings. The extension starts `ctxd-mcp` through `uvx` with
Python 3.12. It does not configure or select source folders for you.

Start with `tree`, then pass a returned source path to `read` or `read_lines`.
Edit a source file, allow synchronization to complete, then read it again.
The supported tools are `ls`, `tree`, `glob`, `stat`, `read` and `read_lines`.
The ctxd 0.1.16 wheel also advertises `grep`, which fails because its implementation
is missing; Python and the CLI provide exact text search.

No hosted ctxd account or server API key is required. Zed's configured model
provider may receive content returned by these tools. This extension is intended
for a local workspace; the ctxd bridge and tracker must share the same user state.

If Zed cannot find `uvx`, set its absolute path in Zed settings:

```json
{
  "context_servers": {
    "mcp-server-ctxd": {
      "settings": { "uvx_path": "/absolute/path/to/uvx" }
    }
  }
}
```

The `settings.env` map can supply an existing ctxd configuration's environment
variables. The extension only launches the bridge; configure sources explicitly.

## Development

On a Linux workstation as a normal user, use Rust with the `wasm32-wasip2`
target installed. In Zed, run **Install Dev Extension** and select this directory.
Test the server in a local workspace before submitting a registry change.

[Get started](https://ctxd.dev) · [Source and GitHub stars](https://github.com/ctxd-dev/ctxd)
