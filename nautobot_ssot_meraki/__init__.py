"""Plugin declaration for nautobot_ssot_meraki."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import NautobotAppConfig


class NautobotSsotMerakiConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_ssot_meraki plugin."""

    name = "nautobot_ssot_meraki"
    verbose_name = "Nautobot SSoT for Meraki"
    version = __version__
    author = "Justin Drew"
    description = "Nautobot SSoT for Meraki."
    base_url = "nautobot-ssot-meraki"
    required_settings = []
    min_version = "1.6.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotSsotMerakiConfig  # pylint:disable=invalid-name
