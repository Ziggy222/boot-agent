import os

def write_file(working_directory, file_path, content):
    # Get the absolute path of the file
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except (ValueError, TypeError) as e:
        return f'Error: Invalid path "{file_path}": {str(e)}'
    
    # Double check that the file is not outside the working directory
    if working_directory not in absolute_path:
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
    