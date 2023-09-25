"""Nautobot SSoT for Meraki Adapter for Meraki SSoT plugin."""

from diffsync import DiffSync


class MerakiAdapter(DiffSync):
    """DiffSync adapter for Meraki."""

    top_level = []

    def __init__(self, *args, job=None, sync=None, client=None, **kwargs):
        """Initialize Meraki.

        Args:
            job (object, optional): Meraki job. Defaults to None.
            sync (object, optional): Meraki DiffSync. Defaults to None.
            client (object): Meraki API client connection object.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync
        self.conn = client

    def load(self):
        """Load data from Meraki into DiffSync models."""
        raise NotImplementedError
