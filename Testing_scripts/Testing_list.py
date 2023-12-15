FLEET_TEXT_TO_FIND = [["vb_manager.mm - info - PFT", "ActionPoint", "started"],
                      ["vb_manager.am - info - PFT", "Action completed."]]

ROBOT_TEXT_TO_FIND = [["Approach completed by sensor"], 
                      ["INFO - Position correct"],
                      ["Robot ready for cooperation"]]

R_INPUT_FILE_PATH = "/home/vb/Downloads/robot.log"
R_OUTPUT_FILE_PATH = "/home/vb/Downloads/testlogsfilteredRob.log"

F_INPUT_FILE_PATH = "/home/vb/Downloads/testlogs.log"
F_OUTPUT_FILE_PATH = "/home/vb/Downloads/testlogsfiltered.log"

def log_filter(input_file_path: str, output_file_path: str, text_to_find: list):
    # Texts to search for in the file
    # Open the input file, read lines containing the specified texts and save to output file
    try:
        with open(input_file_path, 'r') as input_file:
            with open(output_file_path, 'w') as output_file:
                for line in input_file:
                    for keywords in text_to_find:
                        if all(keyword in line for keyword in keywords):
                            output_file.write(line)
        return output_file
    except FileNotFoundError:
        print("File not found. Please provide valid file paths.")
        return None
    except FileExistsError:
        print("The output file already exists. Please provide a different output file path.")
        return None

def main():
    log_filter(F_INPUT_FILE_PATH, F_OUTPUT_FILE_PATH, FLEET_TEXT_TO_FIND)
    print("DONE")
    log_filter(R_INPUT_FILE_PATH, R_OUTPUT_FILE_PATH, ROBOT_TEXT_TO_FIND)
    print("DONE")

if __name__ == "__main__":
    main()