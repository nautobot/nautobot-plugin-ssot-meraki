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
