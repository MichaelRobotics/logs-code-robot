import pandas as pd
import re
from log_generator import LogGenerator

class BaseDataInterpreter:
    def __init__(self, raw_ap_dataframe: LogGenerator):
        self.raw_ap_dataframe = raw_ap_dataframe

    def filter_for_extracting_column_name(self, column):
        column_content = []
        column_name = ""

        try:
            match = re.match(r'(\w+)\(([^)]*)\)', column)
            if not match:
                raise ValueError("Invalid format for column. Expected format: 'column_name(content)'")

            column_name = match.group(1)  # Extracting column name
            content = match.group(2)  # Extracting content within brackets

            # Split the content by commas to create a list
            column_content = [item.strip() for item in content.split(',')]
        except re.error as e:
            raise ValueError(f"Regex error: {e}")
        except Exception as ex:
            raise ValueError(f"An error occurred: {ex}")

        return column_content, column_name
    
    def create_init_data_df(self):
        initial_data = {
            'AP_NAME()': ["initial"],
            'SUCC_RATE()': [0],
            'SUCCESS()': [0],
            'FAILURE()': [0],
            'ACTION_ERROR(DOCK_TRY, UNDOCK_INCORRECT, ACTION_ERROR)': [0],
            'DOCK_ERROR(DOCK_TRY, UNDOCK_INCORRECT)': [0]
        }

        for column, values in initial_data.items():
            if not isinstance(values, list):
                raise ValueError(f"The data for column '{column}' should be a list.")
        
        interpreted_ap_df = pd.DataFrame(initial_data)
        return interpreted_ap_df
    
    def check_for_positive_task(self, value, fail):
        if not isinstance(fail, bool):
            raise ValueError("The 'fail' argument must be a boolean value.")
        
        if fail:
            print(f"succ {value}")
            return value  # No increment if fail is True
        else:
            print(f"succ {value + 1}")
            return value + 1

    def check_for_negative_task(self, value, fail):
        if not isinstance(fail, bool):
            raise ValueError("The 'fail' argument must be a boolean value.")
        
        if not fail:
            print(f"fail {value}")
            return value  # No increment if fail is False
        else:
            print(f"fail {value + 1}")
            return value + 1

    def check_for_succes_rate(self, succ: int, fail: int):
        if succ < 0 or fail < 0 or (succ + fail) == 0:
            raise ValueError("Success and failure counts should be non-negative integers.")
        
        try:
            print(f"{succ} XD")
            print(f"{fail} XD")
            succ_rate = round(succ / (succ + fail), 2) * 100
            return succ_rate
        except ZeroDivisionError:
            # Handle the case where the denominator is zero (avoid division by zero)
            return 0  # You can customize this based on your application logic
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Handle other unexpected errors that might occur

    def check_for_failed_dock(self, column_search_list, value, raw_data_df):
        try:
            fail = False
            new_value = 0        
            DOCK_TRY_MAX_NUMBER = 3
            UNDOCK_INCORRECT_MAX_NUMBER = 0
            for col in raw_data_df.columns:
                # Remove the string within brackets including brackets
                cleaned_col_name = re.sub(r'\(.*\)', '', col).strip()

                # Check if the cleaned column name is in column_search_list
                if cleaned_col_name in column_search_list:
                    if cleaned_col_name == "DOCK_TRY":
                        print(raw_data_df.loc[0, col])
                        if raw_data_df.loc[0, col] >= DOCK_TRY_MAX_NUMBER:
                            new_value = 1
                            fail = True
                    if cleaned_col_name == "UNDOCK_INCORRECT":
                        print(raw_data_df.loc[0, col])
                        if raw_data_df.loc[0, col] > UNDOCK_INCORRECT_MAX_NUMBER:
                            new_value = 1
                            fail = True
                value = value + new_value
            return value, fail
        except Exception as e:
            print(f"Error check_for_failed_dock: {e}")

    def check_for_failed_action(self, column_search_list, value, raw_data_df):
        try:
            fail =  False
            new_value = 0
            for col in raw_data_df.columns:
                # Remove the string within brackets including brackets
                cleaned_col_name = re.sub(r'\(.*\)', '', col).strip()

                # Check if the cleaned column name is in column_search_list
                if cleaned_col_name in column_search_list:
                    if cleaned_col_name == "ACTION_ERROR":
                        if raw_data_df.loc[0, col] > 0:
                            new_value = 1
                            fail = True

                value = value + new_value
            return value, fail
        except Exception as e:
            print(f"Error check_for_failed_action: {e}")

