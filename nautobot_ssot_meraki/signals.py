"""Signals triggered when Nautobot starts to perform certain actions."""
from nautobot.extras.choices import CustomFieldTypeChoices


def nautobot_database_ready_callback(sender, *, apps, **kwargs):  # pylint: disable=unused-argument
    """Adds OS Version and Physical Address CustomField to Devices and System of Record and Last Sync'd to Device, and IPAddress.

    Callback function triggered by the nautobot_database_ready signal when the Nautobot database is fully ready.
    """
    # pylint: disable=invalid-name, too-many-locals
    ContentType = apps.get_model("contenttypes", "ContentType")
    CustomField = apps.get_model("extras", "CustomField")
    LocationType = apps.get_model("dcim", "LocationType")
    Device = apps.get_model("dcim", "Device")
    Interface = apps.get_model("dcim", "Interface")
    Prefix = apps.get_model("ipam", "Prefix")
    IPAddress = apps.get_model("ipam", "IPAddress")
    Manufacturer = apps.get_model("dcim", "Manufacturer")
    Platform = apps.get_model("dcim", "Platform")

    site = LocationType.objects.update_or_create(name="Site", nestable=True)[0]
    site.content_types.add(ContentType.objects.get_for_model(Device))
    site.content_types.add(ContentType.objects.get_for_model(Prefix))

    cisco_manu = Manufacturer.objects.get_or_create(name="Cisco Meraki")[0]
    plat_dict = {
        "name": "Meraki",
        "manufacturer": cisco_manu,
        "network_driver": "meraki",
    }
    Platform.objects.update_or_create(name__icontains="Meraki", defaults=plat_dict)
    os_cf_dict = {
        "key": "os_version",
        "type": CustomFieldTypeChoices.TYPE_TEXT,
        "label": "OS Version",
    }
    ver_field, _ = CustomField.objects.get_or_create(key=os_cf_dict["key"], defaults=os_cf_dict)
    ver_field.content_types.add(ContentType.objects.get_for_model(Device))

    sor_cf_dict = {
        "type": CustomFieldTypeChoices.TYPE_TEXT,
        "key": "system_of_record",
        "label": "System of Record",
    }
    sor_custom_field, _ = CustomField.objects.update_or_create(key=sor_cf_dict["key"], defaults=sor_cf_dict)
    sync_cf_dict = {
        "type": CustomFieldTypeChoices.TYPE_DATE,
        "key": "ssot_last_synchronized",
        "label": "Last sync from System of Record",
    }
    sync_custom_field, _ = CustomField.objects.update_or_create(key=sync_cf_dict["key"], defaults=sync_cf_dict)
    for model in [Device, Interface, Prefix, IPAddress]:
        sor_custom_field.content_types.add(ContentType.objects.get_for_model(model))
        sync_custom_field.content_types.add(ContentType.objects.get_for_model(model))
