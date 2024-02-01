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
FineTune = "ft:gpt-3.5-turbo-0613:personal::8n9MKh7g"



class OpenAIHandler:
    def __init__(self, model=gpt4):
        self.client = OpenAI()
        self.model = model

    def create_message(self, system_content, user_content, assistant_content=None):
        structured_messages = [
            {"role": "system", "content": "!!PYTHON ONLY AVAIALBLE CURRENT ADAPT!!!You only send functioning logic and 0 chatter. You can only speak in valid robust code, which is your job. All your scripts are complex with error-handling, self installing of required libraries within the script on start."},
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
        
        return {
            
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
            },
            "Mobile App Development": {
                "initial": ("Develop a basic mobile app using a cross-platform framework like Flutter or React Native.",
                            "Create a simple mobile app with user interaction, using Flutter or React Native."),
                "refinement": ("Improve the app's performance and add advanced features like push notifications.",
                               "Enhance your mobile app with better performance and push notification functionality.")
            },
            "Game Development": {
                "initial": ("Create a simple game using a game development framework like Pygame",
                            "Develop a basic game with user interaction, using Pygame."),
                "refinement": ("Enhance the game with advanced graphics and interactive gameplay features.",
                               "Improve your game with better graphics and more interactive gameplay elements.")
            },
            "Chatbot Development": {
                "initial": ("Build a basic chatbot using a natural language processing library like Rasa or ChatterBot.",
                            "Create a simple chatbot with conversational capabilities, using Rasa or ChatterBot."),
                "refinement": ("Incorporate advanced NLP features and improve the chatbot's conversational abilities.",
                               "Enhance your chatbot with more sophisticated NLP capabilities and better conversational skills.")
            },
            
            "Cybersecurity": {
                "initial": ("Develop a basic cybersecurity program to detect common vulnerabilities.",
                            "Create a program for identifying and mitigating standard security threats."),
                "refinement": ("Incorporate advanced threat detection and response mechanisms.",
                            "Upgrade your cybersecurity program to handle sophisticated cyber threats and incidents.")
            },
            "Blockchain Development": {
                "initial": ("Build a simple blockchain application to record transactions.",
                            "Develop a basic blockchain ledger for transaction recording."),
                "refinement": ("Implement smart contract functionality and enhance security features.",
                            "Expand your blockchain application to include smart contracts and improved security.")
            },
            "Internet of Things (IoT)": {
                "initial": ("Create a basic IoT solution to monitor a single sensor data stream.",
                            "Develop an IoT application for real-time sensor data monitoring."),
                "refinement": ("Enhance the IoT solution with data analytics and remote control capabilities.",
                            "Improve your IoT application to analyze sensor data and support remote operations.")
            },


            "Natural Language Processing (NLP)": {
                "initial": ("Create a basic NLP program for text analysis and sentiment detection.",
                            "Develop a simple NLP application for text analysis and sentiment detection."),
                "refinement": ("Implement advanced NLP techniques like named entity recognition and language translation.",
                            "Enhance your NLP application with more sophisticated language processing capabilities.")
            },
            
            "Cloud Computing": {
                "initial": ("Set up a basic cloud environment for data storage and computing.",
                            "Create a simple cloud-based solution for data handling and processing."),
                "refinement": ("Expand cloud capabilities to include scalable architecture and advanced services.",
                            "Enhance your cloud setup with scalability features and advanced cloud services.")
            }
        

        }

    def develop_algo(self, algo_code=None, error_message=None):
        system_message, user_message = self._generate_messages(algo_code, error_message)
        messages = self.openai_handler.create_message(system_message, user_message)
        response = self.openai_handler.get_response(messages)
        improved_algo_code = CodingUtils.extract_python_code(response)

        
        conversation_history.append({
            "system_message": system_message,
            "user_message": user_message,
            "assistant_message": improved_algo_code if improved_algo_code else "No improvement"
        })

        if improved_algo_code and CodingUtils.is_code_valid("python",improved_algo_code):
            if len(improved_algo_code) > len(algo_code):
                logging.info("AI algorithm improvement found and validated.")
                return improved_algo_code
            else:
                logging.error("No valid Python code improvements found in the response.")
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
        system_message = "Testing algorithm code"
        user_message = algo_code  # The code being tested is the user's 'input' in this context

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
                assistant_message = f"Test Failed: {stderr}"
                conversation_history.append({
                    "system_message": system_message,
                    "user_message": user_message,
                    "assistant_message": assistant_message
                })
                
                return False, stderr, None  # Add a third return value (None) for the suggestion

            suggestion = self.get_openai_suggestion(algo_code, stdout)
            assistant_message = f"Test Succeeded: {stdout}"
            conversation_history.append({
                "system_message": system_message,
                "user_message": user_message,
                "assistant_message": assistant_message
            })
            logging.info(f"Algorithm Testing Success: {stdout}")
            return True, stdout, suggestion
        except subprocess.TimeoutExpired:
            error_message = "Algorithm testing timed out."
            logging.error(error_message)
            assistant_message = f"Test Failed: {error_message}"
            conversation_history.append({
                "system_message": system_message,
                "user_message": user_message,
                "assistant_message": assistant_message
            })
            return False, error_message, None
        except Exception as e:
            error_message = f"Error in testing algorithm: {e}"
            logging.error(error_message)
            assistant_message = f"Test Failed: {error_message}"
            conversation_history.append({
                "system_message": system_message,
                "user_message": user_message,
                "assistant_message": assistant_message
            })
            return False, str(e), None

    def get_openai_suggestion(self, code, output):
        prompt = f"Review the following Python code and its output, then provide suggestions for improvement:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nSuggestions:"
        messages = self.openai_handler.create_message("You are a code debugger", prompt)
        response = self.openai_handler.get_response(messages)
        return response if response else "No suggestions available."