class AllApDataInterpreter(BaseDataInterpreter):
    def __init__(self, raw_dataframe: LogGenerator):
        super().__init__(raw_dataframe) 

    def look_for_matching_robot_name(self, raw_data_df, interpreted_ap_df):
        try:
            print("TESTMAN")
            if 'AP_NAME' not in raw_data_df.columns:
                raise KeyError("Column 'AP_NAME' not found in raw data.")
            print(raw_data_df)
            unique_name = raw_data_df['AP_NAME'].unique()
            print("Unique values in column 'AP_NAME':", unique_name)
            name_found = False
            if len(unique_name) == 1:
                extracted_value = unique_name[0]
                print("Extracted value from column 'AP_NAME':", extracted_value)
            else:
                raise ValueError("There is more than one unique value in the 'AP_NAME' column.")

            if interpreted_ap_df.loc[0, 'AP_NAME()'] == "initial":
                index_number = 0
                interpreted_ap_df.loc[0, 'AP_NAME()'] = unique_name
            else:
                for index, row in interpreted_ap_df.iterrows():
                    if row['AP_NAME()'] in unique_name:
                        index_number = index
                        name_found = True
                if name_found == False:
                    # Create a new row to add to the DataFrame
                    new_row = {'AP_NAME()': unique_name, 'SUCC_RATE()': 0, "SUCCESS()": 0,
                               'FAILURE()': 0, 'ACTION_ERROR(DOCK_TRY, UNDOCK_INCORRECT, ACTION_ERROR)': 0,
                               'DOCK_ERROR(DOCK_TRY, UNDOCK_INCORRECT)': 0 }  # Define your columns and values
                    new_row_df = pd.DataFrame(new_row, index=[0])
                    print(interpreted_ap_df)
                    print(index)
                    interpreted_ap_df = pd.concat([interpreted_ap_df, new_row_df], ignore_index=True)
                    print(interpreted_ap_df)
                    index_number = index + 1
                    print(index_number)
                    print("xdds")
            return index_number, interpreted_ap_df
        except Exception as e:
            print(f"Error generate_all_robot_dataframe: {e}")
    
    def update_dataframe(self, interpreted_ap_df: pd.DataFrame, current_interpreted_robot_row: int, column: str, new_value: int):
        interpreted_ap_df.loc[current_interpreted_robot_row, column] = new_value

    def single_robot_dataframe_fill(self, raw_data_df: pd.DataFrame, current_interpreted_robot_row: int, interpreted_ap_df: pd.DataFrame):
        new_value = int()
        succ = int()
        fail = int()
        succ_perc = int()
        print(current_interpreted_robot_row)
        print(interpreted_ap_df)
        row_data = interpreted_ap_df.iloc[current_interpreted_robot_row]
        try:
            # At FIRST check if there are any DOCK_ERROR or ACTION_ERROR
            for column, value in row_data.items():
                column_search_list, name = super().filter_for_extracting_column_name(column)
                if name == "DOCK_ERROR":
                    new_value, error = super().check_for_failed_dock(column_search_list, value, raw_data_df)
                    self.update_dataframe(interpreted_ap_df, current_interpreted_robot_row, column, new_value)
                elif name == "ACTION_ERROR":
                    new_value, error = super().check_for_failed_action(column_search_list, value, raw_data_df)
                    self.update_dataframe(interpreted_ap_df, current_interpreted_robot_row, column, new_value)

            # At SECOND check for SUCCES and FAILURE based on DOCK_ERROR and ACTION_ERROR        
            for column, value in row_data.items():
                column_search_list, name = super().filter_for_extracting_column_name(column)
                print(name)
                if name == "SUCCESS":
                    new_value = super().check_for_positive_task(value, error)
                    self.update_dataframe(interpreted_ap_df, current_interpreted_robot_row, column, new_value)
                    succ = new_value
                elif name == "FAILURE":
                    new_value = super().check_for_negative_task(value, error)
                    self.update_dataframe(interpreted_ap_df, current_interpreted_robot_row, column, new_value)
                    fail = new_value

            # At LAST check for SUCC_RATE
            for column, value in row_data.items():
                column_search_list, name = super().filter_for_extracting_column_name(column)
                if name == "SUCC_RATE":
                    new_value = super().check_for_succes_rate(succ, fail)
                    succ_perc = f'{new_value}'
                    interpreted_ap_df.loc[current_interpreted_robot_row, column] = succ_perc
                elif name == "AP_NAME":
                    print("AP data updated")
        except KeyError as e:
            print(f"Error occurred due to missing data or column at single_robot_dataframe_fill: {e}")
            # Handle this error case gracefully, log the issue, or take appropriate action
        except ValueError as e:
            print(f"Value error occurred at single_robot_dataframe_fill: {e}")
            # Handle this error case gracefully, log the issue, or take appropriate action
        except Exception as e:
            print(f"An unexpected error occurred at single_robot_dataframe_fill: {e}")
            # Handle other unexpected errors that might occur

    def generate_all_robot_dataframe(self):
        try:
            interpreted_ap_df = super().create_init_data_df()
            raw_data_list = []  # List to store row data as dictionaries
            for index, row in self.raw_ap_dataframe.iterrows():
                ap = {}  # Dictionary to store column names and values for the current row
                for column, value in row.items():
                    ap[column] = value  # Store column name and its corresponding value in ap  # Append the dictionary for the current row to the list
                raw_data_list.append(ap)
                raw_data_df = pd.DataFrame(raw_data_list)
                raw_data_list = []
                print("XD")
                current_interpreted_robot_row, interpreted_ap_df = self.look_for_matching_robot_name(raw_data_df, interpreted_ap_df)
                print("XD3")
                self.single_robot_dataframe_fill(raw_data_df, current_interpreted_robot_row, interpreted_ap_df)
                print("XD4")
            print(interpreted_ap_df)
        except Exception as e:
            print(f"Error generate_all_robot_dataframe: {e}")


#####################TESTS#####################################
if __name__ == "__main__":
    All_AP_dataframe_file = pd.read_csv('All_AP_dataframe_file.txt', sep='\t')
    obj = AllApDataInterpreter(All_AP_dataframe_file)
    obj.generate_all_robot_dataframe()



################# Class to manage RobotData ############################
#
#class AllRobotDataInterpreter(BaseDataInterpreter):
#    def __init__(self):
#        super().__init__()
#    
#    def look_for_matching_ap_name(self):
#        pass
#
#    def generate_all_ap_dataframe():
#        init_df = super().create_init_data_df
#
################# TO DO ######################################