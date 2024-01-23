
import subprocess
import logging
import time
from openai import OpenAI
import ast
import re

class OpenAIHandler:
    """
    A class representing an algorithm developer.

    Attributes:
        openai_handler: An instance of the OpenAIHandler class used for communication with the OpenAI API.

    Methods:
        __init__(self, openai_handler): Initializes a new instance of the AlgoDeveloper class.
        develop_algo(self, algo_code=None, error_message=None): Develops or improves an AI algorithm based on the provided code and feedback.
    """
    def __init__(self, model="gpt-3.5-turbo-1106"): #gpt4 def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model

    def create_message(self, system_content, user_content, assistant_content=None):
        structured_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        if assistant_content:
            structured_messages.append({"role": "assistant", "content": assistant_content})
        return structured_messages

    def get_response(self, messages):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            response_content = completion.choices[0].message.content
            print(response_content)
            time.sleep(10)
            return response_content
        except Exception as e:
            logging.error(f"Error in getting response: {e}")
            return None

class AlgoDeveloper:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def develop_algo(self, algo_code=None, error_message=None):
        if not algo_code:
            system_message = "Develop a new AI algorithm based on organic learning principles, adhering to Python standards."
            user_message = "Create an initial AI that learns like a stem cell within the Python coding environment."
        else:
            system_message = "Improve the AI algorithm based on the following code and feedback, adhering to Python standards."
            user_message = f"The current AI algorithm is:\n{algo_code}\nError encountered: {error_message}\nHow should the algorithm be improved?"
        
        messages = self.openai_handler.create_message(system_message, user_message)
        response = self.openai_handler.get_response(messages)
        improved_algo_code = CodingUtils.extract_python_code(response)
        if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
            return improved_algo_code
        logging.error("No valid Python code improvements found in the response.")
        return algo_code  # Return the original code if no improvements were made

class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def test_algo(self, algo_code):
        try:
            test_process = subprocess.Popen(["python", "-c", algo_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = test_process.communicate(timeout=30)
            if stderr:
                logging.error(f"Algorithm Testing Failed: {stderr}")
                return False, stderr
            logging.info(f"Algorithm Testing Success: {stdout}")
            return True, stdout
        except subprocess.TimeoutExpired:
            logging.error("Algorithm testing timed out.")
            return False, "Algorithm testing timed out."
        except Exception as e:
            logging.error(f"Error in testing algorithm: {e}")
            return False, str(e)

class CodingUtils:
    @staticmethod
    def is_code_valid(code):
        try:
            ast.parse(code)
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_developer = AlgoDeveloper(openai_handler)
    algo_tester = AlgoTester(openai_handler)
    
    algo_code = ""  # Initialize with an empty script or a base script
    max_iterations = 100  # Prevent infinite loop, set a maximum number of iterations
    error_message = None

    for _ in range(max_iterations):
        algo_code = algo_developer.develop_algo(algo_code, error_message)
        if algo_code:
            test_result, feedback = algo_tester.test_algo(algo_code)
            if test_result:
                logging.info(f"Algorithm tested successfully. Continuing to improve.")
            else:
                logging.error("Algorithm testing failed. Trying to improve again.")
                error_message = feedback  # Pass the error message to the next iteration for improvement
        else:
            logging.error("Algorithm development failed. Ending the loop.")
            break
    logging.info("Iterative improvement process completed.")
