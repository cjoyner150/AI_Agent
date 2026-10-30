import os
import subprocess

from file_utils import validate_filepath

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file at the specified file path with the specified arguments using a subprocess and returns the result of the subprocess as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path" : {
                    "type": "string",
                    "description": "File path of the python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        success, message, target_path = validate_filepath(working_directory, file_path)

        if (not success or not target_path):
            return message if message else "Error: Unknown error"

        if (not os.path.isfile(target_path)):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if (not target_path.endswith(".py")):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if(args):
            command.extend(args)

        completed = subprocess.run(command, text= True, capture_output=True, timeout= 30 )
        output: str = ""

        if (completed.returncode != 0):
            output += "Process exited with code X\n"

        if (not completed.stderr and not completed.stdout):
            output += "No output produced\n"
            return output

        if (completed.stdout):
            output += "STDOUT: " + completed.stdout + "\n"

        if (completed.stderr):
            output += "STDERR: " + completed.stderr + "\n"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
