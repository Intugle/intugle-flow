"""Unit tests for Composio components cloud validation."""

import os
from unittest.mock import MagicMock, patch

import pytest
from lfx.base.composio.composio_base import ComposioBaseComponent
from lfx.inputs.inputs import DropdownInput, StrInput
from lfx.schema.data import Data
from lfx.schema.message import Message
from lfx_bundles.composio.composio_api import ComposioAPIComponent
from lfx_bundles.composio.outlook_composio import ComposioOutlookAPIComponent


@pytest.mark.unit
class TestComposioCloudValidation:
    """Test Composio components cloud validation."""

    def test_composio_api_disabled_in_astra_cloud(self):
        """Test that ComposioAPI build_tool raises error in Astra Cloud."""
        with patch.dict(os.environ, {"ASTRA_CLOUD_DISABLE_COMPONENT": "true"}):
            component = ComposioAPIComponent(api_key="test-key")

            with pytest.raises(ValueError, match=r".*") as exc_info:
                component.build_tool()

            error_msg = str(exc_info.value).lower()
            assert "astra" in error_msg or "cloud" in error_msg

    def test_composio_base_execute_disabled_in_astra_cloud(self):
        """Test that ComposioBase execute_action raises error in Astra Cloud."""
        with patch.dict(os.environ, {"ASTRA_CLOUD_DISABLE_COMPONENT": "false"}):
            component = ComposioBaseComponent(api_key="test-key")

        with patch.dict(os.environ, {"ASTRA_CLOUD_DISABLE_COMPONENT": "true"}):
            with pytest.raises(ValueError, match=r".*") as exc_info:
                component.execute_action()

            error_msg = str(exc_info.value).lower()
            assert "astra" in error_msg or "cloud" in error_msg


def _make_component(action_key: str, fields: dict) -> ComposioOutlookAPIComponent:
    """Build a ComposioOutlookAPIComponent pre-wired with test data, bypassing real API calls."""
    with patch.dict(os.environ, {"ASTRA_CLOUD_DISABLE_COMPONENT": "false"}):
        component = ComposioOutlookAPIComponent(api_key="test-key")

    component.entity_id = "default"
    component.action_button = [{"name": "Send Email"}]

    component._actions_data = {
        action_key: {
            "display_name": "Send Email",
            "action_fields": list(fields.keys()),
            "version": None,
        }
    }
    component._action_schemas = {
        action_key: {
            "input_parameters": {
                "type": "object",
                "properties": {k: {"type": "string"} for k in fields},
                "required": list(fields.keys()),
            }
        }
    }
    component._display_to_key_map = {"Send Email": action_key}
    component._key_to_display_map = {action_key: "Send Email"}

    for name, value in fields.items():
        setattr(component, name, value)

    return component


@pytest.mark.unit
class TestExecuteActionRichTypeCoercion:
    """Regression: Message and Data objects must be coerced to primitives before being passed to the Composio API.

    When a ChatInput node is wired to a str field (e.g. subject, body), Langflow
    stores a Message object in the component attribute.  execute_action previously
    forwarded the raw object to composio.tools.execute, which caused the API call
    to fail or send a stringified object instead of plain text.
    """

    ACTION_KEY = "OUTLOOK_SEND_EMAIL"

    def _run(self, fields: dict) -> dict:
        """Execute the action and return the captured arguments dict."""
        component = _make_component(self.ACTION_KEY, fields)

        captured = {}

        def fake_execute(**kwargs):
            captured.update(kwargs.get("arguments", {}))
            return {"successful": True, "data": {"message": "sent"}}

        mock_composio = MagicMock()
        mock_composio.tools.execute.side_effect = fake_execute

        with (
            patch.object(type(component), "_build_wrapper", return_value=mock_composio),
            patch.object(type(component), "_populate_actions_data"),
            patch.dict(os.environ, {"ASTRA_CLOUD_DISABLE_COMPONENT": "false"}),
        ):
            component.execute_action()

        return captured

    def test_message_coerced_to_text_for_str_field(self):
        args = self._run({"subject": Message(text="Hello world"), "body": "body text"})
        assert args["subject"] == "Hello world"

    def test_data_coerced_to_dict_for_object_field(self):
        payload = {"key": "value"}
        args = self._run({"subject": "hi", "body": Data(data=payload)})
        assert args["body"] == payload

    def test_plain_string_passed_through_unchanged(self):
        args = self._run({"subject": "plain subject", "body": "plain body"})
        assert args["subject"] == "plain subject"
        assert args["body"] == "plain body"

    def test_message_with_empty_text_is_skipped(self):
        args = self._run({"subject": Message(text=""), "body": "body text"})
        assert "subject" not in args

    def test_multiple_message_fields_all_coerced(self):
        args = self._run(
            {
                "subject": Message(text="Subject line"),
                "body": Message(text="Body content"),
            }
        )
        assert args["subject"] == "Subject line"
        assert args["body"] == "Body content"

    def test_none_field_is_skipped(self):
        args = self._run({"subject": "hi", "body": None})
        assert "body" not in args

    def test_message_coercion_happens_before_json_parse(self):
        # body contains JSON-like text — should be passed as a string (schema type is str)
        args = self._run({"subject": "hi", "body": Message(text='{"key": "val"}')})
        assert args["body"] == '{"key": "val"}'


