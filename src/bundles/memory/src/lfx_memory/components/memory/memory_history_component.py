"""Memory History Component - Get change history of a memory.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: memory_history
Args:
    - memory_id (str): ID of the memory to get history for
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


class MemoryHistoryArgs(BaseModel):
    """Arguments for the memory_history tool."""

    memory_id: str = Field(
        ...,
        description="The ID of the memory to get history for. Get this from search or list results.",
    )


# =============================================================================
# Component
# =============================================================================


class MemoryHistoryComponent(Component):
    """Memory History Component - Get change history of a memory.

    This component provides a single tool for retrieving the change
    history of a specific memory, showing all previous versions and
    modifications.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        memory_history(memory_id="abc123")
    """

    display_name = "Memory History"
    description = "Get change history of a memory, showing all previous versions."
    icon = "clock"
    name = "MemoryHistoryComponent"
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

    async def memory_history(self, memory_id: str) -> str:
        """Get the change history of a specific memory."""
        ctx = self._get_memory_context()

        logger.info("Getting history for memory %r", memory_id)

        try:
            history = ctx.memory.history(memory_id=memory_id)

            if not history:
                return f"No history found for memory ID: {memory_id}"

            formatted = []
            for i, entry in enumerate(history, 1):
                event = entry.get("event", "N/A")
                timestamp = entry.get("timestamp", "N/A")
                old_value = entry.get("old_memory", entry.get("prev_value", "N/A"))
                new_value = entry.get("new_memory", entry.get("new_value", "N/A"))

                formatted.append(f"{i}. [{timestamp}] {event}:\n   Old: {old_value}\n   New: {new_value}")

            logger.info("Found %d history entries for memory %r", len(history), memory_id)
            return f"History for memory {memory_id}:\n\n" + "\n\n".join(formatted)

        except Exception as e:
            logger.exception("Error fetching memory history")
            return f"Error fetching memory history: {e!s}"

    async def _get_tools(self) -> list:
        """Return the memory_history tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Memory History"):
            return []

        return [
            StructuredTool(
                name="memory_history",
                description=(
                    "Get the change history of a specific memory, showing all previous "
                    "versions and modifications. Use this to see how a memory has evolved "
                    "over time. Requires the memory_id from search or list results."
                ),
                coroutine=self.memory_history,
                args_schema=MemoryHistoryArgs,
                tags=["memory", "history"],
            ),
        ]
