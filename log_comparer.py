# Comparer class is used to create an object, which process filetered_log_dataframe got from interaction with 
# object of type LogGenerator. Goal of Comparer class is to create AP_dataframe, which contains information
# about all actions related with docking&undocking related to AP found in filetered_log_dataframe. Each row of an dataframe has 1 row and 8 columns.
# AP_dataframe is created from ACTION_PONT_DATAFRAME dictionary. Words contained betwen brackets (), are search for, in each line of filtered_log_dataframe created by LogGenerator object. If found, 
# value for specific row and column, is incremented by 1.


###### CHANGE IF ######:
# - words between brackets which define lines of dataframe related with docking&undocking action change for
# ACTION_ERROR or DOCK_TRY or DOCK_CORRECT or UNDOCK_INCORRECT
# for instance, change from: ACTION_ERROR(waiting, aborted)  ---->  ACTION_ERROR(waiting, aborted)
ACTION_PONT_DATAFRAME = {
    'Robot': ["LOCKED"],
    'TIME_START': ["Initial"],
    'TIME_END': ["Initial"],
    'AP_NAME': ["None"],
    'ACTION_ERROR(waiting, aborted)': [0],
    'DOCK_TRY(Position incorrect)': [0],
    'DOCK_CORRECT(Position correct)': [0],
    'UNDOCK_INCORRECT(Departing failed)': [0]
}
###### FORIBIDDEN ######
# Changing any other parameter in ACTION_PONT_DATAFRAME


# In order to acces class funcionality, call create_final_robot_ap_dataframe function on its object.

# Order of tasks done by function:
# 1. Create initial ACTION_POINT_DATAFRAME
# 2. Then in loop, search for data defining Action point actions in each filtered log file. 
# if found, create action_point_dataframe and complete it by looking for words contained betwen brackets ()
# After creating single ap_dataframe, serach for another action point untill data for ALL ap will be extraced
# from filtered log.



import pandas as pd
import re


