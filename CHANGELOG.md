cloudflare-warp (2026.6.822) unstable; urgency=medium
  This release introduces multiple features from our previous beta release into stable release, including:

  * The client now applies DNS search suffixes configured in your device profile / network policy. Administrators can push a list of DNS search domains that the client appends to single-label queries, alongside any system-configured suffixes. See [DNS search suffixes](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/settings/#dns-search-suffixes) for details.
  * Upgraded security of device registration to be hardware-backed. Registration tokens can now be generated in the TPM (with TPM 2.0+) whenever it is available to provide stronger protection against device impersonation. See [Hardware-backed registration](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/deployment/mdm-deployment/hardware-backed-registration/) for details.
  * Added a local-file signal source for Emergency Disconnect. In addition to the existing HTTPS polling mechanism, administrators can now configure WARP to monitor for a file on disk; the presence of the file triggers an emergency disconnect even if both Cloudflare and your own infrastructure are unreachable. Either signal being asserted triggers disconnect; both must be cleared for normal operation to resume.
  * Added new warp-cli debug commands for interactive connection diagnosis. See [Extra debug logging](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/troubleshooting/diagnostic-logs/#extra-debug-logging) for details.
  * The local DNS proxy now supports DNSSEC passthrough. DNSSEC-signed responses are forwarded to the application intact (including DO/AD bits and RRSIG records), so applications that validate DNSSEC locally — including resolvers and the dig/drill tooling — work correctly through the client.
  * Added a new MDM format for organization-wide settings, including a cleaner way to configure the compliance environment (e.g. FedRAMP). The previous per-configuration approach still works, but the new format is now recommended. See the updated [Cloudflare One MDM documentation](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/deployment/mdm-deployment/parameters/#organization_configs) for details.

  Additional changes and improvements:
  * Cloudflare Mesh functionality using the Cloudflare One Client is now supported on RHEL 9 and 10.
  * Cloudflare Mesh now supports hostname-based routing for Cloudflare Tunnel.
  * Client Certificate device-posture checks now support template variables (e.g. `${serial_number}`, `${device_uuid}`) in the Subject Alternative Name field. Previously only the Common Name field accepted variables, which broke posture rules that pinned identity to a SAN entry.
  * Improved accessibility by using high contrast colors and more defined color boundaries when high contrast is enabled in the system display settings.
  * Path MTU Discovery (PMTUD) is now enabled by default.
  * Fixed the in-client captive-portal browser rendering a blank "Success" page on some airline Wi-Fi networks. The browser now more consistently loads the airline's real portal page so users can complete sign-in from inside the client instead of having to open a separate browser.
  * Fixed an issue in proxy mode where hostnames containing underscores (e.g. ai_app.com) were rejected, breaking apps that depend on such hostnames (notably ChatGPT sandbox apps). The local proxy now accepts underscore-containing hostnames in CONNECT requests.
  * Fixed an issue where DNS queries would fail after the connection was idle, requiring users to retry.
  * Fixed an issue where some Debian releases experienced inaccurate version reporting for posture checks.
  * Users can now register with team names in any case format without errors.
  * New UI fixes:
    * Fixed an issue where users with invalid MDM configurations were returned to the onboarding screen after successful authentication.
    * Added a re-auth button and banner to the home screen so users don't miss it when their session expires.
    * Added clear error messaging when the Cloudflare certificate needs to be installed.
    * Brought back support for pausing the tunnel when connected to user-specified Wi-Fi networks for consumer users.
    * New client UI now surfaces Split tunnel configuration and Local Domain Fallback configuration.
    * Added ability to configure proxy mode for consumer users.
    * Added back the option to quit for consumer users.

  For RHEL deployments, this release introduces a dependency on the Extra Packages for Enterprise Linux repository (EPEL). The EPEL repository provides packages that support the captive portal detection’s in-app browser authentication and system tray icon. See https://docs.fedoraproject.org/en-US/epel/getting-started/ for instructions on enabling EPEL.

  Known issues
  * Registration may hang at "Checking your organization configuration" due to IPC errors. A system reboot should resolve the error, allowing registration to proceed.

 -- Shrey Amin <samin@cloudflare.com>  Mon, 29 Jun 2026 09:53:49 -0400

cloudflare-warp (2026.5.1155) unstable; urgency=medium
  This release introduces the new Cloudflare One Client UI for Linux! You can expect a cleaner and more intuitive design as well as easier access to common actions and information. Here are some of the many things we have found our users appreciate:

  * Right click context menu to access the most common client actions quickly
  * Built-in captive portal login experience

  Changes and improvements:
  * Official support for Ubuntu 26.04 LTS has been added.
  * The client now applies DNS search suffixes configured in your WARP device profile / network policy. Administrators can push a list of DNS search domains that the client appends to single-label queries, alongside any system-configured suffixes. See [DNS search suffixes](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/settings/#dns-search-suffixes) for details.
  * Administrators can now control which virtual networks (VNETs) are available to which users via WARP device profile settings in the Zero Trust dashboard. Previously, every VNET in the organization was visible to every device; you can now scope the VNET picker per profile so users only see the networks relevant to them. See [VNET availability](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/settings/#vnet-availability) for details.
  * WARP Connector now supports hostname-based routing. Administrators can define connector routes using stable hostnames instead of CIDR blocks, removing the need to maintain explicit IP ranges for cloud workloads with dynamic IPs. A new connector configuration also enables NAT mode, which masquerades forwarded tunnel traffic so it appears to originate from the connector host's LAN IP — eliminating the requirement to add static routes for the CGNAT range on every device on the private network.
  * Added a local-file signal source for Emergency Disconnect. In addition to the existing HTTPS polling mechanism, administrators can now configure WARP to monitor for a file on disk; the presence of the file triggers an emergency disconnect even if both Cloudflare and your own infrastructure are unreachable. Either signal being asserted triggers disconnect; both must be cleared for normal operation to resume.
  * Added new warp-cli debug commands for interactive connection diagnosis. See [Extra debug logging](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/troubleshooting/diagnostic-logs/#extra-debug-logging) for details.
  * The local DNS proxy now supports DNSSEC passthrough. DNSSEC-signed responses are forwarded to the application intact (including DO/AD bits and RRSIG records), so applications that validate DNSSEC locally — including resolvers and the dig/drill tooling — work correctly through the client.
  * Added a new MDM format for organization-wide settings, including a cleaner way to configure the compliance environment (e.g. FedRAMP). The previous per-configuration approach still works, but the new format is now recommended. See the updated [Cloudflare One MDM documentation](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/deployment/mdm-deployment/parameters/#organization_configs) for details.
  * Client Certificate device-posture checks now support template variables (e.g. `${serial_number}`, `${device_uuid}`) in the Subject Alternative Name field, matching what the documentation has always claimed. Previously only the Common Name field accepted variables, which broke posture rules that pinned identity to a SAN entry.
  * Support for Ubuntu 20.04 has been removed; it has reached the end of standard support. Customers still on 20.04 should plan an upgrade — the client may continue to install but is no longer tested or supported on that release.
  * Fixed an issue where the WARP tunnel could silently stop carrying traffic on Linux when systemd-networkd restarted (for example, during an unattended apt upgrade). The client now monitors netlink for rule deletions and automatically reconnects to rebuild its routing table and policy rule, restoring connectivity without manual intervention.
  * Fixed reported os_version on newer Debian releases (Debian 13 and any kernel carrying a +debNN+M suffix). Previously the kernel build suffix could cause Cloudflare One device-posture OS-version checks to fail; the client now reports the kernel version in the canonical form posture rules expect.
  * Fixed an issue in proxy mode where hostnames containing underscores (e.g. ai_app.com) were rejected, breaking apps that depend on such hostnames (notably ChatGPT sandbox apps). The local proxy now accepts underscore-containing hostnames in CONNECT requests.

  Known issues
  * Registration may hang at "Checking your organization configuration" due to IPC errors. A system reboot should resolve the error, allowing registration to proceed.
  * Split tunnel list configuration is not available in the new UI. Management of Split Tunnel entries is currently only possible via `warp-cli tunnel ip` and `warp-cli tunnel host`. UI support will be added in a future release.

 -- Yi Huang <yi@cloudflare.com>  Thu, 28 May 2026 10:00:00 -0700

cloudflare-warp (2026.4.1350) unstable; urgency=medium
  This release introduces the new Cloudflare One Client UI for Linux! You can expect a cleaner and more intuitive design as well as easier access to common actions and information. Here are some of the many things we have found our users appreciate:

  * Right click context menu to access the most common client actions quickly
  * Built-in captive portal login experience

  Changes and improvements:
  * Added a new CLI command: warp-cli mdm refresh. This command executes an immediate refresh of the Mobile Device Management (MDM) configuration file.
  * Official support for RHEL 9 has been added for Cloudflare Mesh nodes. To install the RHEL 9 package, the Extra Packages for Enterprise Linux (EPEL) repository must be active, as it contains dependencies required for the tray icon and captive portal webview.

  Known issues
  * Registration may hang at "Checking your organization configuration" due to IPC errors. A system reboot should resolve the error, allowing registration to proceed.

 -- Yi Huang <yi@cloudflare.com>  Fri, 08 May 2026 10:12:52 -0700

cloudflare-warp (2026.3.846) unstable; urgency=medium
  This release contains minor fixes and improvements.

  The next stable release for Linux will introduce the new Cloudflare One Client UI, providing a cleaner and more intuitive design as well as easier access to common actions and information.

  * Empty MDM files are now rejected instead of being incorrectly accepted as a single MDM config
  * Fixed various connection hangs in proxy mode caused by upstream quiche bugs
  * Fixed an issue where the emergency disconnect status of a prior organization persisted after a switch to a different organization.
  * Consumer-only CLI commands are now clearly distinguished from Zero Trust commands
  * Added detailed QUIC connection metrics to diagnostic logs for better troubleshooting
  * Added monitoring for tunnel statistics collection timeouts
  * Switched tunnel congestion control algorithm to Cubic for improved reliability across platforms
  * Fixed initiating managed network detections checks when no network is available, which caused device profile flapping

 -- Rhett Griggs <rhett@cloudflare.com>  Thu, 02 Apr 2026 12:00:00 -0700

cloudflare-warp (2026.3.567) unstable; urgency=medium
  This release contains minor fixes and introduces a brand new visual style for the client interface! The new Cloudflare One Client interface changes the connectivity management from a toggle to a button and brings useful connectivity settings to the homescreen. The redesign also introduces a collapsible navigation bar. When expanded, more client information can be accessed including connectivity, settings, and device profile information. If you have any feedback or questions to share, please visit the community forum topic and let us know.

  * Empty MDM files are now rejected instead of being incorrectly accepted as a single MDM config
  * Fixed various connection hangs in proxy mode caused by upstream quiche bugs
  * Fixed emergency disconnect state from a previous organization incorrectly persisting after switching organizations
  * Consumer-only CLI commands are now clearly distinguished from Zero Trust commands
  * Added detailed QUIC connection metrics to diagnostic logs for better troubleshooting
  * Added monitoring for tunnel statistics collection timeouts
  * Switched tunnel congestion control algorithm to Cubic for improved reliability across platforms
  * Fixed initiating managed network detections checks when no network is available, which caused device profile flapping

  Known issues
  * The client may become stuck in a "connecting" state. To resolve this issue, either 1. press the "disconnect" and then "connect" button in the client or 2. change the client's operation modes.
  * The client may display an empty white screen upon the device waking from sleep. To resolve this issue, exit and then open the client to re-launch it.
  * Canceling login during a single MDM configuration setup results in an empty page with no way to resume authentication. To work around this issue, exit and relaunch the client.

 -- Yi Huang <yi@cloudflare.com>  Mon, 09 Mar 2026 16:38:25 -0700

cloudflare-warp (2026.1.150) unstable; urgency=medium
  This release contains minor fixes, improvements, and new features.

  WARP client version 2025.8.779.0 introduced an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  * Fixed an issue causing failure of the local network access exclusion feature when configured with a timeout of 0.
  * Improvement for more accurate reporting of device colocation information in the Zero Trust dashboard.
  * Fixed an issue where misconfigured DEX HTTP tests prevented new registrations.
  * Fixed issues causing DNS requests to fail with clients in Traffic and DNS mode or DNS only mode.

 -- Yi Huang  <yi@cloudflare.com>  Mon, 23 Feb 2026 17:35:43 +0000

cloudflare-warp (2026.1.89) unstable; urgency=medium
  This release contains minor fixes, improvements, and new features.

  WARP client version 2025.8.779.0 introduced an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  * Fixed an issue causing failure of the local network access exclusion feature when configured with a timeout of 0.
  * Improvement for more accurate reporting of device colocation information in the Zero Trust dashboard.

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Mon, 26 Jan 2026 18:14:00 -0500

cloudflare-warp (2025.10.186) unstable; urgency=medium
  This release contains minor fixes, improvements, and new features including a new feature to manage WARP client connectivity for all devices in your fleet using an external signal.

  WARP client version 2025.8.779.0 introduced an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  * The Local Domain Fallback feature has been fixed for devices running WARP client version 2025.4.929.0 and newer. Previously, these devices could experience failures with Local Domain Fallback unless a fallback server was explicitly configured. This configuration is no longer a requirement for the feature to function correctly.
  * Improvement for WARP client posture check. Linux device posture for encrypted drives now also supports non-filesystem encryption types like dm-crypt.
  * Improvement for WARP modes, proxy mode now supports transparent HTTP proxying in addition to CONNECT-based proxying.
  * Fixed an issue where the GUI becomes unresponsive when the "Re-Authenticate in browser" button is clicked.
  * Added a new feature to Manage device connection using an external signal. This feature allows administrators to send a global signal from an on prem HTTPS endpoint that force disconnects or reconnects all WARP clients in an account based on configuration set on the endpoint.

 -- Rhett Griggs <rhett@cloudflare.com>  Mon, 12 Jan 2026 12:00:00 -0500

cloudflare-warp (2025.9.558) unstable; urgency=medium
  This release contains minor fixes, improvements, and new features including Path Maximum Transmission Unit Discovery (PMTUD). When PMTUD is enabled, the client will dynamically adjust packet sizing to optimize connection performance. There is also a new connection status message in the GUI to inform users that the local network connection may be unstable. This will make it easier to debug connectivity issues.

  WARP client version 2025.8.779.0 introduced an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  * The UI now displays the health of the tunnel and DNS connections by showing a connection status message when the network may be unstable. This will make it easier to debug connectivity issues.
  * Fixed an issue where deleting a registration was erroneously reported as having failed.
  * Path Maximum Transmission Unit Discovery (PMTUD) may now be used to discover the effective MTU of the connection. This allows the WARP client to improve connectivity optimized for each network. PMTUD is disabled by default. To enable it, refer to our developer [documentation](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/warp/deployment/mdm-deployment/path-mtu-discovery/#enable-path-mtu-discovery).

 -- Shrey Amin <samin@cloudflare.com>  Tue, 11 Nov 2025 02:00:00 -0400

cloudflare-warp (2025.9.171) unstable; urgency=medium
  This release contains minor fixes, improvements, and new features including Path Maximum Transmission Unit Discovery (PMTUD). With PMTUD enabled, the client will dynamically adjust packet sizing to optimize connection performance. There is also a new connection status message in the GUI to inform users that the local network connection may be unstable. This will make it easier to debug connectivity issues.

  WARP client version 2025.8.779.0 introduced an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  * The UI now displays the health of the tunnel and DNS connections by showing a connection status message when the network may be unstable. This will make it easier to debug connectivity issues.
  * Deleting registrations no longer returns an error when succeeding.
  * Path Maximum Transmission Unit Discovery (PMTUD) is now used to discover the effective MTU of the connection. This allows the client to improve connection performance optimized for the current network.

  Known issues
  * Devices using WARP client 2025.4.929.0 and up may experience Local Domain Fallback failures if a fallback server has not been configured. To configure a fallback server, refer to [Route traffic to fallback server](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/configure-warp/route-traffic/local-domains/#route-traffic-to-fallback-server).

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Wed, 15 Oct 2025 16:14:00 -0400

cloudflare-warp (2025.8.779) unstable; urgency=medium
  This release contains minor fixes and improvements including including an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com.

  This release contains enhancements to Proxy mode for even faster resolution. The MASQUE protocol is now the only protocol that can use Proxy mode. If you previously configured a device profile to use Proxy mode with Wireguard, you will need to select a new WARP mode or all devices matching the profile will lose connectivity.

 -- Logan Praneis <lpraneis@cloudflare.com>  Tue, 7 Oct 2025 02:00:00 -0400

cloudflare-warp (2025.7.176) unstable; urgency=medium
  This release contains minor fixes and improvements including an updated public key for Linux packages. The public key must be updated if it was installed before September 12, 2025 to ensure the repository remains functional after December 4, 2025. Instructions to make this update are available at pkg.cloudflareclient.com .

  * The MASQUE protocol is now the default protocol for all new WARP device profiles.
  * Improvement to limit idle connections in DoH mode to avoid unnecessary resource usage that can lead to DoH requests not resolving.
  * Improvements to maintain Global WARP Override settings when switching between organization configurations.
  * Improvements to maintain client connectivity during network changes.

 -- Shrey Amin <samin@cloudflare.com>  Tue, 29 Sep 2025 02:00:00 -0400

cloudflare-warp (2025.6.1335) unstable; urgency=medium
  This release contains minor fixes and improvements.

  * Fixed an issue preventing devices from reaching split-tunneled traffic even when WARP was disconnected.
  * Fix to prevent the firewall being re-enabled after user initiated client disconnection.
  * Improvement for faster client connectivity on high-latency captive portal networks.
  * Fixed an issue where recursive CNAME records could cause intermittent WARP connectivity issues.

 -- Shrey Amin <samin@cloudflare.com>  Tue, 19 Aug 2025 02:00:00 -0400

cloudflare-warp (2025.5.924) unstable; urgency=medium
  This release contains minor fixes and improvements.

  * Fixed an issue preventing devices from reaching split-tunneled traffic even when WARP was disconnected.
  * Fix to prevent the firewall being re-enabled after user initiated client disconnection.
  * Improvement to managed network detection checks for faster switching between managed networks.

  Known issues
  * Devices using WARP client 2025.4.929.0 and up may experience Local Domain Fallback failures if a fallback server has not been configured. To learn more about configuring a fallback server, please reference the [Zero Trust documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/configure-warp/route-traffic/local-domains/#route-traffic-to-fallback-server).

 -- Shrey Amin <samin@cloudflare.com>  Wed, 23 Jul 2025 15:26:00 -0400

cloudflare-warp (2025.5.893) unstable; urgency=medium
  This release contains improvements and new exciting features, including post-quantum cryptography. By tunnelling your corporate network traffic over Cloudflare, you can now gain the immediate protection of post-quantum cryptography without needing to upgrade any of your individual corporate applications or systems.

  * Fixed a device registration issue causing WARP connection failures when changing networks.
  * Captive portal improvements and fixes. Captive portal sign in notifications will now be sent through operating system notification services. Fix for firewall configuration issue affecting clients in DoH only mode.
  * Improved the connectivity status message in the client GUI.
  * The WARP client now applies post-quantum cryptography end-to-end on enabled devices accessing resources behind a Cloudflare Tunnel. This feature can be enabled by MDM.
  * Improvement to handle client configuration changes made by MDM during disconnection upon reconnection.
  * Fixed an issue affecting split tunnel include mode, where traffic outside the tunnel was blocked when switching between Wifi and ethernet networks.

 -- Rhett Griggs <rhett@cloudflare.com>  Mon, 30 Jun 2025 12:00:00 -0400

cloudflare-warp (2025.5.828) unstable; urgency=medium
  This release contains improvements and new exciting features, including post-quantum cryptography. By tunnelling your corporate network traffic over Cloudflare, you can now gain the immediate protection of post-quantum cryptography without needing to upgrade any of your individual corporate applications or systems.

  * Fixed a device registration issue causing WARP connection failures when changing networks.
  * Captive portal improvements including showing connectivity status in the client and sending system notifications for captive portal sign in
  * The WARP client now applies post-quantum cryptography end-to-end on enabled devices accessing resources behind a Cloudflare Tunnel. This feature can be enabled by MDM.
  * Improvement to gracefully handle changes made by MDM while WARP is not running.
  * Fixed an issue affecting split tunnel include mode, where traffic outside the tunnel was blocked when switching between Wifi and ethernet networks.

 -- Rhett Griggs <rhett@cloudflare.com>  Thu, 12 Jun 2025 12:00:00 -0400

cloudflare-warp (2025.4.943) unstable; urgency=medium
  This release contains a hotfix for Managed Networks for the 2025.4.929.0 release.

  * Fixed an issue where it could take up to 3 minutes for the correct profile to be applied in some circumstances. In the worst case, it should now only take up to 40 seconds. This will be improved further in a future release.

 -- Shrey Amin <samin@cloudflare.com>  Thu, 22 May 2025 13:30:00 -0400

cloudflare-warp (2025.4.929) unstable; urgency=medium
  This release contains two significant changes all customers should be aware of:
  1. All DNS traffic now flows inside the WARP tunnel. Customers are no longer required to configure their local Firewall rules to allow our DoH IP Address or domains.
  2. When using MASQUE, the connection will fall back to HTTP/2 (TCP) when we detect that HTTP/3 traffic is blocked. This allows for a much more reliable connection on some public WiFi networks.

  * Fixed an issue where the managed network policies could incorrectly report network location beacons as missing.
  * Improved DEX Test Error reporting.
  * Fixed an issue causing client notifications to fail in IPv6 only environments which prevented the client from receiving configuration changes to settings like device profile.
  * Added a TCP fallback for the MASQUE tunnel protocol to improve connectivity on networks that block UDP or http/3 specifically.
  * Added new IPs for Client Orchestration API for operations like tunnel connectivity checks. If your organization uses a firewall or other policies you will need to exempt these IPs.
  * Fixed an issue where frequent network changes could cause WARP to become unresponsive.
  * DNS over HTTPS traffic is now included in the WARP tunnel by default.
  * Improvement for WARP to check if tunnel connectivity fails or times out at device wake before attempting to reconnect.
  * Fixed an issue causing WARP connection disruptions after network changes.

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Mon, 12 May 2025 15:56:00 -0400

cloudflare-warp (2025.4.589) unstable; urgency=medium
  Changes and improvements
  * Fixed an issue where the managed network policies could incorrectly report network location beacons as missing.
  * Improved DEX Test Error reporting.
  * Fixed an issue causing client notifications to fail in IPv6 only environments which prevented the client from receiving configuration changes to settings like device profile.
  * Added a TCP fallback for the MASQUE tunnel protocol to improve compatibility with networks on MASQUE.
  * Added new IPs for Client Orchestration API for operations like tunnel connectivity checks. If your organization uses a firewall or other policies you will need to exempt these IPs.
  * Fixed an issue where frequent network changes could cause WARP to become unresponsive.
  * DNS over HTTPS traffic is now included in the WARP tunnel by default.

 -- Rhett Griggs <rhett@cloudflare.com>  Tue, 22 Apr 2025 12:00:00 -0400

cloudflare-warp (2025.2.600) unstable; urgency=medium
  Changes and improvements
  * Improved captive portal experience to make more public networks compatible and have faster detection.
  * WARP tunnel protocol details can now be viewed by `warp-cli tunnel stats` command
  * Fixed issue with device revocation and re-registration when switching configurations
  * Added a new Global WARP Override setting. This setting puts account admins in control of disabling and enabling WARP across all devices registered to an account from the dashboard. Global WARP Override is disabled by default.

 -- Logan Praneis <lpraneis@cloudflare.com>  Mon, 31 Mar 2025 12:00:00 -0400

cloudflare-warp (2025.1.861) unstable; urgency=medium
  Changes and improvements
  * Improved command line interface for Zero Trust Access for Infrastructure with added function for filtering and ordering.
  * Fixed client connectivity issues when switching between managed network profiles that use different WARP protocols.
  * Added support for WARP desktop to use additional DoH endpoints to help reduce NAT congestion.
  * Improved Wireguard connection stability on reconnections.
  * Added additional HTTP/3 QUIC connectivity test to warp-diag.
  * Added support for collection of system health metrics for enhanced device Digital Experience Monitoring.
  * Automated the removal of active registrations for devices with multiple registrations with the same Zero Trust organization.

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Tue, 18 Feb 2025 16:27:22 -0400

cloudflare-warp (2024.12.554) unstable; urgency=medium
  Changes and improvements
  * Adds support for installing all available custom gateway certificates from an account to the system store.
  * Users can now get a list of installed certificates by running `warp-cli certs`.

 -- Tochukwu Nkemdilim  <tochukwu@cloudflare.com>  Thur, 19 Dec 2024 09:42:22 -0400

cloudflare-warp (2024.12.492) unstable; urgency=medium
  Changes and improvements
  * Consumers can now set the tunnel protocol using "warp-cli tunnel protocol set <proto>".
  * Extended diagnostics collection time in warp-diag to ensure logs are captured reliably.
  * Improved captive portal support by disabling the firewall during captive portal login flows.
  * Improved reliability of connection establishment logic under degraded network conditions.
  * Improved reconnection speed when a Cloudflare server is in a degraded state.
  * Improved captive portal detection on certain public networks.
  * Fixed an issue where admin override displayed an incorrect override end time.
  * Reduced connectivity interruptions on WireGuard include split tunnel configurations.
  * Fixed connectivity issues switching between managed network profiles with different configured protocols
  * QLOGs are now disabled by default and can be enabled with `warp-cli debug qlog enable`. The qlog setting from previous releases will no longer be respected.

 -- Logan Praneis  <lpraneis@cloudflare.com>  Wed, 18 Dec 2024 12:00:00 -0400

cloudflare-warp (2024.11.309) unstable; urgency=medium
  Changes and improvements
  * Fixed an issue where SSH sessions and other connections were dropped when using MASQUE and the device's network interface changed.
  * Improvement made so that device posture client certificate checks now support PKCS#1.
  * Fixed an issue to ensure the managed certificate is installed in the trust store if not already there.
  * Reduced unnecessary log messages when resolv.conf has no owner.
  * Fixed an issue with warp-diag printing benign TLS certificate errors.
  * Fixed an issue with the WARP client becoming unresponsive during startup.
  * Extended diagnostics collection time in warp-diag to ensure logs are captured reliably.
  * Fixed an issue that was preventing proper operation of DNS-over-TLS (DoT) for consumer users.

 -- Keehun Nam <keehun@cloudflare.com>  Mon, 18 Nov 2024 12:00:00 -0400

cloudflare-warp (2024.10.537) unstable; urgency=medium
  New Features
  * Added ability for administrators to initiate remote packet capture (PCAP) and warp-diag collection

  Changes and improvements
  * Reduced unnecessary log messages when resolv.conf has no owner
  * Fixed an issue with warp-diag printing benign TLS certificate errors
  * Improved reliability of connection establishment logic under degraded network conditions
  * Improved captive portal detection behavior by forcing captive portal checks outside the tunnel
  * Allow the ability to configure tunnel protocol for consumer registrations
  * Fixed an issue with the WARP client becoming unresponsive during startup
  * Extended diagnostics collection time in warp-diag to ensure logs are captured reliably

 -- Shrey Amin <samin@cloudflare.com>  Tue, 05 Nov 2024 10:00:00 -0400

cloudflare-warp (2024.10.279) unstable; urgency=medium
  Changes and improvements
  * Fixed an issue where SSH sessions and other connections were dropped when using MASQUE and the device network interface changed.
  * Improvement made so that device posture client certificate checks now support private keys with the ‘RSA PRIVATE KEY’ label (pkcs#1).
  * Fixed an issue to ensure the managed certificate is installed in the trust store if not already there.

 -- Paul Tillotson <ptillotson@cloudflare.com>  Tue, 22 Oct 2024 10:05:46 -0400

cloudflare-warp (2024.9.342) unstable; urgency=medium
  Changes and improvements
  * Added list targets to the warp-cli to enhance the user experience with the Access for Infrastructure SSH solution.
  * Added the ability to customize PCAP options in the warp-cli.
  * Added a list of installed applications in warp-diag.
  * Added a tunnel reset mtu subcommand to the warp-cli.
  * Added the ability for warp-cli to use the team provided in the MDM file for initial registration.
  * Added a JSON output option to the warp-cli.
  * Added the ability to execute a pcap on multiple interfaces with warp-cli.
  * Added MASQUE tunnel protocol support for Consumer WARP.
  * Improved the performance of firewall operations when enforcing split tunnel configuration.
  * Fixed an issue where device posture certificate checks were unexpectedly failing.
  * Fixed an issue where the Linux GUI fails to open the browser login window when registering a new ZT organization.
  * Fixed an issue where clients using service tokens failed to retry after a network change.
  * Fixed an issue where the client, when switching between WireGuard and MASQUE protocols, sometimes required a manual tunnel key reset.
  * Fixed a known issue which required users to re-register when an older single configuration MDM file was deployed after deploying the newer, multiple configuration format.
  * Deprecated warp-cli commands have been removed. If you have any workflows that use the deprecated commands, please update to the new commands where necessary.

  Known issues
  * Using MASQUE as the tunnel protocol may be incompatible if your organization has Regional Services enabled.

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Thu, 3 Oct 2024 16:55:48 -0400

cloudflare-warp (2024.6.497) unstable; urgency=medium
  New Features
  * The WARP client now supports operation on Ubuntu 24.04.
  * Admins can now elect to have ZT WARP clients connect using the MASQUE protocol; this setting is in Device Profiles. Note: before MASQUE can be used, the global setting for Override local interface IP must be enabled. For more detail, see https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/configure-warp/warp-settings/#device-tunnel-protocol. This feature will be rolled out to customers in stages over approximately the next month.
  * The Device Posture client certificate check has been substantially enhanced. The primary enhancement is the ability to check for client certificates that have unique common names, made unique by the inclusion of the device serial number or host name (for example, CN = 123456.mycompany, where 123456 is the device serial number). Additional details can be found here:  https://developers.cloudflare.com/cloudflare-one/identity/devices/warp-client-checks/client-certificate/
  * TCP MSS clamping is now used where necessary to meet the MTU requirements of the tunnel interface. This will be especially helpful in docker use cases.

  Warnings
  * Ubuntu 16.04 and 18.04 are not supported by this version of the client.
  * This is the last GA release that will be supporting older, deprecated warp-cli commands. There are two methods to identify these commands. One, when used in this release, the command will work but will also return a deprecation warning. And two, the deprecated commands do not appear in the output of `warp-cli -h`.

  Known issues
  * There are certain known limitations preventing the use of the MASQUE tunnel protocol in certain scenarios. Do not use the MASQUE tunnel protocol if:
    * A Magic WAN integration is on the account and does not have the latest packet flow path for WARP traffic. Please check migration status with your account team.
    * Your account has Regional Services enabled.
  * The Linux client GUI does not yet support all GUI features found in the Windows and macOS clients. Future releases of the Linux client will be adding these GUI features.
  * ZT Org name not visible in GUI when upgrading from previous GA while under mdm control.
  * Sometimes the Icon will remain gray (disconnected state) while in dark mode.

 -- Shrey Amin <samin@cloudflare.com>  Thu, 15 Aug 2024 12:01:00 -0400

cloudflare-warp (2024.4.133) unstable; urgency=medium
  * Linux client downloads will now contain version numbers in the file name to allow easy identification.
  * Improved the re-connection logic to minimize impact to existing tunneled TCP sessions.
  * Increased the data collected by warp-diag to improve debugging capabilities.

  Known issues
  * The Linux client GUI does not yet support all GUI features found in the Windows and macOS clients. Future releases of the Linux client will be adding these GUI features.
  * ZT Org name not visible in GUI when upgrading from previous GA while under mdm control.
  * Sometimes the Icon will remain gray (disconnected state) while in dark mode.

 -- Tochukwu Nkemdilim <tochukwu@cloudflare.com>  Thu, 11 Apr 2024 14:53:48 -0400

cloudflare-warp (2024.2.62) unstable; urgency=medium
  * Added support for the arm64 architecture.
  * Added the ability for administrators to allow their end users to temporarily obtain access to local network resources in the event their home IP space overlaps with traffic normally routed through the WARP tunnel. Users on Linux interact with this feature via the warp-cli.
  * Added the ability for administrators to specify multiple configurations in MDM files that users can toggle between. This allows users to more easily switch between production and test environments or for China users to switch between their override endpoints within the UI. Users on Linux interact with this feature via the warp-cli. Refer to the help text from "warp-cli mdm --help". GUI integration of this feature will be released in the future.
  * Added the collection of firewall log information and other data to warp-diag to provide additional information for troubleshooting.
  * Added support to run a DHCP server on the same machine as the client (useful in virtual machine scenarios).
  * Added support for os_version_extra on Linux to enhance the OS device posture check.
  * Fixed an issue with sleep notifications making the client more reactive to sleep/wake-up scenarios.
  * Fixed an issue to ensure DEX tests only run when the client is connected.
  * Fixed an issue where IPv6 being disabled at boot time was not detected, leading to errors when the client attempts to set IPv6 addresses.

  Known issues
  * The Linux client GUI does not yet support all GUI features found in the Windows and macOS clients. Future releases of the Linux client will be adding these GUI features.
  * ZT Org name not visible in GUI when upgrading from previous GA while under mdm control
  * Sometimes the Icon will remain gray (disconnected state) while in dark

 -- Keehun Nam <Keehun@cloudflare.com>  Wed, 14 Feb 2024 09:12:57 -0600

cloudflare-warp (2023.9.301) unstable; urgency=medium
  * Added initial implementation of Linux UI for Ubuntu with things like toggle switch, status, ability to switch vnets and better support for joining a Zero Trust organization
  * Added new posture type: Client certificate
  * Added support for IPv6 DEX Traceroute tests (previously only IPv4 addresses could be used)
  * Improved reliability and efficiency in configurating split tunnel rules. Most "error petting the dog" errors should now be gone and organizations with large split tunnel configuration should see reliability improvements
  * Fixed an issue with DEX traceroutes tests where not all hops were correctly reported
  * Fixed an issue where DEX tests would not properly run immediately after a device came out of sleep
  * Fixed an issue where DEX tests would execute simultaneously causing performance issues for accounts with a large number of tests configured
  * Fixed an issue where DoH requests could take too long to timeout causes DNS reliability issues
  * Fixed an issue where DNS could temporarily fail when DHCP updates were processed
  * Fixed an issue on initial device registration that could sometimes cause it to fail and try again
  * Fixed an issue where short DNS timeouts were causing issues with some captive portals (United in particular)
  * Fixed an issue where managed network detection could fail when our firewall rules were not correctly removed under certain disconnect scenarios
  * Fixed an issue with Managed Networks where if the managed endpoint overlapped with your exclude split tunnel configuration, the split tunnel would only be open for IP traffic destined to the same port as your managed TLS endpoint
  * Fixed an issue where IPv6 traffic could be incorrectly sent down the tunnel in exclude mode
  * Fixed an issue where root CA would not be installed if enabled by admin because we were missing ca-certificates dependency
  * Fixed an issue where the client could be stuck on connecting

  Known issues
  * Not all UI features are in place yet, more will be coming in future releases
  * ZT Org name not visible in GUI when upgrading from previous GA while under mdm control
  * Sometimes the Icon will remain gray (disconnected state) while in dark

 -- Naga Tripirineni <naga@cloudflare.com>  Fri, 29 Sep 2023 16:35:29 -0500

cloudflare-warp (2023.7.40) unstable; urgency=medium
  * Added support for "SWG without DNS Filtering" mode. All DNS functionality
    from the WARP client is disabled while in this service mode
  * Added support for distribution name and version to be used in OS Version device posture checks
  * Improved performance of the client when in "Proxy Only" service mode
  * Improved performance of domain-based split tunneling when the IP was already
    split tunneled (seen frequently with Zoom domains and IPs being used)
  * Modified warp-cli settings to show if the applied settings came from local (mdm)
    or network (warp settings profile) policy to make debugging profile issues easier
  * Fixed an issue that could result in increased latency when resolving queries
  * Optimized the performance of DNS queries to prevent minor memory leaks
  * Fixed an issue when service token information was removed from an mdm.xml file
    the client would not prompt for user authentication as expected
  * Fixed an issue where localhost DNS proxy could not be set properly in certain VPN and VM configuration
  * Fixed an issue where the client would attempt to connect even when the "AUTO CONNECT" setting
    was Disabled in WARP Settings or not specified either in an MDM file
  * Fixed an issue where the client would not correctly detect and apply alternate network configuration between network changes

 -- Logan Praneis <lpraneis@cloudflare.com>  Thu, 13 Jul 2023 08:55:29 -0500

cloudflare-warp (2023.3.398) unstable; urgency=medium
  * Added support for millisecond timestamps for use in Digital Experience Monitoring
  * Fixed an issue with Root CA installation feature

  -- Jeff Hiner <jhiner@cloudflare.com> Thu, 7 Apr 2023 09:51:00 -0700


cloudflare-warp (2023.3.258) unstable; urgency=medium
  * Improve timeouts with broken CNAME records that could result in very long load times for certain apps
  * Fixed issue where systems with significantly out of sync system clocks could fail registration
  * Improved user validation logic during manual ZT login
  * Fixed issue where the WARP daemon can crash and lose connectivity
  * Fixed issue where warp-diag could run traceroutes longer than expected.
    Traceroute tests will now timeout after 65 seconds.
  * Fixed issue where manually logging into a ZT org could fail if certificate authentication was used
  * Added support for Zero Trust Digital Experience Monitoring.
    More information coming soon for customers who signed up for the beta
  * Added new log message to help customers and support identify when a users local
    network IP space overlaps with a remote network configured to go through the tunnel
  * Added support for Zero Trust customers to opt in to having the WARP Client install the root CA
    for your organization if TLS Decryption is enabled.
    A new toggle switch will appear in the dashboard under Settings->WARP Client soon to enable this
  * Modified behavior of Managed networks tests to always happen outside the tunnel as per original intent
  * Improved logging of application posture checks to understand rationale behind
    statuses of application checks (file missing, process not found, etc.)
  * Added support for more detailed statuses in the output of warp-cli status
  * Modified initial connectivity check behavior to retry on errors

 -- Logan Praneis <lpraneis@cloudflare.com>  Wed, 22 Mar 2023 12:33:12 -0500


cloudflare-warp (2023.1.133) unstable; urgency=medium
  * Fixed an issue where clients could lose IPv4 connectivity
  * Fixed an issue where clients would attempt to configure DNS in posture-only or proxy modes.
  * Increased MDM check timeout to improve compatibility with certain management solutions.

  -- Logan Praneis <lpraneis@cloudflare.com> Thu, 18 Jan 2023 00:00:00 -0600

cloudflare-warp (2022.12.542) unstable; urgency=medium
  * Added support for network location aware for Zero Trust organizations
  * Improved captive portal handling for some captive portals
  * Fixes for several edge case issues with Zero Trust organizations
  * Turning on DNS logging no longer forces a disconnect and reconnect
  * Modified initial connectivity check behavior to now validate both IPv4 and
    IPv6 are working (previously we only checked IPv4). Test will pass if either
    connects successfully.
  * Fixed DNS issue where TXT records were not being correctly returned when at
    the end of a CNAME chain.
  * Addressed some edge case performance issues with certain NXDOMAIN returns

 -- Jeff Hiner <jhiner@cloudflare.com> Thu, 5 Jan 2023 09:51:00 -0700

cloudflare-warp (2022.10.116) unstable; urgency=medium
  * Modified behavior of warp-cli enable-dns-log to automatically turn off after
    7 days (this is the equivalent of manually running warp-cli disable-dns-log)
  * Fixed issue where device posture timers were paused while device was asleep.
    Posture tests are now immediately ran on device wakeup and all timers
    restarted.
  * Decreased warp-diag zip file sizes by 60-80%.
  * Fixed issue where mdm.xml file updates may have been missed.
  * Fixed issue where warp DNS servers were still set after WARP was turned off

 -- Matt Schulte <mschulte@cloudflare.com> Mon, 21 Nov 2022 11:00:00 -0400

cloudflare-warp (2022.9.591) unstable; urgency=medium
  * Fixed issue where device posture check results stopped sending after 24
    hours (or possibly even sooner)

 -- Matt Schulte <mschulte@cloudflare.com> Wed, 12 Oct 2022 07:00:00 -0700

cloudflare-warp (2022.9.505) unstable; urgency=medium
  * Improved connection time on slow network connections
  * Fixed bug where initial teams registration could take awhile to show up on
    client UI
  * Fixed bug that could cause Teams registration to fail (mostly server side
    but mentioning here as well) and handoff from the success page in the
    browser to the client
  * Fixed DNS fallback timeouts and related performance issues
  * Fixed issue where coming out of sleep on some systems could take an
    unreasonably long time to connect
  * Fixed InvalidPacket error in logs that indicated the client needed to reset
    its connection
  * Fixed issue where user experienced no network after boot
  * Fixed issue where warp-diag rotated daemon logs did not collect older logs

 -- Matt Schulte <mschulte@cloudflare.com> Thu, 6 Oct 2022 11:00:00 -0700

cloudflare-warp (2022.8.936) unstable; urgency=medium

  * Fixed issue where warp-cli set-custom-endpoint could be used by users
    without local admin rights as a way to bypass Gateway policies.
  * Fixed issue where warp-cli add-trusted-ssid worked in Zero Trust mode when
    it should not have.
  * Fixed issue where warp-cli teams-enroll would run even if already joined to
    an organization and users were not allowed to disconnect or leave.
  * Fixed issue that could result in connection issues coming out of certain
    sleep states (AddrInUse error or Multiple WARP Connections or
    NoCurrentSession).
  * Fixed issue that could result in connection flickering between
    connected/disconnected.
  * Fixed issue where connectivity test could report wrong status in logs when
    in Include Only split tunnel configuration.
  * Fixed issue where warp-cli could hang if service was in a bad state.
  * Fixed issue where sometimes Zero Trust device settings configured in the
    dash wouldn't take effect for machines in a disconnected state and asleep
    state.
  * Fixed issue where our DNS proxy wasn't correctly handling EDNS0 requests.
  * Fixed issue where the DNS Answer for records at the end of a CNAME chain
    would appear in the ADDITIONAL response section instead of the ANSWER
    section. This broke certain connectivity checks for Microsoft and Android
    studio in particular (probably other things). We now put the IP address
    found in the ANSWER section.
  * Fixed issue where multiple instances of the service could run at the same
    time.
  * Fixed issue that could occur during registration if the user clicks on on
    the Launch Cloudflare WARP button after already registering.
  * Fixed issue where the Zero Trust client was starting in connected mode when
    dash settings Switched Locked and Auto Connect were turned off/disabled. The
    client should only ever auto connect when these are enabled.
  * Fixed issue where DNS functionality may be in a broken state when device
    wakes from sleep
  * Improved performance of warp-diag to now collects logs in parallel and now
    collect additional routes to help with debugging.
  * Use desktop notifications for re-authentication notifications

 -- Matt Schulte <mschulte@cloudflare.com> Mon, 19 Sep 2022 15:00:00 -0700


cloudflare-warp (2022.7.472) unstable; urgency=medium

  * Fixed issue where OS version and device name may not update in ZT Dashboard
  * Prevent users from brute forcing admin override code
  * Prevent disable-on-wifi feature for ZT customers
  * Add support for environment variables in device posture files paths
  * Prevent flushing all nftable rulesets when WARP is disabled
  * Fix incorrect output in "include-only" mode
  * Fix routing issues when running microk8s
  * Fix issue with wildcard expansion on domain fallback and split tunnel rules
  * Fix issue with `warp-diag feedback` failing to upload
  * Prevent hangs and failures on network traffic when in proxy-mode
  * Prevent log files from growing too large
  * Add "Don't Fragment" bit to encapsulated traffic
  * Ensure our DNS servers stay set if another program tries to change them
  * Add ability to upload device state to API for ZT customers

cloudflare-warp (2022.7.472) unstable; urgency=medium

  * Fixed issue where OS version and device name may not update in ZT Dashboard
  * Prevent users from brute forcing admin override code
  * Prevent disable-on-wifi feature for ZT customers
  * Add support for environment variables in device posture files paths
  * Prevent flushing all nftable rulesets when WARP is disabled
  * Fix incorrect output in "include-only" mode
  * Fix routing issues when running microk8s
  * Fix issue with wildcard expansion on domain fallback and split tunnel rules
  * Fix issue with `warp-diag feedback` failing to upload
  * Prevent hangs and failures on network traffic when in proxy-mode
  * Prevent log files from growing too large
  * Add "Don't Fragment" bit to encapsulated traffic
  * Ensure our DNS servers stay set if another program tries to change them
  * Add ability to upload device state to API for ZT customers

cloudflare-warp (2022.5.346) unstable; urgency=medium

  * Fixed issue where all nftables rulesets were flushed after warp-cli disconnect
  * Fixed false positives when attempting to detect a captive portal
  * Fixed issue where OS version would not be updated in dash after OS update
  * Added support for DNS over TCP
  * Fixed issue where updated posture checks might not take effect until restart
  * Fixed issue with warp-cli where enable/disable with wifi was allowed in Zero Trust mode
  * Fixed issue where too many DNS requests could result in the following error
    appearing in logs: WARN warp::dns: Shedding DNS load
  * Bug fixes and enhancements

 -- Matt Schulte <mschulte@cloudflare.com> Fri, 17 Jun 2022 15:00:00 -0700

cloudflare-warp (2022.4.235) unstable; urgency=medium

  * Removed periodic tunnel checks
  * Changed `warp-cli connect` to mimic 'warp-cli enable-always-on`
  * Changed `warp-cli disconnect` to mimic `warp-cli disable-always-on`
  * Added a simple taskbar icon to show status
  * Added virtual network switching support via warp-cli (`warp-cli
    get-virtual-networks` and `warp-cli set-virtual-network`).
  * Bug fixes and enhancements

 -- Matt Schulte <mschulte@cloudflare.com> Mon, 18 April 2022 12:00:00 -0700

cloudflare-warp (2022.3.253) unstable; urgency=medium

  * `warp-cli delete` run as root will remove the user for an organization
    even if "Allowed To Leave" is disabled in Zero Trust dashboard.
  * Added `warp-cli disable-connectivity-checks` and `warp-cli
    enabled-connectivity-checks` to control connectivity checks
  * Fixed issue with `warp-cli teams-enroll` on platforms where the default
    browser is installed with snap.
  * Added "Device Posture Only" support

 -- Matt Schulte <mschulte@cloudflare.com> Wed, 40 March 2022 15:30:00 -0700

cloudflare-warp (2022.2.288) unstable; urgency=medium

  * Fixed an issue where the organization name became case sensitive and could
    cause a device to lose registration

 -- Matt Schulte <mschulte@cloudflare.com> Thu, 24 Feb 2022 10:10:00 -0800

cloudflare-warp (2022.2.29) unstable; urgency=medium

  * Fixed issue with warp working on distros with v248 of systemd or newer
  * Fixed issue with device posture application checks detecting running
    processes
  * Now that settings exist in the Zero Trust Dashboard the Client UI should
    behave the same regardless of if you manually joined to a Team or if you
    were forced to by local mdm.xml policy
  * Fixed issue where the WARP Client might not get updated settings when it
    initial starts
  * Fixed issue where the Last Seen value was not updated properly in the Zero
    Trust Dashboard while in "doh" mode
  * Fixed issue where device name was not updated in the Zero trust Dashboard if
    the computer name changed after initial registration
  * Added the ability for daemon to parse mdm.xml file on Linux
  * Shows the Zero Trust Terms of Service when user joins an organization

 -- Matt Schulte <mschulte@cloudflare.com> Wed, 9 Feb 2022 14:07:00 -0800

cloudflare-warp (2021.12.0) unstable; urgency=high

  * Removes leaked signing key from apt key store
  * Fixed connectivity issue when attempting to reconnect to WARP
  * Add a background connectivity check
  * you can now specify specific DNS servers to use for domains in Local
    Domain fallback in the Teams Dashboard.

 -- Matt Schulte <mschulte@cloudflare.com> Fri, 10 Dec 2021 14:34:00 -0700

cloudflare-warp (2021.10.0) unstable; urgency=medium

  * Client now supports include only split tunnel rules while in Teams mode
  * Improved overall reliability of DNS and general connectivity when in Teams
    modes
  * Improved logging and fixed bug where we got incomplete logs from warp-diag
  * Fixed connectivity issues some users experienced when coming out of sleep
  * Fixed occasional registration issues when trying to join Teams
    organization
  * Fixed bug in restoring previous DNS settings on crash
  * Fixed bug in Linux firewall blocking certain DNS requests
  * Fixed issues in handling SIGTERM/SIGINT

 -- Matt Schulte <mschulte@cloudflare.com>  Wed, 27 Oct 2021 10:13:15 -0700

cloudflare-warp (2021.8.1) unstable; urgency=low

  * Minor fixes to network changes while in proxy mode
  * Minor stability fixes and improvements

 -- Jeff Hiner <jhiner@cloudflare.com>  Fri, 13 Aug 2021 15:50:50 -0600

cloudflare-warp (2021.8.0) unstable; urgency=medium

  * Rewrite teams-client enrollment flow for Linux clients, including no-auth
  * Implement nftables support for Linux
  * Fix potential stack overflow errors in some clients
  * Fix an issue where the client would stop working properly after a suspend
  * Various stability improvements and other minor fixes

 -- Jeff Hiner <jhiner@cloudflare.com>  Thu, 12 Aug 2021 12:24:00 -0600

cloudflare-warp (2021.7.1) unstable; urgency=medium

  * Teams registration now correctly sends serial number
  * Added reset-settings command to CLI
  * Fixed an issue that could prevent Teams registration on some systems
  * Clarified behavior of host-based tunnel exclusion in Teams mode.
    (Not yet supported, but doesn't drop traffic.)
  * Minor bug fixes and improvements

 -- Jeff Hiner <jhiner@cloudflare.com>  Fri, 26 Jul 2021 12:11:01 -0600

cloudflare-warp (2021.7.0) unstable; urgency=medium

  * Logging into Teams can now be done automatically from the CLI.
  * The client can now collect requested device metadata and device posture
    information in Teams mode.
  * The client now sets system resolvers to better capture DNS traffic.
  * Logs have been move to /var/logs/cloudflare-warp.
  * Minor bug fixes and improvements.

 -- Brendan McMillion <brendan@cloudflare.com>  Fri, 9 Jul 2021 12:59:36 -0700

cloudflare-warp (2021.6.0) unstable; urgency=medium

  * warp-diag can now directly upload logs to Cloudflare.
  * Improves performance of DNS resolution.
  * Minor bug fixes and improvements.

 -- Brendan McMillion <brendan@cloudflare.com>  Thu, 10 Jun 2021 12:38:41 -0700

cloudflare-warp (2021.5.0) unstable; urgency=medium

  * No longer requires sudo to run warp-diag.
  * Fills in extended metadata when Zendesk tickets are submitted.
  * Minor bug fixes and improvements.

 -- Brendan McMillion <brendan@cloudflare.com>  Tue, 04 May 2021 08:47:32 -0700

cloudflare-warp (2021.4.1) unstable; urgency=medium

  * Initial release.

 -- Brendan McMillion <brendan@cloudflare.com>  Mon, 03 May 2021 18:13:12 -0700
