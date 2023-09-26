"""Utility functions for working with Meraki."""
import meraki


class DashboardClient:
    """Client for interacting with Meraki dashboard."""

    def __init__(self, logger, org_id: str, token: str, *args, **kwargs):
        """Initialize Meraki dashboard client."""
        self.logger = logger
        self.org_id = org_id
        self.token = token
        self.conn = self.connect_dashboard()
        self.network_map = {}

    def connect_dashboard(self):  # pylint: disable=inconsistent-return-statements
        """Connect to Meraki dashboard and return connection object."""
        try:
            dashboard = meraki.DashboardAPI(
                api_key=self.token,
                base_url="https://api.meraki.com/api/v1/",
                output_log=False,
                print_console=False,
            )
            return dashboard
        except meraki.APIError as err:
            self.logger.log_failure(f"Unable to connect to Meraki dashboard: {err.message}")

    def validate_organization_exists(self):
        """Confirm defined organization ID is seen in Dashboard to confirm we have access.

        Returns:
            boolean: Whether Organiztion ID was found in Dashboard.
        """
        orgs = self.conn.organizations.getOrganizations()
        ids = [org["id"] for org in orgs]
        if self.org_id in ids:
            return True
        return False

    def get_org_networks(self):
        """Retrieve all networks for specified Organization ID.

        Returns:
            list: List of found networks. Empty list if error retrieving networks.
        """
        networks = []
        try:
            networks = self.conn.organizations.getOrganizationNetworks(organizationId=self.org_id)
            self.network_map = {net["name"]: net for net in networks}
        except meraki.APIError as err:
            self.logger.log_failure(
                message=f"Meraki API error: {err}\nstatus code = {err.status}\nreason = {err.reason}\nerror = {err.message}"
            )
        return networks

    def get_org_devices(self):
        """Retrieve all devices for specified Organization ID.

        Returns:
            list: List of found devices. Empty list if error retrieving devices.
        """
        devices = []
        try:
            devices = self.conn.organizations.getOrganizationDevices(organizationId=self.org_id)
        except meraki.APIError as err:
            self.logger.log_failure(
                message=f"Meraki API error: {err}\nstatus code = {err.status}\nreason = {err.reason}\nerror = {err.message}"
            )
        return devices

    def get_device_status(self, device_name: str):
        """Retrieve device status from Meraki dashboard.

        Args:
            device_name (str): Name of Device to pull status for.
        """
        status = "dormant"
        try:
            response = self.conn.organizations.getOrganizationDevicesStatuses(organizationId=self.org_id)
            statuses = {dev["name"]: dev["status"] for dev in response}
            if device_name in statuses:
                status = statuses[device_name]
        except meraki.APIError as err:
            self.logger.log_failure(
                message=f"Meraki API error: {err}\nstatus code = {err.status}\nreason = {err.reason}\nerror = {err.message}"
            )
        return status
