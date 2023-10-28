file_path = '/tmp/Bsst-logs-code/logs/file'

# Define the content you want to write to the file
file_content = "This is some text that will be written to the file."

# Create the file and write content
try:
    with open(file_path, 'w') as file:
        file.write(file_content)
    print(f"File '{file_path}' created and content written successfully.")
except Exception as e:
    print(f"Error: {e}")