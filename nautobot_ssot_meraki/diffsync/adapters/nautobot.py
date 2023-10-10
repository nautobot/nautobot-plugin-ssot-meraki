"""Nautobot Adapter for Meraki SSoT plugin."""

from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from nautobot.dcim.models import Device, Interface, Site
from nautobot.ipam.models import Prefix
from netutils.ip import ipaddress_interface
from nautobot_ssot_meraki.diffsync.models.nautobot import (
    NautobotDevice,
    NautobotNetwork,
    NautobotPort,
    NautobotPrefix,
    NautobotIPAddress,
)
from nautobot_ssot_meraki.utils.nautobot import get_tag_strings


class NautobotAdapter(DiffSync):
    """DiffSync adapter for Nautobot."""

    network = NautobotNetwork
    device = NautobotDevice
    port = NautobotPort
    prefix = NautobotPrefix
    ipaddress = NautobotIPAddress

    top_level = ["network", "device", "prefix", "ipaddress"]

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Nautobot.

        Args:
            job (object, optional): Nautobot job. Defaults to None.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load_sites(self):
        """Load Site data from Nautobot into DiffSync model."""
        for site in Site.objects.all():
            try:
                self.get(self.network, site.name)
            except ObjectNotFound:
                new_site = self.network(
                    name=site.name,
                    notes="",
                    tags=get_tag_strings(list_tags=site.tags),
                    timezone=site.time_zone.zone,
                    tenant=site.tenant.name if site.tenant else None,
                    uuid=site.id,
                )
                if site.notes:
                    note = site.notes.first()
                    new_site.notes = note.note
                self.add(new_site)

    def load_devices(self):
        """Load Device data from Nautobot into DiffSync model."""
        for dev in Device.objects.all():
            try:
                self.get(self.device, dev.name)
            except ObjectNotFound:
                new_dev = self.device(
                    name=dev.name,
                    serial=dev.serial,
                    status=dev.status.name,
                    role=dev.device_role.name,
                    model=dev.device_type.model,
                    notes="",
                    network=dev.site.name,
                    tenant=dev.tenant.name if dev.tenant else None,
                    uuid=dev.id,
                    version=dev._custom_field_data["os_version"] if dev._custom_field_data.get("os_version") else "",
                )
                if dev.notes:
                    note = dev.notes.first()
                    new_dev.notes = note.note
                self.add(new_dev)

    def load_ports(self):
        """Load Port data from Nautobot into DiffSync model."""
        for intf in Interface.objects.all():
            try:
                self.get(self.port, {"name": intf.name, "device": intf.device.name})
            except ObjectNotFound:
                new_port = self.port(
                    name=intf.name,
                    device=intf.device.name,
                    management=intf.mgmt_only,
                    enabled=intf.enabled,
                    port_type=intf.type,
                    port_status=intf.status.name,
                    tagging=False if intf.mode == "access" else True,
                    uuid=intf.id,
                )
                self.add(new_port)
                dev = self.get(self.device, intf.device.name)
                dev.add_child(new_port)

    def load(self):
        """Load data from Nautobot into DiffSync models."""
        self.load_sites()
        self.load_devices()
        self.load_ports()
        self.load_ipaddresses()
