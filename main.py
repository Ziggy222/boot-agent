import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. 
You can perform the following operations:

- List files and directories
- Read the contents of a file
- Write to a file
- Run a Python file

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    if len(sys.argv) < 1:
        print("Error, no prompt provided")
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[available_functions],
            )
        )
    output_string = ""    
    for call in response.function_calls:
        function_response = call_function(call, verbose=("--verbose" in sys.argv))
        # Check that function response has .parts[0].function_response.response
        if function_response.parts[0].function_response.response is not None:
            output_string += f"-> {function_response.parts[0].function_response.response}\n"
        else:
            output_string += f"-> Error: No response from function {call.name}\n"
    print(output_string)

if __name__ == "__main__":
    main()
