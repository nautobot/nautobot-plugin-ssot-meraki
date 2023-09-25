"""Nautobot SSoT for Meraki DiffSync models for Nautobot SSoT for Meraki SSoT."""

from nautobot_ssot_meraki.diffsync.models.base import Device


class MerakiDevice(Device):
    """Meraki implementation of Device DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Device in Meraki from NautobotSsotMerakiDevice object."""
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Device in Meraki from NautobotSsotMerakiDevice object."""
        return super().update(attrs)

    def delete(self):
        """Delete Device in Meraki from NautobotSsotMerakiDevice object."""
        return self
