import os

from file_utils import validate_filepath

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        success, warning_message, target_path = validate_filepath(working_directory, file_path)

        if (not success or not target_path):
            return warning_message if warning_message else "Error: Unknown error"

        if (os.path.isdir(target_path)):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        dir_path = target_path.split("/")[:-1]
        dir_path = "/".join(dir_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(target_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except OSError as e:
        return f"Error: Something has gone horribly wrong: {e}"

    except Exception as e:
        return f"Error: Caught unhandled exception: {e}"
