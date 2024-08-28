"""Jobs for Meraki SSoT integration."""

from django.conf import settings
from diffsync.enum import DiffSyncFlags
from nautobot.core.celery import register_jobs
from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot.extras.jobs import BooleanVar, ObjectVar
from nautobot.extras.models import ExternalIntegration
from nautobot.tenancy.models import Tenant
from nautobot_ssot.jobs.base import DataSource
from nautobot_ssot_meraki.diffsync.adapters import meraki, nautobot
from nautobot_ssot_meraki.utils.meraki import DashboardClient


PLUGIN_CFG = settings.PLUGINS_CONFIG["nautobot_ssot_meraki"]

name = "Meraki SSoT"  # pylint: disable=invalid-name


class MerakiDataSource(DataSource):  # pylint: disable=too-many-instance-attributes
    """Meraki SSoT Data Source."""

    instance = ObjectVar(
        model=ExternalIntegration,
        queryset=ExternalIntegration.objects.all(),
        description="ExternalIntegration containing information for connecting to Meraki dashboard.",
        display_field="display",
        label="Meraki Instance",
        required=True,
    )
    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)
    tenant = ObjectVar(model=Tenant, label="Tenant", required=False)

    def __init__(self):
        """Initialize job objects."""
        super().__init__()
        self.data = None
        self.diffsync_flags = DiffSyncFlags.CONTINUE_ON_FAILURE


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
        _sg = self.instance.secrets_group
        org_id = _sg.get_secret_value(
            access_type=SecretsGroupAccessTypeChoices.TYPE_HTTP,
            secret_type=SecretsGroupSecretTypeChoices.TYPE_USERNAME,
        )
        token = _sg.get_secret_value(
            access_type=SecretsGroupAccessTypeChoices.TYPE_HTTP,
            secret_type=SecretsGroupSecretTypeChoices.TYPE_TOKEN,
        )
        client = DashboardClient(logger=self, org_id=org_id, token=token)
        self.source_adapter = meraki.MerakiAdapter(job=self, sync=self.sync, client=client, tenant=self.tenant)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync, tenant=self.tenant)
        self.target_adapter.load()

    def run(
        self, dryrun, memory_profiling, instance, debug, tenant, *args, **kwargs
    ):  # pylint: disable=arguments-differ, too-many-arguments
        """Perform data synchronization."""
        self.dryrun = dryrun
        self.memory_profiling = memory_profiling
        self.instance = instance
        self.debug = debug
        self.tenant = tenant
        super().run(dryrun - self.dryrun, memory_profiling=self.memory_profiling, *args, **kwargs)


jobs = [MerakiDataSource]
register_jobs(*jobs)
