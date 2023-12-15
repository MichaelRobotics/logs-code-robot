import pandas as pd

# Creating example DataFrames
raw_data_df = pd.DataFrame({
    'ID': [1],
    'AP_NAME': ['RobotA']
})

interpreted_ap_df = pd.DataFrame({
    'ID': [101, 102, 103],
    'AP_NAME2': ['RobotX', 'RobotY', 'RobotA']
})

def look_for_matching_robot_name(raw_data_df, interpreted_ap_df):
    # Assuming raw_data_df is your DataFrame
    unique_names = raw_data_df['AP_NAME'].unique()

    if len(unique_names) == 1:
        extracted_value = unique_names[0]
        print("Extracted value from column 'AP_NAME':", extracted_value)
    else:
        raise ValueError("There is more than one unique value in the 'AP_NAME' column.")

    for index, row in interpreted_ap_df.iterrows():
        if row['AP_NAME2'] in unique_names:
            index_number = index   

    return index_number

matching_robot_names = look_for_matching_robot_name(raw_data_df, interpreted_ap_df)
print(matching_robot_names)
