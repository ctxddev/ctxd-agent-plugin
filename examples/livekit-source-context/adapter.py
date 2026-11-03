"""A LiveKit function tool that reads a configured source through ctxd."""

import asyncio
from typing import Any

from ctxd import Client
from ctxd.exceptions import CtxdError
from livekit.agents import Agent, function_tool


class SourceAgent(Agent):
    def __init__(self, client: Client, source_path: str):
        self._client = client
        self._source_path = source_path
        super().__init__(
            instructions=(
                "Read the current project instructions before answering questions "
                "about the project. If the source is unavailable, say so."
            )
        )

    @function_tool()
    async def read_project_instructions(self) -> dict[str, Any]:
        """Read up to 80 lines of the project's synchronized source instructions."""
        try:
            result = await asyncio.to_thread(
                self._client.files.read_lines,
                self._source_path,
                start_line=1,
                end_line=80,
            )
        except CtxdError as error:
            if error.status_code == 404:
                return {"available": False, "path": self._source_path}
            raise
        return {
            "available": True,
            "path": self._source_path,
            "lines": result.lines,
        }
