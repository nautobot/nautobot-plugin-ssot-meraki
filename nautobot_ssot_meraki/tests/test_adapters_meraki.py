"""Test Meraki adapter."""
import uuid
from unittest.mock import MagicMock

from django.contrib.contenttypes.models import ContentType
from nautobot.extras.models import Job, JobResult
from nautobot.utilities.testing import TransactionTestCase
from nautobot_ssot_meraki.diffsync.adapters.meraki import MerakiAdapter
from nautobot_ssot_meraki.jobs import MerakiDataSource
from nautobot_ssot_meraki.tests.fixtures import fixtures as fix


class TestMerakiAdapterTestCase(TransactionTestCase):
    """Test NautobotSsotMerakiAdapter class."""

    databases = ("default", "job_logs")

    def setUp(self):
        """Initialize test case."""
        self.meraki_client = MagicMock()
        self.meraki_client.get_org_networks.return_value = fix.GET_ORG_NETWORKS_SENT_FIXTURE
        self.meraki_client.network_map = fix.NETWORK_MAP_FIXTURE
        self.meraki_client.get_org_devices.return_value = fix.GET_ORG_DEVICES_FIXTURE
        self.meraki_client.get_device_statuses.return_value = fix.GET_DEVICE_STATUSES_FIXTURE
        self.meraki_client.get_management_port_names.return_value = fix.GET_MANAGEMENT_PORT_NAMES_RECV_FIXTURE
        self.meraki_client.get_uplink_settings.return_value = fix.GET_UPLINK_SETTINGS_RECV
        self.meraki_client.get_switchport_statuses.return_value = fix.GET_SWITCHPORT_STATUSES
        self.meraki_client.get_org_uplink_statuses.return_value = fix.GET_ORG_UPLINK_STATUSES_RECV_FIXTURE

        self.job = MerakiDataSource()
        self.job.job_result = JobResult.objects.create(
            name=self.job.class_path, obj_type=ContentType.objects.get_for_model(Job), user=None, job_id=uuid.uuid4()
        )
        self.meraki = MerakiAdapter(job=self.job, sync=None, client=self.meraki_client)

    def test_data_loading(self):
        """Test Nautobot SSoT for Meraki load() function."""
        self.meraki_client.validate_organization_exists.return_value = True
        self.meraki.load()
        self.assertEqual(
            {net["name"] for net in fix.GET_ORG_NETWORKS_SENT_FIXTURE},
            {net.get_unique_id() for net in self.meraki.get_all("network")},
        )
        self.assertEqual(
            {dev["name"] for dev in fix.GET_ORG_DEVICES_FIXTURE},
            {dev.get_unique_id() for dev in self.meraki.get_all("device")},
        )
        wan1_ports = [f"wan1__{dev['name']}" for dev in fix.GET_ORG_DEVICES_FIXTURE]
        wan2_ports = [f"wan2__{dev['name']}" for dev in fix.GET_ORG_DEVICES_FIXTURE]
        expected_ports = set(wan1_ports + wan2_ports)
        self.assertEqual(expected_ports, {port.get_unique_id() for port in self.meraki.get_all("port")})
