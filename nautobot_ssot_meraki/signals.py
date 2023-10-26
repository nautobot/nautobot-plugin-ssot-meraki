"""Signals triggered when Nautobot starts to perform certain actions."""
from nautobot.extras.choices import CustomFieldTypeChoices


def nautobot_database_ready_callback(sender, *, apps, **kwargs):  # pylint: disable=unused-argument
    """Adds OS Version and Physical Address CustomField to Devices and System of Record and Last Sync'd to Device, and IPAddress.

    Callback function triggered by the nautobot_database_ready signal when the Nautobot database is fully ready.
    """
    # pylint: disable=invalid-name, too-many-locals
    ContentType = apps.get_model("contenttypes", "ContentType")
    CustomField = apps.get_model("extras", "CustomField")
    Device = apps.get_model("dcim", "Device")
    Interface = apps.get_model("dcim", "Interface")
    IPAddress = apps.get_model("ipam", "IPAddress")
    Manufacturer = apps.get_model("dcim", "Manufacturer")
    Platform = apps.get_model("dcim", "Platform")

    cisco_manu = Manufacturer.objects.get_or_create(name="Cisco Meraki")[0]
    plat_dict = {
        "name": "Meraki",
        "manufacturer": cisco_manu,
        "slug": "meraki",
        "network_driver": "meraki",
    }
    Platform.objects.update_or_create(name__icontains="Meraki", defaults=plat_dict)
    os_cf_dict = {
        "name": "os_version",
        "slug": "os_version",
        "type": CustomFieldTypeChoices.TYPE_TEXT,
        "label": "OS Version",
    }
    ver_field, _ = CustomField.objects.get_or_create(name=os_cf_dict["name"], defaults=os_cf_dict)
    ver_field.content_types.add(ContentType.objects.get_for_model(Device))

    sor_cf_dict = {
        "type": CustomFieldTypeChoices.TYPE_TEXT,
        "name": "system_of_record",
        "slug": "system_of_record",
        "label": "System of Record",
    }
    sor_custom_field, _ = CustomField.objects.update_or_create(name=sor_cf_dict["name"], defaults=sor_cf_dict)
    sync_cf_dict = {
        "type": CustomFieldTypeChoices.TYPE_DATE,
        "name": "ssot_last_synchronized",
        "slug": "ssot_last_synchronized",
        "label": "Last sync from System of Record",
    }
    sync_custom_field, _ = CustomField.objects.update_or_create(name=sync_cf_dict["name"], defaults=sync_cf_dict)
    for model in [Device, Interface, IPAddress]:
        sor_custom_field.content_types.add(ContentType.objects.get_for_model(model))
        sync_custom_field.content_types.add(ContentType.objects.get_for_model(model))
