import os

from dataclasses import dataclass


@dataclass
class FileData:
    name: str
    size: int
    is_dir: bool

def collect_file_data(path: str) -> "FileData":
    name = path.split("/")[-1]
    size = os.path.getsize(path)
    is_dir = os.path.isdir(path)
    return FileData(name= name, size= size, is_dir= is_dir)

def validate_filepath(working_directory: str, directory: str) -> tuple[bool, str | None, str | None]:
    target_dir, working_directory_path = create_directory_paths(working_directory, directory)

    allowed = is_filepath_allowed(working_directory_path, target_dir)
    if (not allowed):
        return (allowed, f'Error: Cannot list "{directory}" as it is outside the permitted working directory', None)

    return (True, f'Success: "{directory}" is within the working directory', target_dir)

def validate_directory(working_directory: str, directory: str) -> tuple[bool, str | None, str | None]:
    success, warning_message, target_dir = validate_filepath(working_directory, directory)

    if (target_dir):
        if (not os.path.isdir(target_dir)):
            return (False, f'Error: "{target_dir}" is not a directory', None)

    return (success, warning_message, target_dir)

def create_directory_paths(working_directory: str, directory: str) -> tuple[str, str]:
    working_directory_path = os.path.abspath(working_directory)
    return os.path.normpath(os.path.join(working_directory_path, directory)), working_directory_path

def is_filepath_allowed(working_directory_path: str, target_directory_path: str) -> bool:
    return os.path.commonpath([target_directory_path, working_directory_path]) == working_directory_path
