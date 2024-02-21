"""Nautobot DiffSync models for Meraki SSoT."""
from datetime import datetime
from nautobot.dcim.models import Device as NewDevice
from nautobot.dcim.models import DeviceType, Interface, Location
from nautobot.extras.models import Note, Role
from nautobot.ipam.models import IPAddress as OrmIPAddress
from nautobot.ipam.models import Prefix as OrmPrefix
from nautobot.ipam.models import IPAddressToInterface
from nautobot_ssot_meraki.diffsync.models.base import Device, Hardware, Network, Port, Prefix, IPAddress, IPAssignment
from nautobot_ssot_meraki.utils.nautobot import add_software_lcm, assign_version_to_device

try:
    import nautobot_device_lifecycle_mgmt  # noqa: F401

    LIFECYCLE_MGMT = True
except ImportError:
    print("Device Lifecycle plugin isn't installed so will revert to CustomField for OS version.")
    LIFECYCLE_MGMT = False


class NautobotNetwork(Network):
    """Nautobot implementation of Network DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Site in Nautobot from NautobotNetwork object."""
        new_site = Location(
            name=ids["name"],
            location_type_id=diffsync.locationtype_map["Site"],
            parent_id=diffsync.location_map["Global Region"],
            status_id=diffsync.status_map["Active"],
            time_zone=attrs["timezone"],
        )
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=diffsync.job.user,
                assigned_object_type_id=diffsync.contenttype_map["location"],
                assigned_object_id=new_site.id,
            )
            diffsync.objects_to_create["notes"].append(new_note)
        if attrs.get("tags"):
            new_site.tags.set(attrs["tags"])
            for tag in new_site.tags.all():
                tag.content_types.add(diffsync.contenttype_map["location"])
        if attrs.get("tenant"):
            new_site.tenant_id = diffsync.tenant_map[attrs["tenant"]]
        new_site.validated_save()
        diffsync.site_map[ids["name"]] = new_site.id
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Site in Nautobot from NautobotNetwork object."""
        site = Location.objects.get(id=self.uuid)
        if "timezone" in attrs:
            site.time_zone = attrs["timezone"]
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=self.diffsync.job.user,
                assigned_object_type_id=self.diffsync.contenttype_map["location"],
                assigned_object_id=site.id,
            )
            new_note.validated_save()
        if "tags" in attrs:
            site.tags.set(attrs["tags"])
            for tag in site.tags.all():
                tag.content_types.add(self.diffsync.contenttype_map["location"])
        if "tenant" in attrs:
            if attrs.get("tenant"):
                site.tenant_id = self.diffsync.tenant_map[attrs["tenant"]]
            else:
                site.tenant = None
        site.validated_save()
        return super().update(attrs)


class NautobotHardware(Hardware):
    """Nautobot implementation of Hardware DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create DeviceType in Nautobot from NautobotHardware object."""
        new_dt = DeviceType(model=ids["model"], manufacturer_id=diffsync.manufacturer_map["Cisco Meraki"])
        diffsync.objects_to_create["devicetypes"].append(new_dt)
        diffsync.devicetype_map[ids["model"]] = new_dt.id
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def delete(self):
        """Delete DeviceType in Nautobot from NautobotHardware object."""
        super().delete()
        devicetype = DeviceType.objects.get(id=self.uuid)
        self.diffsync.objects_to_delete["devicetypes"].append(devicetype)
        return self


class NautobotDevice(Device):
    """Nautobot implementation of Meraki Device model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Device in Nautobot from NautobotDevice object."""
        dev_role, created = Role.objects.get_or_create(name=attrs["role"])
        if created:
            dev_role.content_types.add(diffsync.contenttype_map["device"])
            diffsync.devicerole_map[attrs["role"]] = dev_role.id
        new_device = NewDevice(
            name=ids["name"],
            platform_id=diffsync.platform_map["Meraki"],
            serial=attrs["serial"],
            status_id=diffsync.status_map[attrs["status"]],
            role_id=diffsync.devicerole_map[attrs["role"]],
            device_type_id=diffsync.devicetype_map[attrs["model"]],
            location_id=diffsync.site_map[attrs["network"]],
        )
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=diffsync.job.user,
                assigned_object_type_id=diffsync.contenttype_map["device"],
                assigned_object_id=new_device.id,
            )
            diffsync.objects_to_create["notes"].append(new_note)
        if attrs.get("tags"):
            new_device.tags.set(attrs["tags"])
            for tag in new_device.tags.all():
                tag.content_types.add(diffsync.contenttype_map["device"])
        if attrs.get("tenant"):
            if attrs.get("tenant"):
                new_device.tenant_id = diffsync.tenant_map[attrs["tenant"]]
            else:
                new_device.tenant = None
        if attrs.get("version"):
            if LIFECYCLE_MGMT:
                soft_lcm = add_software_lcm(version=attrs["version"])
                assign_version_to_device(diffsync=diffsync, device=new_device, software_lcm=soft_lcm)
            new_device._custom_field_data["os_version"] = attrs["version"]
        new_device._custom_field_data["system_of_record"] = "Meraki SSoT"
        new_device._custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        diffsync.objects_to_create["devices"].append(new_device)
        diffsync.device_map[new_device.name] = new_device.id
        diffsync.port_map[new_device.name] = {}
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Device in Nautobot from NautobotDevice object."""
        device = NewDevice.objects.get(id=self.uuid)
        if "serial" in attrs:
            device.serial = attrs["serial"]
        if "status" in attrs:
            device.status_id = self.diffsync.status_map[attrs["status"]]
        if "role" in attrs:
            device.role_id = self.diffsync.devicerole_map[attrs["role"]]
        if "model" in attrs:
            device.device_type_id = self.diffsync.devicetype_map[attrs["model"]]
        if "network" in attrs:
            device.location_id = self.diffsync.site_map[attrs["network"]]
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=self.diffsync.job.user,
                assigned_object_type_id=self.diffsync.contenttype_map["device"],
                assigned_object_id=device.id,
            )
            new_note.validated_save()
        if "tags" in attrs:
            device.tags.set(attrs["tags"])
            for tag in device.tags.all():
                tag.content_types.add(self.diffsync.contenttype_map["device"])
        if "tenant" in attrs:
            if attrs.get("tenant"):
                device.tenant_id = self.diffsync.tenant_map[attrs["tenant"]]
            else:
                device.tenant = None
        if "version" in attrs:
            if LIFECYCLE_MGMT:
                soft_lcm = add_software_lcm(version=attrs["version"])
                assign_version_to_device(diffsync=self.diffsync, device=device, software_lcm=soft_lcm)
            device._custom_field_data["os_version"] = attrs["version"]
        device._custom_field_data["system_of_record"] = "Meraki SSoT"
        device._custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        device.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Device in Nautobot from NautobotDevice object."""
        dev = NewDevice.objects.get(id=self.uuid)
        super().delete()
        self.diffsync.objects_to_delete["devices"].append(dev)
        return self


class NautobotPort(Port):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Interface in Nautobot from NautobotDevice object."""
        new_port = Interface(
            name=ids["name"],
            device_id=diffsync.device_map[ids["device"]],
            enabled=attrs["enabled"],
            mode="access" if not attrs["tagging"] else "tagged",
            mgmt_only=attrs["management"],
            type=attrs["port_type"],
            status_id=diffsync.status_map[attrs["port_status"]],
        )
        new_port.custom_field_data["system_of_record"] = "Meraki SSoT"
        new_port.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        diffsync.objects_to_create["ports"].append(new_port)
        diffsync.port_map[ids["device"]][ids["name"]] = new_port.id
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Interface in Nautobot from NautobotDevice object."""
        port = Interface.objects.get(id=self.uuid)
        if "enabled" in attrs:
            port.enabled = attrs["enabled"]
        if "tagging" in attrs:
            port.mode = "access" if not attrs["tagging"] else "tagged"
        if "management" in attrs:
            port.mgmt_only = attrs["management"]
        if "port_type" in attrs:
            port.type = attrs["port_type"]
        if "port_status" in attrs:
            port.status_id = self.diffsync.status_map[attrs["port_status"]]
        port.custom_field_data["system_of_record"] = "Meraki SSoT"
        port.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        port.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Interface in Nautobot from NautobotDevice object."""
        port = Interface.objects.get(id=self.uuid)
        super().delete()
        self.diffsync.objects_to_delete["ports"].append(port)
        return self


