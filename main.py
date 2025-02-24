# A Python script that monitors internet connectivity and automatically reboots the
# network if a connection issue is detected. Designed to run on a home server, it
# ensures continuous internet access by resetting the Virgin Media router when necessary.

# Import the required libraries
import os
import time
import requests
import json
import subprocess
import program_setup

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
def user_input_ip_address():
    while True:
        user_input = input("Enter the IP address of the router: ")
        if verify_user_input_ip_address(user_input):
            return user_input
        print(f"\n{format.RED}Invalid IP address. Please try again.{format.END}")
        print("The IP address must be in the format: xxx.xxx.xxx.xxx (if you are unsure, please read the README.md file)")

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

# Program welcome message
def program_boot_message():
    # Print the program boot message
    print(format.GREEN + format.BOLD + "\n=========== Automatic Network Rebooter ( version: 0.0.0 ) ===========" + format.END)
    print("This python script monitors the network's internet connectivity and automatically reboots\nthe network if a connection issue is detected. It's designed for the Virgin Media Hub 5\nrouter / modem")
    print("Contributions are very much welcome! Improve the program by adding more features, settings\nand wider modem / router support.")
    print(f"\nCreated by {format.BOLD + format.BLUE}Majdi Jaigirdar{format.END} - Check out my github at {format.YELLOW}https://github.com/majdiJ" + format.END)
    print(f"visit my website at {format.YELLOW}https://majdij.github.io{format.END} and {format.YELLOW}https://alamnetwork.com/{format.END}")
    print(format.GREEN + "======================================================================" + format.END + "\n\n")

# Load the configuration settings from the config.json file
def load_configuration_settings():
    try:
        # Load the configuration settings from the config.json file
        with open("config.json", "r") as file:
            configuration_settings = json.load(file)
            return configuration_settings
    except Exception as e:
        print(f"{format.RED}Error loading the configuration settings from the 'config.json' file. Please try again.{format.END}")
        print(f"Error: {e}")
        return

# Confirm the configuration settings to load
def confirm_settings_to_load():
    # Ask the user to confirm the configuration settings they are about to start the program with
    # If the config is not set up correctly and carefully, the program may not work as expected and
    # the useer may put their network at risk to a loop of reboots that may cause the ISP to limit the
    # connection or lock the router. If the user only has remote access to the router, they may lose
    # access to the router and the network if the configuration is not set up correctly.
    print(format.BOLD + format.RED + "\n\n====================  Warning:  ====================" + format.END)
    print("Please confirm the configuration settings carefully before starting the program.")
    print("If the configuration settings are not set up correctly, the program may not work as expected.")
    print("If the program is not set up correctly, it may cause the network to go into a loop of reboots.")
    print("If the network goes into a loop of reboots, the ISP may limit the connection or lock the router.")
    print("If you only have remote access to the router, you may lose access to the router and the network.")
    print("Please confirm the configuration settings carefully before starting the program...")
    print("Please make sure you have permission to reboot the network and access the router.")
    print(format.RED + "You are responsible for the configuration settings and the network." + format.END)
    print(format.BOLD + format.RED + "=====================================================" + format.END)

    print(format.BOLD + format.PINK + "\nDo you want to start the program with these settings?" + format.END)
    print("If you choose 'Y', the program will start monitoring the network with the configuration settings loaded.")
    print("If you choose 'N', the program will end")
    start_program = user_input_yes_no()
    if start_program.lower() == "y":
        print("Starting the program with the configuration settings loaded...")
    else:
        print("Ending the program...")
        exit()

