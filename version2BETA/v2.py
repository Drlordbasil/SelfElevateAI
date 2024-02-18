import logging
import ast
import subprocess
import os
from datetime import datetime
from pathlib import Path
import re
import black
from openai import OpenAI  # OpenAI API usage remains untouched

# Enhanced logging for better readability and troubleshooting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(funcName)s - %(message)s')

def generate_project_directory(base_path="projects"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    project_dir = Path(base_path) / f"project_{timestamp}"
    project_dir.mkdir(parents=True, exist_ok=False)
    logging.info(f"Project directory {project_dir} created for your AI Maestro workspace.")
    return project_dir

class OpenAIHandler:
    def __init__(self, model, project_dir):
        self.client = OpenAI()  # Ensured OpenAI client initialization remains unchanged
        self.model = model
        self.project_dir = project_dir
        logging.info(f"AI Maestro Handler for {model} initialized in {project_dir}")

    def get_response_with_message(self, system_content, user_content, model_override=None):
        model = model_override if model_override else self.model
        messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
        logging.info(f"AI Maestro requests completion from model {model}.")
        try:
            completion = self.client.chat.completions.create(model=model, messages=messages, temperature=0.5)
            response_content = completion.choices[0].message.content.strip()
            logging.info("AI Maestro successfully received response from OpenAI.")
            return response_content
        except Exception as e:
            logging.error(f"AI Maestro encountered an error with OpenAI: {e}")
            return ""

class CollaborativeAI:
    def __init__(self, project_dir):
        self.maestro_handler = OpenAIHandler("gpt-4-0125-preview", project_dir)
        self.agent_handlers = [OpenAIHandler("gpt-3.5-turbo-0125", project_dir) for _ in range(3)]
        self.project_dir = project_dir
        logging.info("AI Maestro collaborative environment ready.")

    def delegate_tasks(self, initial_task_description):
        logging.info("AI Maestro begins task delegation")
        maestro_response = self.maestro_handler.get_response_with_message(
            "Organizing tasks among agents", initial_task_description
        )

        if not maestro_response:
            logging.error("AI Maestro did not receive delegation instructions.")
            return []

        results = self.process_maestro_response(maestro_response)
        return results

    def process_maestro_response(self, response):
        if "divide" in response:
            task_contents = response.split("divide")
        else:
            task_contents = [response]

        tasks = [{"task_id": str(i), "content": content.strip(), "agent_id": (i-1) % len(self.agent_handlers)} for i, content in enumerate(task_contents, start=1)]

        results = []
        for task in tasks:
            task_dir = self.project_dir / f"task_{task['task_id']}"
            task_dir.mkdir(exist_ok=True)
            agent = self.agent_handlers[task["agent_id"]]
            logging.info(f"Delegating task {task['task_id']} to AI agent {task['agent_id']}.")
            agent_response = agent.get_response_with_message("Processing task", task['content'])
            results.append({'task_id': task['task_id'], 'agent_response': agent_response})
            with open(task_dir / "response.txt", "w") as f:
                f.write(agent_response)
        return results

class EnvironmentManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.venv_path = project_dir / "venv"

    def setup_venv(self):
        logging.info("AI Maestro is setting up the virtual environment.")
        try:
            subprocess.run(["python", "-m", "venv", str(self.venv_path)], check=True, capture_output=True)
            logging.info("Virtual environment ready for AI Maestro projects.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Virtual environment setup failed: {e}")

    def install_dependencies(self, requirements="requirements.txt"):
        requirements_path = self.project_dir / requirements
        if not requirements_path.exists():
            logging.info("Creating a default requirements.txt for AI Maestro.")
            with open(requirements_path, 'w') as f:
                f.write("requests\nnumpy\npandas")

        pip_path = self.venv_path / "Scripts" / "pip.exe" if os.name == 'nt' else self.venv_path / "bin" / "pip"
        logging.info("AI Maestro installs project dependencies.")
        try:
            subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True, capture_output=True)
            logging.info("Dependencies installation complete.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install dependencies: {e.output.decode()}")



class CodingUtils:
    @staticmethod
    def remove_comments(code):
        return "\n".join(line for line in code.split('\n') if not line.strip().startswith("#") and '#' not in line)

    @staticmethod
    def is_code_valid(code):
        try:
            ast.parse(code)
            logging.info("Code validation by AI Maestro confirmed.")
            return True
        except (SyntaxError, IndentationError) as e:
            logging.error(f"AI Maestro detected a syntax issue: {e}")
            return False

    @staticmethod
    def extract_python_code(markdown_text):
        matches = re.findall(r"```python\n(.*?)```", markdown_text, re.DOTALL)
        if not matches:
            logging.warning("AI Maestro found no Python code blocks.")
            return ""
        return CodingUtils.remove_comments(matches[0].strip())

    @staticmethod
    def format_python_code(code):
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            logging.info("AI Maestro formatted the Python code.")
            return True, formatted_code
        except Exception as e:
            logging.error(f"AI Maestro encountered an error during code formatting: {e}")
            return False, code 

if __name__ == "__main__":
    project_dir = generate_project_directory()
    collaborative_ai = CollaborativeAI(project_dir)
    initial_task_description = "Design an innovative solution for optimizing AI workflows."
    delegated_results = collaborative_ai.delegate_tasks(initial_task_description)

    env_manager = EnvironmentManager(project_dir)
    env_manager.setup_venv()
    env_manager.install_dependencies()

    for result in delegated_results:
        logging.info(f"AI Maestro has successfully processed Task {result['task_id']} with AI agents.")
