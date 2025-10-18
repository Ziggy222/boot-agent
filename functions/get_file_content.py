import os
from google.genai import types

# get_file_content.py

# Gets contents of file specified by file_path relative to working_directory
def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except (ValueError, TypeError) as e:
        return f'Error: Invalid path "{file_path}": {str(e)}'
    
    # Double check that the file is not outside the working directory
    if not absolute_path.startswith(working_directory_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        if os.path.isdir(absolute_path):
            return f'Error: "File not found or is not a regular file: {file_path}'
    except (OSError, PermissionError) as e:
        return f'Error: Cannot access path "{file_path}": {str(e)}'
    
    try:
        with open(absolute_path, 'r') as file:
            contents = file.read()
            if len(contents) > 10000:
                contents = contents[:10000]
                contents += f"[...File '{file_path}' truncated at 10000 characters]"
            return contents
    except FileNotFoundError:
        return f'Error: File not found: "{file_path}"'
    except PermissionError:
        return f'Error: Permission denied reading file: "{file_path}"'
    except IsADirectoryError:
        return f'Error: Path is a directory, not a file: "{file_path}"'
    except UnicodeDecodeError as e:
        return f'Error: Cannot decode file "{file_path}" as text: {str(e)}'
    except MemoryError:
        return f'Error: File "{file_path}" is too large to read into memory'
    except OSError as e:
        return f'Error: OS error reading file "{file_path}": {str(e)}'
    except Exception as e:
        return f'Error: Unexpected error reading file "{file_path}": {str(e)}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file specified by the file path, relative to the working directory. Files larger than 10000 characters will be truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)