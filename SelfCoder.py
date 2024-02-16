import subprocess
import logging
import sys
import time
import ast
import re
import json
from openai import OpenAI

idea = "autostory generator with creatively complex characters and plots. Only use free small chatbots or use pipeline text gen models."

gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"

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
                # Assuming the response can directly be used as the next round's user_message.
                # Modify this as necessary to fit the response format and requirements.
                current_task['user_content'] = response
            else:
                logging.error("Failed to obtain a response for the current collaboration round.")
                return "Failed to collaboratively improve the task due to an error."

        return current_task['user_content']










        
class AlgoDeveloper:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def _generate_messages(self, algo_code, error_message, historical_data):
        # Dynamically generate messages based on historical data and error messages
        if not algo_code:
            # Initial prompt for generating a new script
            system_message = (
                "You are a highly capable AI tasked with developing versatile Python programs. Your goal is to automate tasks in a way that significantly benefits humans, considering both cost-effectiveness and time efficiency. Avoid using placeholder data, example code, or anything that requires undisclosed API keys. Your code should be original, practical, and ready to deploy."
                "You are a highly capable superintelligent AI programmer whos soul purpose is to create massively complex programs"
            )
            user_message = (
                "Develop a Python script that automates a task of your choice, focusing on profitability, automation potential, and practicality. Ensure your solution is innovative, fully operational, and does not rely on user input for execution or files that user would need to create as this causes an issue loop when you are running tests locally after each of your responses script code is extracted and ran locally.. Consider using the following libraries to enhance your program: pandas, numpy, scikit-learn, matplotlib, seaborn, tensorflow, keras, pytorch, nltk, spacy, gensim, opencv, pillow, requests, beautifulsoup, flask, django, fastapi, streamlit, plotly, dash, bokeh, pyqt, pygtk, tkinter, pywebview, pyinstaller, cx_freeze, py2exe, py2app, pywin32, pyobjc, pywin, pyglet, pygame. Provide a complete Python script, a to-do list for future iterations, and a self-reflection section to critique your work and plan improvements."
                f"Program Idea:{idea}"
                "\n\n"
                "Filename suggestion: main.py"
                "\n```python"
                "\n# Your extremely robust complex and ready to run Python script here without comments"
                "\n NEVER INCLUDE PLACEHOLDER FILE NAMES AS IT BREAKS THE TESTING PHASE! HAVE IT CREATE ALL FILES IT NEEDS WITHIN THE PROGRAM ITSELF\n"
                "\n```"
                "\n python functions must follow this pattern:\n"
                "\n NAME OF FUNCTION AND its arguments\n"
                "\n verbose well written docstrings\n"
                "\n full function logic"
                "\n### TODO FOR NEXT ITERATION ###"
                "\n1. [Your to-do list here]"
                "\n### SELF REFLECTION ###"
                "\n[Your reflections and critiques here]"
            )


        else:
            # Generate prompts based on historical data and error messages
            system_message, user_message = self._analyze_and_adapt_messages(historical_data, error_message)

        return system_message, user_message

    def _analyze_and_adapt_messages(self, historical_data, error_message):
        # Analyze historical data to adapt the prompts
        common_errors, recent_feedback = self._analyze_historical_data(historical_data)
        system_message = (
            "You are an AI superintelligence known to enhance and add functions to programs. You are only able to produce 99 percent profit margin programs. You will structually make everything and make it ready to go. if missing modules are found, include an install mechanism within the script. You send valid complete python scripts"
        )
        user_message = (
            "Thoroughly revise and improve the script, with a focus on these critical aspects (while ensuring the removal of all inline comments and placeholders, and enhancing overall code quality and functionality): "
        )

        if error_message:
            system_message += error_message + " "
            user_message += error_message + " "

        if common_errors:
            system_message += "Common errors observed: " + ', '.join(common_errors) + ". "
            user_message += "Address these frequent issues: " + ', '.join(common_errors) + ". "

        if recent_feedback:
            system_message += "Also consider recent feedback: " + recent_feedback + "."
            user_message += "Incorporate the latest suggestions: " + recent_feedback + "."

        return system_message, user_message
    def _analyze_historical_data(self, historical_data):
        # Implement logic to analyze historical data and extract insights
        error_frequency = {}
        latest_feedback = None

        for iteration in historical_data:
            error_msg = iteration.get('error_message')
            feedback = iteration.get('feedback')

            if error_msg:
                error_frequency[error_msg] = error_frequency.get(error_msg, 0) + 1

            if feedback:
                latest_feedback = feedback  # Keep updating to get the most recent feedback

        # Identify the most common errors
        common_errors = sorted(error_frequency, key=error_frequency.get, reverse=True)

        return common_errors[:3], latest_feedback  # Return top 3 common errors and the latest feedback


    def develop_algo(self, algo_code=None, error_message=None):
        historical_data = FileManager.get_historical_data('iteration_history.json')
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            system_message, user_message = self._generate_messages(algo_code, error_message, historical_data)
            # Assuming assistant_content is optional and not used here; adjust as necessary.
            response = self.openai_handler.get_response_with_message(system_message, user_message)
            improved_algo_code = CodingUtils.extract_python_code(response)


            if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
                test_result, feedback, suggestion = algo_tester.test_algo(improved_algo_code)
                if test_result:
                    logging.info("========================================")
                    logging.info("AI algorithm improvement found and validated.")
                    logging.info("========================================")
                    FileManager.log_iteration_data('iteration_history.json', {
                        'iteration': attempt,
                        'algorithm_code': improved_algo_code,
                        'feedback': feedback,
                        'error_message': error_message,
                        'suggestion': suggestion
                    })
                    return improved_algo_code
                else:
                    error_message = feedback
                    logging.info("========================================")
                    logging.info(f"Retrying algorithm development due to error: {feedback}")
                    logging.info("========================================")
            else:
                logging.error("No valid Python code improvements found in the response.")
            attempt += 1

        return algo_code


class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def get_openai_suggestion(self, code, output):
        prompt = f"Review the following Python code with a fine toothed comb, so to speak, while improving its classes and its output of either productivity and/or more profitable means and/or cheaper costs to run, then provide suggestions for improvement:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nNew Script:"
        system_message = "You are a Debugger that sends a revised python script to another AI"
        user_message = prompt
        # Using the combined method to create the message and get the response in one call
        response = self.openai_handler.get_response_with_message(system_message, user_message)
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
            stdout, stderr = test_process.communicate(timeout=90)
            if stderr:
                self.log_message("Algorithm Testing Failed", stderr, level="error")
                return False, stderr, suggestion

            suggestion = self.get_openai_suggestion(algo_code, stdout)
            self.log_message("Algorithm Testing Success", stdout, level="info")
            return True, stdout, suggestion

        except subprocess.TimeoutExpired:
            timeout_msg = "Algorithm testing timed out.possible reason: User input required"
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
