import pandas as pd

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}

df = pd.DataFrame(data)

# Function to check if column names exist in a text line and update values
def update_values(df, text_line):
    for column_name in df.columns:
        if column_name in text_line:
            # Find the index of the first occurrence of the column name in the text line
            idx = text_line.index(column_name)
            # Set the value of the first row under the column name to the column name itself
            df.at[0, column_name] = column_name
    
    return df

# Sample text line
text_line_to_check = "This text line contains the column Name and City."

# Update values in DataFrame based on column names found in the text line
df_updated = update_values(df.copy(), text_line_to_check)
print(df_updated)