# ctxd agent plugin

ctxd is open-source context infrastructure between agents and data. Its tracker synchronizes source content into ctxfs, so agents can inspect paths and read current source material.

### MCP tools

- Inspect paths: `ls`, `tree`, `glob`, `stat`.
- Read source content: `read`, `read_lines`.
- Updates come from the tracker. Edit a source, synchronize it, then read the changed content.

Python and the CLI also provide exact text search.

### Local setup

On your Linux workstation as your normal user, use Python 3.11 or 3.12 and ensure the system `ps` command is available. In your Python environment:

```bash
pip install ctxd
ctxd backend set ctxfs
ctxd folders add /path/to/your/source --name Source
python -m ctxd.tracker_service sync-once
ctxd tracker start
```

Replace `/path/to/your/source` with the folder you want to track. Start your MCP client as the same user. With `uv` installed, use this server configuration:

```json
{
  "mcpServers": {
    "ctxd": {
      "command": "uvx",
      "args": ["--python", "3.12", "--from", "ctxd", "ctxd-mcp"]
    }
  }
}
```

The bridge uses local standard input/output (stdio). No hosted account or API key is needed. Start with `tree`, then pass a returned path to `read` or `read_lines`.

[Get started with ctxd](https://ctxd.dev) · [Source and GitHub stars](https://github.com/ctxd-dev/ctxd)

The package is free and MIT-licensed: https://github.com/ctxd-dev/ctxd/blob/main/LICENSE

## Install in Gemini CLI

After setting up the source and tracker above, run on your workstation as the same user:

```bash
gemini extensions install https://github.com/ctxddev/ctxd-agent-plugin
```

## Install in Kiro

Open Powers, select Add Custom Power, then Import power from GitHub. Enter:

https://github.com/ctxddev/ctxd-agent-plugin

The plugin uses `uvx` to start the local ctxd MCP bridge. It needs the ctxfs store and tracker configured under the same user account.

## Support and privacy

For setup questions, contact [hi@ctxd.dev](mailto:hi@ctxd.dev) or open an issue in this repository.

[Privacy policy](PRIVACY.md)
