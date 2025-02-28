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
    ITALIC = "\033[3m"
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
    print("\nPlease read the README.md file for more information on how to use the program.")
    print(f"Github Repository: {format.YELLOW}https://github.com/majdiJ/automatic-network-rebooter{format.END}")
    print(f"\nCreated by {format.BOLD + format.BLUE}Majdi Jaigirdar{format.END} - Check out my github at {format.YELLOW}https://github.com/majdiJ" + format.END)
    print(f"visit my website at {format.YELLOW}https://majdij.github.io{format.END} and {format.YELLOW}https://alamnetwork.com/{format.END}")
    print(format.GREEN + "======================================================================" + format.END)

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
    print(format.BOLD + format.RED + "\n====================  Warning:  ====================" + format.END)
    print("Please confirm the configuration settings carefully before starting the program.")
    print("If the configuration settings are not set up correctly, the program may not work as expected.")
    print("If the program is not set up correctly, it may cause the network to go into a loop of reboots.")
    print("If the network goes into a loop of reboots, the ISP may limit the connection or lock the router.")
    print("If you only have remote access to the router, you may lose access to the router and the network.")
    print("Please confirm the configuration settings carefully before starting the program...")
    print("Please make sure you have permission to reboot the network and access the router.")
    print(format.RED + "You are responsible for the configuration settings and the network." + format.END)
    print(format.BOLD + format.RED + "=====================================================" + format.END)

    print(format.BOLD + format.RED + "\nDo you want to start the program with these settings?" + format.END)
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
        if response.status_code == 204:
            print(f"{format.GREEN}Logout successful!{format.END}")
        else:
            print("Logout failed. Server response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Test: Login to the router
def test_login_to_router(configuration_settings):
    router_ip_address = configuration_settings["router_details"]["router_ip_address"]
    router_password = configuration_settings["router_details"]["router_password"]
    base_url = f"http://{router_ip_address}"

    # Generate login token
    print(f" >>> Generating login token for {router_ip_address}...")
    token = generate_login_token(base_url, router_password)
    if token:
        print(f"     - {format.GREEN}{format.BOLD}Login test successful!{format.END}")
        time.sleep(2)
        
        # Logout
        print(" >>> Logging out...")
        logout(base_url, token)
    else:
        print("Login test failed. Please check the configuration, the router IP address and password.")
        print("If you need help, please read the README.md and/or visit the Github repository.")
        print("Stopping the program...")
        exit()

# Test: Reboot the network
def test_reboot_network(configuration_settings):
    router_ip_address = configuration_settings["router_details"]["router_ip_address"]
    router_password = configuration_settings["router_details"]["router_password"]
    base_url = f"http://{router_ip_address}"

    # Generate login token
    print(f" >>> Generating login token for {router_ip_address}...")
    token = generate_login_token(base_url, router_password)
    if token:
        print(f"     - {format.GREEN}{format.BOLD}Login successful!{format.END}")
        time.sleep(2)

        # Reboot the system using the token
        print(" >>> Rebooting the network...")
        reboot_system(base_url, token)

        # Logout
        print(" >>> Logging out...")
        logout(base_url, token)
    else:
        print("Reboot test failed. Please check the configuration, the router IP address and password.")
        print("Make sure your router is supported by the program.")
        print("If you need help, please read the README.md and/or visit the Github repository.")
        print("Stopping the program...")
        exit()

if __name__ == "__main__":

    # Clear the terminal window
    os.system("clear")

    # Print the program boot message
    program_boot_message()

    # Press to continue
    print(f"\n{format.ITALIC}Press enter to continue...{format.END}")
    input()

    # Clear the terminal window
    os.system("clear")

    # check if the config file exists
    print(f"\n{format.BOLD}Checking to see if `config.json` exists...{format.END}")
    print(f"`config.json` is the configuration file that stores the settings for the program. Such as the router IP address, password, ping list and more")
    print(f"If it does not exist, the program will start the program setup wizard to make a new config.json file.")

    if os.path.exists("config.json"):

        # Check successful
        print(f" > {format.GREEN}{format.BOLD}Success!{format.END} `config.json` exists.\n")

        configuration_settings = load_configuration_settings()
        
        # Confirm the configuration settings to load
        confirm_settings_to_load()

        # Clear the terminal window
        os.system("clear")

        # Check if config.json has the router IP address set
        print(f"\n{format.BOLD}Checking to see if `config.json` has the router IP address and password set...{format.END}")
        print(f"You can chose not save these settings in the configuration settings and enter them manually each time the program starts for security reasons. This is optional.")

        if configuration_settings["router_details"]["router_ip_address"] == "" or configuration_settings["router_details"]["router_ip_address"] == None or "router_ip_address" not in configuration_settings["router_details"]:
            print(f" > {format.RED}{format.BOLD}Unsuccess.{format.END} The router IP address is not set in the configuration settings.")
            print("Please enter the IP address of the router to continue...")
            configuration_settings["router_details"]["router_ip_address"] = user_input_ip_address()
            print(f"Router IP address set to: {configuration_settings['router_details']['router_ip_address']} (not saved in the configuration settings)")
        else:
            print(f" > {format.GREEN}{format.BOLD}Success!{format.END} The router IP address is set in the configuration settings.")

        if configuration_settings["router_details"]["router_password"] == "" or configuration_settings["router_details"]["router_password"] == None or "router_password" not in configuration_settings["router_details"]:
            print(f" > {format.RED}{format.BOLD}Unsuccess.{format.END} The router password is not set in the configuration settings.")
            print("Please enter the password of the router to continue...")
            configuration_settings["router_details"]["router_password"] = input("Enter the password of the router: ")
            print(f"Router password set (not saved in the configuration settings)")
        else:
            print(f" > {format.GREEN}{format.BOLD}Success!{format.END} The router password is set in the configuration settings.")

        # Ask the user if they would like to test if the program can login to the router
        print(f"\n{format.BOLD}{format.CYAN}Do you want to test if the program can login to the router?{format.END}")
        print("This will test if the program can login to the router using the password provided in the configuration settings.")
        print("It will attempt to generate a login token, login to the router then logout. It will NOT reboot the network.")
        print("If you choose 'Y', the program will attempt to login to the router.")
        print("If you choose 'N', the program will skip the login test.")
        login_test = user_input_yes_no()

        if login_test.lower() == "y":
            test_login_to_router(configuration_settings)
        else:
            print(f"{format.ITALIC}Skipping the login test...{format.END}")

        # Ask the user if they would like to test if the program can reboot the network
        print(f"\n{format.BOLD}{format.CYAN}Do you want to test if the program can reboot the network?{format.END}")
        print("This will test if the program can login to the router, reboot the network then logout.")
        print("If you choose 'Y', the program will attempt to reboot the network.")
        print("If you choose 'N', the program will skip the network reboot test.")
        reboot_test = user_input_yes_no()

        if reboot_test.lower() == "y":
            test_reboot_network(configuration_settings)
        else:
            print(f"{format.ITALIC}Skipping the network reboot test...{format.END}")

        # Clear the terminal window
        os.system("clear")

        # Ask the user if they would like to start the program now
        print(f"\n{format.BOLD}{format.CYAN}Do you want to start the program now?{format.END}")
        print("If you choose 'Y', the program will start monitoring the network with the configuration settings loaded.")
        print("If you choose 'N', the program will end.")
        start_program = user_input_yes_no()

        if start_program.lower() == "y":
            print(f"{format.ITALIC}Starting the program with the configuration settings loaded...{format.END}\n")
        else:
            print("Ending the program...")
            exit()

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
                        print(f">>>({format.GREEN}Ping successful{format.END}) - {ping_address} - (attempt: {i + 1}/{ping_retry_amount + 1})")
                        break
                    else:
                        if ping_retry_amount > 1:
                            print(f">>>({format.RED}Ping failed{format.END}) - {ping_address} - Will retry in {ping_retry_interval} seconds (attempt: {i + 1}/{ping_retry_amount + 1})")
                        else:
                            print(f">>>({format.RED}Ping failed{format.END}) - {ping_address}")
                        specific_failed_pings += 1
                        time.sleep(ping_retry_interval)
                
                if specific_failed_pings == ping_retry_amount:
                    failed_pings += 1
            
            number_of_reboots_in_a_row = 0

            # Check if threshold is reached, and reboot the network
            if failed_pings >= unreachable_ping_threshold:
                print(f"\n>>> {format.RED}Internet connection is considered unstable. ({failed_pings}/{unreachable_ping_threshold} failed pings){format.END}")
                print(f">>> Rebooting the network...")

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

                    # wait after rebooting the network
                    print(f">>> Waiting for {configuration_settings['network']['network_reboot_interval']} minutes after rebooting the network...")
                    time.sleep(configuration_settings["network"]["network_reboot_interval"] * 60)
                    
            else:
                print(f"\n>>> {format.GREEN}Internet connection is considered stable. ({failed_pings}/{unreachable_ping_threshold} failed pings){format.END}")
                number_of_reboots_in_a_row = 0

            # if the number of reboots in a row is greater than the network reboot retry count, go into cooldown period
            if number_of_reboots_in_a_row >= configuration_settings["network"]["network_reboot_retry_count"]:
                print(f">>> {format.RED}Network reboot retry count reached. Going into cooldown period for {configuration_settings['network']['network_reboot_cooldown_period']} minutes...{format.END}")
                time.sleep(configuration_settings["network"]["network_reboot_cooldown_period"] * 60)
                print(f">>> Cooldown period ended. Resuming network monitoring...")

            ping_check_frequency = configuration_settings["ping"]["ping_check_frequency"]
            print(f">>> Waiting for {ping_check_frequency} minutes before checking the internet connection again...")
            time.sleep(ping_check_frequency * 60)
    else:
        # Check failed
        print(f" > {format.RED}{format.BOLD}Unsuccess.{format.END} `config.json` does not exist.")
        print(f"{format.ITALIC}Starting the program setup wizard...{format.END}")

        program_setup.program_setup_wizzard()
        print("\nRestart the program to start monitoring the network with the configuration settings loaded.")