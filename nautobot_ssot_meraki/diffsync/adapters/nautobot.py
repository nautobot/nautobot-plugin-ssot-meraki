"""Nautobot Adapter for Meraki SSoT plugin."""

from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from nautobot.dcim.models import Site
from nautobot_ssot_meraki.diffsync.models.nautobot import NautobotDevice, NautobotNetwork
from nautobot_ssot_meraki.utils.nautobot import get_tag_strings


class NautobotAdapter(DiffSync):
    """DiffSync adapter for Nautobot."""

    network = NautobotNetwork
    device = NautobotDevice

    top_level = ["network", "device"]

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Nautobot.

        Args:
            job (object, optional): Nautobot job. Defaults to None.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load_sites(self):
        """Load Site data from Nautobot into DiffSync model."""
        for site in Site.objects.all():
            try:
                self.get(self.network, site.name)
            except ObjectNotFound:
                new_site = self.network(
                    name=site.name,
                    notes="",
                    tags=get_tag_strings(list_tags=site.tags),
                    timezone=site.time_zone.zone,
                    tenant=site.tenant.name if site.tenant else None,
                    uuid=site.id,
                )
                if site.notes:
                    note = site.notes.first()
                    new_site.note = note.note
                self.add(new_site)

    def load(self):
        """Load data from Nautobot into DiffSync models."""
        self.load_sites()
