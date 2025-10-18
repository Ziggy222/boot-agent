import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# A Dictionary mapping the function names to the function themselves
name_to_function = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

# Identifies if we know the function and returns either the result of calling 
#  the function or an error message detailing we don't know the function being requested
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")
    # Function is unknown, return types.Content with error
    if function_name not in name_to_function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_responses(
                    name=function_name,
                    response=[{"error": f"Unknown function: {function_name}"}]
                )
            ]
        )
    # Function is known, execute it and return types.Content with response
    else:
        # Enforce working_directory to always be ./calculator
        kwargs = {**function_args, "working_directory": "./calculator"}
        function_result = name_to_function[function_name](**kwargs) 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )    