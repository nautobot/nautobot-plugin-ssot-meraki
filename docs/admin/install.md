# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

!!! warning "Developer Note - Remove Me!"
    Detailed instructions on installing the App. You will need to update this section based on any additional dependencies or prerequisites.

## Prerequisites

- The plugin is compatible with Nautobot 1.6.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

Access to the Meraki dashboard at https://dashboard.meraki.com from your Nautobot instance is required.

## Install Guide

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this plugin is [`nautobot-ssot-meraki`](https://pypi.org/project/nautobot-ssot-meraki/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-ssot-meraki
```

To ensure Nautobot SSoT for Meraki is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-ssot-meraki` package:

```shell
echo nautobot-ssot-meraki >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_ssot_meraki"` to the `PLUGINS` list.
- Append the `"nautobot_ssot_meraki"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_ssot", "nautobot_ssot_meraki"]

PLUGINS_CONFIG = {
    "nautobot_ssot": {
        "hide_example_jobs": True,
    },
    "nautobot_ssot_meraki": {
        "meraki_org_id": os.getenv("MERAKI_ORG_ID", ""),
        "meraki_token": os.getenv("MERAKI_TOKEN", ""),
        "update_locations": is_truthy(os.getenv("NAUTOBOT_DNAC_SSOT_UPDATE_LOCATIONS", False)),
        "hostname_mapping": [],
        "devicetype_mapping": [],
    },
}
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

!!! warning "Developer Note - Remove Me!"
    Any configuration required to get the App set up. Edit the table below as per the examples provided.

The plugin behavior can be controlled with the following list of settings:

| Key                  | Example                  | Default  | Description                                                                                  |
| -------------------- | ------------------------ | -------- | -------------------------------------------------------------------------------------------- |
| `meraki_org_id`      |      `12345`             |    ``    | A string representing the organization ID to use when querying the Meraki dashboard.         |
| `meraki_token`       |      `123456abcde`       |    ``    | A string representing the authentication token to use querying the Meraki dashboard.         |
| `update_locations`   |      True                |   False  | Boolean value to determine whether locations should be updated if found during a sync.       |
| `hostname_mapping`   | [(".*FW.*", "Firewall")] |   []     | List of tuples containing a regex pattern to comparse hostname against and Role name.        |
| `devicetype_mapping` |   [("MX", "Firewall")]   |   []     | List of tuples containing a model series, ie MR, and the defined Role name.                  |
