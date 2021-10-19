# pylint: disable=no-self-use

from rabbitai.commands.exceptions import CommandInvalidError
from rabbitai.commands.importers.v1.utils import is_valid_config
from tests.integration_tests.base_tests import SupersetTestCase


class TestCommandsExceptions(SupersetTestCase):
    def test_command_invalid_error(self):
        exception = CommandInvalidError("A test")
        assert str(exception) == "A test"


class TestImportersV1Utils(SupersetTestCase):
    def test_is_valid_config(self):
        assert is_valid_config("metadata.yaml")
        assert is_valid_config("databases/examples.yaml")
        assert not is_valid_config(".DS_Store")
        assert not is_valid_config(
            "__MACOSX/chart_export_20210111T145253/databases/._examples.yaml"
        )