TESTING_PATH_VBMANAGERLOGS = "/home/vb/Downloads/AP_CREATION_TEST.txt"
class Comparer:
    def __init__(self, vb_manager_filtered_log_path: str, robot_id):
        try:
            with open(vb_manager_filtered_log_path, 'r') as file:
                self.vbmanager_logs = file.read()
            if not self.vbmanager_logs:
                raise ValueError("File is empty")
        except FileNotFoundError:
            print(f"File not found: {vb_manager_filtered_log_path}")
            self.vbmanager_logs = ""
        
        self.robot_dataframe = None
        self.action_point_raw_dataframe = None
        self.action_point_dataframe = None
        self.final_robot_dataframe = None
        self.robot_id = robot_id
        self.AP_completed = 0

    def create_initial_robot_dataframe(self): 
        """
        Create a dataframe from the VB Manager log.
        """        
        data = []

        try:
            for line in self.vbmanager_logs.split("\n"):
                if line.strip() != "":
                    try:
                        timestamp = line.split(" - ")[0].strip("'")
                        rest = " - ".join(line.split(" - ")[1:]).strip("'")
                        data.append([timestamp, rest])
                    except IndexError:
                        print("Error while splitting line: ", line)
                        continue

            init_df = pd.DataFrame(data, columns=["Time", "rest"])
            init_df['Time'] = pd.to_datetime(init_df['Time'], format='%Y-%m-%d %H:%M:%S,%f')
            init_df['Time'] = init_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            print("Initial DataFrame:")
            print(init_df)
            #!! WRITING TO CSV ONLY FOR TESTING !!#
            init_df.to_csv('output_file.txt', index=False, sep='\t')
            self.robot_dataframe = init_df

        except Exception as e:
            print(f"Error in create_initial_robot_dataframe: {e}")
    
    def look_for_first_ap(self):
        try:
            """
            Until AP exists, return time frames, cuts and saves them.
            """ 
            self.search_for_AP = False   
            found_started = False
            found_end = False
            filtered_rows = []
            self.AP_completed = 0

            # Iterate through each row to search for "start" in the "rest" column and stop if "Santa" is found
            for index, row in self.robot_dataframe.iterrows():
                if found_started:
                    filtered_rows.append(row)
                    if "Action completed" in row['rest']:
                        found_end = True
                        break
                    elif "ActionPoint(id:" in row['rest']:
                        self.AP_completed += 1
                        break
                elif "ActionPoint(id:" in row['rest']:
                    filtered_rows.append(row)
                    self.AP_completed = 1
                    found_started = True  # Set flag to start saving rows
            if found_started == True and found_end == True and self.AP_completed == 1:
                self.search_for_AP = True
            else:
                self.search_for_AP = False
                filtered_rows = []
            # Create a new DataFrame with filtered rows
            return filtered_rows
        
        except Exception as e:
            print(f"Error in get_raw_ap_df_from_initial_robot_dataframe: {e}")
            return None
        
    def get_raw_ap_df_from_initial_robot_dataframe(self, filtered_rows):
        try:
            if filtered_rows:
                ap_raw_df = pd.DataFrame(filtered_rows)
                print("Dataframe: AP data found in dataframe:")
            else:
                self.stop = True
                raise Exception("String 'ActionPoint(id:' was not found in any row before 'Action completed' in the 'rest' column.")

            # Assuming self.robot_dataframe and ap_raw_df are your DataFrames
            print("Dataframe: Data Left to processing:")
            print(self.robot_dataframe)
            # Get indexes that are common to both DataFrames
            common_indexes = self.robot_dataframe.index.intersection(ap_raw_df.index)

            # Drop rows from self.robot_dataframe that have the same index as rows in ap_raw_df
            self.robot_dataframe.drop(index=common_indexes, inplace=True)
            # Drop rows from self.robot_dataframe that match rows in ap_raw_df
            print("Dataframe: Data after processing")
            print(self.robot_dataframe)
            self.action_point_raw_dataframe = ap_raw_df

        except Exception as e:
            print(f"Error in get_raw_ap_df_from_initial_robot_dataframe: {e}")

    def algorithm_for_setting_ap_dataframe_actions(self):
        try:
            for index, row in self.action_point_raw_dataframe.iterrows():
                rest_value = row['rest']
                for col in self.action_point_dataframe.columns[3:]:  # Starting from the 4th column onwards
                    # Extracting values between parentheses using split and strip
                    values_inside_parentheses = col.split('(')[-1].split(')')[0].strip()

                    # Creating a list by splitting the extracted values using comma as a delimiter
                    result_list = [value.strip() for value in values_inside_parentheses.split(',')]
                    if any(string in rest_value for string in result_list):
                        self.action_point_dataframe.at[0, col] = self.action_point_dataframe.at[0, col] + 1
        except Exception as e:
            print(f"Error in algorithm_for_setting_ap_dataframe_actions: {e}")

    def extract_text_within_quotes(self, text):
        """
        Extract text within quotes from a string.
        """
        try:
            matches = re.findall(r"'(.*?)'", text)
            return matches[0] if matches else ''
        except Exception as e:
            print(f"Error in extract_text_within_quotes: {e}")
            return ''

    def extract_text_within_parentheses_and_quotes(self, text):
        """
        Extract text within parentheses and then within quotes from a string.
        """
        try:
            matches = re.findall(r'\((.*?)\)', text)
            if matches:
                text_within_parentheses = matches[0]
                return self.extract_text_within_quotes(text_within_parentheses)
            else:
                return ''
        except Exception as e:
            print(f"Error in extract_text_within_parentheses_and_quotes: {e}")
            return ''
                
    def algorithm_for_setting_ap_name(self):
        try:
            """
            Iterate through the DataFrame and set the AP_NAME column based on the 'rest' column.
            """
            for index, row in self.action_point_raw_dataframe.iterrows():
