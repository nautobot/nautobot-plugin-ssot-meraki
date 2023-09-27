"""Unit tests for the Nautobot DiffSync adapter."""
import uuid
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceType, DeviceRole, Manufacturer, Site
from nautobot.extras.models import Job, JobResult, Note, Status
from nautobot.utilities.testing import TransactionTestCase

from nautobot_ssot_meraki.diffsync.adapters.nautobot import NautobotAdapter
from nautobot_ssot_meraki.jobs import MerakiDataSource

User = get_user_model()


class NautobotDiffSyncTestCase(TransactionTestCase):
    """Test the NautobotAdapter class."""

    databases = ("default", "job_logs")

    def __init__(self, *args, **kwargs):
        """Initialize shared variables."""
        super().__init__(*args, **kwargs)

    def setUp(self):  # pylint: disable=too-many-locals
        """Per-test-case data setup."""
        super().setUp()
        self.status_active = Status.objects.get(name="Active")

        job = MerakiDataSource()
        job.job_result = JobResult.objects.create(
            name=job.class_path, obj_type=ContentType.objects.get_for_model(Job), user=None, job_id=uuid.uuid4()
        )
        self.nb_adapter = NautobotAdapter(job=job, sync=None)
        self.nb_adapter.job = MagicMock()
        self.nb_adapter.job.log_info = MagicMock()
        self.nb_adapter.job.log_warning = MagicMock()

        site1 = Site.objects.create(
            name="Lab",
            status=self.status_active,
            time_zone="America/Chicago",
        )
        site1.validated_save()
        site1.tags.set(["Test"])
        site1.validated_save()
        new_note = Note.objects.create(
            note="Test",
            user=User.objects.first(),
            assigned_object_type=ContentType.objects.get_for_model(Site),
            assigned_object_id=site1.id,
        )
        new_note.validated_save()

        cisco_manu = Manufacturer.objects.create(name="Cisco", slug="cisco")
        cisco_manu.validated_save()

        asr1k = DeviceType.objects.create(model="ASR1000", manufacturer=cisco_manu)
        asr1k.validated_save()

        core_role = DeviceRole.objects.get_or_create(name="CORE")[0]

        lab01 = Device.objects.create(
            name="Lab01",
            serial="ABC-123-456",
            status=self.status_active,
            device_role=core_role,
            device_type=asr1k,
            site=site1,
        )
        lab01.validated_save()

    def test_data_loading(self):
        """Test the load() function."""
        self.nb_adapter.load()
        self.assertEqual(
            {site.name for site in Site.objects.all()},
            {site.get_unique_id() for site in self.nb_adapter.get_all("network")},
        )
        self.assertEqual(
            {dev.name for dev in Device.objects.all()},
            {dev.get_unique_id() for dev in self.nb_adapter.get_all("device")},
        )
