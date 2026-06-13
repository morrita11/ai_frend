import os
import subprocess
from google import genai 
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="selects and runs a unique file in a file path directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file",
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_target_file = os.path.commonpath([working_dir_abs,target_path]) == working_dir_abs
    if not valid_target_file:
       return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    regular_file = os.path.isfile(target_path)
    if not regular_file:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    ends_with = target_path.endswith(".py")
    if not ends_with:
        return f'Error: "{file_path}" is not a Python file'
    try:
        output_parts = []
        command = ["python", target_path]
        if args:
            command.extend(args)
        completed = subprocess.run(command, cwd=working_dir_abs, capture_output=True,text=True,timeout=30)
        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")
        if not completed.stdout and not completed.stderr:
            output_parts.append("No output produced")
        else:
            if completed.stdout:
                output_parts.append(f"STDOUT:\n{completed.stdout}")
            if completed.stderr:
                output_parts.append(f"STDERR:\n{completed.stderr}")
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"


    
    