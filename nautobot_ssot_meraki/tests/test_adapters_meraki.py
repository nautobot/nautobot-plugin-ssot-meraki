"""Test Meraki adapter."""

import json
import uuid
from unittest.mock import MagicMock

from django.contrib.contenttypes.models import ContentType
from nautobot.extras.models import Job, JobResult
from nautobot.utilities.testing import TransactionTestCase
from nautobot_ssot_meraki.diffsync.adapters.meraki import MerakiAdapter
from nautobot_ssot_meraki.jobs import MerakiDataSource


def load_json(path):
    """Load a json file."""
    with open(path, encoding="utf-8") as file:
        return json.loads(file.read())


GET_ORG_NETWORKS_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_networks.json")
NETWORK_MAP_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/network_map.json")
GET_ORG_DEVICES_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_devices.json")
GET_DEVICE_STATUSES_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_device_statuses.json")


class TestMerakiAdapterTestCase(TransactionTestCase):
    """Test NautobotSsotMerakiAdapter class."""

    databases = ("default", "job_logs")

    def setUp(self):
        """Initialize test case."""
        self.meraki_client = MagicMock()
        self.meraki_client.get_org_networks.return_value = GET_ORG_NETWORKS_FIXTURE
        self.meraki_client.network_map = NETWORK_MAP_FIXTURE
        self.meraki_client.get_org_devices.return_value = GET_ORG_DEVICES_FIXTURE
        self.meraki_client.get_device_statuses.return_value = GET_DEVICE_STATUSES_FIXTURE

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
            {net["name"] for net in GET_ORG_NETWORKS_FIXTURE},
            {net.get_unique_id() for net in self.meraki.get_all("network")},
        )
        self.assertEqual(
            {dev["name"] for dev in GET_ORG_DEVICES_FIXTURE},
            {dev.get_unique_id() for dev in self.meraki.get_all("device")},
        )
