import pandas as pd
import re

# Given text
text = """
2023-10-03 10:50:03,768 - vb_manager.mm - info - PFT.9f779.1 - ActionPoint(id: 'GTW01') started.
2023-10-03 11:00:17,057 - vb_manager.am - info - PFT.9f779.1 - Action completed.
2023-10-03 11:00:17,288 - vb_manager.mm - info - PFT.9f779.2 - ActionPoint(id: 'C0309') started.
"""

# Define a regex pattern to extract relevant information
pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\S+) - (\S+) - (\S+) - (.*)'

# Find all matches in the text
matches = re.findall(pattern, text)

# Create DataFrame from the matches
df = pd.DataFrame(matches, columns=['Timestamp', 'Module', 'LogLevel', 'Identifier', 'Message'])

# Convert 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S,%f')
# Drop 'Module' and 'LogLevel' columns
df.drop(['Module', 'LogLevel'], axis=1, inplace=True)
#df['Message'] = df['Message'].str.replace('ActionPoint', '').str.replace('started', '')
df['Message'] = df['Message'].apply(lambda x: re.findall(r"'(.*?)'", x)[0] if re.findall(r"'(.*?)'", x) else '')
df['Message'] = df['Message'].apply(lambda x: 'END' if not x.strip() else x)
df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').str.split('.').str[0]
# Convert 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Sort DataFrame by 'Timestamp' column in ascending order
df = df.sort_values(by='Timestamp')

print(df)
# Save DataFrame to a text file
with open('dataframe_content.txt', 'w') as file:
    file.write(df.to_string(index=False))

log_data = [
    '2023-10-03 08:54:10,090 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 08:54:10,586 - tool - INFO - Position correct.',
    '2023-10-03 09:19:29,701 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 09:19:30,184 - tool - INFO - Position correct.',
    '2023-10-03 09:30:31,762 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 09:30:32,161 - tool - INFO - Position correct.',
    '2023-10-03 09:41:19,910 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 09:41:20,392 - tool - INFO - Position correct.',
    '2023-10-03 09:58:32,571 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 09:58:32,998 - tool - INFO - Position correct.',
    '2023-10-03 10:01:59,857 - tool - INFO - Approach completed by sensor.',
    '2023-10-03 10:02:00,396 - tool - INFO - Position correct.'
]

# Splitting log-like strings to extract information
split_data = [log.split(' - ') for log in log_data]
timestamps = [log[0] for log in split_data]
tool_status = [log[2] for log in split_data]
messages = [log[3] for log in split_data]

# Create a DataFrame from extracted data
df2 = pd.DataFrame({
    'Timestamp': timestamps,
    'Tool_Status': tool_status,
    'Message': messages
})

# Convert 'Timestamp' column to datetime
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'], format='%Y-%m-%d %H:%M:%S,%f')

# Truncate everything after the first dot in 'Timestamp'
df2['Timestamp'] = df2['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Drop the 'Tool_Status' column
df2.drop('Tool_Status', axis=1, inplace=True) 

print(df2)

merged_df = pd.merge(df, df2, on='Timestamp', how='inner')
