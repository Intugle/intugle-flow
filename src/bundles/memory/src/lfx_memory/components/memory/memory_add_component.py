"""Memory Add Component - Store new memories.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: add_memory
Args:
    - content (str): The memory content to store
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


class AddMemoryArgs(BaseModel):
    """Arguments for the add_memory tool."""

    content: str = Field(
        ...,
        description="The memory content to store. Can be facts, preferences, or any information to remember.",
    )


# =============================================================================
# Component
# =============================================================================


class MemoryAddComponent(Component):
    """Memory Add Component - Store new memories.

    This component provides a single tool for storing new memories.
    The content will be embedded and indexed for later retrieval
    via semantic search.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        add_memory(content="User prefers dark mode and uses Python")
    """

    display_name = "Memory Add"
    description = "Store new memories. Content will be embedded and indexed for later retrieval."
    icon = "plus"
    name = "MemoryAddComponent"
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

    async def add_memory(self, content: str) -> str:
        """Store a new memory."""
        ctx = self._get_memory_context()

        logger.info("Adding memory for user %r: %r...", ctx.user_id, content[:50])

        try:
            result = ctx.memory.add(
                content,
                user_id=ctx.user_id,
                metadata={},
            )

            rows = result.get("results", []) if isinstance(result, dict) else result or []

            count = len(rows) if rows else 1

            logger.info("Successfully stored %d memory item(s) for user %r", count, ctx.user_id)

        except Exception as e:
            logger.exception("Error adding memory")
            return f"Error adding memory: {e!s}"
        else:
            return f"Successfully stored {count} memory item(s)."

    async def _get_tools(self) -> list:
        """Return the add_memory tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Add Memory"):
            return []

        return [
            StructuredTool(
                name="add_memory",
                description=(
                    "Store a new memory. The content will be embedded and indexed for "
                    "later retrieval via search. Use this to remember important information "
                    "about the user, their preferences, or key facts from the conversation."
                ),
                coroutine=self.add_memory,
                args_schema=AddMemoryArgs,
                tags=["memory", "add"],
            ),
        ]
