import pandas as pd
from log_comparer import Comparer
import os


VB_MANAGER_LOG_BUFF_PATH = "/tmp/fleetlogbuffile.txt"
SAFETY_BRIDGE_BUFF_PATH = "/tmp/safetybridgefile.txt"


VB_MANAGER_TEXT_TO_FIND = [["vb_manager.am - info - PFT", "Action completed."], 
                      ["vb_manager.mm - info - PFT", "ActionPoint", "started"],
                      ["vb_manager.am", "Action", "waiting", "help"],
                      ["vb_manager.am", "Action", "aborted"],
                      ["vb_manager.action", "Position correct"],
                      ["vb_manager.action", "error", "Position incorrect because position sensor (tr) is not active"],
                      ["vb_manager.action", "Departing failed"]
                      ]

SAFETY_BRIDGE = [["tool.modbus", "Connected"],
                 ["tool.modbus", "Disconnected"]]

class LogGenerator:
    def __init__(self, robotlist: list):
        self.robotlist = robotlist
        self.All_AP_data = None


    def log_filter(self, input_file_path: str, output_file_path: str, text_to_find: list):
        # Texts to search for in the file
        # Open the input file, read lines containing the specified texts and save to output file
        try:
            print(f"Input file path: {input_file_path}")
            print(f"Output file path: {output_file_path}")
            with open(input_file_path, 'r') as input_file:
                irn = input_file.readlines()
                with open(output_file_path, 'w') as output_file:
                    for line in irn:
                        for keywords in text_to_find:
                            if all(keyword in line for keyword in keywords):
                                print(line)
                                output_file.write(line)
                                output_file.seek(0, os.SEEK_END)  # Go to the end of the file
                                if output_file.tell() == 0:  # If the current position is 0, the file is empty
                                    raise ValueError("Output file is empty after write operation")
            return output_file
        except FileNotFoundError:
            print("File not found. Please provide valid file paths.")
            return None
        except FileExistsError:
            print("The output file already exists. Please provide a different output file path.")
            return None

    def filter_vbmanagerlog(self, path_to_save: str, texts_to_find: list ):
        output_file_path = VB_MANAGER_LOG_BUFF_PATH
        self.log_filter(path_to_save, output_file_path, texts_to_find)
        return output_file_path

    def filter_safetybridge(self, path_to_save: str, texts_to_find: list ):
        output_file_path = SAFETY_BRIDGE_BUFF_PATH
        self.log_filter(path_to_save, output_file_path, texts_to_find)
        return output_file_path

    def generate_log_output(self):
        print(self.robotlist)
        for robot in self.robotlist:
            path_to_save_tool = f"/home/vb/logo_{robot.id}.txt"
            path_to_save_vbmanager = f"/home/vb/logo_{robot.id}.txt"

            #  ADDED IN TESTING, REMOVE IN PRODUCTION!!!
            if robot.id == "robotone":
                log_path_vbmanager = f"/home/vbmichal2/log/latest/robot.log"
            elif robot.id == "robottwo":
                log_path_vbmanager = f"/home/dev/log/latest/robot.log"
            elif robot.id == "robotthree":
                log_path_vbmanager = f"/home/vb/log/latest/robot.log"
            else:
                pass
            robot.capture_container_log_data(path_to_save_vbmanager, log_path_vbmanager)

#        robot_id = "robotwo"
#        path_to_save_vbmanager = f"/home/vb/log_{robot_id}.txt"
            vb_manager_filtered_log_path = self.filter_vbmanagerlog(path_to_save_vbmanager, VB_MANAGER_TEXT_TO_FIND)
#            safety_bridge_filtered_log_path = self.filter_safetybridge(path_to_save_tool)
            print(vb_manager_filtered_log_path)
            print("DF")
            single_robot_AP_data = Comparer(vb_manager_filtered_log_path, robot.id)
            print("CF")
        
            if self.All_AP_data is None:
                self.All_AP_data = single_robot_AP_data.create_final_robot_ap_dataframe()
                print(type(self.All_AP_data))
#                print(self.All_AP_data)
            else:
                self.All_AP_data = pd.concat([self.All_AP_data, single_robot_AP_data.create_final_robot_ap_dataframe()], axis=0)
                print(type(self.All_AP_data))
        return self.All_AP_data
            
if __name__ == "__main__":
    obj = LogGenerator(None)
    final_dataframe = obj.generate_log_output()
    final_dataframe.to_csv('APFinalYYY.txt', sep='\t', index=False)