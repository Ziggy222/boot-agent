import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    # Get the absolute path of the file
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except (ValueError, TypeError) as e:
        return f'Error: Invalid path "{file_path}": {str(e)}'
    
    # Double check that the file is not outside the working directory
    if working_directory not in absolute_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check that the file exists
    try:
        exists = os.path.exists(absolute_path)
    except Exception as e:
        return f"Error: {e}"
    if not exists:
        return f'Error: File "{file_path}" not found.'

    # Check that the file is a Python file
    if not absolute_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file.'
    
    # Run the file with conditions:
        # 1. Timeout of 30 seconds
        # 2. Capturing both stdout and stderr
        # 3. Sets the working directory correctly to the given working_directory
        # 4. Passes the given args to the file
    try:
        complete_process = subprocess.run(
            ['python', absolute_path, *args],
            check=True,
            timeout=30,
            capture_output=True,
            cwd=working_directory,
        )
    except: 
        return f"Error: executing Python file: {e}"
    
    response_string = ""
    if complete_process.stdout is not None:
        response_string += f"STDOUT: {complete_process.stdout}"
    if complete_process.stderr is not None:
        response_string += f"STDERR: {complete_process.stderr}"
    if complete_process.returncode != 0:
        response_string += f" Process exited with code {complete_process.returncode}"
    if len(response_string) == 0:
        response_string = "No output produced."
    return response_string

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments. The file must be within the working directory. Execution times out after 30 seconds.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)