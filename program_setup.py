# This file is used to setup the configuration for the automatic network rebooter
# This file can be run by itself to setup the configuration or be imported and ran
# by the main program (`main.py`) when it detects that the configuration file is missing
# and / or first time setup is needed.

# Import the required libraries
import json

# Console colour variables
class format:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PINK = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

# User input verification: IP address
def verify_user_input_ip_address(ip_str):
    # Split the string on dots.
    parts = ip_str.split('.')
    # IPv4 must have exactly 4 parts.
    if len(parts) != 4:
        return False
    for part in parts:
        # Each part must contain only digits.
        if not part.isdigit():
            return False
        num = int(part)
        # Check if the integer is in the valid IPv4 range.
        if num < 0 or num > 255:
            return False
        # Prevent leading zeros (e.g., "01" or "001"), unless the part is exactly "0".
        if len(part) > 1 and part[0] == '0':
            return False
    return True

# User input handling: IP address
def user_input_ip_address(allow_none=False):
    while True:
        user_input = input("Enter the IP address of the router: ")
        if allow_none and user_input == "":
            return None
        if verify_user_input_ip_address(user_input):
            return user_input
        print(f"\n{format.RED}Invalid IP address. Please try again.{format.END}")
        print("The IP address must be in the format: xxx.xxx.xxx.xxx (if you are unsure, please read the README.md file)")

# User input verification: URL
def verify_user_input_url(url):
    if '.' in url:
        return True
    return False

# User input verification: Yes or No (Y/N)
def verify_user_input_yes_no(user_input):
    if user_input.lower() == "y" or user_input.lower() == "n":
        return True
    return False

# User input handling: Yes or No (Y/N)
def user_input_yes_no(allow_none=False):
    while True:
        user_input = input("Enter your choice (Y/N): ")
        if allow_none and user_input == "":
            return None
        if verify_user_input_yes_no(user_input):
            return user_input
        print(f"\n{format.RED}Invalid choice. Please try again.{format.END}")

# User input handling: List of ping addresses
def user_input_ping_list():
    ping_list = []
    print("\nEnter the list of URLs or IP addresses that you want to ping to check the internet connection. Enter 'done' or empty when you are finished.")
    i = 1
    while True:
        user_input = input(f"Enter address {i}: ")
        if user_input == "" or user_input.lower() == "done":
            if len(ping_list) == 0:
                print(f"\n{format.RED}The list must contain at least one value. Please enter a URL or IP address.{format.END}")
                continue
            return ping_list
        if verify_user_input_url(user_input) or verify_user_input_ip_address(user_input):
            ping_list.append(user_input)
            i += 1
        else:
            print(f"\n{format.RED}Invalid URL or IP address. Please try again.{format.END}")

# User input verification: Number in range
def verify_user_input_number_in_range(user_input, min, max):
    if user_input.isdigit():
        num = int(user_input)
        if num >= min and num <= max:
            return True
    return False

# User input handling: Number in range
def user_input_number_in_range(min, max, allow_none=False):
    while True:
        user_input = input(f"Enter a number between {min} and {max}: ")
        if allow_none and user_input == "":
            return None
        if verify_user_input_number_in_range(user_input, min, max):
            return int(user_input)
        print(f"\n{format.RED}Invalid number. Please try again.{format.END}")

