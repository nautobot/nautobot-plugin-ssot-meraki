"""Nautobot DiffSync models for Meraki SSoT."""
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device as NewDevice
from nautobot.dcim.models import Manufacturer, Site, DeviceRole, DeviceType
from nautobot.extras.models import Note, Status
from nautobot.tenancy.models import Tenant
from nautobot_ssot_meraki.diffsync.models.base import Device, Network


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
        cisco_manu = Manufacturer.objects.get_or_create(name="Cisco")[0]
        new_device = NewDevice(
            name=ids["name"],
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
            new_device.tenant = Tenant.objects.get(name=attrs["tenant"])
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
