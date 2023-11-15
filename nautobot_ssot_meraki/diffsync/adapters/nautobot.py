"""Nautobot Adapter for Meraki SSoT plugin."""

from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from nautobot.dcim.models import Device, DeviceType, Interface, Location, LocationType, Manufacturer, Platform
from nautobot.extras.models import Note, Relationship, RelationshipAssociation, Role, Status
from nautobot.ipam.models import IPAddress, IPAddressToInterface, Namespace, Prefix
from nautobot_ssot_meraki.diffsync.models.nautobot import (
    NautobotDevice,
    NautobotHardware,
    NautobotNetwork,
    NautobotPort,
    NautobotPrefix,
    NautobotIPAddress,
)
from nautobot_ssot_meraki.utils.nautobot import get_tag_strings, get_cf_version_map, get_dlc_version_map


class NautobotAdapter(DiffSync):
    """DiffSync adapter for Nautobot."""

    network = NautobotNetwork
    hardware = NautobotHardware
    device = NautobotDevice
    port = NautobotPort
    prefix = NautobotPrefix
    ipaddress = NautobotIPAddress

    top_level = ["network", "hardware", "device", "prefix", "ipaddress"]

    def __init__(self, *args, job, sync=None, **kwargs):
        """Initialize Nautobot.

        Args:
            job (object): Nautobot job.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load_sites(self):
        """Load Site data from Nautobot into DiffSync model."""
        site_type = LocationType.objects.get(name="Site")
        for site in Location.objects.filter(location_type=site_type):
            try:
                self.get(self.network, site.name)
            except ObjectNotFound:
                new_site = self.network(
                    name=site.name,
                    notes="",
                    tags=get_tag_strings(list_tags=site.tags),
                    timezone=site.time_zone.zone if site.time_zone else None,
                    tenant=site.tenant.name if site.tenant else None,
                    uuid=site.id,
                )
                if site.notes:
                    note = site.notes.last()
                    new_site.notes = note.note.rstrip()
                self.add(new_site)

    def load_devicetypes(self):
        """Load DeviceType data from Nautobot into DiffSync model."""
        for dt in DeviceType.objects.filter(manufacturer__name="Cisco Meraki"):
            try:
                self.get(self.hardware, dt.model)
            except ObjectNotFound:
                new_dt = self.hardware(model=dt.model, uuid=dt.id)
                self.add(new_dt)
                self.devicetype_map[dt.model] = dt.id

    def load_devices(self):
        """Load Device data from Nautobot into DiffSync model."""
        for dev in Device.objects.filter(_custom_field_data__system_of_record="Meraki SSoT"):
            try:
                self.get(self.device, dev.name)
            except ObjectNotFound:
                new_dev = self.device(
                    name=dev.name,
                    serial=dev.serial,
                    status=dev.status.name,
                    role=dev.role.name,
                    model=dev.device_type.model,
                    notes="",
                    network=dev.location.name,
                    tenant=dev.tenant.name if dev.tenant else None,
                    uuid=dev.id,
                    version=dev._custom_field_data["os_version"] if dev._custom_field_data.get("os_version") else "",
                )
                if dev.notes:
                    note = dev.notes.last()
                    new_dev.notes = note.note.rstrip()
                self.add(new_dev)

    def load_ports(self):
        """Load Port data from Nautobot into DiffSync model."""
        for intf in Interface.objects.filter(_custom_field_data__system_of_record="Meraki SSoT"):
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
                if len(intf.ip_addresses.all()) > 0:
                    for ipaddr in intf.ip_addresses.all():
                        pf_found = Prefix.objects.net_contains(ipaddr.host).last()
                        if pf_found:
                            try:
                                self.get(
                                    self.prefix, {"prefix": str(pf_found.prefix), "namespace": pf_found.namespace.name}
                                )
                            except ObjectNotFound:
                                new_pf = self.prefix(
                                    prefix=str(pf_found.prefix),
                                    location=pf_found.location.name,
                                    namespace=pf_found.namespace.name,
                                    tenant=pf_found.tenant.name if pf_found.tenant else None,
                                    uuid=pf_found.id,
                                )
                                self.add(new_pf)
                        else:
                            self.job.logger.warning(f"Unable to find prefix for IP Address {ipaddr.host}.")
                        new_ip = self.ipaddress(
                            address=str(ipaddr.address),
                            device=intf.device.name,
                            port=intf.name,
                            prefix=str(pf_found.prefix) if pf_found else "",
                            primary=bool(
                                len(ipaddr.primary_ip4_for.all()) > 0 or len(ipaddr.primary_ip6_for.all()) > 0
                            ),
                            tenant=intf.device.tenant.name if intf.device.tenant else None,
                            uuid=ipaddr.id,
                        )
                        self.add(new_ip)

    def load(self):
        """Load data from Nautobot into DiffSync models."""
        self.load_sites()
        self.load_devicetypes()
        self.load_devices()
        self.load_ports()
