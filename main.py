import os
import argparse
import json
import sys

from dotenv import load_dotenv
from openai import OpenAI
from collections.abc import Iterable
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionToolUnionParam
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCallUnion
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

API_KEY_ENV_LOCATION = "OPENROUTER_API_KEY"

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():

    load_dotenv()
    API_KEY = os.environ.get(API_KEY_ENV_LOCATION)

    if (not API_KEY):
        raise RuntimeError(f"API key was not found at {API_KEY_ENV_LOCATION}")

    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )

    for i in range(20):
        response = generate_response(client, messages)
        messages, complete = handle_response(messages, response)

        if (complete):
            break;
        elif (i >= 19):
            sys.exit(1)
            break;


def handle_response(messages: Iterable[ChatCompletionMessageParam], response: ChatCompletion) -> tuple[Iterable[ChatCompletionMessageParam], bool]:
    message = response.choices[0].message
    msg = messages.copy()
    if (not response.usage):
        raise RuntimeError(f"{response.model} failed to respond to API call")

    if (not message):
        raise RuntimeError(f"{response.model} failed to produce a message")

    print_header(response)

    msg.append(message)
    complete = not message.tool_calls

    if (complete):
        print(message.content)
    else:
        msg = run_tool_calls(msg, message.tool_calls)

    print("\n=========================================================\n")

    return (msg, complete)

def run_tool_calls(messages: Iterable[ChatCompletionMessageParam], tool_calls) -> Iterable[ChatCompletionMessageParam]:
    msg = messages.copy()

    for tool in tool_calls:
        function_args = json.loads(tool.function.arguments or "{}")
        print(f"Calling function: {tool.function.name}({function_args})")

        result_message = call_function(tool)
        msg.append(result_message)

        if (args.verbose):
            content = result_message.get("content", None)
            if (not content):
                raise RuntimeError("Tool call returned with no content.")
            print(f"-> {result_message['content']}")

    return msg

def print_header(response: ChatCompletion) -> None:
    if (args.verbose):
        print("\n==================== bootdev chatbot ====================\n")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print("\n======================= response ========================\n")

def generate_response(client: OpenAI, messages: "Iterable[ChatCompletionMessageParam]") -> "ChatCompletion":
    return client.chat.completions.create(
        model= "openrouter/free",
        messages= messages,
        tools= available_functions
    )


if __name__ == "__main__":
    main()
