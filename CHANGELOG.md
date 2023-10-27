# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!--next-version-placeholder-->

## v0.7.0 (2023-10-27)

### Feature

* ✨ Add Tenant to Prefix object and update CRUD functions. ([`3a5cc61`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/3a5cc619f00421d583d7f962bc1c1d1ca083f4bd))
* ✨ Add ability to use Device model to determine DeviceRole. ([`729c666`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/729c6667d938dd7b1087bc4a8cc13edd7b623b94))

### Fix

* 🐛 Correct user definition for updating Notes on Device ([`d72c342`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/d72c34281aec9535cec186bfead47eca974dbc5b))

### Documentation

* 📝 Update documentation to add info about plugin settings and remove unnecessary bits. ([`13743d6`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/13743d6c5405f6d1ba50163d813cf8dc132557e5))

## v0.6.0 (2023-10-26)

### Feature

* ✨ Add SSoT CustomFields to denote origin of object and last update. ([`da6054d`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/da6054dc9858c6ed95522118e739590a0a509327))

### Fix

* 🐛 Ensure SoT CustomField is applied to Ports and set right on Device and Site ([`29eb491`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/29eb49189124242cd20b6061364809744c4e6e07))
* 🐛 Validate that timezone is defined in Site before trying to load value. ([`02b0444`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/02b0444bbc20c2332de60f475a76e838e885d719))

## v0.5.0 (2023-10-12)

### Feature

* ✨ Add support for Device Lifecycle Mgmt App if found installed. ([`19a07c3`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/19a07c3d72be59c4ac40cdd7db991485a5ca3fd7))

### Fix

* 🐛 Correct function call to updated name. ([`1a5fb9c`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/1a5fb9c8b4d8976605dea486621860366cf2c304))

## v0.4.0 (2023-10-12)

### Feature

* ✨ Add Tenant attribute to IPAddress DiffSync model. ([`22987aa`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/22987aa0beba4fe2e9c5f5f2df208930a60ed8ef))
* ✨ Add Prefix DiffSync model to keep track of involved Prefixes ensure no duplicates. ([`976baa2`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/976baa23bd7d1de8d330d097432ead73b2ac3dab))
* ✨ Add CRUD functions for NautobotIPAddress ([`d8c1228`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/d8c1228e29f921144bbea994eed1cf5c28565120))
* ✨ Add load functions to both Adapters to pull in IP information and fill DiffSync models. ([`b386f6b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/b386f6b0fa5c0c64fd6626f626812418d6feee3d))
* ✨ Add MerakiIPAddress class ([`85a8363`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/85a83632736e2c633130d9b77e44dc42dc2371d3))
* ✨ Add base IPAddress DiffSync model. ([`50583da`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/50583dae2fca1a614024f5b50b635937c509dc74))
* ✨ Add function for loading MR ports ([`a86a917`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/a86a917ea688fba4b344a14974bf54316eccf0b9))
* ✨ Add function to load ports for MS devices ([`09b4dbe`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/09b4dbe9ce5b43e9ef1fb9644122b071a53568d0))
* ✨ Add function to get appliance switchports for MX, MG, and Z devices ([`2249a8b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/2249a8b2b9f57636ac7976421776c49526e8b1b0))
* ✨ Add CRUD functions for imported Ports ([`36d7050`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/36d70509bb6e4754d99d0cdbfc1e61aac5572653))
* ✨ Add function to load ports in Nautobot adapter ([`fb07775`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/fb07775bbcca14b65e47247d7e68f5eddce98339))
* ✨ Add function to retrieve statuses for switch ports. ([`8d7eee6`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/8d7eee6e11ef35d63a6be46f9db70ca91457dbe6))
* ✨ Add function to retrieve all ports for switches in organization ([`85368f6`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/85368f63c0fe665b0d242399944d05b37e82f32a))
* ✨ Add MerakiPort model ([`011b2e9`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/011b2e9215cde0520210b281cd60e890b18c2cdf))
* ✨ Add function to load management ports for devices. ([`1e6db93`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/1e6db932c1d2362555133cc78b5004cd78a2784c))
* ✨ Create functions to grab information about uplink settings and statuses for loading ports. ([`d7a187b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/d7a187b190a9ab9ca1524d35c2a630b64d1f3d0a))
* ✨ Add device map for referencing device information later. ([`5e47d12`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/5e47d12d69eb6b872e55a1836b1245497f72bdd5))
* ✨ Add Port DiffSync model. ([`10586c9`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/10586c9bc5a4c972b31d8ed4c280bd600f240d77))

### Fix

* 🐛 Redo how primary IP is set so first Active interface is assigned as primary when multiple found. ([`abb1a8c`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/abb1a8c1b6d0c09e6d0a0f13fd8d826b302f8ffe))
* 🐛 Redo updating of primary to check value of primary attr ([`b8d2095`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/b8d2095954ddf7c1ce9ee76e34e646bf3d8394f1))
* 🐛 Correct address to include cidr notation. ([`1d7a746`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/1d7a746b6de9410d5307d35d60d47c42088dff88))
* 🐛 Correct filter to be icontains ([`78609e6`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/78609e6d72814d75b3a095f4771bc0943a03176d))
* 🐛 Correct prefix to use network ([`96b11ac`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/96b11acf523d1f462f051902b8d9ef16db030f66))
* 🐛 Ensure IPAddress object is saved once assigned. ([`769aa5b`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/769aa5b49f026004d5f9e26a5cfce20ae7d20f09))
* 🐛 Correct use of interfaces key to only happen if API request successful. ([`b1140e1`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/b1140e136ccffa2196c56038b6fa480397355120))
* 🐛 Correct get_management_ports to return API result. ([`e2e563d`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/e2e563d04fc5080a8a1cce3606c7c9e54520c797))
* 🐛 Specify Platform during device creation. ([`7c556f1`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/7c556f1c7a16d6bac76b9af337c96dc2306b5a59))
* 🐛 Correct object call to NewDevice to address conflict from DiffSync model of same name. ([`0f5b1a1`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/0f5b1a1da71c7c701a6d2b9377c48511d4dbb2d9))

### Documentation

* 📝 Clarify function applies only to MS devices ([`e0e395a`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/e0e395acb7020ac306b733ec6480df55928f6f5f))
* 📝 Update docstrings to note raises and returns ([`fa994b3`](https://github.com/networktocode-llc/nautobot-plugin-ssot-meraki/commit/fa994b3e2ed9ca69d3be9ed16be85efcfab69f35))

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
