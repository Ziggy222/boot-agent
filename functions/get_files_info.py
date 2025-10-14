import os

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    
    try:
        if working_directory not in absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isfile(absolute_path):
            return f'Error: "{directory}" is not a directory'
        return_string = ""
        for file in os.scandir(absolute_path):
            # f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            return_string += f"- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}\n"
        return return_string
    except:
        return f"Error: something went wrong" 