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


SITE_FIXTURE = []


class TestMerakiAdapterTestCase(TransactionTestCase):
    """Test NautobotSsotMerakiAdapter class."""

    databases = ("default", "job_logs")

    def setUp(self):
        """Initialize test case."""
        self.meraki_client = MagicMock()
        self.meraki_client.get_sites.return_value = SITE_FIXTURE

        self.job = MerakiDataSource()
        self.job.job_result = JobResult.objects.create(
            name=self.job.class_path, obj_type=ContentType.objects.get_for_model(Job), user=None, job_id=uuid.uuid4()
        )
        self.meraki = MerakiAdapter(job=self.job, sync=None, client=self.meraki_client)

    def test_data_loading(self):
        """Test Nautobot SSoT for Meraki load() function."""
        # self.meraki.load()
        # self.assertEqual(
        #     {site["name"] for site in SITE_FIXTURE},
        #     {site.get_unique_id() for site in self.meraki.get_all("site")},
        # )
