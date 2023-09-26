"""Jobs for Meraki SSoT integration."""
from django.conf import settings
from nautobot.extras.jobs import BooleanVar, Job
from nautobot_ssot.jobs.base import DataSource
from nautobot_ssot_meraki.diffsync.adapters import meraki, nautobot
from nautobot_ssot_meraki.utils.meraki import DashboardClient


PLUGIN_CFG = settings.PLUGINS_CONFIG["nautobot_ssot_meraki"]

name = "Meraki SSoT"  # pylint: disable=invalid-name


class MerakiDataSource(DataSource, Job):
    """Meraki SSoT Data Source."""

    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)

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
        self.source_adapter = meraki.MerakiAdapter(job=self, sync=self.sync, client=client)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()


jobs = [MerakiDataSource]
