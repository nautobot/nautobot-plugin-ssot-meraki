# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!--next-version-placeholder-->

## v0.3.0 (2023-09-27)

### Feature

* ✨ Add CRUD functions for creating Devices in Nautobot ([`62d7073`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/62d707329d321b4572fac38939c0b218046c99fc))
* ✨ Add load_devices function to Nautobot adapter. ([`a92e6df`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/a92e6df277bc99ac10c17181adbcdea5cd1ffcbb))
* ✨ Add version attribute to Device DiffSync model. ([`990ca14`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/990ca140fe0d8adb2cdacb33387e689326ca0382))
* ✨ Add OS Version CustomField to be created in database ready signal. ([`e02facd`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/e02facdb0ca9ef7b400f17e540dfc2e166c957d8))
* ✨ Add load_devices function to Meraki adapter. ([`95eb967`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/95eb967e9694e52b6fcca0a7af16e3e6bd4465b2))
* ✨ Add notes attribute to Device DiffSync model. ([`60eae11`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/60eae1161b501c918f1c3bdb2681e861bce60691))
* ✨ Add function to parse hostname for device role ([`25a23e1`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/25a23e17dd520d9eb7198fe0b158f6910d24b572))

### Fix

* ✅ Update test fixture to match correct expected setup for map. ([`26bac8d`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/26bac8d2ef4cc66d5a342867c3f49344d5090e0a))
* 🐛 Ensure latest note loaded into device DiffSync model. ([`509d3c3`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/509d3c3a59d87099ed0267c257f267ff83799515))
* 🐛 Update device load to ignore Devices without hostname and log warning if found. ([`0e2bf1f`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/0e2bf1fb6981990f067f39737a4fe10d1313ca7a))
* 🐛 Specify Site model for updating tags ([`e22ad20`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/e22ad20f16f65b95396cfb83745ac8765a283169))

## v0.2.0 (2023-09-27)

### Feature

* ✨ Update Job Form to specify Tenant to be assigned to Networks/Devices ([`c828a1b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/c828a1be7ad4d7d5667f7c9a62e352ea4d3248b5))
* ✨ Update Site CRUD functions to handle all attrs and add tags in create ([`f8e4f61`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/f8e4f6183dc3f6424fecc76be8ebbd3f2fcad340))
* ✨ Add function to load Sites from Nautobot into Network model ([`14dc607`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/14dc6078b6260af625e9e954e15d934db32c9ee2))
* ✨ Add tenant to Network & Device, add serial to Device base models ([`72c387b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/72c387b5c05e03fe9fce74caa13bed3d2874ab41))
* ✨ Add function to get Device status ([`7a84e4d`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/7a84e4da6cbf76ae39265fa127b829cd127fc99d))
* ✨ Add network map to DashboardClient ([`1235e6b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/1235e6b6e02de66a21bc7638524e301629fdc92b))
* ✨ Add function to load networks into DiffSync model ([`d8b93f0`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/d8b93f0382e14aad4129269e6bbb86a7ff1c6b8a))
* ✨ Add MerakiNetwork model and correct docstrings for MerakiDevice ([`4956d01`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/4956d017b61637a354a3d0fa4f3ae2c9319a20bc))
* ✨ Add DashboardClient class for interacting with API. ([`141cee6`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/141cee65f60b2d52778a362e0950a8a409a632f7))
* Update Device base model ([`add767f`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/add767f3042d12054add891ac6a91cc924402898))
* Add network base model ([`7e4acbc`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/7e4acbcdc153e598ef4d703f6f1c624a39b89eda))
* ✨ Add initial SSoT structure ([`4870d81`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/4870d81d7001f17f019e4deaea54458c82d1701b))

### Fix

* 🐛 Correct attribute to notes ([`f06f86d`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/f06f86d9f1c36563d208517f0917934bea329388))
* 🐛 Correct timezone name to be pulled from zone attribute on time_zone object. ([`159dd96`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/159dd96eabd6660193ca355417d1aba0aa296986))
* 🐛 Correct UUID to be pulled from self and not attrs ([`e2ec226`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/e2ec226df07d73951cef23a25e46c8b3ebda52ee))
* 🐛 Update Job to use DashboardClient and use PLUGIN_CFG settings ([`a925916`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/a9259161c24cf0513f51f26139f401b1c3564af5))

### Documentation

* 📝 Correct docstrings ([`b929083`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/b9290834b2f941c9e34af7965e6ce7b5a08dab6c))
