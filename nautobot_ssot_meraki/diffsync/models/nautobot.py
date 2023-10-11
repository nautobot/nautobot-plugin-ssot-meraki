"""Nautobot DiffSync models for Meraki SSoT."""
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device as NewDevice
from nautobot.dcim.models import Manufacturer, Site, DeviceRole, DeviceType, Interface, Platform
from nautobot.extras.models import Note, Status
from nautobot.ipam.models import IPAddress as OrmIPAddress
from nautobot.ipam.models import Prefix as OrmPrefix
from nautobot.tenancy.models import Tenant
from nautobot_ssot_meraki.diffsync.models.base import Device, Network, Port, Prefix, IPAddress


class NautobotNetwork(Network):
    """Nautobot implementation of Meraki Device model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Site in Nautobot from NautobotNetwork object."""
        new_site = Site(
            name=ids["name"],
            status=Status.objects.get(name="Active"),
            time_zone=attrs["timezone"],
        )
        new_site.validated_save()
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=diffsync.job.request.user,
                assigned_object_type=ContentType.objects.get_for_model(Site),
                assigned_object_id=new_site.id,
            )
            new_note.validated_save()
        if attrs.get("tags"):
            new_site.tags.set(attrs["tags"])
        if attrs.get("tenant"):
            new_site.tenant = Tenant.objects.get(name=attrs["tenant"])
        new_site.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Site in Nautobot from NautobotNetwork object."""
        site = Site.objects.get(id=self.uuid)
        if "timezone" in attrs:
            site.time_zone = attrs["timezone"]
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=self.diffsync.job_result.user,
                assigned_object_type=ContentType.objects.get_for_model(Site),
                assigned_object_id=site.id,
            )
            new_note.validated_save()
        if "tags" in attrs:
            site.tags.set(attrs["tags"])
        if "tenant" in attrs:
            if attrs.get("tenant"):
                site.tenant = Tenant.objects.get(name=attrs["tenant"])
            else:
                site.tenant = None
        site.validated_save()
        return super().update(attrs)


class NautobotDevice(Device):
    """Nautobot implementation of Meraki Device model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Device in Nautobot from NautobotDevice object."""
        cisco_manu = Manufacturer.objects.get(name="Cisco Meraki")
        new_device = NewDevice(
            name=ids["name"],
            platform=Platform.objects.get(name="Meraki"),
            serial=attrs["serial"],
            status=Status.objects.get_or_create(name=attrs["status"])[0],
            device_role=DeviceRole.objects.get_or_create(name=attrs["role"])[0],
            device_type=DeviceType.objects.get_or_create(model=attrs["model"], manufacturer=cisco_manu)[0],
            site=Site.objects.get_or_create(name=attrs["network"])[0],
        )
        new_device.validated_save()
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=diffsync.job.request.user,
                assigned_object_type=ContentType.objects.get_for_model(NewDevice),
                assigned_object_id=new_device.id,
            )
            new_note.validated_save()
        if attrs.get("tags"):
            new_device.tags.set(attrs["tags"])
        if attrs.get("tenant"):
            if attrs.get("tenant"):
                new_device.tenant = Tenant.objects.get(name=attrs["tenant"])
            else:
                new_device.tenant = None
        if attrs.get("version"):
            new_device._custom_field_data["os_version"] = attrs["version"]
        new_device.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Device in Nautobot from NautobotDevice object."""
        device = NewDevice.objects.get(id=self.uuid)
        if "serial" in attrs:
            device.serial = attrs["serial"]
        if "status" in attrs:
            device.status = Status.objects.get_or_create(name=attrs["status"])[0]
        if "role" in attrs:
            device.device_role = DeviceRole.objects.get_or_create(name=attrs["role"])[0]
        if "model" in attrs:
            device.device_type = DeviceType.objects.get_or_create(model=attrs["model"])[0]
        if "network" in attrs:
            device.site = Site.objects.get_or_create(name=attrs["network"])[0]
        if attrs.get("notes"):
            new_note = Note(
                note=attrs["notes"],
                user=self.diffsync.job.request.user,
                assigned_object_type=ContentType.objects.get_for_model(NewDevice),
                assigned_object_id=device.id,
            )
            new_note.validated_save()
        if "tags" in attrs:
            device.tags.set(attrs["tags"])
        if "tenant" in attrs:
            if attrs.get("tenant"):
                device.tenant = Tenant.objects.get(name=attrs["tenant"])
            else:
                device.tenant = None
        if "version" in attrs:
            device._custom_field_data["os_version"] = attrs["version"]
        device.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Device in Nautobot from NautobotDevice object."""
        dev = NewDevice.objects.get(id=self.uuid)
        super().delete()
        dev.delete()
        return self


class NautobotPort(Port):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Interface in Nautobot from NautobotDevice object."""
        new_port = Interface.objects.create(
            name=ids["name"],
            device=NewDevice.objects.get(name=ids["device"]),
            enabled=attrs["enabled"],
            mode="access" if not attrs["tagging"] else "tagged",
            mgmt_only=attrs["management"],
            type=attrs["port_type"],
            status=Status.objects.get(name=attrs["port_status"]),
        )
        new_port.validated_save()
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
            port.status = Status.objects.get(name=attrs["port_status"])
        port.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Interface in Nautobot from NautobotDevice object."""
        port = Interface.objects.get(id=self.uuid)
        super().delete()
        port.delete()
        return self


class NautobotPrefix(Prefix):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Prefix in Nautobot from NautobotPrefix object."""
        new_pf = OrmPrefix.objects.create(
            prefix=ids["prefix"], site=Site.objects.get(name=ids["location"]), status=Status.objects.get(name="Active")
        )
        new_pf.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def delete(self):
        """Delete Prefix in Nautobot from NautobotPrefix object."""
        del_pf = OrmPrefix.objects.get(id=self.uuid)
        super().delete()
        del_pf.delete()
        return self


