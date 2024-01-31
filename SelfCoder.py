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
                return algo_code  # revert to the previous best iteration
        else:
            logging.error("No valid Python code improvements found in the response.")
            return algo_code

    def _generate_messages(self, algo_code, error_message):
        if not algo_code:
            system_message = (
                "Create an AI model using mathematical principles, neural networks (NN), OR Proximal Policy Optimization/Reinforcement Learning (PPO/RL). "
                "Structure the model with distinct classes for each core functionality, aiming for a total of approximately 10 classes. "
                "Ensure the model embodies a concrete purpose and aligns with the concept of a evolving AI capable of adaptive learning within the Python ecosystem. "
                "The code should be free from pseudocode, inline commentary, and placeholders."
            )
            user_message = (
                "Construct a foundational, adaptable AI entity akin to a 'stem cell'. "
                "Utilize math-based AI principles, integrating NN and PPO/RL techniques. "
                "Develop a clean, well-structured codebase with individual classes for distinct functionalities, avoiding any form of inline commentary or placeholders. "
                "Focus on creating a practical, purpose-driven model. only send valid code, no chat. Only send code."
            )
        else:
            system_message = (
                "Refine the AI model by integrating real, qualitative data sources. "
                "Continuously enhance the model by incrementally enriching the dataset in each iteration. "
                "Avoid the use of fictitious or illustrative data. Make fully dynamic variables for the model. "
                "Focus on enhancing the model's ability to preserve and retrieve its state effectively, ensuring a logical, result-oriented output. "
                "Address any existing issues in the model, especially in error management and maintaining a cohesive main loop for operational consistency. "
                "Refine the model further by removing any placeholders or inline notes, and by ensuring the logic is comprehensive and fully articulated."
            )
            user_message = (
                "Enhance the AI model by infusing it with authentic, quality data sources, incrementally improving with each iteration. "
                "Implement robust mechanisms for model preservation and state retrieval, focusing on generating genuine, logical results. "
                "Review the current model structure, ensuring sophisticated error management and a cohesive main loop are in place for smooth operation. "
                f"Address the listed issues ({error_message}), improving debugging visibility if necessary. "
                "Direct efforts towards refining the model by eliminating placeholders, avoiding inline notes, and ensuring the logic is comprehensive, well-articulated, and never truncated. "
                "Remember, the program you create is akin to your child, so nurture and refine it with care and attention to detail."
            )
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
                return False, stderr

            suggestion = self.get_openai_suggestion(algo_code, stdout)
            logging.info(f"Algorithm Testing Success: {stdout}")
            return True, stdout, suggestion
        except subprocess.TimeoutExpired:
            logging.error("Algorithm testing timed out.")
            return False, "Algorithm testing timed out.", None
        except Exception as e:
            logging.error(f"Error in testing algorithm: {e}")
            return False, str(e), None

    def get_openai_suggestion(self, code, output):
        prompt = f"Review the following Python code and its output, then provide suggestions for improvement:\n\nCode:\n{code}\n\nOutput:\n{output}\n\nSuggestions:"
        response = self.openai_handler.make_api_call(prompt)
        return response if response else "No suggestions available."


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
            logging.error("Failed to develop a valid algorithm. Stopping the iterative process.")
            break

    FileManager.save_script('final_algo_script.py', algo_code)
    FileManager.save_conversation_dataset('conversation_dataset.json', conversation_history)
    logging.info("Iterative improvement process completed.")
    logging.info(f"Final performance metrics: {performance_metrics}")


