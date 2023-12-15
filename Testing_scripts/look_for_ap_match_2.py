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
    unique_names = raw_data_df['AP_NAME'].unique()
    matching_rows = []
    matching_row_indices = []

    for name in unique_names:
        # Check if the name exists in AP_NAME2 column
        if name in interpreted_ap_df['AP_NAME2'].values:
            # Get the index of the name in AP_NAME2 column
            index_of_name = interpreted_ap_df['AP_NAME2'][interpreted_ap_df['AP_NAME2'] == name].index[0]
            matching_row_indices.append(index_of_name)

            # Get the row based on the index and convert it to a list
            matching_rows.append(list(interpreted_ap_df.iloc[index_of_name]))

    return matching_rows, matching_row_indices

matching_robot_rows, matching_row_indices = look_for_matching_robot_name(raw_data_df, interpreted_ap_df)
print("Matching Rows:")
print(matching_robot_rows)
print("\nIndices of Names in interpreted_ap_df['AP_NAME2']:")
print(matching_row_indices)

# Storing row indices in a separate variable
new_variable = matching_row_indices
print("\nNew Variable (Row Indices):")
print(new_variable)
