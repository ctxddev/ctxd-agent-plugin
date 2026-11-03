"""Run a local source-refresh check through a registered LiveKit function tool."""

import argparse
import asyncio
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from importlib.metadata import version
from pathlib import Path

from ctxd import Client
from ctxd.folders import FolderConfig
from ctxd.tracker import TrackerPaths, sync_once
from livekit.agents.llm import FunctionTool
from livekit.agents.llm.utils import function_arguments_to_pydantic_model

from adapter import SourceAgent


async def exercise(client, folder, endpoint, tracker, source):
    source_path = f"{folder.prefix}/{source.name}"
    agent = SourceAgent(client, source_path)
    registered = {tool.id: tool for tool in agent.tools}
    assert set(registered) == {"read_project_instructions"}
    tool = registered["read_project_instructions"]
    assert isinstance(tool, FunctionTool)
    schema = function_arguments_to_pydantic_model(tool).model_json_schema()
    assert schema.get("properties") == {}

    before = "Project instructions\nRun the test suite before sharing changes.\n"
    after = "Project instructions\nRun the test suite and linter before sharing changes.\n"
    source.write_text(before, encoding="utf-8")
    await asyncio.to_thread(sync_once, folders=[folder], endpoint=endpoint, paths=tracker)
    initial = await tool()
    assert initial["available"] and initial["lines"] == before.splitlines()

    source.write_text(after, encoding="utf-8")
    unsynchronized = await tool()
    assert unsynchronized["lines"] == before.splitlines()
    await asyncio.to_thread(sync_once, folders=[folder], endpoint=endpoint, paths=tracker)
    refreshed = await tool()
    assert refreshed["available"] and refreshed["lines"] == after.splitlines()

    source.unlink()
    await asyncio.to_thread(sync_once, folders=[folder], endpoint=endpoint, paths=tracker)
    removed = await tool()
    assert removed == {"available": False, "path": source_path}
    return {
        "registered_tools": list(registered),
        "tool_schema": schema,
        "initial_read": initial,
        "edit_before_sync": unsynchronized,
        "edit_after_sync": refreshed,
        "read_after_removal_and_sync": removed,
    }


def run():
    with tempfile.TemporaryDirectory(prefix="ctxd-livekit-example-") as temporary:
        root = Path(temporary)
        source_dir = root / "sources"
        source_dir.mkdir()
        socket = root / "ctxfs.sock"
        endpoint = f"unix://{socket}"
        folder = FolderConfig(name="ProjectDocs", path=str(source_dir), prefix="local-files/livekit-example")
        tracker = TrackerPaths(state_file=root / "tracker.json")
        client = Client(backend="ctxfs", ctxfs_endpoint=endpoint)
        environment = {key: value for key, value in os.environ.items() if not key.startswith("CTXD_")}
        environment.update(CTXD_CONFIG_PATH=str(root / "config.json"), CTXD_CTXFS_SOCKET=str(socket))
        (root / "config.json").write_text('{"backend":"ctxfs"}', encoding="utf-8")
        with (root / "service.log").open("w+") as log:
            server = subprocess.Popen(
                [sys.executable, "-m", "ctxd.local_ctxfs_service", "serve", "--root", str(root / "store"), "--socket", str(socket)],
                env=environment, stdout=log, stderr=log,
            )
            try:
                for _ in range(100):
                    if server.poll() is not None:
                        raise RuntimeError("The temporary ctxfs service exited before becoming ready.")
                    try:
                        client.files.tree(folder.prefix, limit=10)
                        break
                    except Exception:
                        time.sleep(0.1)
                else:
                    raise RuntimeError("The temporary ctxfs service did not start within ten seconds.")
                checks = asyncio.run(exercise(client, folder, endpoint, tracker, source_dir / "project.md"))
            finally:
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()
    return {
        "passed": True,
        "runtime": {"python": platform.python_version(), "system": platform.system()},
        "packages": {name: version(name) for name in ("ctxd", "livekit-agents")},
        "scope": "Registered LiveKit tool called locally; explicit ctxd synchronization; no model or voice session.",
        "checks": checks,
        "sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ("adapter.py", "demo.py", "requirements.txt")},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON evidence file")
    args = parser.parse_args()
    evidence = run()
    print("PASS: registered tool, first read, edit before sync, refreshed read, removal.")
    if args.output:
        args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
