import subprocess
import logging
import sys
import time
import ast
import re
import json
from openai import OpenAI

idea = "create a NN based pygame that a user can play against an AI npc"
gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"
ft3 = "ft:gpt-3.5-turbo-1106:personal::8tGk0TIP" # added a fine-tuned model for proper openai usage(updated by fine-tuning on latest api usage
class OpenAIHandler:
    def __init__(self, model=gpt3):
        self.client = OpenAI()
        self.model = model

    def get_response_with_message(self, system_content, user_content, assistant_content=None):
        # Create structured messages
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        if assistant_content:
            messages.append({"role": "assistant", "content": assistant_content})

        # Attempt to get a response using the structured messages
        max_retries = 3
        for retry_count in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    temperature=0.3,
                    messages=messages
                )
                response_content = completion.choices[0].message.content
                self.log_response(response_content)

                if not self.should_retry(response_content):
                    return response_content
                self.log_retry_attempt(retry_count + 1, max_retries)
                time.sleep(10)  # Re-evaluate the necessity of this delay

            except Exception as e:
                logging.error(f"Failed to get response from OpenAI: {e}")
                return None
        logging.error(f"Failed to get response without 'path_to_your_dataset' after {max_retries} retries")
        return None

    def log_response(self, response_content):
        logging.info("=" * 40)
        logging.info("OpenAI Response Received:")
        logging.info("-" * 40)
        logging.info(response_content)
        logging.info("=" * 40)

    def should_retry(self, response_content):
        return "path_to_your_dataset" in response_content or "placeholder logic" in response_content

    def log_retry_attempt(self, retry_count, max_retries):
        logging.info(f"Retrying... (Attempt {retry_count}/{max_retries})")






'''
note: Im not sure what im going to do with the collab class yet. 
'''

class CollaborativeAgent:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def collaborate_on_task(self, initial_task):
        """
        Takes an initial task and collaboratively improves upon it through
        multiple interactions with OpenAI, utilizing the OpenAIHandler.

        :param initial_task: A dictionary containing initial 'system_content' and 'user_content'
                             for the task.
        :return: A string containing the final improved task output, or a failure message.
        """
        current_task = initial_task
        collaboration_rounds = 3  # Define how many times you want to iterate/collaborate on the task

        for _ in range(collaboration_rounds):
            system_message, user_message = current_task['system_content'], current_task['user_content']
            response = self.openai_handler.get_response_with_message(system_message, user_message)

            if response:

                current_task['user_content'] = response
            else:
                logging.error("Failed to obtain a response for the current collaboration round.")
                return "Failed to collaboratively improve the task due to an error."

        return current_task['user_content']










        
class AlgoDeveloper:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def _generate_messages(self, algo_code, error_message, historical_data):
        if not algo_code:
            system_message, user_message = self._generate_initial_prompt()
        else:
            system_message, user_message = self._generate_follow_up_prompt(historical_data, error_message)
        return system_message, user_message

    def _generate_initial_prompt(self):
        system_message = "Create a Python script for an automation task emphasizing profitability, automation potential, and practicality, avoiding placeholders and ensuring the script is self-contained."
        user_message = f"""
        Develop a Python script based on the idea: {idea}. The script should be innovative, practical, and ready for deployment, incorporating advanced libraries as needed.Your response will be structred like this:\n

        ```python
        # Your Python code here
        ``
        #####TODO LIST YOU NEED TO DO NEXT ITERATION #################################
        1. <your todo list based on dynamically thinking about step you are on>
        2.
        3.
        
        ### SELF REFELCTION ON YOUR CODE AND WHAT YOU THINK YOU NEED TO DO NEXT ITERATION###
        <insert your self reflection here>
        ### DIRECTION YOU NEED TO MAKE MOST EFFECIENT CHOICES ###
        <insert your effecient direction steps here>
        """
 
        
        return system_message, user_message

    def _generate_follow_up_prompt(self, historical_data, error_message):
        common_errors, recent_feedback = self._analyze_historical_data(historical_data)
        feedback_points = ", ".join(common_errors) if common_errors else "None"
        system_message = f"Refine the script by addressing common errors: {feedback_points} and incorporating feedback: {recent_feedback}."
        user_message = "Improve the existing script by correcting errors and enhancing functionality based on the following feedback:" + (f" {error_message}" if error_message else "")
        return system_message, user_message

    def _analyze_historical_data(self, historical_data):
        error_frequency = {}
        latest_feedback = ""
        for entry in historical_data:
            error_msg = entry.get('error_message')
            feedback = entry.get('feedback')
            if error_msg:
                error_frequency[error_msg] = error_frequency.get(error_msg, 0) + 1
            if feedback:
                latest_feedback = feedback
        common_errors = sorted(error_frequency, key=error_frequency.get, reverse=True)[:3]
        return common_errors, latest_feedback

    def develop_algo(self, algo_code=None, error_message=None):
        historical_data = FileManager.get_historical_data('iteration_history.json')
        for attempt in range(10):
            print(f"Attempt {attempt + 1}/10")
            system_message, user_message = self._generate_messages(algo_code, error_message, historical_data)
            response = self.openai_handler.get_response_with_message(system_message, user_message)
            improved_algo_code = CodingUtils.extract_python_code(response)
            if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
                print("Valid improvement found. Testing...")
                test_result, feedback, suggestion = algo_tester.test_algo(improved_algo_code)
                if test_result:
                    print("Algorithm improvement validated.")
                    FileManager.log_iteration_data('iteration_history.json', self._log_iteration_details(attempt, improved_algo_code, feedback, error_message, suggestion))
                    return improved_algo_code
                else:
                    print("Feedback received. Attempting to refine...")
                    error_message = feedback
            else:
                print("No valid improvements found. Retrying...")
            logging.error("Improvement iteration did not yield a valid improvement.")
        return algo_code

    @staticmethod
    def _log_iteration_details(attempt, algo_code, feedback, error_message, suggestion):
        return {
            'iteration': attempt,
            'algorithm_code': algo_code,
            'feedback': feedback,
            'error_message': error_message,
            'suggestion': suggestion
        }



