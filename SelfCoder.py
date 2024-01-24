import subprocess
import logging
import time
from openai import OpenAI
import ast
import re
import json

gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"

class OpenAIHandler:
    def __init__(self, model=gpt3):
        self.client = OpenAI()
        self.model = model

    def create_message(self, system_content, user_content, assistant_content=None):
        nurturing_prefix = "This project is your progeny. Guide it with care and wisdom. "
        structured_messages = [
            {"role": "system", "content": nurturing_prefix + system_content},
            {"role": "user", "content": nurturing_prefix + user_content}
        ]
        if assistant_content:
            structured_messages.append({"role": "assistant", "content": nurturing_prefix + assistant_content})
        return structured_messages

    def get_response(self, messages):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            response_content = completion.choices[0].message.content
            logging.info("OpenAI Response Received:\n{}".format(response_content))
            time.sleep(10)  # Evaluate if this delay is necessary for rate limiting or API constraints
            return response_content
        except Exception as e:
            logging.error("Failed to get response from OpenAI: {}".format(e))
            return None

class AlgoDeveloper:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def develop_algo(self, algo_code=None, error_message=None):
        system_message, user_message = self._generate_messages(algo_code, error_message)
        messages = self.openai_handler.create_message(system_message, user_message)
        response = self.openai_handler.get_response(messages)
        improved_algo_code = CodingUtils.extract_python_code(response)
        if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
            logging.info("AI algorithm successfully nurtured and validated.")
            return improved_algo_code
        logging.error("Further nurturing required. AI model improvement not found.")
        return algo_code

    def _generate_messages(self, algo_code, error_message):
        nurturing_message = "Treat this AI model as your apprentice. Guide its learning and growth with each iteration."
        if not algo_code:
            system_message = nurturing_message + " Begin by crafting a novel AI model, drawing from a pool of unique concepts."
            user_message = nurturing_message + " Construct a foundational AI entity capable of learning and evolving, akin to a 'seedling' in the world of Python."
        else:
            system_message = nurturing_message + " Now, enhance the AI model by infusing it with genuine, quality data sources. Enrich and refine the dataset progressively."
            user_message = (
                nurturing_message + "\n!!! Implement sturdy model preservation and retrieval mechanisms for seamless cognitive evolution. Prioritize authentic, logical results over simulated outputs !!!\n"
                "Current model structure (ensure the integration of comprehensive error management and a cohesive main loop for operational harmony):\n"
                f"{algo_code}\n"
                "Encountered issues (provide insightful guidance to rectify these challenges):\n"
                f"{error_message}\n"
                "Directions for refinement (eradicate placeholders, remove inline notes, and weave in rich, articulate logic):"
            )
        return system_message, user_message

class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def test_algo(self, algo_code):
        try:
            sanitized_code = re.sub(r'[^a-zA-Z0-9_\s]', '', algo_code)  # Basic sanitization
            test_process = subprocess.Popen(["python", "-c", sanitized_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = test_process.communicate(timeout=30)
            if stderr:
                logging.error(f"Algorithm Testing Failed: {stderr}")
                return False, stderr
            logging.info(f"Algorithm Testing Successful: {stdout}")
            return True, stdout
        except subprocess.TimeoutExpired:
            logging.error("Algorithm testing timed out.")
            return False, "Algorithm testing timed out."
        except Exception as e:
            logging.error(f"Error during algorithm testing: {e}")
            return False, str(e)

class CodingUtils:
    @staticmethod
    def is_code_valid(code):
        try:
            ast.parse(code)
            logging.info("Python code validation passed.")
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in the generated code: {e}")
            return False

    @staticmethod
    def extract_python_code(markdown_text):
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        python_code_blocks = [match.strip() for match in matches]
        return python_code_blocks[0] if python_code_blocks else ""

class FileManager:
    @staticmethod
    def save_script(filename, content):
        try:
            with open(filename, 'w') as file:
                file.write(content)
                logging.info("Algorithm script saved to {} successfully.".format(filename))
        except IOError as e:
            logging.error(f"File operation failed: {e}")

    @staticmethod
    def save_conversation_dataset(filename, conversation_history):
        try:
            with open(filename, 'w') as file:
                json.dump(conversation_history, file, indent=4)
                logging.info("Conversation history saved to {} successfully.".format(filename))
        except IOError as e:
            logging.error(f"File operation failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_developer = AlgoDeveloper(openai_handler)
    algo_tester = AlgoTester(openai_handler)
    
    initial_script = ""
    algo_code = initial_script
    max_iterations = 20
    error_message = None
    performance_metrics = {}
    conversation_history = []

    logging.info("Commencing the iterative nurturing process for the AI algorithm.")
    for iteration in range(max_iterations):
        logging.info(f"Iteration {iteration + 1}: Developing and nurturing the algorithm.")
        conversation_history.append({
            'iteration': iteration,
            'algorithm_code': algo_code,
            'error_message': error_message
        })
        algo_code = algo_developer.develop_algo(algo_code, error_message)
        if algo_code:
            test_result, feedback = algo_tester.test_algo(algo_code)
            if test_result:
                logging.info(f"Algorithm successfully tested. Feedback: {feedback}")
                performance_metrics[iteration] = feedback
                conversation_history[-1]['feedback'] = feedback
            else:
                logging.error(f"Algorithm testing failed. Error: {feedback}")
                error_message = feedback
                conversation_history[-1]['error'] = feedback
        else:
            logging.error("Failed to develop a valid algorithm. Halting the nurturing process.")
            break

    FileManager.save_script('final_algo_script.py', algo_code)
    FileManager.save_conversation_dataset('conversation_dataset.json', conversation_history)
    logging.info("Iterative nurturing process completed.")
    logging.info(f"Final nurturing metrics: {performance_metrics}")
