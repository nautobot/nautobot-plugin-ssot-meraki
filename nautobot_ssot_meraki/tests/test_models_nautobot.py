"""Unit tests for Nautobot IPAM model CRUD functions."""

from unittest.mock import patch
from django.contrib.contenttypes.models import ContentType
from diffsync import DiffSync
from nautobot.core.testing import TransactionTestCase
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status
from nautobot.ipam.models import Namespace, Prefix
from nautobot.tenancy.models import Tenant
from nautobot_ssot_meraki.diffsync.models.nautobot import NautobotPrefix


class TestNautobotPrefix(TransactionTestCase):  # pylint: disable=too-many-instance-attributes
    """Test the NautobotPrefix class."""

    def setUp(self):
        super().setUp()
        self.status_active = Status.objects.get(name="Active")
        site_lt = LocationType.objects.get(name="Site")
        site_lt.content_types.add(ContentType.objects.get_for_model(Prefix))
        self.test_site = Location.objects.create(name="Test", location_type=site_lt, status=self.status_active)
        self.update_site = Location.objects.create(name="Update", location_type=site_lt, status=self.status_active)
        self.test_tenant = Tenant.objects.get_or_create(name="Test")[0]
        self.update_tenant = Tenant.objects.get_or_create(name="Update")[0]
        self.test_ns = Namespace.objects.get_or_create(name="Test")[0]
        self.prefix = Prefix.objects.create(
            prefix="10.0.0.0/24", namespace=self.test_ns, status=self.status_active, tenant=self.test_tenant
        )
        self.diffsync = DiffSync()
        self.diffsync.namespace_map = {"Test": self.test_ns.id, "Update": self.update_site.id}
        self.diffsync.site_map = {"Test": self.test_site.id, "Update": self.update_site.id}
        self.diffsync.tenant_map = {"Test": self.test_tenant.id, "Update": self.update_tenant.id}
        self.diffsync.status_map = {"Active": self.status_active.id}
        self.diffsync.prefix_map = {}
        self.diffsync.objects_to_create = {"prefixes": []}
        self.diffsync.objects_to_delete = {"prefixes": []}

    def test_create(self):
        """Validate the NautobotPrefix create() method creates a Prefix."""
        self.prefix.delete()
        ids = {"prefix": "10.0.0.0/24", "namespace": "Test"}
        attrs = {"location": "Test", "tenant": "Test"}
        result = NautobotPrefix.create(self.diffsync, ids, attrs)
        self.assertIsInstance(result, NautobotPrefix)
        self.assertEqual(len(self.diffsync.objects_to_create["prefixes"]), 1)
        subnet = self.diffsync.objects_to_create["prefixes"][0]
        self.assertEqual(str(subnet.prefix), ids["prefix"])
        self.assertEqual(self.diffsync.prefix_map[ids["prefix"]], subnet.id)
        self.assertEqual(subnet.custom_field_data["system_of_record"], "Meraki SSoT")

    def test_update(self):
        """Validate the NautobotPrefix update() method updates a Prefix."""
        test_pf = NautobotPrefix(
            prefix="10.0.0.0/24",
            namespace="Test",
            location="Test",
            tenant="Test",
            uuid=self.prefix.id,
        )
        test_pf.diffsync = self.diffsync
        update_attrs = {"location": "Update", "tenant": "Update"}
        actual = NautobotPrefix.update(self=test_pf, attrs=update_attrs)
        self.prefix.refresh_from_db()
        self.assertEqual(self.prefix.location, self.update_site)
        self.assertEqual(self.prefix.tenant, self.update_tenant)
        self.assertEqual(actual, test_pf)

    @patch("nautobot_ssot_meraki.diffsync.models.nautobot.OrmPrefix.objects.get")
    def test_delete(self, mock_prefix):
        """Validate the NautobotPrefix delete() deletes a Prefix."""
        test_pf = NautobotPrefix(
            prefix="10.0.0.0/24",
            namespace="Test",
            location="Test",
            tenant="Test",
            uuid=self.prefix.id,
        )
        test_pf.diffsync = self.diffsync
        mock_prefix.return_value = self.prefix
        test_pf.delete()
        self.assertEqual(len(self.diffsync.objects_to_delete["prefixes"]), 1)
        self.assertEqual(self.diffsync.objects_to_delete["prefixes"][0].id, self.prefix.id)