# Ping an address to check the internet connection
def ping_address_bool(address):
    try:
        result = subprocess.run(["ping", "-c", "1", address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        return False

# Generate login token
def generate_login_token(base_url, password):
    payload = {"password": password}
    url = base_url + "/rest/v1/user/login"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            json_response = response.json()
            token = json_response.get("created", {}).get("token")
            if token:
                print("Login successful! Token:", token)
                return token
            else:
                print("Unexpected response format:", json_response)
                return None
        else:
            print("Login failed. Server response:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
# Reboot system
def reboot_system(base_url, token):
    payload = {"reboot": {"enable": True}}
    url = base_url + "/rest/v1/system/reboot"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    try:
        # Set a timeout of 5 seconds; if no response is received, it will raise a Timeout exception
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        # If a response is received, then something might be wrong (e.g., authentication issue)
        print("Reboot request failed. Server response:", response.text)
    except requests.exceptions.Timeout:
        # If a timeout occurs, assume the modem is rebooting as expected
        print("No response after 5 seconds. Assuming the modem is rebooting successfully.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Logout
def logout(base_url, token):
    url = base_url + "/rest/v1/user/3/token/" + token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    try:
        response = requests.delete(url, headers=headers)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":

    # Clear the terminal window
    os.system("clear")

    # Print the program boot message
    program_boot_message()

    # wait for 3 seconds to let the user read the boot message
    time.sleep(3)

    # check if the config file exists
    if os.path.exists("config.json"):
        print("'config.json' file found. Loading the configuration settings...")
        configuration_settings = load_configuration_settings()
        
        # Confirm the configuration settings to load
        confirm_settings_to_load()

        print("\nStarting the program with the configuration settings loaded...\n\n")

        while True:
            # check the internet connection with the ping list
            print(">>> Checking the internet connection...")

            list_of_ping_addresses = configuration_settings["ping"]["ping_list"]
            unreachable_ping_threshold = configuration_settings["ping"]["unreachable_ping_threshold"]
            ping_retry_amount = configuration_settings["ping"]["ping_retry_amount"]
            ping_retry_interval = configuration_settings["ping"]["ping_retry_interval"]

            # Number of failed pings
            failed_pings = 0

            # loop through the list of ping addresses
            for ping_address in list_of_ping_addresses:

                # if total failed pings is greater than the unreachable ping threshold, break the loop
                if failed_pings >= unreachable_ping_threshold:
                    break

                specific_failed_pings = 0
                
                # Loop for numbwer of ping retries
                for i in range(ping_retry_amount):
                    # Ping the address to check the internet connection
                    if ping_address_bool(ping_address):
                        print(f">>>({format.GREEN}Ping successful{format.END} - {ping_address}")
                        break
                    else:
                        print(f">>>({format.RED}Ping failed{format.END} - {ping_address}")
                        specific_failed_pings += 1
                        time.sleep(ping_retry_interval)
                
                if specific_failed_pings == ping_retry_amount:
                    failed_pings += 1
            
            number_of_reboots_in_a_row = 0

            # Check if threshold is reached, and reboot the network
            if failed_pings >= unreachable_ping_threshold:
                print(f"\n>>> {format.RED}Internet connection is unstable. Should reboot...{format.END}")
                number_of_reboots_in_a_row += 1
                # Reboot the network
                
                router_ip_address = configuration_settings["router_details"]["router_ip_address"]
                router_password = configuration_settings["router_details"]["router_password"]
                base_url = f"http://{router_ip_address}"

                # Generate login token
                print(">>> Generating login token...")
                token = generate_login_token(base_url, router_password)
                if token:
                    print(">>> Token generated successfully!")
                    time.sleep(2)
                    
                    # Reboot the system using the token
                    print(">>> Rebooting the network...")
                    reboot_system(base_url, token)

                    # Logout
                    print(">>> Logging out...")
                    logout(base_url, token)

            else:
                print(f"\n>>> {format.GREEN}Internet connection is stable. No need to reboot.{format.END}")
                number_of_reboots_in_a_row = 0

            # if the number of reboots in a row is greater than the network reboot retry count, go into cooldown period
            if number_of_reboots_in_a_row >= configuration_settings["network"]["network_reboot_retry_count"]:
                print(f"\n>>> {format.RED}Network reboot retry count reached. Going into cooldown period for {configuration_settings['network']['network_reboot_cooldown_period']} minutes...{format.END}")
                time.sleep(configuration_settings["network"]["network_reboot_cooldown_period"] * 60)


            ping_check_frequency = configuration_settings["ping"]["ping_check_frequency"]
            time.sleep(ping_check_frequency * 60)
            break
    else:
        program_setup.program_setup_wizzard()
        print("\nRestart the program to start monitoring the network with the configuration settings loaded.")