class NautobotPrefix(Prefix):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Prefix in Nautobot from NautobotPrefix object."""
        new_pf = OrmPrefix(
            prefix=ids["prefix"],
            location_id=diffsync.site_map[attrs["location"]],
            namespace_id=diffsync.namespace_map[ids["namespace"]],
            status_id=diffsync.status_map["Active"],
            tenant_id=diffsync.tenant_map[attrs["tenant"]] if attrs.get("tenant") else None,
        )
        new_pf.custom_field_data["system_of_record"] = "Meraki SSoT"
        new_pf.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        diffsync.objects_to_create["prefixes"].append(new_pf)
        diffsync.prefix_map[ids["prefix"]] = new_pf.id
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Prefix in Nautobot from NautobotPrefix object."""
        prefix = OrmPrefix.objects.get(id=self.uuid)
        if "location" in attrs:
            if attrs.get("location"):
                prefix.location_id = self.diffsync.site_map[attrs["location"]]
            else:
                prefix.location = None
        if "tenant" in attrs:
            if attrs.get("tenant"):
                prefix.tenant_id = self.diffsync.tenant_map[attrs["tenant"]]
            else:
                prefix.tenant = None
        prefix.custom_field_data["system_of_record"] = "Meraki SSoT"
        prefix.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        prefix.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Prefix in Nautobot from NautobotPrefix object."""
        del_pf = OrmPrefix.objects.get(id=self.uuid)
        super().delete()
        self.diffsync.objects_to_delete["prefixes"].append(del_pf)
        return self


class NautobotIPAddress(IPAddress):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create IPAddress in Nautobot from NautobotIPAddress object."""
        new_ip = OrmIPAddress(
            address=ids["address"],
            namespace=diffsync.namespace_map[attrs["tenant"]]
            if attrs.get("tenant")
            else diffsync.namespace_map["Global"],
            status_id=diffsync.status_map["Active"],
            tenant_id=diffsync.tenant_map[attrs["tenant"]] if attrs.get("tenant") else None,
        )
        diffsync.objects_to_create["ipaddrs-to-prefixes"].append((new_ip, diffsync.prefix_map[attrs["prefix"]]))
        new_ip.custom_field_data["system_of_record"] = "Meraki SSoT"
        new_ip.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        diffsync.objects_to_create["ipaddrs"].append(new_ip)
        if attrs["tenant"] not in diffsync.ipaddr_map:
            diffsync.ipaddr_map[attrs["tenant"]] = {}
        diffsync.ipaddr_map[attrs["tenant"]][ids["address"]] = new_ip.id
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update IPAddress in Nautobot from NautobotIPAddress object."""
        ip = OrmIPAddress.objects.get(id=self.uuid)
        if "tenant" in attrs:
            if attrs.get("tenant"):
                ip.tenant_id = self.diffsync.tenant_map[attrs["tenant"]]
            else:
                ip.tenant = None
        ip.custom_field_data["system_of_record"] = "Meraki SSoT"
        ip.custom_field_data["ssot_last_synchronized"] = datetime.today().date().isoformat()
        ip.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete IPAddress in Nautobot from NautobotIPAddress object."""
        ip = OrmIPAddress.objects.get(id=self.uuid)
        super().delete()
        self.diffsync.objects_to_delete["ipaddrs"].append(ip)
        return self


