import random
import subprocess
import logging
import sys
import time
import ast
import re
import json
from openai import OpenAI
import tkinter as tk
gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"

def submit():
    selected_model = model_var.get()
    # Perform actions based on the selected model
    print("Selected Model:", selected_model)


    root = tk.Tk()
    root.title("Model Selection")

    # Variable Definitions
    gpt4 = gpt4
    gpt3 = gpt3

    # Create a drop-down menu
    model_var = tk.StringVar(root)
    model_var.set(gpt4)  # Set the default value

    model_label = tk.Label(root, text="Select Model:")
    model_label.pack()

    model_dropdown = tk.OptionMenu(root, model_var, gpt4, gpt3)
    model_dropdown.pack()

    # Create a submit button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    root.mainloop()
    return selected_model,gpt4,gpt3


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
        self.categories = self._init_categories()

    def _init_categories(self):
        # Define top 5 Python categories and their prompts
        return {
            "Web Development": {
                "initial": ("Create a basic web application using Flask or Django. Include routes, views, and templates.",
                            "Develop a simple web app with user interaction, using Flask/Django."),
                "refinement": ("Improve the web app's performance and user interface.",
                               "Enhance your web app's UI/UX and optimize backend performance.")
            },
            "Data Science": {
                "initial": ("Develop a data analysis script using pandas and numpy. Include data cleaning and basic analysis functions.",
                            "Write a Python script for data cleaning and analysis using pandas."),
                "refinement": ("Implement advanced data visualization and statistical analysis techniques.",
                               "Expand your data script to include sophisticated visualization and deeper statistical insights.")
            },
            "Machine Learning": {
                "initial": ("Create a machine learning model using scikit-learn. Start with data preprocessing and a simple model.",
                            "Build a basic ML model with scikit-learn, focusing on preprocessing and model training."),
                "refinement": ("Enhance the ML model's accuracy and efficiency. Experiment with different algorithms.",
                               "Improve your ML model's performance by experimenting with various algorithms and tuning.")
            },
            "Automation": {
                "initial": ("Develop a script to automate a routine task, such as file organization or web scraping.",
                            "Write a Python script to automate a daily task, like organizing files or scraping web data."),
                "refinement": ("Optimize the automation script for efficiency and error handling.",
                               "Refine your automation script to handle errors gracefully and run more efficiently.")
            },
            "API Development": {
                "initial": ("Build a RESTful API using Flask-RESTful or Django REST framework.",
                            "Create a REST API for a simple application, using Flask or Django."),
                "refinement": ("Enhance API security and implement rate limiting and data caching.",
                               "Improve your API with security features, rate limiting, and caching mechanisms.")
            }
        }

    def develop_algo(self, algo_code=None, error_message=None):
        system_message, user_message = self._generate_messages(algo_code, error_message)
        messages = self.openai_handler.create_message(system_message, user_message)
        response = self.openai_handler.get_response(messages)
        improved_algo_code = CodingUtils.extract_python_code(response)
        if improved_algo_code and CodingUtils.is_code_valid(improved_algo_code):
            if len(improved_algo_code) > len(algo_code):
                logging.info("AI algorithm improvement found and validated.")
                return improved_algo_code
            else:
                logging.error("No valid Python code improvements found in the response.")
                return algo_code
        else:
            logging.error("No valid Python code improvements found in the response.")
            return algo_code

    def _generate_messages(self, algo_code, error_message):
        category_key = random.choice(list(self.categories.keys()))
        category = self.categories[category_key]

        message_type = "initial" if not algo_code else "refinement"
        system_message, user_message = category[message_type]

        if message_type == "refinement":
            user_message = user_message.format(error_message=error_message)

        return system_message, user_message



class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def test_algo(self, algo_code):
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
                return False, stderr, None  # Add a third return value (None) for the suggestion

            suggestion = self.get_openai_suggestion(algo_code, stdout)
            logging.info(f"Algorithm Testing Success: {stdout}")
            return True, stdout, suggestion
        except subprocess.TimeoutExpired:
            logging.error("Algorithm testing timed out.")
            return False, "Algorithm testing timed out.", None
        except Exception as e:
            logging.error(f"Error in testing algorithm: {e}")
            return False, str(e), None  # Make sure to return three values here too


    def get_openai_suggestion(self, code, output):
        prompt = f"Review the following Python code and its output, then provide suggestions for improvement:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nSuggestions:"
        response = self.openai_handler.make_api_call(prompt)
        return response if response else "No suggestions available."


