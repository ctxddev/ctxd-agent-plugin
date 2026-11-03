# Read current source context from a LiveKit tool

This example gives a LiveKit `Agent` a `@function_tool` that reads project
instructions through ctxd. Change the source, synchronize it, then call the same
tool to read the new instructions.

Run on a Linux workstation as your normal user, with Python 3.12. From this
example's directory:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python demo.py
```

The demo starts its own temporary ctxfs service, registers the tool on an actual
LiveKit agent, and calls that registered tool locally. It checks the first read,
an edit before synchronization, the refreshed read after synchronization, and a
removed source. It cleans up the temporary service and files afterward.

Look for `PASS: registered tool, first read, edit before sync, refreshed read, removal.`
No model API key or LiveKit Cloud account is needed. This check covers the local
tool and source-refresh path; it does not start a voice conversation.

## Use the adapter

`SourceAgent` in [adapter.py](adapter.py) takes a ctxd `Client` and a source path
from your context store. Its tool reads up to 80 lines and returns the source
path alongside the text. Synchronization stays in the application or tracker;
the read tool does not mutate the source.

Use this agent with your application's LiveKit session and model configuration.
Choose a source you intend the agent to read. The demo uses synthetic project
instructions so it can run without accessing your own data.

[Try ctxd](https://ctxd.dev) · [Why ctxd](https://ctxd.dev/blog/why-ctxd) ·
[LiveKit function tools](https://docs.livekit.io/agents/logic/tools/definition/)