class CodingUtils:
    @staticmethod
    def is_code_valid(code, language):

        if language == "python":
            try:
                ast.parse(code)
                logging.info("Python code validation passed.")
                return True, "No syntax errors detected."
            except SyntaxError as e:
                logging.error(f"Syntax error in Python code: {e}")
                return False, str(e)
        elif language == "javascript":
            try:
                result = subprocess.check_output(["prettier", "--check", code], stderr=subprocess.STDOUT, text=True)
                logging.info("JavaScript code validation passed.")
                return True, "No syntax errors detected."
            except subprocess.CalledProcessError as e:
                logging.error(f"Syntax error in JavaScript code: {e.output}")
                return False, str(e.output)
        elif language == "html":
            # Basic HTML validation logic
            if "<" in code and ">" in code and "</" not in code:
                logging.error("Missing closing HTML tags.")
                return False, "Missing closing HTML tags."
            logging.info("Basic HTML code validation passed.")
            return True, "No obvious syntax errors detected."
        else:
            logging.error("Unsupported language for validation.")
            return False, "Unsupported language."

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
    @staticmethod
    def extract_javascript_code(markdown_text):

        pattern = r"```javascript\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No JavaScript code blocks found.")
            return ""
        return "\n".join(matches).strip()

    @staticmethod
    def format_javascript_code(code):

        try:
            formatted_code = subprocess.check_output(["prettier", "--write", code], stderr=subprocess.STDOUT, text=True)
            return True, formatted_code
        except subprocess.CalledProcessError as e:
            logging.error(f"Error formatting JavaScript code: {e.output}")
            return False, str(e.output)

    @staticmethod
    def extract_html_code(markdown_text):
        
        pattern = r"```html\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No HTML code blocks found.")
            return ""
        return "\n".join(matches).strip()

    @staticmethod
    def format_html_code(code):
        
        formatted_code = code.replace('>', '>\n').replace('<', '\n<')
        return True, formatted_code



class FileManager:
    @staticmethod
    def detect_language(content):
        
        if isinstance(content, list):
            content = '\n'.join(content)  

        first_line = content.split('\n', 1)[0]
        if "#lang=" in first_line:
            return first_line.split('=')[1].strip()
        elif "<!--lang=" in first_line:
            return first_line.split('=')[1].split('-->')[0].strip()
        return "unknown"


    @staticmethod
    def get_file_extension(language):
        # Mapping languages to file extensions
        return {
            "python": ".py",
            "html": ".html",
            "javascript": ".js",
            "css": ".css"
        }.get(language, ".txt")

    @staticmethod
    def save_script(filename, content):
        # Detect language and save file with correct extension
        language = FileManager.detect_language(content)
        extension = FileManager.get_file_extension("python" or language)
        filename_with_extension = f"{filename}{extension}"
        with open(filename_with_extension, 'w') as file:
            file.write(content)
            logging.info(f"Script saved to {filename_with_extension} successfully.")

def save_with_unique_name(base_name, content, file_type):
    # Generate a unique timestamp
    timestamp = int(time.time())
    
    file_name = f"{base_name}_{timestamp}.{file_type}"  

    # Handling different types of content
    if file_type == 'json':
        # Serialize and save JSON content
        with open(file_name, 'w') as file:
            json.dump(content, file)
    else:
        # For other file types, use FileManager to save
        FileManager.save_script(file_name, content)

    return file_name




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_developer = AlgoDeveloper(openai_handler)
    algo_tester = AlgoTester(openai_handler)

    # Number of loops for the entire process
    number_of_loops = 5

    for process_loop in range(number_of_loops):
        initial_script = ""  # Reset the initial script for each loop
        algo_code = initial_script
        max_iterations = 5
        error_message = None
        performance_metrics = {}
        conversation_history = []

        logging.info(f"Starting loop {process_loop + 1} of the iterative improvement process for the AI algorithm.")

        iteration = 0
        while iteration < max_iterations:
            logging.info(f"Iteration {iteration + 1}: Developing and testing the algorithm.")
            conversation_history.append({
                'iteration': iteration,
                'algorithm_code': algo_code,
                'error_message': ''
            })
            algo_code = algo_developer.develop_algo(algo_code, error_message)
            if algo_code:
                test_result, feedback, suggestion = algo_tester.test_algo(algo_code)

                if test_result:
                    logging.info(f"Algorithm successfully tested. Feedback: {feedback}")
                    performance_metrics[iteration] = feedback
                    conversation_history[-1]['feedback'] = feedback
                    iteration += 1
                else:
                    logging.error(f"Algorithm testing failed. Error: {feedback}")
                    error_message = feedback
                    conversation_history[-1]['error'] = feedback

        unique_algo_file = save_with_unique_name(f"final_algo_script_loop_{process_loop + 1}", algo_code, "py")
        unique_convo_file = save_with_unique_name(f"conversation_dataset_loop_{process_loop + 1}", conversation_history, "json")
        print(f"Algorithm script for loop {process_loop + 1} saved as: {unique_algo_file}")
        print(f"Conversation dataset for loop {process_loop + 1} saved as: {unique_convo_file}")

        logging.info(f"Loop {process_loop + 1} of the iterative improvement process completed.")
        logging.info(f"Final performance metrics for loop {process_loop + 1}: {performance_metrics}")

    logging.info("All loops of the iterative improvement process completed.")