class AdaptiveCodeGenerator:
    def __init__(self, openai_handler, epochs=10):
        self.openai_handler = openai_handler
        self.epochs = epochs
        self.successful_prompts = []
        self.unsuccessful_prompts = []
        self.learning_rate = 0.1

    def train(self):
        for epoch in range(self.epochs):
            chosen_prompt = self.choose_prompt_strategy()
            if chosen_prompt:
                response = self.generate_code(chosen_prompt)
                success = self.evaluate_success(response)
                self.provide_feedback(chosen_prompt, success)
                self.adjust_learning_rate(epoch)

    def generate_code(self, prompt):
        generated_code = self.openai_handler.make_api_call(prompt)
        return generated_code

    def provide_feedback(self, prompt, success):
        if success:
            self.successful_prompts.append(prompt)
        else:
            self.unsuccessful_prompts.append(prompt)

    def choose_prompt_strategy(self):
        if self.successful_prompts and random.random() < self.learning_rate:
            return random.choice(self.successful_prompts)
        elif self.unsuccessful_prompts:
            return random.choice(self.unsuccessful_prompts)
        return None

    def adjust_learning_rate(self, epoch):
        self.learning_rate += (1 / self.epochs) * (0.5 - random.random())

    def evaluate_success(self, code):
        try:
            ast.parse(code) if ast.parse(code) else True    

            return True
        except SyntaxError:
            return False



class CodingUtils:
    @staticmethod
    def is_code_valid(code):
        # Enhanced logic for code validation
        try:
            ast.parse(code)
            logging.info("Python code validation passed.")
            return True, "No syntax errors detected."
        except SyntaxError as e:
            logging.error(f"Syntax error in the generated code: {e}")
            return False, str(e)

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
        return python_code_blocks[0]

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
                # Format the entry for fine-tuning
                formatted_entry = {
                    "messages": [
                        {"role": "system", "content": entry.get("system_message", "")},
                        {"role": "user", "content": entry.get("user_message", "")},
                        {"role": "assistant", "content": entry.get("assistant_message", "")}
                    ]
                }
                file.write(json.dumps(formatted_entry) + '\n')
            logging.info(f"Conversation history saved to {filename} successfully.")
def save_with_unique_name(base_name, content, file_type):
    # Generate a unique timestamp
    timestamp = int(time.time())
    # Create a unique file name
    file_name = f"{base_name}_{timestamp}.{file_type}"
    # Save the file using FileManager
    if file_type == 'py':
        FileManager.save_script(file_name, content)
    elif file_type == 'json':
        FileManager.save_conversation_dataset(file_name, content)
    else:
        raise ValueError("Unsupported file type")
    return file_name
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_developer = AlgoDeveloper(openai_handler)
    algo_tester = AlgoTester(openai_handler)
    adaptive_generator = AdaptiveCodeGenerator(openai_handler)
    initial_script = ""
    algo_code = initial_script
    max_iterations = 5
    error_message = None
    performance_metrics = {}
    conversation_history = []

    logging.info("Starting the iterative improvement process for the AI algorithm.")
    for iteration in range(max_iterations):
        logging.info(f"Iteration {iteration + 1}: Developing and testing the algorithm.")
        conversation_history.append({
            'iteration': iteration,
            'algorithm_code': algo_code,
            'error_message': error_message
        })
        algo_code = algo_developer.develop_algo(algo_code, error_message)
        if algo_code:
            test_result, feedback, suggestion = algo_tester.test_algo(algo_code)

            if test_result:
                logging.info(f"Algorithm successfully tested. Feedback: {feedback}")
                performance_metrics[iteration] = feedback
                conversation_history[-1]['feedback'] = feedback
                #adaptive_generator.train()
            else:
                logging.error(f"Algorithm testing failed. Error: {feedback}")
                error_message = feedback
                conversation_history[-1]['error'] = feedback
        else:
            logging.error("Failed to develop a valid algorithm. Stopping the iterative process.")
            break
    
    unique_algo_file = save_with_unique_name("final_algo_script", algo_code, "py")
    unique_convo_file = save_with_unique_name("conversation_dataset", conversation_history, "json")
    print(f"Algorithm script saved as: {unique_algo_file}")
    print(f"Conversation dataset saved as: {unique_convo_file}")
    logging.info("Iterative improvement process completed.")
    logging.info(f"Final performance metrics: {performance_metrics}")


