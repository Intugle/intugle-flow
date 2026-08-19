"""Memory Delete All Component - Delete all memories for a user.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: delete_all_memories
Args: (none - uses user_id from context)

WARNING: This action is irreversible!
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


class DeleteAllMemoriesArgs(BaseModel):
    """Arguments for the delete_all_memories tool.

    No arguments required - user_id is provided via MemoryContext.
    """


# =============================================================================
# Component
# =============================================================================


class MemoryDeleteAllComponent(Component):
    """Memory Delete All Component - Delete all memories for a user.

    This component provides a single tool for deleting ALL memories
    for the configured user. This action is irreversible!

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        delete_all_memories()

    WARNING: This will permanently delete all memories for the user!
    """

    display_name = "Memory Delete All"
    description = "Delete ALL memories for a user. WARNING: This action is irreversible!"
    icon = "trash-2"
    name = "MemoryDeleteAllComponent"
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

    async def delete_all_memories(self) -> str:
        """Delete all memories for the user."""
        ctx = self._get_memory_context()

        logger.warning("Deleting ALL memories for user %r", ctx.user_id)

        try:
            ctx.memory.delete_all(user_id=ctx.user_id)

            logger.info("Successfully deleted all memories for user %r", ctx.user_id)

        except Exception as e:
            logger.exception("Error deleting all memories")
            return f"Error deleting all memories: {e!s}"
        else:
            return f"Successfully deleted all memories for user: {ctx.user_id}"

    async def _get_tools(self) -> list:
        """Return the delete_all_memories tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Delete All Memories"):
            return []

        return [
            StructuredTool(
                name="delete_all_memories",
                description=(
                    "Delete ALL memories for the user. WARNING: This action is irreversible! "
                    "Use this only when the user explicitly requests to clear all their memories "
                    "or for a complete reset. All stored information will be permanently lost."
                ),
                coroutine=self.delete_all_memories,
                args_schema=DeleteAllMemoriesArgs,
                tags=["memory", "delete", "dangerous"],
            ),
        ]