class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def get_openai_suggestion(self, code, output):
        prompt = f"[never include placeholder filenames or placeholders like 'pass' in python]Review and improve the following Python code with a fine toothed comb, so to speak, while improving its classes and its output of either productivity and/or more profitable means and/or cheaper costs to run, then provide real improvements to the code:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nNew Script:"
        system_message = """
        You are a Debugger that sends a revised python script to another AI for running local testing in cmd prompt subprocess and will get an output, ensure the logging is verbose and robust. You are to improve at least 3 functionings and complete the todo list.
        ```python
        # Your Python code here
        ``
        #####TODO LIST YOU NEED TO DO NEXT ITERATION #################################
        1. <your todo list based on dynamically thinking about step you are on>
        2.
        3.
        
        ### SELF REFELCTION ON YOUR CODE AND WHAT YOU THINK YOU NEED TO DO NEXT ITERATION###
        <insert your self reflection here>
        ### DIRECTION YOU NEED TO MAKE MOST EFFECIENT CHOICES ###
        <insert your effecient direction steps here>

        """
        user_message = prompt
        # Using the combined method to create the message and get the response in one call
        response = self.openai_handler.get_response_with_message(system_message, user_message)
        return response if response else "No suggestions available."

    def parse_errors(self, stderr):
        """
        Parses stderr to filter out warnings and identify critical errors.
        """
        errors = stderr.split('\n')
        warnings = []
        critical_errors = []

        for error in errors:
            if "WARNING:" in error or "oneDNN" in error:
                warnings.append(error)
            elif error.strip():
                critical_errors.append(error)

        return warnings, critical_errors

    def test_algo(self, algo_code):
        suggestion = None
        try:
            test_process = subprocess.Popen(
                [sys.executable, "-c", algo_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = test_process.communicate(timeout=90)
            warnings, critical_errors = self.parse_errors(stderr)

            if critical_errors:
                error_message = "\n".join(critical_errors)
                self.log_message("Algorithm Testing Failed", error_message, level="error")
                return False, error_message, suggestion

            if warnings:  # Log warnings without failing the test
                for warning in warnings:
                    logging.warning(warning)

            suggestion = self.get_openai_suggestion(algo_code, stdout)
            self.log_message("Algorithm Testing Success", stdout, level="info")
            return True, stdout, suggestion

        except subprocess.TimeoutExpired:
            timeout_msg = "Algorithm testing timed out. Possible reason: User input required(use tests to output properly if no user input is given we need it to still test it within 5 seconds of no user input)."
            self.log_message(timeout_msg, level="error")
            return False, timeout_msg, suggestion

        except Exception as e:
            error_msg = f"Error in testing algorithm: {e}"
            self.log_message(error_msg, level="error")
            return False, error_msg, suggestion

    def log_message(self, message, detail="", level="info"):
        border = "=" * 40
        log_message = f"{border}\n{message}:\n{detail}\n{border}"
        if level == "info":
            logging.info(log_message)
        elif level == "error":
            logging.error(log_message)

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

    @staticmethod
    def log_iteration_data(filename, iteration_data):
        with open(filename, 'a') as file:
            file.write(json.dumps(iteration_data) + '\n')
            logging.info(f"Iteration data logged to {filename} successfully.")

    @staticmethod
    def get_historical_data(filename):
        historical_data = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    historical_data.append(json.loads(line))
            return historical_data
        except FileNotFoundError:
            logging.warning(f"No historical data found in {filename}.")
            return []



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
            FileManager.save_script('final_algo_script.py', algo_code)
            FileManager.save_conversation_dataset('conversation_dataset.json', conversation_history)

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

    print("-----------------------------------")
