"""Memory List Component - List all memories for a user.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: list_all_memories
Args: (none - uses user_id from context)
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.tools import StructuredTool
from lfx.custom.custom_component.component import Component
from lfx.io import HandleInput, StrInput
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# =============================================================================
# Tool Arguments Schema
# =============================================================================


class ListAllMemoriesArgs(BaseModel):
    """Arguments for the list_all_memories tool.

    No arguments required - user_id is provided via MemoryContext.
    """


# =============================================================================
# Component
# =============================================================================


class MemoryListComponent(Component):
    """Memory List Component - List all memories for a user.

    This component provides a single tool for listing all stored memories
    for the configured user. Useful for getting an overview of what
    information has been stored.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        list_all_memories()
    """

    display_name = "Memory List"
    description = "List all stored memories for the user."
    icon = "list"
    name = "MemoryListComponent"
    add_tool_output = True

    inputs = [
        HandleInput(
            name="memory_context",
            display_name="Memory Context",
            input_types=["MemoryContext"],
            info="Connect to MemoryConfigProvider output. Provides shared Memory instance and configuration.",
            required=True,
        ),
        StrInput(
            name="tool_trigger",
            display_name="",
            show=False,
            tool_mode=True,
            required=False,
        ),
    ]

    def build(self) -> None:
        """Tools are exposed through ``_get_tools`` rather than a data output."""
        return

    def _get_memory_context(self) -> Any:
        """Retrieve and validate the MemoryContext input."""
        ctx = self.memory_context
        if ctx is None:
            message = "memory_context is required. Connect MemoryConfigProvider output to this component."
            raise ValueError(message)
        if not hasattr(ctx, "memory") or not hasattr(ctx, "user_id"):
            message = "Invalid memory_context. Expected MemoryContext object from MemoryConfigProvider."
            raise ValueError(message)
        return ctx

    async def list_all_memories(self) -> str:
        """List all stored memories for the user."""
        ctx = self._get_memory_context()

        logger.info("Listing all memories for user %r", ctx.user_id)

        try:
            results = ctx.memory.get_all(filters={"user_id": ctx.user_id})

            rows = results.get("results", []) if isinstance(results, dict) else results or []

            if not rows:
                return f"No memories found for user: {ctx.user_id}"

            formatted = []
            for i, row in enumerate(rows, 1):
                memory_text = row.get("memory", row.get("text", str(row)))
                memory_id = row.get("id", "N/A")
                formatted.append(f"{i}. [ID: {memory_id}]: {memory_text}")

            return f"Found {len(rows)} memories:\n" + "\n".join(formatted)

        except Exception as e:
            logger.exception("Error listing memories")
            return f"Error listing memories: {e!s}"

    async def _get_tools(self) -> list:
        """Return the list_all_memories tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("List All Memories"):
            return []

        return [
            StructuredTool(
                name="list_all_memories",
                description=(
                    "List all stored memories for the user. Returns all memories "
                    "with their IDs and content. Use this to see everything that "
                    "has been remembered about the user."
                ),
                coroutine=self.list_all_memories,
                args_schema=ListAllMemoriesArgs,
                tags=["memory", "list"],
            ),
        ]
