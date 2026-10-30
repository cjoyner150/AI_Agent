import os

from file_utils import validate_directory
from file_utils import collect_file_data


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        success, warning_message, target_dir = validate_directory(working_directory, directory)

        if (not success):
            return warning_message if warning_message else 'Error: Unknown error'

        if (not target_dir):
            return "Error: no target directory found"

        file_paths = os.listdir(target_dir)
        file_paths = list(map(lambda path: target_dir + "/" + path, file_paths))

        data = [collect_file_data(path)for path in file_paths]

        return f"Success: results from '{directory}':\n" + "\n".join(f"- {file.name}: file_size={file.size}, is_dir={file.is_dir}" for file in data)

    except Exception as e:
        return f'Error: Caught unhandled exception: {e}'
