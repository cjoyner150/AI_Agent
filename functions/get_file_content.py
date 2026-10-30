import os

from file_utils import validate_filepath
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        success, warning_message, target_dir = validate_filepath(working_directory, file_path)

        if (not target_dir or not success):
            return warning_message if (warning_message) else "Error: Unknown error."

        if (not os.path.isfile(target_dir)):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file = open(target_dir)
        content = file.read(MAX_CHARS)

        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: Caught unhandled exception: {e}'
