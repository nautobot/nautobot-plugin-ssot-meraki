"""Collection of fixtures to be used for unit testing."""
import json


def load_json(path):
    """Load a json file."""
    with open(path, encoding="utf-8") as file:
        return json.loads(file.read())


GET_ORG_NETWORKS_SENT_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_networks_sent.json")
GET_ORG_NETWORKS_RECV_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_networks_recv.json")
NETWORK_MAP_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/network_map.json")
GET_ORG_DEVICES_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_devices.json")
GET_DEVICE_STATUSES_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_device_statuses.json")
GET_MANAGEMENT_PORT_NAMES_SENT_FIXTURE = load_json(
    "./nautobot_ssot_meraki/tests/fixtures/get_management_port_names_sent.json"
)
GET_ORG_SWITCHPORTS_SENT_FIXTURE = load_json("./nautobot_ssot_meraki/tests/fixtures/get_org_switchports_sent.json")
GET_ORG_UPLINK_STATUSES_SENT_FIXTURE = load_json(
    "./nautobot_ssot_meraki/tests/fixtures/get_org_uplink_statuses_sent.json"
)
GET_SWITCHPORT_STATUSES = load_json("./nautobot_ssot_meraki/tests/fixtures/get_switchport_statuses.json")
GET_UPLINK_SETTINGS = load_json("./nautobot_ssot_meraki/tests/fixtures/get_uplink_settings.json")
