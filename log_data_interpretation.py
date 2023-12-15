import pandas as pd
import re
from log_generator import LogGenerator

class BaseDataInterpreter:
    def __init__(self, raw_ap_dataframe: LogGenerator):
        self.raw_ap_dataframe = raw_ap_dataframe

    def filter_for_extracting_column_name(self, column):
        column_content = []
        column_name = ""

        # Using regex to match column name and content within brackets
        match = re.match(r'(\w+)\(([^)]*)\)', column)

        if match:
            column_name = match.group(1)  # Extracting column name
            content = match.group(2)  # Extracting content within brackets

            # Split the content by commas to create a list
            column_content = [item.strip() for item in content.split(',')]

        return column_content, column_name
    
    def create_init_data_df(self):
        interpreted_ap_df = pd.DataFrame({
            'AP_NAME()': ["initial"],
            'SUCC_RATE()': [0],
            'SUCCES()': [0],
            'FAILURE()': [0],
            'ACTION_ERROR(DOCK_TRY, UNDOCK_INCORRECT, ACTION_ERROR)': [0],
            'DOCK_ERROR(DOCK_TRY, UNDOCK_INCORRECT)': [0]
        })
        return interpreted_ap_df

    def check_for_positive_task(self):
        pass
    def check_for_negative_task(self):
        pass
    def check_for_failed_dock(self):
        pass
    def check_for_failed_action(self):
        pass
    def check_for_succes_rate(self):
        pass
    def create_final_ap_data(self):
        pass

class AllRobotDataInterpreter(BaseDataInterpreter):
    def __init__(self):
        super().__init__() 

    def look_for_matching_robot_name(self, raw_data_df, interpreted_ap_df):
        unique_name = raw_data_df['AP_NAME'].unique()
        name_found = False
        if len(unique_name) == 1:
            extracted_value = unique_name[0]
            print("Extracted value from column 'AP_NAME':", extracted_value)
        else:
            raise ValueError("There is more than one unique value in the 'AP_NAME' column.")
        
        if interpreted_ap_df['AP_NAME()'].iloc[0] == "initial":
            index_number = 0
            interpreted_ap_df['AP_NAME()'].iloc[0] = unique_name
        else:
            for index, row in interpreted_ap_df.iterrows():
                if row['AP_NAME()'] in unique_name:
                    index_number = index
                    name_found = True
            if name_found == False:
                # Create a new row to add to the DataFrame
                new_row = {'AP_NAME()': unique_name, 'SUCC_RATE()': 0, "SUCCES()": 0,
                           'FAILURE()': 0, 'ACTION_ERROR(DOCK_TRY, UNDOCK_INCORRECT, ACTION_ERROR)': 0,
                           'DOCK_ERROR(DOCK_TRY, UNDOCK_INCORRECT)': 0 }  # Define your columns and values
                # Append the new row to interpreted_ap_df
                interpreted_ap_df = interpreted_ap_df.append(new_row, ignore_index=True)   
                index_number = index + 1
            
        return index_number

    def single_robot_dataframe_fill(self, raw_data_df: pd.DataFrame, current_interpreted_robot_row: int, interpreted_ap_df: pd.DataFrame):
        row_data = interpreted_ap_df.iloc[current_interpreted_robot_row]
        for column, value in reversed(row_data.items()):
            column_search_list, name = super().filter_for_extracting_column_name(column)
            if name == "DOCK_ERROR":
                super().check_for_failed_dock(column_search_list, name, value)
            elif name == "ACTION_ERROR":
                super().check_for_failed_action(column_search_list, name, value)
            elif name == "SUCCESS":
                super().check_for_positive_task(column_search_list, name, value)
            elif name == "FAILURE":
                super().check_for_negative_task(column_search_list, name, value)
            elif name == "SUCC_RATE":
                super().check_for_succes_rate(column_search_list, name, value)
            elif name == "AP_NAME":
                print("AP data updated")
            else:
                print("Error in name of column")

    def generate_all_robot_dataframe(self):
        interpreted_ap_df = super().create_init_data_df()
        raw_data_list = []  # List to store row data as dictionaries
        for index, row in self.raw_ap_dataframe.iterrows():
            ap = {}  # Dictionary to store column names and values for the current row
            for column, value in row.items():
                ap[column] = value  # Store column name and its corresponding value in ap  # Append the dictionary for the current row to the list
            raw_data_list.append(ap)
        raw_data_df = pd.DataFrame(raw_data_list)
        current_interpreted_robot_row = self.look_for_matching_robot_name(raw_data_df, interpreted_ap_df)
        self.single_robot_dataframe_fill(raw_data_df, current_interpreted_robot_row, interpreted_ap_df)







################# for later tests ############################
#
#class AllApDataInterpreter(BaseDataInterpreter):
#    def __init__(self):
#        super().__init__()
#    
#    def look_for_matching_ap_name(self):
#        pass
#
#    def generate_all_ap_dataframe():
#        init_df = super().create_init_data_df
#
################# TO DO ############################
#
#
# 1. Create initial dataframe of an robot / Ap for Final Dataframe
# 2. Find to which Ap connect this data
# 3. Create an algorith for finding which datafame of ap ctually i should fill in filling
#
#
#
#