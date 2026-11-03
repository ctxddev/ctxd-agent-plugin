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

## Run in Docker

The container packages ctxd 0.1.16 from PyPI with Python 3.12. It starts ctxfs,
synchronizes the mounted source folder, starts the tracker and serves MCP over
stdio. The tracker checks for source changes every ten seconds plus processing
time. The context store is rebuilt when a new container starts. Paths keep the
`local-files/source/` prefix across containers, including gateways that start
a fresh process for each tool call.

On your Linux workstation as a user with Docker access, build the image:

```bash
docker build -t ctxd-mcp https://github.com/ctxddev/ctxd-agent-plugin.git
```

Use this configuration in your MCP client on that workstation. Replace
`/absolute/path/to/source` with a folder readable by the container's user
(UID 10001). Choose only source material you want the client to access.

```json
{
  "mcpServers": {
    "ctxd": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--init", "--network=none", "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--mount", "type=bind,src=/absolute/path/to/source,dst=/sources,readonly",
        "ctxd-mcp"
      ]
    }
  }
}
```

Start with `tree`, then read a returned path. Source files are mounted read-only;
the container makes no network requests at runtime. The MCP client can send read
content to its configured model provider. The tracker accepts its documented
text formats; it does not ingest arbitrary file formats.

The six tools listed above work in this package. The package also advertises
`grep`, but calling it fails because `CtxfsFiles.grep` is missing in 0.1.16.
Use Python or the CLI for exact text search. No remote MCP endpoint or credentials
are required by this container.

## Support and privacy

For setup questions, contact [hi@ctxd.dev](mailto:hi@ctxd.dev) or open an issue in this repository.

Report security issues privately to [hi@ctxd.dev](mailto:hi@ctxd.dev).

[Privacy policy](PRIVACY.md)
