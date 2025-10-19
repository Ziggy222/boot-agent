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

MAX_ITERATIONS = 20

def main():
    if len(sys.argv) < 1:
        print("Error, no prompt provided")
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    # Initialize messages with user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    # Agent feedback loop
    for iteration in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteration {iteration + 1}/{MAX_ITERATIONS} ---")
        
        try:
            # Generate content with entire message history
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[available_functions],
                )
            )
            
            # Add candidates to messages
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            # Handle function calls first (all of them)
            if response.function_calls:
                # Execute all function calls and collect their responses
                function_response_parts = []
                for call in response.function_calls:
                    function_response = call_function(call, verbose=verbose)
                    function_response_parts.extend(function_response.parts)
                
                # Convert all function responses to role="user" and append
                user_message = types.Content(role="user", parts=function_response_parts)
                messages.append(user_message)
                continue  # Go to next iteration
            
            # Check for final text response (only if no function calls)
            if response.text:
                print(response.text)
                break
            
            # If no text and no function calls, something unexpected happened
            if verbose:
                print("No text response or function calls in this iteration")
            
        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            break
    else:
        # Loop completed without break (max iterations reached)
        print(f"\nReached maximum iterations ({MAX_ITERATIONS}) without final response")

if __name__ == "__main__":
    main()
