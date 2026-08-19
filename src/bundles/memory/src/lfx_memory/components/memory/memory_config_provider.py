"""Memory Config Provider Component - Entry point for Memory tool components.

This is a FULLY SELF-CONTAINED component. No cross-imports required.
Copy this entire file as a single Langflow component.

This component accepts JSON configuration directly from the user,
creates a Mem0 Memory instance, and outputs a MemoryContext dict
that can be connected to all Memory tool components.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from lfx.custom.custom_component.component import Component
from lfx.io import MultiselectInput, NestedDictInput, Output, StrInput
from lfx.schema.data import Data
from mem0 import Memory
from mem0.configs.base import MemoryConfig

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration Classes (self-contained)
# =============================================================================


@dataclass
class SubscriptionConfig:
    """Validated subscription configuration for Mem0."""

    subscription_id: str
    llm_config: dict[str, Any]
    embedding_config: dict[str, Any]
    vectordb_config: dict[str, Any]
    history_db_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "llm_config": self.llm_config,
            "embedding_config": self.embedding_config,
            "vectordb_config": self.vectordb_config,
            "history_db_path": self.history_db_path,
        }


def validate_config(
    *,
    subscription_id: str,
    llm_config: dict[str, Any],
    embedding_config: dict[str, Any],
    vectordb_config: dict[str, Any],
    history_db_path: str,
) -> SubscriptionConfig:
    """Validate and create a SubscriptionConfig from JSON inputs."""
    errors: list[str] = []

    if not subscription_id or not str(subscription_id).strip():
        errors.append("subscription_id is required and cannot be empty.")

    if not isinstance(llm_config, dict) or not llm_config:
        errors.append("llm_config must be a non-empty dictionary.")
    elif "provider" not in llm_config:
        errors.append("llm_config must contain 'provider' key.")
    elif "config" not in llm_config:
        errors.append("llm_config must contain 'config' key.")

    if not isinstance(embedding_config, dict) or not embedding_config:
        errors.append("embedding_config must be a non-empty dictionary.")
    elif "provider" not in embedding_config:
        errors.append("embedding_config must contain 'provider' key.")
    elif "config" not in embedding_config:
        errors.append("embedding_config must contain 'config' key.")

    if not isinstance(vectordb_config, dict) or not vectordb_config:
        errors.append("vectordb_config must be a non-empty dictionary.")
    elif "provider" not in vectordb_config:
        errors.append("vectordb_config must contain 'provider' key.")
    elif "config" not in vectordb_config:
        errors.append("vectordb_config must contain 'config' key.")

    if not history_db_path or not str(history_db_path).strip():
        errors.append("history_db_path is required and cannot be empty.")

    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(errors))

    return SubscriptionConfig(
        subscription_id=str(subscription_id).strip(),
        llm_config=llm_config,
        embedding_config=embedding_config,
        vectordb_config=vectordb_config,
        history_db_path=str(history_db_path).strip(),
    )


# =============================================================================
# Memory Context (self-contained)
# =============================================================================


@dataclass
class MemoryContext:
    """Shared context passed between Memory components."""

    user_id: str
    subscription_id: str
    memory: Memory
    config: SubscriptionConfig
    enabled_tools: list[str] = field(default_factory=list)
    _created_at: str = field(default="", repr=False)

    def __post_init__(self):
        if not self.user_id or not str(self.user_id).strip():
            message = "user_id is required and cannot be empty"
            raise ValueError(message)
        if not self.subscription_id or not str(self.subscription_id).strip():
            message = "subscription_id is required and cannot be empty"
            raise ValueError(message)
        if self.memory is None:
            message = "memory instance is required"
            raise ValueError(message)
        if self.config is None:
            message = "config is required"
            raise ValueError(message)
        if not self.enabled_tools:
            message = "At least one tool must be enabled"
            raise ValueError(message)
        self._created_at = datetime.now(UTC).isoformat()

    def is_tool_enabled(self, tool_name: str) -> bool:
        """Check if a specific tool is enabled by display name."""
        return tool_name in self.enabled_tools

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "subscription_id": self.subscription_id,
            "llm_provider": self.config.llm_config.get("provider", "unknown"),
            "embedding_provider": self.config.embedding_config.get("provider", "unknown"),
            "vectordb_provider": self.config.vectordb_config.get("provider", "unknown"),
            "history_db_path": self.config.history_db_path,
            "enabled_tools": self.enabled_tools,
            "created_at": self._created_at,
        }


# Global cache for Memory instances
_memory_cache: dict[str, Memory] = {}


def get_or_create_memory(subscription_id: str, config: SubscriptionConfig) -> Memory:
    """Get cached Memory instance or create a new one."""
    if subscription_id in _memory_cache:
        logger.debug("Returning cached Memory instance for subscription %r", subscription_id)
        return _memory_cache[subscription_id]

    logger.info("Creating new Memory instance for subscription %r", subscription_id)

    memory = Memory(
        config=MemoryConfig(
            vector_store=config.vectordb_config,
            llm=config.llm_config,
            embedder=config.embedding_config,
            history_db_path=config.history_db_path,
        )
    )

    _memory_cache[subscription_id] = memory
    return memory


# =============================================================================
# Component
# =============================================================================


class MemoryConfigProvider(Component):
    """Memory Configuration Provider - Entry point for Memory components.

    This component:
    1. Accepts user_id, subscription_id, and configuration JSONs as inputs
    2. Validates all configurations
    3. Creates a shared Mem0 Memory instance
    4. Outputs MemoryContext for downstream tool components

    Connect the "Memory Context" output to all Memory tool components.
    """

    display_name = "Memory Config Provider"
    description = (
        "Accepts memory configuration and creates shared Memory instance. Connect output to all Memory tool components."
    )
    icon = "settings"
    name = "MemoryConfigProvider"

    inputs = [
        StrInput(
            name="user_id",
            display_name="User ID",
            info="User identifier. All memory operations will be scoped to this user.",
            required=True,
            value="",
        ),
        StrInput(
            name="subscription_id",
            display_name="Subscription ID",
            info="Subscription identifier. Used for organizing configs and history DB path.",
            required=True,
            value="",
        ),
        NestedDictInput(
            name="llm_config",
            display_name="LLM Config",
            info='LLM configuration JSON. Required keys: "provider", "config".',
            required=True,
            value={},
        ),
        NestedDictInput(
            name="embedding_config",
            display_name="Embedding Config",
            info='Embedding configuration JSON. Required keys: "provider", "config".',
            required=True,
            value={},
        ),
        NestedDictInput(
            name="vectordb_config",
            display_name="Vector DB Config",
            info='Vector database configuration JSON. Required keys: "provider", "config".',
            required=True,
            value={},
        ),
        StrInput(
            name="history_db_path",
            display_name="History DB Path",
            info="Path to SQLite history database. Example: /mem0/history_db/subscription_id.db",
            required=True,
            value="",
        ),
        MultiselectInput(
            name="memory_enabled_tools",
            display_name="Enabled Tools",
            info="Select which memory tools to expose to the agent. At least one tool must be enabled.",
            options=[
                "Search Memory",
                "Add Memory",
                "List All Memories",
                "Update Memory",
                "Delete Memory",
                "Delete All Memories",
                "Memory History",
            ],
            value=[
                "Search Memory",
                "Add Memory",
                "List All Memories",
                "Update Memory",
                "Delete Memory",
                "Delete All Memories",
                "Memory History",
            ],
            advanced=True,
        ),
    ]

    outputs = [
        Output(
            display_name="Memory Context",
            name="memory_context",
            method="build_memory_context",
            types=["MemoryContext"],
            cache=True,
        ),
        Output(
            display_name="Config Status",
            name="config_status",
            method="get_config_status",
        ),
    ]

    def _check_required_inputs(self) -> None:
        errors: list[str] = []
        if not self.user_id or not str(self.user_id).strip():
            errors.append("user_id is required and cannot be empty.")
        if not self.subscription_id or not str(self.subscription_id).strip():
            errors.append("subscription_id is required and cannot be empty.")
        if not self.memory_enabled_tools or len(self.memory_enabled_tools) == 0:
            errors.append("enabled_tools: At least one tool must be enabled.")
        if errors:
            raise ValueError("Input validation failed:\n" + "\n".join(errors))

    def build_memory_context(self) -> MemoryContext:
        """Build and return MemoryContext with shared Memory instance."""
        self._check_required_inputs()

        user_id = str(self.user_id).strip()
        subscription_id = str(self.subscription_id).strip()

        logger.info("Building MemoryContext for user %r, subscription %r", user_id, subscription_id)

        config = validate_config(
            subscription_id=subscription_id,
            llm_config=self.llm_config or {},
            embedding_config=self.embedding_config or {},
            vectordb_config=self.vectordb_config or {},
            history_db_path=self.history_db_path or "",
        )

        memory = get_or_create_memory(subscription_id, config)

        ctx = MemoryContext(
            user_id=user_id,
            subscription_id=subscription_id,
            memory=memory,
            config=config,
            enabled_tools=self.memory_enabled_tools or [],
        )

        logger.info("MemoryContext created successfully: %s", ctx.to_dict())
        return ctx

    def get_config_status(self) -> Data:
        """Return configuration status for debugging/monitoring."""
        try:
            self._check_required_inputs()

            user_id = str(self.user_id).strip()
            subscription_id = str(self.subscription_id).strip()

            config = validate_config(
                subscription_id=subscription_id,
                llm_config=self.llm_config or {},
                embedding_config=self.embedding_config or {},
                vectordb_config=self.vectordb_config or {},
                history_db_path=self.history_db_path or "",
            )

            return Data(
                data={
                    "status": "configured",
                    "user_id": user_id,
                    "subscription_id": subscription_id,
                    "history_db_path": config.history_db_path,
                    "llm_provider": config.llm_config.get("provider", "unknown"),
                    "embedding_provider": config.embedding_config.get("provider", "unknown"),
                    "vectordb_provider": config.vectordb_config.get("provider", "unknown"),
                    "enabled_tools": self.memory_enabled_tools or [],
                }
            )
        except (TypeError, ValueError) as e:
            return Data(data={"status": "error", "error": str(e)})