@pytest.mark.unit
class TestComposioBuildConfigHydration:
    """Regression coverage for restoring saved dedicated Composio component state."""

    @staticmethod
    def _component() -> ComposioBaseComponent:
        component = ComposioBaseComponent(api_key="saved-key")
        component.app_name = "gmail"
        component._actions_data = {
            "GMAIL_SEND_EMAIL": {
                "display_name": "Send Email",
                "action_fields": ["subject"],
            }
        }
        component._display_to_key_map = {"Send Email": "GMAIL_SEND_EMAIL"}
        component._key_to_display_map = {"GMAIL_SEND_EMAIL": "Send Email"}
        return component

    @staticmethod
    def _build_config() -> dict:
        return {
            "api_key": {"value": "saved-key"},
            "auth_link": {
                "connection_id": "existing-connection",
                "value": "validated",
                "auth_scheme": "OAUTH2",
            },
            "auth_mode": {"value": "OAUTH2", "show": True},
            "action_button": {
                "value": [{"name": "Send Email"}],
                "options": [],
                "show": True,
            },
            "subject": {"value": "Saved subject", "show": True},
        }

    def test_api_key_hydration_preserves_connection_and_action(self):
        component = self._component()
        build_config = self._build_config()

        with (
            patch.object(component, "_get_toolkit_schema", return_value={}),
            patch.object(component, "_render_auth_mode_dropdown"),
            patch.object(component, "_restore_selected_action_config") as restore_action,
            patch.object(component, "_check_connection_status_by_id", return_value="ACTIVE"),
            patch.object(component, "_get_connection_auth_info", return_value=("OAUTH2", True)),
        ):
            component.update_build_config(build_config, "saved-key", "api_key")

        assert build_config["auth_link"]["connection_id"] == "existing-connection"
        assert build_config["auth_link"]["value"] == "validated"
        assert build_config["auth_mode"]["value"] == "OAUTH2"
        assert build_config["action_button"]["value"] == [{"name": "Send Email"}]
        restore_action.assert_called_once_with(build_config)

    def test_api_key_change_invalidates_connection(self):
        component = self._component()
        build_config = self._build_config()

        with (
            patch.object(component, "_get_toolkit_schema", return_value={}),
            patch.object(component, "_render_auth_mode_dropdown"),
            patch.object(component, "_restore_selected_action_config"),
            patch.object(component, "_find_active_connection_for_app", return_value=None),
        ):
            component.update_build_config(build_config, "new-key", "api_key")

        assert "connection_id" not in build_config["auth_link"]
        assert build_config["auth_link"]["value"] == "connect"

    def test_restore_selected_action_preserves_dynamic_field_values(self):
        component = self._component()
        build_config = self._build_config()
        build_config["action_button"]["options"] = [{"name": "Send Email"}]

        with patch.object(
            component,
            "_validate_schema_inputs",
            return_value=[StrInput(name="subject", display_name="Subject", value="")],
        ):
            component._restore_selected_action_config(build_config)

        assert build_config["subject"]["value"] == "Saved subject"
        assert build_config["subject"]["show"] is True

    def test_restore_selected_action_preserves_shared_dynamic_field_values(self):
        component = self._component()
        component._actions_data["GMAIL_SEND_EMAIL"]["action_fields"].append("format")
        component._actions_data["GMAIL_CREATE_DRAFT"] = {
            "display_name": "Create Draft",
            "action_fields": ["format"],
        }
        component._display_to_key_map["Create Draft"] = "GMAIL_CREATE_DRAFT"
        component._key_to_display_map["GMAIL_CREATE_DRAFT"] = "Create Draft"

        build_config = self._build_config()
        build_config["action_button"]["options"] = [{"name": "Send Email"}, {"name": "Create Draft"}]
        build_config["format"] = {"value": "html", "show": True}

        def action_inputs(_action_key: str):
            return [DropdownInput(name="format", display_name="Format", options=["text", "html"], value="text")]

        with patch.object(component, "_validate_schema_inputs", side_effect=action_inputs):
            component._restore_selected_action_config(build_config)

        assert build_config["format"]["value"] == "html"
        assert build_config["format"]["show"] is True

    def test_restore_selected_action_keeps_complete_optional_field_configuration(self):
        component = self._component()
        component._actions_data["GMAIL_SEND_EMAIL"]["action_fields"].append("format")
        component._all_fields = {"subject", "format"}

        build_config = self._build_config()
        build_config["action_button"]["options"] = [{"name": "Send Email"}]
        build_config["format"] = {
            "value": "html",
            "options": ["text", "html"],
            "advanced": True,
            "show": True,
        }

        with patch.object(component, "_update_action_config") as update_action_config:
            component._restore_selected_action_config(build_config)

        update_action_config.assert_not_called()
        assert build_config["format"]["value"] == "html"
        assert build_config["format"]["options"] == ["text", "html"]
