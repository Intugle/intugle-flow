"""Memory Delete Component - Delete a specific memory.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: delete_memory
Args:
    - memory_id (str): ID of the memory to delete
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.tools import StructuredTool
from lfx.custom.custom_component.component import Component
from lfx.io import HandleInput, StrInput
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# =============================================================================
# Tool Arguments Schema
# =============================================================================


class DeleteMemoryArgs(BaseModel):
    """Arguments for the delete_memory tool."""

    memory_id: str = Field(
        ...,
        description="The ID of the memory to delete. Get this from search or list results.",
    )


# =============================================================================
# Component
# =============================================================================


class MemoryDeleteComponent(Component):
    """Memory Delete Component - Delete a specific memory.

    This component provides a single tool for deleting a specific
    memory by its ID. This action is irreversible.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        delete_memory(memory_id="abc123")
    """

    display_name = "Memory Delete"
    description = "Delete a specific memory by ID. This action is irreversible."
    icon = "trash"
    name = "MemoryDeleteComponent"
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

    async def delete_memory(self, memory_id: str) -> str:
        """Delete a specific memory by its ID."""
        ctx = self._get_memory_context()

        logger.info("Deleting memory %r for user %r", memory_id, ctx.user_id)

        try:
            ctx.memory.delete(memory_id=memory_id)

            logger.info("Successfully deleted memory %r", memory_id)

        except Exception as e:
            logger.exception("Error deleting memory")
            return f"Error deleting memory: {e!s}"
        else:
            return f"Successfully deleted memory with ID: {memory_id}"

    async def _get_tools(self) -> list:
        """Return the delete_memory tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Delete Memory"):
            return []

        return [
            StructuredTool(
                name="delete_memory",
                description=(
                    "Delete a specific memory by its ID. This action is irreversible. "
                    "Use this when a memory is no longer needed or contains incorrect "
                    "information. Requires the memory_id from search or list results."
                ),
                coroutine=self.delete_memory,
                args_schema=DeleteMemoryArgs,
                tags=["memory", "delete"],
            ),
        ]