#                print(self.action_point_raw_dataframe)
                if "started." in row['rest']:
                    rest_value = row['rest']
                    extracted_text = self.extract_text_within_parentheses_and_quotes(rest_value)
                    self.action_point_dataframe.at[0, "AP_NAME"] = extracted_text
        except Exception as e:
            print(f"Error in algorithm_for_setting_ap_name: {e}")

    def algorithm_for_setting_time(self):
        try:
            start_date = "initial"
            end_date = "initial"

            # Iterate through each row in the DataFrame
            for index, row in self.action_point_raw_dataframe.iterrows():
                if "started" in row['rest']:
                    start_date = row['Time']
                elif "Action completed" in row['rest']:
                    end_date = row['Time']

            # Set the start and end times in the ap_df DataFrame
            self.action_point_dataframe.at[0, 'TIME_START'] = start_date
            self.action_point_dataframe.at[0, 'TIME_END'] = end_date
        except Exception as e:
            print(f"Error in algorithm_for_setting_time: {e}")

    def create_single_ap_dataframe_template(self): 
        try:
            self.action_point_dataframe = pd.DataFrame(ACTION_PONT_DATAFRAME)
            self.action_point_dataframe['Robot'] = self.robot_id
        except Exception as e:
            print(f"Error creating single AP dataframe template: {e}")


    def create_final_single_action_point_dataframe(self, filtered_rows):   
        try:
            self.get_raw_ap_df_from_initial_robot_dataframe(filtered_rows)
            self.create_single_ap_dataframe_template()
            self.algorithm_for_setting_ap_dataframe_actions()
            self.algorithm_for_setting_ap_name()
            self.algorithm_for_setting_time()
            self.action_point_dataframe.to_csv('APFinal.txt', sep='\t', index=False)
            return self.action_point_dataframe
        except Exception as e:
            print(f"Error creating final action point dataframe: {e}")

    def create_final_robot_ap_dataframe(self):
        try:
            self.create_initial_robot_dataframe()
            while True:
                filtered_rows = self.look_for_first_ap()
                if len(filtered_rows) < 1 or self.search_for_AP == False:
                    if self.robot_dataframe.empty and not filtered_rows:
                        print(f"""
                        No more AP found or malformed input data.
                        Is robot dataframe empty: {self.robot_dataframe.empty}
                        List of ap rows: {filtered_rows}
                        !!!ALL AP HAVE BEEN FOUND!!!.
                        """)
#                        print(self.AP_completed)
                    elif not self.robot_dataframe.empty and not filtered_rows:
                        print(f"""
                        No more AP found or malformed input data.
                        Is robot dataframe empty: {self.robot_dataframe.empty}
                        List of ap rows: {filtered_rows}
                        !!!CANNOT FIND AP - robot_dataframe DATA MALFORMED!!!.
                        """)
                    break
                else:
                    single_ap_df = self.create_final_single_action_point_dataframe(filtered_rows)
                    if self.final_robot_dataframe is None:
                        self.final_robot_dataframe = single_ap_df
                        print(self.final_robot_dataframe)

                    else:
                        if set(self.final_robot_dataframe.columns) == set(single_ap_df.columns):
                            self.final_robot_dataframe = pd.concat([self.final_robot_dataframe, single_ap_df], axis=0)
                            print("Dataframe: AP data extracted from dataframe:")
                            print(self.final_robot_dataframe)
                        else:
                            raise Exception("Column structures are not identical. Cannot append.")
            return self.final_robot_dataframe
                            
        except Exception as e:
            print(f"create_final_robot_ap_dataframe {e}")


if __name__ == "__main__":
    obj = Comparer(TESTING_PATH_VBMANAGERLOGS,"ROBOT ONE")
    final_dataframe = obj.create_final_robot_ap_dataframe()
    final_dataframe.to_csv('APFinal.txt', sep='\t', index=False)