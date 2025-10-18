import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # Get the absolute path of the file
    try:
        working_directory_abs = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except (ValueError, TypeError) as e:
        return f'Error: Invalid path "{file_path}": {str(e)}'
    
    # Double check that the file is not outside the working directory
    if not absolute_path.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # Create the file if it does not exist
    try:
        exists = os.path.exists(absolute_path)
    except Exception as e:
        return f"Error: {e}"
    if not exists:
        try:
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        except Exception as e:
            return f"Error: {e}"
        try:
            with open(absolute_path, 'w') as file:
                file.write(content)
        except Exception as e:
            return f"Error: {e}"
    # Write the content to the file
    try:
        with open(absolute_path, 'w') as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path, relative to the working directory. Creates the file and any necessary parent directories if they don't exist. Overwrites the file if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file should be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)