"""Nautobot SSoT for Meraki Adapter for Meraki SSoT plugin."""

from diffsync import DiffSync
from diffsync.exceptions import ObjectNotFound
from nautobot_ssot_meraki.diffsync.models.meraki import MerakiNetwork, MerakiDevice


class MerakiAdapter(DiffSync):
    """DiffSync adapter for Meraki."""

    network = MerakiNetwork
    device = MerakiDevice

    top_level = ["network", "device"]

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

    def load_networks(self):
        """Load networks from Meraki dashboard into DiffSync models."""
        for net in self.conn.get_org_networks():
            try:
                self.get(self.network, net["name"])
                self.job.log_warning(message=f"Duplicate network {net['name']} found and being skipped.")
            except ObjectNotFound:
                if self.tenant:
                    tenant = self.tenant.name
                else:
                    tenant = None
                new_network = self.network(
                    name=net["name"],
                    timezone=net["timeZone"],
                    notes=net["notes"] if net.get("notes") else "",
                    tags=net["tags"],
                    tenant=tenant,
                    uuid=None,
                )
                self.add(new_network)

    def load(self):
        """Load data from Meraki into DiffSync models."""
        if self.conn.validate_organization_exists():
            self.load_networks()
        else:
            self.job.log_failure(message="Specified organization ID not found in Meraki dashboard.")
