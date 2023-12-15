import pandas as pd

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
