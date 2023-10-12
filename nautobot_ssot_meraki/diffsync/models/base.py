"""DiffSyncModel subclasses for Nautobot-to-Meraki data sync."""
from typing import List, Optional
from uuid import UUID
from diffsync import DiffSyncModel
from diffsync.enum import DiffSyncModelFlags


class Network(DiffSyncModel):
    """DiffSync model for Meraki networks."""

    model_flags = DiffSyncModelFlags.SKIP_UNMATCHED_DST

    _modelname = "network"
    _identifiers = ("name",)
    _attributes = ("timezone", "notes", "tags", "tenant")
    _children = {}

    name: str
    timezone: Optional[str]
    notes: Optional[str]
    tags: Optional[List[str]]
    tenant: Optional[str]

    uuid: Optional[UUID]


class Device(DiffSyncModel):
    """DiffSync model for Meraki devices."""

    _modelname = "device"
    _identifiers = ("name",)
    _attributes = ("notes", "serial", "status", "role", "model", "network", "tenant", "version")
    _children = {"port": "ports"}

    name: str
    notes: Optional[str]
    serial: Optional[str]
    status: Optional[str]
    role: Optional[str]
    model: Optional[str]
    network: str
    tenant: Optional[str]
    version: Optional[str]
    ports: List["Port"] = []

    uuid: Optional[UUID]


class Port(DiffSyncModel):
    """DiffSync model for Meraki device ports."""

    _modelname = "port"
    _identifiers = ("name", "device")
    _attributes = ("management", "enabled", "port_type", "port_status", "tagging")
    _children = {}

    name: str
    device: str
    management: bool
    enabled: bool
    port_type: str
    port_status: str
    tagging: bool

    uuid: Optional[UUID]


class Prefix(DiffSyncModel):
    """DiffSync model for Meraki Prefixes."""

    _modelname = "prefix"
    _identifiers = ("prefix", "location")
    _attributes = ()
    _children = {}

    prefix: str
    location: str

    uuid: Optional[UUID]


class IPAddress(DiffSyncModel):
    """DiffSync model for Meraki IP Addresses."""

    _modelname = "ipaddress"
    _identifiers = ("address", "location")
    _attributes = ("device", "port", "prefix", "primary", "tenant")
    _children = {}

    address: str
    device: str
    location: str
    port: str
    prefix: str
    primary: bool
    tenant: Optional[str]

    uuid: Optional[UUID]
