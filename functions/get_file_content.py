import os

from file_utils import validate_filepath
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a file at the specified file path and returns it as a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path" : {
                    "type": "string",
                    "description": "File path to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

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
