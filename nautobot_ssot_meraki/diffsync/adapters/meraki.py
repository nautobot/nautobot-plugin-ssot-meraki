"""Nautobot SSoT for Meraki Adapter for Meraki SSoT plugin."""
from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from nautobot_ssot_meraki.diffsync.models.meraki import MerakiNetwork, MerakiDevice, MerakiPort
from nautobot_ssot_meraki.utils.meraki import parse_hostname_for_role


class MerakiAdapter(DiffSync):
    """DiffSync adapter for Meraki."""

    network = MerakiNetwork
    device = MerakiDevice
    port = MerakiPort

    top_level = ["network", "device", "port"]

    def __init__(self, job, sync, client, tenant=None, *args, **kwargs):
        """Initialize Meraki.

        Args:
            job (object): Meraki SSoT job.
            sync (object): Meraki DiffSync.
            client (object): Meraki API client connection object.
            tenant (object): Tenant specified in Job form to attach to imported Devices.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync
        self.conn = client
        self.tenant = tenant
        self.device_map = {}

    def load_networks(self):
        """Load networks from Meraki dashboard into DiffSync models."""
        if self.tenant:
            tenant = self.tenant.name
        else:
            tenant = None
        for net in self.conn.get_org_networks():
            try:
                self.get(self.network, net["name"])
                self.job.log_warning(message=f"Duplicate network {net['name']} found and being skipped.")
            except ObjectNotFound:
                new_network = self.network(
                    name=net["name"],
                    timezone=net["timeZone"],
                    notes=net["notes"] if net.get("notes") else "",
                    tags=net["tags"],
                    tenant=tenant,
                    uuid=None,
                )
                self.add(new_network)

    def load_devices(self):
        """Load devices from Meraki dashboard into DiffSync models."""
        self.device_map = {dev["name"]: dev for dev in self.conn.get_org_devices()}
        if self.tenant:
            tenant = self.tenant.name
        else:
            tenant = None
        statuses = self.conn.get_device_statuses()
        status = "Offline"
        for dev in self.device_map.values():
            if dev.get("name"):
                if dev["name"] in statuses:
                    if statuses[dev["name"]] == "online":
                        status = "Active"
                try:
                    self.get(self.device, dev["name"])
                    self.job.log_warning(message=f"Duplicate device {dev['name']} found and being skipped.")
                except ObjectNotFound:
                    new_dev = self.device(
                        name=dev["name"],
                        notes=dev["notes"],
                        serial=dev["serial"],
                        status=status,
                        role=parse_hostname_for_role(dev_hostname=dev["name"]),
                        model=dev["model"],
                        network=self.conn.network_map[dev["networkId"]]["name"],
                        tenant=tenant,
                        uuid=None,
                        version=dev["firmware"],
                    )
                    self.add(new_dev)
                    self.load_management_port(device_name=dev["name"], serial=dev["serial"])
            else:
                self.job.log_warning(message=f"Device serial {dev['serial']} is missing hostname so will be skipped.")

    def load_management_port(self, device_name: str, serial: str):
        """Load management port of a device from Meraki dashboard into DiffSync models."""
        mgmt_port_names = self.conn.get_management_port_names(serial=serial)
        uplink_settings = self.conn.get_uplink_settings(serial=serial)
        uplink_statuses = self.conn.get_org_uplink_statuses()

        for port in mgmt_port_names:
            try:
                self.get(self.port, {"name": port, "device": device_name})
            except ObjectNotFound:
                uplink_status = "Planned"
                if self.device_map[device_name]["networkId"] in uplink_statuses:
                    uplinks = uplink_statuses[self.device_map[device_name]["networkId"]]["uplinks"]
                    for link in uplinks:
                        if link["interface"] == port and link["status"] == "active":
                            uplink_status = "Active"
                new_port = self.port(
                    name=port,
                    device=device_name,
                    management=True,
                    enabled=uplink_settings[port]["enabled"],
                    port_type="1000base-t",
                    port_status=uplink_status,
                    tagging=uplink_settings[port]["vlanTagging"]["enabled"],
                    uuid=None,
                )
                self.add(new_port)

    def load(self):
        """Load data from Meraki into DiffSync models."""
        if self.conn.validate_organization_exists():
            self.load_networks()
            self.load_devices()
        else:
            self.job.log_failure(message="Specified organization ID not found in Meraki dashboard.")
