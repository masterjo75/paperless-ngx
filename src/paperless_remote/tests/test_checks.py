from django.test import TestCase
from django.test import override_settings

from paperless_remote import check_remote_parser_configured


class TestChecks(TestCase):
    @override_settings(REMOTE_PARSER_ENGINE=None)
    def test_no_engine(self):
        msgs = check_remote_parser_configured(None)
        self.assertEqual(len(msgs), 0)

    @override_settings(REMOTE_PARSER_ENGINE="something")
    @override_settings(REMOTE_PARSER_API_KEY=None)
    def test_no_api_key(self):
        msgs = check_remote_parser_configured(None)
        self.assertEqual(len(msgs), 1)
        self.assertTrue(
            msgs[0].msg.startswith(
                "No remote engine API key is configured.",
            ),
        )

    @override_settings(REMOTE_PARSER_ENGINE="azureaivision")
    @override_settings(REMOTE_PARSER_API_KEY="somekey")
    @override_settings(REMOTE_PARSER_ENDPOINT=None)
    def test_azure_no_endpoint(self):
        msgs = check_remote_parser_configured(None)
        self.assertEqual(len(msgs), 1)
        self.assertTrue(
            msgs[0].msg.startswith(
                "Azure remote parser requires endpoint to be configured.",
            ),
        )

    @override_settings(REMOTE_PARSER_ENGINE="something")
    @override_settings(REMOTE_PARSER_API_KEY="somekey")
    def test_valid_configuration(self):
        msgs = check_remote_parser_configured(None)
        self.assertEqual(len(msgs), 0)