# Program first start up, setup wizzard
def program_setup_wizzard():

    while True:
        print(format.PINK + format.BOLD + "\n=============   Setup Wizzard   =============" + format.END)
        print(format.BOLD + "Welcome to the Automatic Network Rebooter setup wizzard!" + format.END)
        print("It seems like this is the first time you are running the program, no config file was found.")
        print("This wizzard will guide you through the setup process of the Automatic Network Rebooter.")
        print("Please follow the instructions carefully to ensure the program works correctly.")
        print(f"If you need help with setup, please read the README.md file or visit the github page at:\n{format.YELLOW}https://github.com/majdiJ/automatic-network-rebooter{format.END}")

        # Let user know that blank inputs will use the default values
        print(format.BOLD + format.PINK + "\nNote:" + format.END)
        print("If you leave any input blank, the program will use the default values for that setting if available.")
        print("You can change these settings later by editing the 'config.json' file in the program directory.")

        # Ask the user to enter the router's IP address / gateway address
        print(format.BOLD + format.PINK + "\nStep 01/9384: Router IP Address" + format.END)
        print("Please enter the IP address of your router / modem. This is usually the gateway address.")
        router_ip_address = user_input_ip_address(True)

        # Ask the user to enter the router's password
        print(format.BOLD + format.PINK + "\nStep 02/9384: Router Password" + format.END)
        print("Please enter the password of your router / modem. This is the password you use to login to the router's admin panel.")
        print("You can leave this empty to not save it to the config file, but you will be asked to enter it every time the program runs.")
        router_password = input("Enter the router password: ") # No verification needed for password

        # Ask the user to enter the list of urls / ip addresses to ping, or use the default list
        print(format.BOLD + format.PINK + "\nStep 03/9384: Ping List" + format.END)
        print("This is the list of websites / servers / IP addresses that the program will ping to check the internet connection.")
        print("By default, the program will ping the following list of websites/servers:")
        print("1) 8.8.8.8             (Google's Public DNS Server)")
        print("2) 1.1.1.1             (Cloudflare's Public DNS Server)")
        print("3) www.apple.com       (Apple's website)")
        print("4) www.azure.com       (Microsoft's Azure website)")
        print("5) www.amazonaws.com   (Amazon's AWS website)")
        print("\nDo you want to use the default list of websites / servers to ping?")
        print("If you choose 'N', you will be asked to enter your own list of addresses.")
        custom_ping_list = user_input_yes_no()
        if custom_ping_list.lower() == "n":
            ping_list = user_input_ping_list()
        else:
            ping_list = ["8.8.8.8", "1.1.1.1", "www.apple.com", "www.azure.com", "www.amazonaws.com"]

        # Ask the user to enter how many of the ping addresses must be reachable to consider the internet connection as unstable
        print(format.BOLD + format.PINK + "\nStep 04/9384: Ping Addresses Threshold" + format.END)
        print("This is the number of ping addresses that must be failed to consider the internet connection as unstable.")
        print("For example, if you enter '2', the program will consider the internet connection as unstable if 2 or more ping addresses are unreachable and will reboot the network.")
        print(f"By default, the program will consider the internet connection as unstable if 100% of the ping addresses ({len(ping_list)}) are unreachable.")
        print(f"Enter the number of unreachable ping addresses to consider the internet connection as unstable (1-{len(ping_list)}):")
        unreachable_ping_threshold = user_input_number_in_range(1, len(ping_list), True)

        # Ask the user to enter the frequency of the ping check cycles
        print(format.BOLD + format.PINK + "\nStep 05/9384: Ping Check Cycle Frequency" + format.END)
        print("This is the number of seconds to wait between each ping check cycle.")
        print("For example, if you enter '30', the program will check the internet connection every 30 minutes.")
        print("By default, the program will check the internet connection every 10 minutes.")
        print("Enter the number of minutes to check the internet connection (in minutes 1-483840):")
        ping_check_frequency = user_input_number_in_range(1, 483840, True)

        # Ask the user to enter the number of times to retry the ping if it fails
        print(format.BOLD + format.PINK + "\nStep 06/9384: Ping Retry Interval" + format.END)
        print("This is the number of retries to attempt if the ping fails for an address.")
        print("For example, if you enter '2', the program will retry the ping 2 times before considering the address as unreachable.")
        print("Or if you enter '0', the program will not retry the ping and consider the address as unreachable after the first failed ping.")
        print("By default, the program will retry the ping 2 times before considering the address as unreachable.")
        print("Enter the number of times to retry the ping if it fails (0-10):")
        ping_retry_amount = user_input_number_in_range(0, 10, True)

        # Ask the user to enter the number of seconds to wait between each ping retry if the ping fails
        print(format.BOLD + format.PINK + "\nStep 07/9384: Ping Retry Interval" + format.END)
        print("This is the number of seconds to wait between each ping retry if the ping fails.")
        print("For example, if you enter '10', the program will wait 10 seconds between each ping retry.")
        print("By default, the program will wait 10 seconds between each ping retry.")
        print("Enter the number of seconds to wait between each ping retry (in sceonds, 1-300):")
        ping_retry_interval = user_input_number_in_range(1, 300, True)

        # Ask the user to enter the number of seconds to wait between each network reboot
        print(format.BOLD + format.PINK + "\nStep 08/9384: Network Reboot Interval" + format.END)
        print("This is the number of minutes to wait before checking the internet connection after rebooting the network.")
        print("For example, if you enter '15', the program will wait 15 minutes before checking the internet connection after rebooting the network.")
        print("By default, the program will wait 15 minutes before starting the internet connection check cycle after rebooting the network.")
        print("Enter the number of minutes to wait before checking the internet connection after rebooting the network (in minutes, 5-1440):")
        network_reboot_interval = user_input_number_in_range(5, 1440, True)

        # Ask the user to enter the number of times to reboot the network before giving up (going into cooldown, then retrying)
        print(format.BOLD + format.PINK + "\nStep 09/9384: Network Reboot Retry Count" + format.END)
        print("This is the number of times the program will reboot the network before giving up if the internet connection is still unstable.")
        print("For example, if you enter '3', the program will reboot the network 3 times and if the internet connection is still unstable in a row, the program will go into a cooldown period (which you will specify next).")
        print("By default, the program will reboot the network 3 times before giving up.")
        print("Enter the number of times to reboot the network before giving up (1-10):")
        network_reboot_retry_count = user_input_number_in_range(1, 10, True)

        # Ask the user to enter the cooldown period after consecutive network reboots
        print(format.BOLD + format.PINK + "\nStep 10/9384: Network Reboot Cooldown Period" + format.END)
        print("This is the number of minutes to wait before checking the internet connection again after multiple consecutive network reboots.")
        print("For example, if you enter '60', the program will wait 60 minutes (1 hour) before checking the internet connection again after multiple reboots.")
        print("By default, the program will wait 120 minutes before checking the internet connection again after multiple reboots.")
        print("Enter the number of minutes to wait before checking the internet connection again after multiple reboots (1-1440):")
        network_reboot_cooldown_period = user_input_number_in_range(1, 1440, True)

        # Ask the user to enter if they want to log the connection status, checks and reboots to a file
        print(format.BOLD + format.PINK + "\nStep 11/9384: Log File" + format.END)
        print("Do you want to log the connection status, checks and reboots to a file? (located in `logs` folder as json)")
        print("If you choose 'Y', the program will log the connection status, checks and reboots to a file in the program directory. If you choose 'N', the program will not log the connection status, checks and reboots to a file.")
        print("By default, the program will not log the connection status, checks and reboots to a file for privacy security.")
        print("Do you want to log the connection status, checks and reboots to a file?")
        log_file = user_input_yes_no(True)

        # Set blank values to default values
        if router_ip_address == "" or router_ip_address == None:
            router_ip_address = "" # Enter on runtime
        if router_password == "" or router_password == None:
            router_password = "" # Enter on runtime
        if unreachable_ping_threshold == "" or unreachable_ping_threshold == None:
            unreachable_ping_threshold = len(ping_list)
        if ping_check_frequency == "" or ping_check_frequency == None:
            ping_check_frequency = 10
        if ping_retry_amount == "" or ping_retry_amount == None:
            ping_retry_amount = 2
        if ping_retry_interval == "" or ping_retry_interval == None:
            ping_retry_interval = 10
        if network_reboot_interval == "" or network_reboot_interval == None:
            network_reboot_interval = 15
        if network_reboot_retry_count == "" or network_reboot_retry_count == None:
            network_reboot_retry_count = 3
        if network_reboot_cooldown_period == "" or network_reboot_cooldown_period == None:
            network_reboot_cooldown_period = 120
        if log_file == "" or log_file == None or log_file.lower() == "n":
            log_file = False
        elif log_file.lower() == "y":
            log_file = True

        # Print the configuration settings to the user
        print(format.BOLD + format.PINK + "\nConfiguration Settings" + format.END)  
        print(f"Router IP Address: {router_ip_address}")
        print(f"Router Password: {router_password}")
        print(f"Ping List: {ping_list}")
        print(f"Unreachable Ping Threshold: {unreachable_ping_threshold}")
        print(f"Ping Check Frequency: {ping_check_frequency}")
        print(f"Ping Retry Amount: {ping_retry_amount}")
        print(f"Ping Retry Interval: {ping_retry_interval}")
        print(f"Network Reboot Interval: {network_reboot_interval}")
        print(f"Network Reboot Retry Count: {network_reboot_retry_count}")
        print(f"Network Reboot Cooldown Period: {network_reboot_cooldown_period}")
        print(f"Log File: {log_file}")

        # Ask the user to confirm the configuration settings
        print(format.BOLD + format.PINK + "\nDo you want to save these settings?" + format.END)
        print("If you choose 'Y', the program will save these settings to the 'config.json' file in the program directory.")
        print("If you choose 'N', the program will ask you to re-enter the settings.")
        save_settings = user_input_yes_no()
        if save_settings.lower() == "y":
            break

    # set the values to the configuration settings dictionary
    configuration_settings = {
        "router_details": {
            "router_ip_address": router_ip_address,
            "router_password": router_password
        },
        "ping": {
            "ping_list": ping_list,
            "unreachable_ping_threshold": unreachable_ping_threshold,
            "ping_check_frequency": ping_check_frequency,
            "ping_retry_amount": ping_retry_amount,
            "ping_retry_interval": ping_retry_interval
        },
        "network": {
            "network_reboot_interval": network_reboot_interval,
            "network_reboot_retry_count": network_reboot_retry_count,
            "network_reboot_cooldown_period": network_reboot_cooldown_period
        },
        "log_file": log_file
    }

    try:
        # Save the configuration settings to the config.json file
        with open("config.json", "w") as file:
            json.dump(configuration_settings, file, indent=4)

            # Print the success message
            print(format.GREEN + format.BOLD + "\nConfiguration settings saved successfully!" + format.END)
            print("You can change the configuration settings by editing the 'config.json' file in the program directory or by deleting the file and running the program again.")
            print("If you need help with the configuration settings, please read the README.md file or visit the github page at:")
            print(f"{format.YELLOW}https://github.com/majdiJ/automatic-network-rebooter{format.END}")

    except Exception as e:
        print(f"{format.RED}Error saving the configuration settings to the 'config.json' file.{format.END}")
        print(f"Error: {e}")
        return

# Run the program setup wizzard if the file is run by itself
if __name__ == "__main__":
    program_setup_wizzard()