"""Memory Update Component - Update existing memories.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: update_memory
Args:
    - memory_id (str): ID of the memory to update
    - content (str): New content for the memory
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


class UpdateMemoryArgs(BaseModel):
    """Arguments for the update_memory tool."""

    memory_id: str = Field(
        ...,
        description="The ID of the memory to update. Get this from search or list results.",
    )
    content: str = Field(
        ...,
        description="The new content for the memory. This will replace the existing content.",
    )


# =============================================================================
# Component
# =============================================================================


class MemoryUpdateComponent(Component):
    """Memory Update Component - Update existing memories.

    This component provides a single tool for updating the content
    of an existing memory. The old version is preserved in history.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        update_memory(memory_id="abc123", content="Updated preference information")
    """

    display_name = "Memory Update"
    description = "Update existing memories. Old versions are preserved in history."
    icon = "edit"
    name = "MemoryUpdateComponent"
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

    async def update_memory(self, memory_id: str, content: str) -> str:
        """Update the content of an existing memory."""
        ctx = self._get_memory_context()

        logger.info("Updating memory %r for user %r: %r...", memory_id, ctx.user_id, content[:50])

        try:
            ctx.memory.update(memory_id=memory_id, data=content)

            logger.info("Successfully updated memory %r", memory_id)

        except Exception as e:
            logger.exception("Error updating memory")
            return f"Error updating memory: {e!s}"
        else:
            return f"Successfully updated memory with ID: {memory_id}"

    async def _get_tools(self) -> list:
        """Return the update_memory tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Update Memory"):
            return []

        return [
            StructuredTool(
                name="update_memory",
                description=(
                    "Update the content of an existing memory. The old version is "
                    "preserved in history. Use this when information needs to be "
                    "corrected or updated. Requires the memory_id from search or list results."
                ),
                coroutine=self.update_memory,
                args_schema=UpdateMemoryArgs,
                tags=["memory", "update"],
            ),
        ]
