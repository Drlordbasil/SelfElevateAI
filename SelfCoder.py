import subprocess
import logging
import sys
import time
import ast
import re
import json
from openai import OpenAI

gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"

class OpenAIHandler:
    def __init__(self, model=gpt3):
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
            logging.info("OpenAI Response Received:\n{}".format(response_content))
            time.sleep(10)  # Evaluate if this delay is necessary
            return response_content
        except Exception as e:
            logging.error("Failed to get response from OpenAI: {}".format(e))
            return None

class AlgoDeveloper:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def _generate_messages(self, algo_code, error_message):
        if not algo_code:
            # Initial prompt for generating a new script
            system_message = (
                "Create an AI model using mathematical principles, neural networks (NN), or Proximal Policy Optimization/Reinforcement Learning (PPO/RL). "
                "Structure the model with distinct classes for each core functionality, aiming for approximately 10 classes. "
                "The model should embody a concrete purpose and align with the concept of an evolving AI capable of adaptive learning. "
                "The code should be free from pseudocode, inline commentary, and placeholders."
            )
            user_message = (
                "Construct a foundational, adaptable AI entity, akin to a 'stem cell'. "
                "Utilize math-based AI principles, integrating NN and PPO/RL techniques. "
                "Develop a clean, well-structured codebase with individual classes for distinct functionalities. "
                "Focus on creating a practical, purpose-driven model. Only send valid code."
            )
        else:
            # Subsequent prompts for improving the script based on feedback
            system_message = "Improve the Python script to address the following feedback: "
            user_message = "Revise the script considering this feedback: "
            if error_message:
                system_message += error_message
                user_message += error_message
            else:
                system_message += "No specific errors, please enhance the script's functionality and performance."
                user_message += "Make general improvements to enhance functionality and performance."
        
        return system_message, user_message

    def develop_algo(self, algo_code=None, error_message=None):
        max_attempts = 10
        attempt = 0
        while attempt < max_attempts:
            system_message, user_message = self._generate_messages(algo_code, error_message)
            messages = self.openai_handler.create_message(system_message, user_message)
            response = self.openai_handler.get_response(messages)
            improved_algo_code = CodingUtils.extract_python_code(response)

            if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
                test_result, feedback, suggestion = algo_tester.test_algo(improved_algo_code)
                if test_result:
                    logging.info("AI algorithm improvement found and validated.")
                    return improved_algo_code
                else:
                    error_message = feedback
                    logging.info(f"Retrying algorithm development due to error: {feedback}")
            else:
                logging.error("No valid Python code improvements found in the response.")
            attempt += 1

        return algo_code

class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def get_openai_suggestion(self, code, output):
        prompt = f"Review the following Python code and its output, then provide suggestions for improvement:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nNew Script:"
        response = self.openai_handler.create_message("You are a Debugger that sends a revised python script to another AI", prompt)
        response = self.openai_handler.get_response(response)
        return response if response else "No suggestions available."

    def test_algo(self, algo_code):
        suggestion = None
        try:
            test_process = subprocess.Popen(
                [sys.executable, "-c", algo_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = test_process.communicate(timeout=30)
            if stderr:
                logging.error(f"Algorithm Testing Failed: {stderr}")
                return False, stderr, suggestion
            suggestion = self.get_openai_suggestion(algo_code, stdout)
            logging.info(f"Algorithm Testing Success: {stdout}")
            return True, stdout, suggestion
        except subprocess.TimeoutExpired:
            logging.error("Algorithm testing timed out.")
            return False, "Algorithm testing timed out.", suggestion
        except Exception as e:
            logging.error(f"Error in testing algorithm: {e}")
            return False, str(e), suggestion

class CodingUtils:
    @staticmethod
    def remove_comments(code):
        new_lines = []
        lines = code.split('\n')
        for line in lines:
            if not line.strip().startswith("#"):
                if '#' in line:
                    line = line.split('#', 1)[0]
                new_lines.append(line)
        return '\n'.join(new_lines)

    @staticmethod
    def is_code_valid(code):
        try:
            ast.parse(code)
            logging.info("Python code validation passed.")
            return True
        except (SyntaxError, IndentationError) as e:
            logging.error(f"Syntax error in the generated code: {e}")
            return False

    @staticmethod
    def extract_python_code(markdown_text):
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No Python code blocks found in the Markdown text.")
            return ""
        python_code_blocks = [match.strip() for match in matches]
        if len(python_code_blocks) > 1:
            logging.info("Multiple Python code blocks found. Returning the first block.")
        clean_code = CodingUtils.remove_comments(python_code_blocks[0])
        return clean_code

    @staticmethod
    def format_python_code(code):
        try:
            import black
            formatted_code = black.format_str(code, mode=black.FileMode())
            return True, formatted_code
        except Exception as e:
            logging.error(f"Error formatting Python code: {e}")
            return False, str(e)

class FileManager:
    @staticmethod
    def save_script(filename, content):
        with open(filename, 'w') as file:
            file.write(content)
            logging.info(f"Algorithm script saved to {filename} successfully.")

    @staticmethod
    def save_conversation_dataset(filename, conversation_history):
        with open(filename, 'w') as file:
            for entry in conversation_history:
                formatted_entry = {
                    "messages": [
                        {"role": "system", "content": entry.get("system_message", "")},
                        {"role": "user", "content": entry.get("user_message", "")},
                        {"role": "assistant", "content": entry.get("assistant_message", "")}
                    ]
                }
                file.write(json.dumps(formatted_entry) + '\n')
            logging.info(f"Conversation history saved to {filename} successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_developer = AlgoDeveloper(openai_handler)
    algo_tester = AlgoTester(openai_handler)
    
    initial_script = ""
    algo_code = initial_script
    max_iterations = 5
    error_message = None
    performance_metrics = {}
    conversation_history = []

    print("-----------------------------------")
    logging.info("Starting the iterative improvement process for the AI algorithm.")
    print("-----------------------------------")

    for iteration in range(max_iterations):
        print("-----------------------------------")
        logging.info(f"Iteration {iteration + 1}: Developing and testing the algorithm.")
        print("-----------------------------------")
        
        conversation_history.append({
            'iteration': iteration,
            'algorithm_code': algo_code,
            'error_message': error_message
        })

        algo_code = algo_developer.develop_algo(algo_code, error_message)
        if algo_code:
            test_result, feedback, suggestion = algo_tester.test_algo(algo_code)
            if test_result:
                performance_metrics[iteration] = feedback
                conversation_history[-1]['feedback'] = feedback
            else:
                error_message = feedback
                conversation_history[-1]['error'] = feedback
        else:
            logging.error("Failed to develop a valid algorithm. Stopping the iterative process.")
            break

    FileManager.save_script('final_algo_script.py', algo_code)
    FileManager.save_conversation_dataset('conversation_dataset.json', conversation_history)
    logging.info("Iterative improvement process completed.")
    logging.info(f"Final performance metrics: {performance_metrics}")
