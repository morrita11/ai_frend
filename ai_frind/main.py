import os
import argparse
import sys
from promts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import available_functions
from call_function import call_function

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file],
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("Gemini key not valid or not installed")
client = genai.Client(api_key = api_key)

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages,args)


def generate_content(client, messages,args):

    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ))
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("Gemini is bessy")
        if args.verbose is True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Response: {response.text}")
        if not response.function_calls:
            print(f"Response: {response.text}")
            return
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    
        function_responses = []

        for candidate_part in response.function_calls:
            function_call_results = call_function(candidate_part, verbose= args.verbose)
            if not function_call_results.parts:
                raise Exception("no result parts")
            function_response = function_call_results.parts[0].function_response
            if function_response is None:
                raise Exception("no function response")
            if function_response.response is None:
                raise Exception("no function response")
            function_responses.append(function_call_results.parts[0])
            if args.verbose:
                print(f"-> {function_response.response}")
        messages.append(types.Content(role="tool", parts=function_responses))
    print("Maximum iterations reached")
    sys.exit(1)



if __name__ == "__main__":
    main()
