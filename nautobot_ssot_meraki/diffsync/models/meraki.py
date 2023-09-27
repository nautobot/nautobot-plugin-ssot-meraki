"""Nautobot SSoT for Meraki DiffSync models for Nautobot SSoT for Meraki SSoT."""

from nautobot_ssot_meraki.diffsync.models.base import Device, Network


class MerakiNetwork(Network):
    """Meraki implementation of Network DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Network in Meraki from MerakiNetwork object."""
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Network in Meraki from MerakiNetwork object."""
        return super().update(attrs)

    def delete(self):
        """Delete Network in Meraki from MerakiNetwork object."""
        return self


class MerakiDevice(Device):
    """Meraki implementation of Device DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Device in Meraki from MerakiDevice object."""
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Device in Meraki from MerakiDevice object."""
        return super().update(attrs)

    def delete(self):
        """Delete Device in Meraki from MerakiDevice object."""
        return self
