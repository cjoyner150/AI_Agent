import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from collections.abc import Iterable
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion

API_KEY_ENV_LOCATION = "OPENROUTER_API_KEY"

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    API_KEY = os.environ.get(API_KEY_ENV_LOCATION)

    if (not API_KEY):
        raise RuntimeError(f"API key was not found at {API_KEY_ENV_LOCATION}")

    messages: "Iterable[ChatCompletionMessageParam]" = [
        {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )

    response = generate_response(client, messages)

    if (not response.usage):
        raise RuntimeError(f"{response.model} failed to respond to API call")

    if (args.verbose):
        print("\n==================== bootdev chatbot ====================\n")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print("\n======================= response ========================\n")
    print(response.choices[0].message.content)
    print("\n=========================================================\n")

def generate_response(client: OpenAI, messages: "Iterable[ChatCompletionMessageParam]") -> "ChatCompletion":
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )

if __name__ == "__main__":
    main()
