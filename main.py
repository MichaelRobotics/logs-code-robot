#!/usr/bin/env python3

from log_generator import LogGenerator
from robot_data import RobotData
from log_data_interpretation import AllApDataInterpreter
import requests
import json
from utils import BearerAuth
from os import getenv
from urllib3.exceptions import InsecureRequestWarning
from pathlib import Path

home_directory = Path.home()

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Fleet Address
FLEET_PORT = ":443"
FLEET_IP = "192.168.1.31"

# Log paths on robots
PATH_TO_LOGS_ROBOT = "/home/vb/log/latest/robot.log"

# Paths for final output
# ADD FINAL PATHS

def connect_to_all_active_robots(ip_values, id_values, username_values, password_values):

    objects_list = []
    username_iterator = iter(username_values)
    password_iterator = iter(password_values)
    print(ip_values)
    print(id_values)
    print(username_values)
    print(password_values)
    # Create objects that communicate to PC's with robots onboard
    for ip_val, id_val in zip(ip_values, id_values):
        try:
            username = next(username_iterator)
            password = next(password_iterator)
            robot_data_obj = RobotData(ip_val, id_val, 22, username, password)
            objects_list.append(robot_data_obj)
            print(objects_list)
        except Exception as e:
            print(f"An error occurred when creating RobotData object for robot '{ip_val}': {e}")

    # Printing PC's identification
    for obj in objects_list:
        print("XF")
        print(f"ip_val: {obj.hostname}, user: {obj.username}")
    return objects_list

#  MUST MODIFY IN PRODUCTION!!!
def connect_to_fleet(ip_value):
    try:
        fleet_data_obj = RobotData(ip_value, None, 22, "vb", "Versabot2001")
        return fleet_data_obj
    except Exception as e:
        print(f"An error occurred when creating RobotData object for fleet '{ip_value}': {e}")
        return None

def transform_ip_pas_usr(ip_values):
    """
        !!! TESTING_FUNCTION! NOT USED IN PRODUCTION !!! 
    """
    actual_ip_val = []
    actual_username_val = []
    actual_password_val = []
    for ip_val in ip_values:
        if ip_val == "robotone":
            actual_ip_val.append("192.168.1.78")
            actual_username_val.append("vbmichal2")
            actual_password_val.append("vbrobot123")
        elif ip_val == "robottwo":
            actual_ip_val.append("192.168.1.73")
            actual_username_val.append("dev")
            actual_password_val.append("vbrobot123")
        elif ip_val == "robotthree":
            actual_ip_val.append("192.168.1.31")
            actual_username_val.append("vb")
            actual_password_val.append("Versabot2001")
        else:
            print(f"Invalid IP value: {ip_val}")
    return actual_ip_val, actual_username_val, actual_password_val

def get_data_active_robots():
    try:
        auth_bearer = BearerAuth(getenv('JWT_API_KEY',
                                     'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTc2MTU1MjIsIm5iZiI6MTY1NzYxNTUyMiwianRpIjoiYmYzZDY0YmQtOGZmNC00NGZhLWJmZDItZmExZGE0MzhiMDcwIiwiZW1haWwiOiJ2YiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInJvbGVzIjpbIlNVUEVSX1VTRVIiXX0.J917aI2m8vTOFkAD8WjKs7s86fDM5x1nHH9sWwdfaVA'))
        response = requests.get(
            f'https://{FLEET_IP}{FLEET_PORT}/api/v1/fleet/robot-info',
            auth=auth_bearer, verify=False, timeout=50)
        response.raise_for_status()  # Raise an exception if the HTTP response status code is not in the 200-299 range
    except requests.exceptions.RequestException as e:
        # Handle network-related exceptions (e.g., connection errors, timeouts)
        print(f"RequestException: {e}")
        return  None
    try:
    ##############COMMENTED FOR NOT WORKING FLEET API###############
    #    workers = response.json()  # Parse the JSON response
    #    ip_values = [item['robotSpec']['ip'] for item in workers]
    #    id_values = [item['robotSpec']['id'] for item in workers]
    #    online_values = [item['online'] for item in workers]
    #    merged_ip_online = {ip: online for ip, online in zip(ip_values, online_values)}
    #    merged_id_online = {id: online for id, online in zip(id_values, online_values)}
    #    active_robot_ip_list = [key for key, val in merged_ip_online.items() if val == True]
    #    active_robot_id_list = [key for key, val in merged_id_online.items() if val == True]
    #    print(active_robot_ip_list)
    #    print(active_robot_id_list)
    ########################################################
        active_robot_ip_list = ["robotone", "robottwo", "robotthree"]
        active_robot_id_list = ["robotone", "robottwo", "robotthree"]
        return active_robot_ip_list, active_robot_id_list
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"JSONDecodeError: {e}")
        return  None

def main():
    try:
        # Get Ip from active robots on fleet
        ip_values, id_values = get_data_active_robots()

        actual_ip_val, actual_username_val, actual_password_val = transform_ip_pas_usr(ip_values)
        if ip_values is None:
            raise ValueError("The 'ip_values' variable is None.")
        robot_list = connect_to_all_active_robots(actual_ip_val, id_values, actual_username_val, actual_password_val)
        print("xfxfsdf")
        print(robot_list)
        All_AP_dataframe = LogGenerator(robot_list) #PATH_TO_LOGS_ROBOT
        All_AP_dataframe_file = All_AP_dataframe.generate_log_output()
        All_AP_dataframe_file.to_csv('All_AP_dataframe_file.txt', sep='\t', index=False)
        print(All_AP_dataframe_file)
        Data_interpreter_instance = AllApDataInterpreter(All_AP_dataframe_file)
        print("whatsup")
        Data_interpreter_instance.generate_all_robot_dataframe()

#        print(Data_interpreter_instance.filter_for_correct_ap_actions())

    except Exception as e:
        print(f"An error occurred when executing main script: {e}")
        # You can also log the exception or take other actions as needed

if __name__ == "__main__":
    main()


    ############## FOR TESTING! ###############
    #
    # Not every user of this script have an PC named VB!! change this in code.
    # 
    # TO DO:
    # 1. Put Logs and manage excpectations of log_data_interpretation
    # 2. Try to make it more readable and ready to customize and reprezentation
    # 3. Make version for sim and Robots
    # 4. Discuss for proper logs interpretation
    #
    #
    ########################################

