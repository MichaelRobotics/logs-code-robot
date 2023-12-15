import pandas as pd

# Sample DataFrames JUST AN SAMPLE !!!
data1 = {
    'rest': ['Sometext waiting', 'sometext start', 'Position incorrect', 'Position correct'],
    'Value': [10, 20, 30, 40]
}
data2 = {
        'Robot': [0],
        'TIME_START(started)': ["Initial"],
        'TIME_END(Action completed)': ["Initial"],
        'AP_NAME(started)': ["None"],
        'ACTION_ERROR(waiting, aborted)': [0],
        'DOCK_TRY(Position incorrect)': [0],
        'DOCK_CORRECT(Position correct)': [0],
        'UNDOCK_INCORRECT(Departure failed)': [0]
}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
print(df1)
# Iterate through 'rest' column in df1 and update df2 from the 4th column onwards
for row in df1.iterrows():
    rest_value = row['rest']
    for col in df2.columns[3:]:  # Starting from the 4th column onwards
        # Extracting values between parentheses using split and strip
        values_inside_parentheses = col.split('(')[-1].split(')')[0].strip()

        # Creating a list by splitting the extracted values using comma as a delimiter
        result_list = [value.strip() for value in values_inside_parentheses.split(',')]
        text_line = df1.at[row,"rest"]
        if any(string in rest_value for string in result_list):
            df2[1, col] = df2[1, col] + 1