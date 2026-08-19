"""Memory Search Component - Search memories by semantic similarity.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

Tool: search_memory
Args:
    - query (str): The search query to find relevant memories
    - limit (int): Maximum number of results to return (default: 5)
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


class SearchMemoryArgs(BaseModel):
    """Arguments for the search_memory tool."""

    query: str = Field(
        ...,
        description="The search query to find relevant memories. Use natural language.",
    )
    limit: int = Field(
        default=5,
        gt=0,
        le=100,
        description="Maximum number of results to return (1-100).",
    )


# =============================================================================
# Component
# =============================================================================


class MemorySearchComponent(Component):
    """Memory Search Component - Search memories by semantic similarity.

    This component provides a single tool for searching memories using
    semantic similarity matching. The agent can use this tool to find
    relevant memories based on a natural language query.

    Input:
        - memory_context: Connect from MemoryConfigProvider

    Tool Usage by Agent:
        search_memory(query="user preferences", limit=5)
    """

    display_name = "Memory Search"
    description = "Search memories using semantic similarity. Returns most relevant memories matching the query."
    icon = "search"
    name = "MemorySearchComponent"
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

    async def search_memory(self, query: str, limit: int = 5) -> str:
        """Search memories by semantic similarity."""
        ctx = self._get_memory_context()

        logger.info("Searching memories for user %r with query %r (limit=%d)", ctx.user_id, query, limit)

        try:
            results = ctx.memory.search(
                query=query,
                filters={"user_id": ctx.user_id},
                top_k=limit,
            )

            rows = results.get("results", []) if isinstance(results, dict) else results or []

            if not rows:
                return f"No memories found matching query: '{query}'"

            formatted = []
            for i, row in enumerate(rows, 1):
                memory_text = row.get("memory", row.get("text", str(row)))
                memory_id = row.get("id", "N/A")
                score = row.get("score", "N/A")
                formatted.append(f"{i}. [ID: {memory_id}] (score: {score}): {memory_text}")

            return f"Found {len(rows)} memories:\n" + "\n".join(formatted)

        except Exception as e:
            logger.exception("Error searching memories")
            return f"Error searching memories: {e!s}"

    async def _get_tools(self) -> list:
        """Return the search_memory tool for the agent. Respects enabled_tools from config."""
        ctx = self._get_memory_context()

        # Check if this tool is enabled in the config provider
        if hasattr(ctx, "is_tool_enabled") and not ctx.is_tool_enabled("Search Memory"):
            return []

        return [
            StructuredTool(
                name="search_memory",
                description=(
                    "Search memories by semantic similarity. Returns the most relevant "
                    "memories matching the query. Use this to find information the user "
                    "has shared previously or to recall past conversations."
                ),
                coroutine=self.search_memory,
                args_schema=SearchMemoryArgs,
                tags=["memory", "search"],
            ),
        ]
