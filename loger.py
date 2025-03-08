# This is file is used by the program to log the data about the automatic network
# rebooter. This file is not inteded to be ran by itself, but rather imported by
# the main program (`main.py`) when the user configures the program to log data.
# The log files will be saved in a folder called `logs`, these logs will be saved
# in folders named by the year, and each file will be named by the month. 
# This is done as log files can get quite large, and this way the program can
# easily manage the files and easier for the user to access. Additionally, there
# will be `view-log.html` file that will allow the user to easily view the 
# {month}.json file in a more user friendly way.

# Import the required modules
import os
import json
import datetime

# Initials a log file for the current month in the logs/{year} folder
def Initialise_log_file():
    # Get the current date
    now = datetime.datetime.now()
    # Get the current year
    year = now.year
    # Get the current month
    month = now.strftime("%B")
    # Create the folder if it doesn't exist
    if not os.path.exists(f"logs/{year}"):
        os.makedirs(f"logs/{year}")
    # Create the log file for the current month
    with open(f"logs/{year}/{month}.json", "w") as file:
        file.write("[]")

# [
#     {
#         "timestamp": "2025-03-01T00:00:00.000Z",
#         "status": "success",
#         "log": {
#             "message": "User logged in",
#             "internet_connection": "yes",
#             "network_reboot": "no"
#         }
#     }
# ]

# Example of what they can be
# status: success, error, neutral
# ping_status: success, error, n/a
# internet_connection: yes, no, n/a
# network_reboot: yes, no, n/a

def write_to_log_file(status, message, ping_status = "n/a", internet_connection = "n/a", network_reboot = "n/a"):
    # Get the current date and time in the ISO format
    timestamp = datetime.datetime.now().isoformat()
    # Get the current year
    year = datetime.datetime.now().year
    # Get the current month
    month = datetime.datetime.now().strftime("%B")
    # Open the log file for the current month
    with open(f"logs/{year}/{month}.json", "r") as file:
        # Load the data from the file
        data = json.load(file)
    # Append the new log data to the list
    data.append({
        "timestamp": timestamp,
        "status": status,
        "log": {
            "message": message,
            "ping_status": ping_status,
            "internet_connection": internet_connection,
            "network_reboot": network_reboot
        }
    })
    # Write the new data to the file
    with open(f"logs/{year}/{month}.json", "w") as file:
        json.dump(data, file, indent=4)
    

if __name__ == "__main__":
    Initialise_log_file()

    # Test the write_to_log_file function
    write_to_log_file("success", "User logged in", "yes", "no")
    write_to_log_file("error", "Failed to ping address", "no", "no")
    write_to_log_file("error", "Failed to reboot network", "yes", "no")
    write_to_log_file("success", "User logged out", "yes", "no")

# To do:
# - Design how the log file will be structured
# - Write the log functions:
#   - Log when the program starts
#   - Log when the program stops
#   - Log when the program reboots the network
#   - Log when the program fails to ping the addressess
#   - Log when the program fails to reboot the network
# - Make `view-log.html` file (this will be a simple html file, not a proper web app)