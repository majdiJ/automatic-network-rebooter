# automatic-network-rebooter (version: 1.0.0)

A Python script that monitors internet connectivity and automatically reboots your network via its admin portal if a connection issue is detected. Designed to run 24/7 on a computer connected to a Virgin Media network.

## Overview
Routers can sometimes lose internet connectivity even when everything appears normal. This script periodically pings a WAN address, and if no connection is detected, it reboots your router (designed for the Virgin Media Hub 5). Feel free to modify the code to support other routers - contributions are welcome! 💙🧑‍💻

## Requirements
- A computer that can run continuously on your network.
- Python 3.7 or higher.
- The `requests` package (install with `pip install requests` or `pip install -r requirements.txt`).
- Supported router:
    - Virgin Media Hub 5 (router or modem mode)
- Gateway IP address and router admin credentials.

## Recommendations
- Run this on a device connected via Ethernet.
- Avoid deploying on networks or devices you can’t physically access to prevent accidental lockouts.
- Logging is disabled by default; enable it for troubleshooting if needed.

## Disclaimer
- Use this tool only on networks you are authorised to manage.
- Verify your `config.json` settings to avoid unintentional reboot loops.

## Getting Started
1. **Install dependencies:**
   ```bash
   pip install requests
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the script:**
   ```bash
   python main.py
   ```
3. **First-time setup:**  
   If no `config.json` is found, you’ll be guided through a setup wizard to create one. You can edit or delete this file later to reconfigure the program.

## Support
### Router Details
- **Gateway IP Address:** Typically for vigin media hub 5 `192.168.0.1` (or `192.168.100.1` in modem mode).
- **Admin Password:** Found on your router or accompanying documentation/ Passwords vary per device.

## Privacy, Security, and Transparency
- **No Data Collection:** The script solely pings to check connectivity and never collects or transmits personal data.
- **Optional Local Logging:** Debug logs are stored locally and remain off by default.
- **Minimal Dependencies:** Only relies on the `requests` package; all other libraries are built into Python.
- **User Configurability:** All network check targets and credentials are fully configurable via `config.json`.
- **Open Source:** The full source code is available for review, ensuring complete transparency.

### TL;DR
- **No data is collected or transmitted.**
- **Logging is optional and local.**
- **Minimal dependencies and full configurability.**
- **Open source for complete transparency.**