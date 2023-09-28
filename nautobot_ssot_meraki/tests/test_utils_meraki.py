"""Unit tests for Meraki utility functions."""
from unittest import TestCase
from unittest.mock import MagicMock, patch
import meraki
from nautobot_ssot_meraki.utils.meraki import DashboardClient


class TestDashboardClient(TestCase):
    """Unit tests for the DashboardClient class."""

    @patch("meraki.DashboardAPI")
    def test_successful_connection(self, mock_api):
        """Test successful connection to Meraki dashboard with valid API key and base URL."""
        logger = MagicMock()
        org_id = "12345"
        token = "valid_token"  # nosec: B105
        dashboard_client = DashboardClient(logger, org_id, token)

        mock_api.assert_called_once_with(
            api_key=token, base_url="https://api.meraki.com/api/v1/", output_log=False, print_console=False
        )

        self.assertIsNotNone(dashboard_client.conn)
        self.assertEqual(dashboard_client.logger, logger)
        self.assertEqual(dashboard_client.org_id, org_id)
        self.assertEqual(dashboard_client.token, token)

    @patch("meraki.DashboardAPI")
    def test_invalid_api_key(self, mock_api):
        """Test that an Raises an exception of type 'meraki.APIError' if API key is invalid or missing."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.reason = "Invalid API key"
        mock_api.side_effect = meraki.APIError(
            metadata={"operation": "GET", "tags": ["Failed"]}, response=mock_response
        )

        logger = MagicMock()
        org_id = "12345"
        token = "invalid_token"  # nosec: B105

        with self.assertRaises(meraki.APIError):
            DashboardClient(logger, org_id, token)
