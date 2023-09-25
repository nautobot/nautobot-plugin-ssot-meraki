"""Jobs for Meraki SSoT integration."""

from diffsync import DiffSyncFlags
from nautobot.extras.jobs import BooleanVar, Job
from nautobot_ssot.jobs.base import DataSource, DataTarget
from nautobot_ssot_meraki.diffsync.adapters import meraki, nautobot


name = "Meraki SSoT"  # pylint: disable=invalid-name


class MerakiDataSource(DataSource, Job):
    """Meraki SSoT Data Source."""

    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)

    def __init__(self):
        """Initialize Meraki Data Source."""
        super().__init__()
        self.diffsync_flags = self.diffsync_flags | DiffSyncFlags.CONTINUE_ON_FAILURE

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta data for Meraki."""

        name = "Meraki to Nautobot"
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
        self.source_adapter = meraki.MerakiAdapter(job=self, sync=self.sync)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()


class MerakiDataTarget(DataTarget, Job):
    """Meraki SSoT Data Target."""

    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)

    def __init__(self):
        """Initialize Meraki Data Target."""
        super().__init__()
        self.diffsync_flags = self.diffsync_flags | DiffSyncFlags.CONTINUE_ON_FAILURE

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta data for Meraki."""

        name = "Nautobot to Meraki"
        data_source = "Nautobot"
        data_target = "Meraki"
        description = "Sync information from Nautobot to Meraki"

    @classmethod
    def config_information(cls):
        """Dictionary describing the configuration of this DataTarget."""
        return {}

    @classmethod
    def data_mappings(cls):
        """List describing the data mappings involved in this DataSource."""
        return ()

    def load_source_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.source_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Meraki into DiffSync models."""
        self.target_adapter = meraki.MerakiAdapter(job=self, sync=self.sync)
        self.target_adapter.load()


jobs = [MerakiDataSource, MerakiDataTarget]
