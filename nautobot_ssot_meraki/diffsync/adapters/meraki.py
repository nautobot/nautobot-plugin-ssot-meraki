"""Nautobot SSoT for Meraki Adapter for Meraki SSoT plugin."""
from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from netutils.ip import ipaddress_interface, netmask_to_cidr
from nautobot_ssot_meraki.diffsync.models.meraki import MerakiNetwork, MerakiDevice, MerakiPort, MerakiIPAddress
from nautobot_ssot_meraki.utils.meraki import parse_hostname_for_role


class MerakiAdapter(DiffSync):
    """DiffSync adapter for Meraki."""

    network = MerakiNetwork
    device = MerakiDevice
    port = MerakiPort
    ipaddress = MerakiIPAddress

    top_level = ["network", "device", "port", "ipaddress"]

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
        self.org_uplink_statuses = self.conn.get_org_uplink_statuses()

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
                    if dev["model"].startswith(("MX", "MG", "Z")):
                        self.load_firewall_ports(
                            device_name=dev["name"], serial=dev["serial"], network_id=dev["networkId"]
                        )
                    if dev["model"].startswith("MS"):
                        self.load_switch_ports(device_name=dev["name"], serial=dev["serial"])
                    if dev["model"].startswith("MR"):
                        self.load_ap_ports(device_name=dev["name"], serial=dev["serial"])
            else:
                self.job.log_warning(message=f"Device serial {dev['serial']} is missing hostname so will be skipped.")

    def load_firewall_ports(self, device_name: str, serial: str, network_id: str):
        """Load ports of a firewall, cellular, or teleworker device from Meraki dashboard into DiffSync models."""
        mgmt_ports = self.conn.get_management_ports(serial=serial)
        uplink_settings = self.conn.get_uplink_settings(serial=serial)
        lan_ports = self.conn.get_appliance_switchports(network_id=network_id)

        for port in mgmt_ports.keys():
            try:
                self.get(self.port, {"name": port, "device": device_name})
            except ObjectNotFound:
                uplink_status = "Planned"
                if serial in self.org_uplink_statuses:
                    uplinks = self.org_uplink_statuses[serial]["uplinks"]
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
                if uplink_settings[port]["svis"]["ipv4"]["assignmentMode"] == "static":
                    port_svis = uplink_settings[port]["svis"]["ipv4"]
                    prefix = ipaddress_interface(ip=port_svis["address"], attr="with_prefixlen")
                    self.load_ipaddress(
                        address=port_svis["address"],
                        dev_name=device_name,
                        location=self.conn.network_map[network_id]["name"],
                        port=port,
                        prefix=prefix,
                        primary=True,
                    )
        for port in lan_ports:
            try:
                self.get(self.port, {"name": port["number"], "device": device_name})
            except ObjectNotFound:
                new_port = self.port(
                    name=port["number"],
                    device=device_name,
                    management=False,
                    enabled=port["enabled"],
                    port_type="1000base-t",
                    port_status="Active",
                    tagging=bool(port["type"] == "trunk"),
                    uuid=None,
                )
                self.add(new_port)

    def load_switch_ports(self, device_name: str, serial: str):
        """Load ports of a switch device from Meraki dashboard into DiffSync models."""
        mgmt_ports = self.conn.get_management_ports(serial=serial)
        org_switchports = self.conn.get_org_switchports()

        for port in mgmt_ports.keys():
            try:
                self.get(self.port, {"name": port, "device": device_name})
            except ObjectNotFound:
                mgmt_port = self.port(
                    name=port,
                    device=device_name,
                    management=True,
                    enabled=True,
                    port_type="1000base-t",
                    port_status="Active",
                    tagging=False,
                    uuid=None,
                )
                self.add(mgmt_port)
                if mgmt_ports[port].get("usingStaticIp"):
                    prefix = ipaddress_interface(
                        ip=f"{mgmt_ports[port]['staticIp']}/{netmask_to_cidr(netmask=mgmt_ports[port]['staticSubnetMask'])}",
                        attr="with_prefixlen",
                    )
                    self.load_ipaddress(
                        address=mgmt_ports[port]["staticIp"],
                        dev_name=device_name,
                        location=self.conn.network_map[self.device_map[device_name]["networkId"]]["name"],
                        port=port,
                        prefix=prefix,
                        primary=True,
                    )
        if serial in org_switchports:
            for port in org_switchports[serial]["ports"]:
                new_port = self.port(
                    name=port["portId"],
                    device=device_name,
                    management=False,
                    enabled=port["enabled"],
                    port_type="1000base-t",
                    port_status="Active",
                    tagging=True if port["type"] == "trunk" else False,
                    uuid=None,
                )
                self.add(new_port)

    def load_ap_ports(self, device_name: str, serial: str):
        """Load ports of a MR device from Meraki dashboard into DiffSync models."""
        mgmt_ports = self.conn.get_management_ports(serial=serial)

        for port in mgmt_ports.keys():
            try:
                self.get(self.port, {"name": port, "device": device_name})
            except ObjectNotFound:
                new_port = self.port(
                    name=port,
                    device=device_name,
                    management=True,
                    enabled=True,
                    port_type="1000base-t",
                    port_status="Active",
                    tagging=False,
                    uuid=None,
                )
                self.add(new_port)
                if mgmt_ports[port].get("usingStaticIp"):
                    prefix = ipaddress_interface(
                        ip=f"{mgmt_ports[port]['staticIp']}/{netmask_to_cidr(netmask=mgmt_ports[port]['staticSubnetMask'])}",
                        attr="with_prefixlen",
                    )
                    self.load_ipaddress(
                        address=mgmt_ports[port]["staticIp"],
                        dev_name=device_name,
                        location=self.conn.network_map[self.device_map[device_name]["networkId"]]["name"],
                        port=port,
                        prefix=prefix,
                        primary=True,
                    )

    def load_ipaddress(self, address: str, dev_name: str, location: str, port: str, prefix: str, primary: bool):
        """Load IPAddresses of devices into DiffSync models."""
        try:
            self.get(self.ipaddress, {"address": address, "location": location})
        except ObjectNotFound:
            new_ip = self.ipaddress(
                address=address,
                location=location,
                device=dev_name,
                port=port,
                prefix=prefix,
                primary=primary,
                uuid=None,
            )
            self.add(new_ip)

    def load(self):
        """Load data from Meraki into DiffSync models."""
        if self.conn.validate_organization_exists():
            self.load_networks()
            self.load_devices()
        else:
            self.job.log_failure(message="Specified organization ID not found in Meraki dashboard.")
