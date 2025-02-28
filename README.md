# automatic-network-rebooter
A Python script that monitors internet connectivity and automatically reboots the network if a connection issue is detected. Designed to run on a home server, it ensures continuous internet access by resetting the Virgin Media router when necessary.

## How to get started
The program only has one required package (`requests`), to run the program you will first need to install this by running either running `pip install requests` or `pip install -r requirements.txt` in your terminal / console.

## Support
### Gateway IP address / Router IP Address
This is the IP address of the router / modem you want to rebbot. For Virgin media Hub 5 that's ussualy `192.168.0.1` (or `192.168.100.1` if your hub is set to modem mode).

## Privacy, Security, and Transparency Notice

Privacy is a fundamental human right—everyone deserves security and the freedom to know exactly how a program works. This script is built with that philosophy in mind:

## TL;DR:
- No user data is collected or transmitted.  
- Optional logs are stored locally and off by default.  
- Only essential, built-in dependencies are used.  
- Network check targets and credentials are fully user-configurable.  
- The source code is open for review, ensuring complete transparency.  

- **No Data Collection**  
  - The program does not collect or transmit any user data to a central server.  
  - Its sole function is to monitor connectivity via pings, not to harvest personal information.

- **Optional Local Logging**  
  - Detailed logs are available if enabled, but are **turned off by default**.  
  - When activated, logs are stored only in the program folder and are not shared externally.

- **Minimal Dependencies**  
  - Only one external module is needed (Python’s built-in request library); all other features use standard Python libraries.

- **User Configurable Network Checks**  
  - The list of IP addresses/websites to ping (e.g., generic targets like `azure.com` or similar services) is entirely user-configurable in the setup file.  
  - The default list is chosen to avoid targeting any specific site and can be modified at any time.

- **Secure Handling of Sensitive Information**  
  - Router credentials (IP address and password) can be saved in the configuration file or entered at runtime, ensuring no sensitive data is stored permanently.  
  - Any sensitive tokens are partially masked and are never displayed in logs.

- **Open Source Transparency**  
  - The entire source code is open for review. You are encouraged to read it so you know exactly how the program operates.  
  - The only user-generated data is the configuration file created during setup, which can be deleted at any time.  
  - No information about your computer is collected or uploaded. (Note: the pinged addresses may see your IP address, but this is fully under your control.)

By using this script, you can be confident that your privacy and security are respected at every step.
