import os
from google import genai 
from google.genai import types 
max_chars = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="shows the content of the file in the directory ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_target_file = os.path.commonpath([working_dir_abs,target_path]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    valid_target_path = os.path.isfile(target_path)
    if not valid_target_path:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path,"r") as f:
            file_content_string = f.read(max_chars)
            if f.read(1):
                file_content_string += f"[...File {file_path} truncated at {max_chars} characters]"
            return file_content_string
    except Exception as e:
        return f"Error: {e}"