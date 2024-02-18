import subprocess
import logging
import sys
import ast
import json
from openai import OpenAI

class OpenAIHandler:
    def __init__(self, model="gpt-3.5-turbo-0125"):
        self.client = OpenAI()
        self.model = model
        logging.info(f"OpenAI Handler initialized with model {model}")

    def get_response_with_message(self, system_content, user_content, model_override=None):
        model = model_override if model_override else self.model
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        logging.info(f"Fetching response for model {model} with system and user content.")
        try:
            completion = self.client.chat.completions.create(model=model, temperature=0.3, messages=messages)
            response_content = completion.choices[0].message.content
            logging.info("Response successfully received from OpenAI.")
            return response_content
        except Exception as e:
            logging.error(f"OpenAI API call failed: {e}")
            return None

class CollaborativeAI:
    def __init__(self):
        self.maestro_handler = OpenAIHandler(model="gpt-4-0125-preview")
        self.agent_handlers = [OpenAIHandler(model="gpt-3.5-turbo-0125") for _ in range(3)]
        logging.info("Collaborative AI system initialized with Maestro and Agent handlers.")

    def delegate_tasks(self, initial_task_description):
        system_content = "Maestro AI: Organize and direct your agents to collaboratively design, enhance, and validate a sophisticated algorithm. Employ the strengths of each agent to maximize efficiency and effectiveness."
        maestro_task = {"system_content": system_content, "user_content": initial_task_description}
        logging.info("Delegating initial task to Maestro AI.")
        maestro_response = self.maestro_handler.get_response_with_message(**maestro_task)

        try:
            task_delegations = json.loads(maestro_response)
            logging.info("Tasks successfully parsed from Maestro AI response.")
        except json.JSONDecodeError:
            logging.error("Failed to decode maestro response into JSON.")
            return []

        results = []
        for task in task_delegations.get('tasks', []):
            agent_id = task.get('agent_id', 0) % len(self.agent_handlers)
            agent_task = {"system_content": task.get('system_content', ''), "user_content": task.get('user_content', '')}
            logging.info(f"Delegating task to Agent {agent_id}.")
            agent_response = self.agent_handlers[agent_id].get_response_with_message(**agent_task)
            results.append({'task_id': task.get('task_id', ''), 'agent_id': agent_id, 'response': agent_response})

        return results

    def compile_results(self, delegated_results):
        compiled_results = {}
        for result in delegated_results:
            task_id = result['task_id']
            if task_id not in compiled_results:
                compiled_results[task_id] = []
            compiled_results[task_id].append(result)
            logging.info(f"Compiling result for Task ID {task_id} from Agent ID {result['agent_id']}.")
        return compiled_results

class TaskManager:
    @staticmethod
    def validate_code(code):
        try:
            ast.parse(code)
            logging.info("Code validation successful.")
            return True, "Code is syntactically correct."
        except SyntaxError as e:
            logging.error(f"Code validation failed: {e}")
            return False, str(e)

    @staticmethod
    def execute_code(code):
        try:
            exec(code)
            logging.info("Code executed successfully.")
            return True, "Code executed successfully."
        except Exception as e:
            logging.error(f"Code execution failed: {e}")
            return False, str(e)

    @staticmethod
    def format_results(compiled_results):
        formatted_result = ""
        for task_id, results in compiled_results.items():
            formatted_result += f"Task ID: {task_id}\n"
            for result in results:
                formatted_result += f"Agent ID: {result['agent_id']}, Response: {result['response']}\n"
        logging.info("Results formatted successfully.")
        return formatted_result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    collaborative_ai = CollaborativeAI()

    initial_task_description = "Develop a Python-based solution for analyzing and predicting stock market trends using historical data and machine learning models."
    logging.info("Starting task delegation process.")
    delegated_results = collaborative_ai.delegate_tasks(initial_task_description)
    compiled_results = collaborative_ai.compile_results(delegated_results)

    logging.info("Starting code validation and execution process.")
    for task_id, results in compiled_results.items():
        for result in results:
            valid, validation_message = TaskManager.validate_code(result['response'])
            if valid:
                exec_status, exec_message = TaskManager.execute_code(result['response'])
                logging.info(f"Execution Status for Task ID {task_id}, Agent ID {result['agent_id']}: {exec_message}")
            else:
                logging.error(f"Validation Error for Task ID {task_id}, Agent ID {result['agent_id']}: {validation_message}")

    formatted_result = TaskManager.format_results(compiled_results)
    logging.info(f"Final Compiled Task Results:\n{formatted_result}")