class NautobotIPAddress(IPAddress):
    """Nautobot implementation of Meraki Port model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create IPAddress in Nautobot from NautobotIPAddress object."""
        new_ip = OrmIPAddress.objects.create(
            address=ids["address"],
            status=Status.objects.get(name="Active"),
        )
        new_ip.validated_save()
        if attrs.get("device") and attrs.get("port"):
            try:
                dev = NewDevice.objects.get(name=attrs["device"])
                intf = Interface.objects.get(name=attrs["port"], device=dev)
                new_ip.assigned_object_type = ContentType.objects.get_for_model(Interface)
                new_ip.assigned_object_id = intf.id
                new_ip.validated_save()

                if attrs.get("primary"):
                    if new_ip.family == 4:
                        dev.primary_ip4 = new_ip
                    else:
                        dev.primary_ip6 = new_ip
                dev.validated_save()
            except NewDevice.DoesNotExist:
                diffsync.job.log_warning(message=f"Unable to find Device {attrs['device']} to assign {new_ip.address}.")
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update IPAddress in Nautobot from NautobotIPAddress object."""
        ip = OrmIPAddress.objects.get(id=self.uuid)
        if "port" in attrs and "device" not in attrs:
            intf = Interface.objects.get(name=attrs["port"], device=NewDevice.objects.get(name=self.device))
            intf.assigned_object_id = ip.id
            intf.validated_save()
        if "device" in attrs:
            dev = NewDevice.objects.get(name=attrs["device"])
            if attrs.get("port"):
                intf = Interface.objects.get(name=attrs["port"], device=dev)
                intf.assigned_object_id = ip.id
                intf.validated_save()
        if "primary" in attrs:
            dev = ip.assigned_object.device
            if ip.family == 4:
                dev.primary_ip4 = ip
            else:
                dev.primary_ip6 = ip
            dev.validated_save()
        if "tenant" in attrs:
            if attrs.get("tenant"):
                ip.tenant = Tenant.objects.get(name=attrs["tenant"])
            else:
                ip.tenant = None
        ip.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete IPAddress in Nautobot from NautobotIPAddress object."""
        ip = OrmIPAddress.objects.get(id=self.uuid)
        super().delete()
        ip.delete()
        return self
