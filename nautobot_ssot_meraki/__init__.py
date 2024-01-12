"""Plugin declaration for nautobot_ssot_meraki."""
from importlib import metadata
from nautobot.core.signals import nautobot_database_ready
from nautobot.extras.plugins import NautobotAppConfig
from nautobot_ssot_meraki.signals import nautobot_database_ready_callback

__version__ = metadata.version(__name__)


class NautobotSsotMerakiConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_ssot_meraki plugin."""

    name = "nautobot_ssot_meraki"
    verbose_name = "Nautobot SSoT for Meraki"
    version = __version__
    author = "Justin Drew"
    description = "Nautobot SSoT for Meraki."
    base_url = "nautobot-ssot-meraki"
    required_settings = []
    min_version = "2.1.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}

    def ready(self):
        """Trigger callback when database is ready."""
        super().ready()

        nautobot_database_ready.connect(nautobot_database_ready_callback, sender=self)


config = NautobotSsotMerakiConfig  # pylint:disable=invalid-name
