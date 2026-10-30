import json

from collections.abc import Callable
from typing import cast, Iterable
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCallUnion
from openai.types.chat.chat_completion_message_function_tool_call import ChatCompletionMessageFunctionToolCall
from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info
from functions.run_python_file import schema_run_python_file
from functions.run_python_file import run_python_file
from functions.write_file import schema_write_file
from functions.write_file import write_file

available_functions: Iterable[ChatCompletionToolParam] = cast(Iterable[ChatCompletionToolParam], [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
])

func_lookup: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(tool_call: ChatCompletionMessageToolCallUnion, verbose: bool = False) -> dict:
    try:
        if (not isinstance(tool_call, ChatCompletionMessageFunctionToolCall)):
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: attemted custom tool call not allowed. Only use function tool calls.",
            }

        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments or "{}")

        if (verbose):
            print(f" - Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")

        function = func_lookup.get(function_name, None)
        if (not function):
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown function: {function_name}",
            }

        function_args["working_directory"] = "./calculator"
        result = function(**function_args)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }

    except Exception as e:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Caught unhandled exception: {e}",
        }
