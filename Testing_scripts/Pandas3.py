import pandas as pd
from io import StringIO

# Your log data
log_data = """
'2023-04-04 06:32:12,795 - tool - INFO - Tool 'bsst' initialized.'
'2023-04-04 06:32:17,719 - tool.plc - INFO - sending initial data to tool signalization'
'2023-04-04 06:32:17,719 - tool.plc - INFO - Sending state type LightType.SLOW_BLINK color LightColor.RED'
'2023-04-04 06:32:17,720 - tool.plc - ERROR - Could not establish connection with modbus server while trying to send data.'
'2023-04-04 06:32:17,756 - tool.modbus - INFO - Connected.'
'2023-04-04 06:32:17,756 - tool.rfid - INFO - Connecting with receiver...'
'2023-04-04 06:32:17,758 - tool.rfid - INFO - Connected.'
'2023-04-04 06:32:17,842 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:17,952 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,064 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,175 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,290 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,405 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,549 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
'2023-04-04 06:32:18,666 - tool.plc - ERROR - Response received from https://vbdocker:10443/api/v1/robot/state is marked as not ok'
"""

# Load the log data into a DataFrame
data = []
for line in log_data.split("\n"):
    if line.strip() != "":
        timestamp = line.split(" - ")[0].strip("'")
        rest = " - ".join(line.split(" - ")[1:]).strip("'")
        data.append([timestamp, rest])

df = pd.DataFrame(data, columns=["Time", "rest"])
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S,%f')

# Display the DataFrame
print(df)
