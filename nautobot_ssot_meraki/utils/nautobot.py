"""Utility functions for working with Nautobot."""
from typing import List
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, Platform
from nautobot.extras.models import Relationship, RelationshipAssociation

try:
    from nautobot_device_lifecycle_mgmt.models import SoftwareLCM

    LIFECYCLE_MGMT = True
except ImportError:
    print("Device Lifecycle plugin isn't installed so will revert to CustomField for OS version.")
    LIFECYCLE_MGMT = False


def get_tag_strings(list_tags: TaggableManager) -> List[str]:
    """Gets string values of all Tags in a list.

    This is the opposite of the `get_tags` function.

    Args:
        list_tags (TaggableManager): List of Tag objects to convert to strings.

    Returns:
        List[str]: List of string values matching the Tags passed in.
    """
    _strings = list(list_tags.names())
    if len(_strings) > 1:
        _strings.sort()
    return _strings


def add_software_lcm(version: str):
    """Add OS Version as SoftwareLCM if Device Lifecycle Plugin found."""
    _platform = Platform.objects.get(name="Meraki")
    try:
        os_ver = SoftwareLCM.objects.get(device_platform=_platform, version=version)
    except SoftwareLCM.DoesNotExist:
        os_ver = SoftwareLCM(
            device_platform=_platform,
            version=version,
        )
        os_ver.validated_save()
    return os_ver


def assign_version_to_device(diffsync, device, software_lcm):
    """Add Relationship between Device and SoftwareLCM."""
    software_relation = Relationship.objects.get(label="Software on Device")
    relations = device.get_relationships()
    for _, relationships in relations.items():
        for relationship, queryset in relationships.items():
            if relationship == software_relation:
                if diffsync.job.debug:
                    diffsync.job.logger.warning(
                        f"Deleting Software Version Relationships for {device.name} to assign a new version."
                    )
                queryset.delete()

    new_assoc = RelationshipAssociation(
        relationship=software_relation,
        source_type=ContentType.objects.get_for_model(SoftwareLCM),
        source=software_lcm,
        destination_type=ContentType.objects.get_for_model(Device),
        destination=device,
    )
    diffsync.objects_to_create["relationship_assocs"].append(new_assoc)


def get_dlc_version_map():
    """Method to create nested dictionary of Software versions mapped to their ID along with Platform.

    This should only be used if the Device Lifecycle plugin is found to be installed.

    Returns:
        dict: Nested dictionary of versions mapped to their ID and to their Platform.
    """
    version_map = {}
    for ver in SoftwareLCM.objects.only("id", "device_platform", "version"):
        if ver.device_platform.name not in version_map:
            version_map[ver.device_platform.name] = {}
        version_map[ver.device_platform.name][ver.version] = ver.id
    return version_map


def get_cf_version_map():
    """Method to create nested dictionary of Software versions mapped to their ID along with Platform.

    This should only be used if the Device Lifecycle plugin is not found. It will instead use custom field "OS Version".

    Returns:
        dict: Nested dictionary of versions mapped to their ID and to their Platform.
    """
    version_map = {}
    for dev in Device.objects.only("id", "platform", "_custom_field_data"):
        if dev.platform.name not in version_map:
            version_map[dev.platform.name] = {}
        if "os_version" in dev.custom_field_data:
            version_map[dev.platform.name][dev.custom_field_data["os_version"]] = dev.id
    return version_map
