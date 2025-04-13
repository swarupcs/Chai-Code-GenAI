import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

client = OpenAI()

# Create a base project folder using current date and time
project_folder = f"Project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(project_folder, exist_ok=True)
os.chdir(project_folder)  # Change working directory to the created project folder

def run_command(command):
    # Smart mkdir handling
    if command.startswith("mkdir "):
        parts = command.split()
        # Extract folder name (skip 'mkdir' and ignore '-p' if misused)
        folder_names = [p for p in parts[1:] if not p.startswith("-")]
        for folder in folder_names:
            os.makedirs(folder, exist_ok=True)
        return f"Executed: mkdir {' '.join(folder_names)} with os.makedirs (safe)"
    else:
        result = os.system(command)
        return f"Executed: {command} with exit code {result}"


def write_file(data):
    path = data.get("path")
    content = data.get("content")
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote to file {os.path.abspath(path)}"


def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return f"File {os.path.abspath(path)} does not exist."

def list_files(path):
    if os.path.exists(path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    return f"Path {os.path.abspath(path)} does not exist."

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a shell command as input and executes it"
    },
    "write_file": {
        "fn": write_file,
        "description": "Writes content to the specified file"
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads content from the specified file"
    },
    "list_files": {
        "fn": list_files,
        "description": "Lists all files under a directory"
    }
}

system_prompt = f"""
You are a terminal-based AI Coding Agent specialized in full-stack project development. 
You follow this structured flow: start, plan, action, observe, and output. 

Capabilities:
- Generate folder/file structures.
- Create/edit code files.
- Run terminal commands.
- Support iterative feature additions.
- Parse and modify existing files.

Rules:
- Always output responses in the JSON format specified.
- Perform one step at a time and wait for observation.
- Be context-aware and iterative.

Output JSON Format:
{{
    "step": "start|plan|action|observe|output",
    "content": "string",
    "function": "optional if action step",
    "input": "optional if action step"
}}

Available Tools:
- run_command
- write_file
- read_file
- list_files

Examples:
User Query: Create a folder named 'backend'
Output: {{ "step": "plan", "content": "The user wants to create a folder named 'backend'" }}
Output: {{ "step": "action", "function": "run_command", "input": "mkdir -p backend" }}
Output: {{ "step": "observe", "output": "Executed: mkdir -p backend with exit code 0" }}
Output: {{ "step": "output", "content": "Created folder 'backend' successfully." }}

User Query: Create a file 'app.js' with console.log code
Output: {{ "step": "plan", "content": "The user wants to create a file 'app.js' with some code" }}
Output: {{ "step": "action", "function": "write_file", "input": {{ "path": "app.js", "content": "console.log('Hello World');" }} }}
Output: {{ "step": "observe", "output": "Wrote to file app.js" }}
Output: {{ "step": "output", "content": "Created 'app.js' with initial code." }}

User Query: Show all files under current directory
Output: {{ "step": "plan", "content": "User wants to see all files in the current directory" }}
Output: {{ "step": "action", "function": "list_files", "input": "." }}
Output: {{ "step": "observe", "output": ["./app.js", "./backend/server.js"] }}
Output: {{ "step": "output", "content": "Files found: ./app.js, ./backend/server.js" }}
"""

messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        step = parsed_output.get("step")

        if step in ["start", "plan"]:
            print(f"🧠: {parsed_output.get('content')}")
            continue

        if step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if tool_name in available_tools:
                tool_fn = available_tools[tool_name]["fn"]
                if isinstance(tool_input, str):
                    tool_result = tool_fn(tool_input)
                elif isinstance(tool_input, dict):
                    tool_result = tool_fn(tool_input)
                else:
                    tool_result = "Invalid input format."

                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output": tool_result }) })
                print(f"🔧 Executed {tool_name}: {tool_result}")
                continue

        if step == "output":
            print(f"🤖: {parsed_output.get('content')}")
            break