class NautobotIPAssignment(IPAssignment):
    """Nautobot implementation of Citrix ADM IPAddressOnInterface model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create IPAddressToInterface in Nautobot from IPAddressOnInterface object."""
        new_map = IPAddressToInterface(
            ip_address_id=diffsync.ipaddr_map[attrs["namespace"]][ids["address"]],
            interface_id=diffsync.port_map[ids["device"]][ids["port"]],
        )
        diffsync.objects_to_create["ipaddrs-to-intfs"].append(new_map)
        if attrs.get("primary"):
            if new_map.ip_address.ip_version == 4:
                diffsync.objects_to_create["device_primary_ip4"].append(
                    new_map.interface.device.id, new_map.ip_address.id
                )
            else:
                diffsync.objects_to_create["device_primary_ip6"].append(
                    new_map.interface.device.id, new_map.ip_address.id
                )
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update IP Address in Nautobot from IPAddressOnInterface object."""
        mapping = IPAddressToInterface.objects.get(id=self.uuid)
        if attrs.get("primary"):
            if mapping.ip_address.ip_version == 4:
                self.diffsync.objects_to_create["device_primary_ip4"].append(
                    mapping.interface.device.id, mapping.ip_address.id
                )
            else:
                self.diffsync.objects_to_create["device_primary_ip6"].append(
                    mapping.interface.device.id, mapping.ip_address.id
                )
        mapping.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete IPAddressToInterface in Nautobot from NautobotIPAddressOnInterface object."""
        mapping = IPAddressToInterface.objects.get(id=self.uuid)
        super().delete()
        self.diffsync.job.logger.info(
            f"Deleting IPAddress to Interface mapping between {self.address} and {self.device}'s {self.port} port."
        )
        mapping.delete()
        return self
