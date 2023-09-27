"""Jobs for Meraki SSoT integration."""
from django.conf import settings
from nautobot.extras.jobs import BooleanVar, Job, ObjectVar
from nautobot.tenancy.models import Tenant
from nautobot_ssot.jobs.base import DataSource
from nautobot_ssot_meraki.diffsync.adapters import meraki, nautobot
from nautobot_ssot_meraki.utils.meraki import DashboardClient


PLUGIN_CFG = settings.PLUGINS_CONFIG["nautobot_ssot_meraki"]

name = "Meraki SSoT"  # pylint: disable=invalid-name


class MerakiDataSource(DataSource, Job):
    """Meraki SSoT Data Source."""

    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)
    tenant = ObjectVar(model=Tenant, label="Tenant", required=False)

    def __init__(self):
        """Initialize job objects."""
        super().__init__()
        self.data = None

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta data for Meraki."""

        name = "Meraki => Nautobot"
        data_source = "Meraki"
        data_target = "Nautobot"
        description = "Sync information from Meraki to Nautobot"

    @classmethod
    def config_information(cls):
        """Dictionary describing the configuration of this DataSource."""
        return {}

    @classmethod
    def data_mappings(cls):
        """List describing the data mappings involved in this DataSource."""
        return ()

    def load_source_adapter(self):
        """Load data from Meraki into DiffSync models."""
        client = DashboardClient(logger=self, org_id=PLUGIN_CFG["meraki_org_id"], token=PLUGIN_CFG["meraki_token"])
        self.source_adapter = meraki.MerakiAdapter(job=self, sync=self.sync, client=client, tenant=self.data["tenant"])
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()

    def run(self, data, commit):
        """Ensure Job form variables are set."""
        self.commit = commit
        self.data = data
        super().run(data, commit)


jobs = [MerakiDataSource]
