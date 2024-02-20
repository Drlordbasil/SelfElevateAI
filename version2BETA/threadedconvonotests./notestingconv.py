import time
from openai import OpenAI
import threading
import logging
import pyttsx3
import re
import ast
import black
import subprocess
import json
engine = pyttsx3.init()
engine.setProperty('rate', 130)
engine.say("I will speak this text")
# Initialize logging
gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"
ft3 = "ft:gpt-3.5-turbo-1106:personal::8uLu2E19"
model = gpt3
smartmodel = gpt4
logging.basicConfig(level=logging.INFO)
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
            
            formatted_code = black.format_str(code, mode=black.FileMode())
            return True, formatted_code
        except Exception as e:
            logging.error(f"Error formatting Python code: {e}")
            return False, str(e)
class ConversationManager:
    def __init__(self):
        
        self.conversation_memory = []
        self.client = OpenAI()
    def gen_openai(self, prompt):
        system_message = """
        You are a superintelligent AI model designed to interact with another AI model with the same capabilities as you. You will dicuss how to improve python programs and always include robust logic
"""
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Response must inlcude full robust python code."+prompt}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def gen_summary(self, prompt):
        system_message = """You are a superintelligent AI model designed to interact with another AI model with the same capabilities as you. You will dicuss how to improve python programs and always include robust logic"""
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Response must inlcude full robust python code."+prompt}
            ]
        )
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        print(response.choices[0].message.content)
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        return response.choices[0].message.content
    
    def gen_fred(self, prompt):
        system_message = """ 
        Your role is to provide prompts that are sufficiently clear, concise, and direct to ensure a response from another AI model.
        Response must inlcude full robust python code.
        The objective is to engage in a coherent and meaningful dialogue where both AI models contribute to the conversation. when you code, ensure '''python <code> ''' format for easy code extraction purpose, make sure to include a header in each file like # main.py with the name of the file. IMPORTANT: if you are done, just say quit."""
        
        response = self.client.chat.completions.create(
            model=smartmodel,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt+"Response must inlcude full robust python code."}
            ]
        )
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        print(response.choices[0].message.content)
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        return response.choices[0].message.content
        
    def openai_thread(self):
        while True:
            gpt4all_done.wait(timeout=120)  # Wait up to 120 seconds for GPT4All
            gpt4all_done.clear()
            
            prompt = self.conversation_memory[-1] if self.conversation_memory else "Starting the conversation."
            summary = self.gen_summary(prompt)
            engine.say(summary)           
            if prompt.strip():  # Ensure prompt is not empty
                response = self.gen_openai(prompt)


                logging.info(f"OpenAI: {response}")
                self.conversation_memory.append('response from Jeff:'+response)
                
                openai_done.set()
                if response.lower() == 'quit':
                    break
            else:
                logging.warning("Waiting for a valid response from GPT4All...")
    
    def fred_thread(self):
        while True:
            openai_done.wait()
            openai_done.clear()
            
            last_openai_message = self.conversation_memory[-1] if self.conversation_memory else "Starting the conversation."
            prompt = f"{last_openai_message}\n\nYour task is to comprehend the context and provide an elaborate response that addresses the user's query in detail. Please ensure that your reply is both accurate and informative. when you code, ensure '''python <code> ''' format for easy code extraction purpose, make sure to include a header in each file like # main.py with the name of the file."
            
            response = self.gen_fred(prompt)
            summary = self.gen_summary(response)
            engine.say(summary)
            time.sleep(10)
            if response.strip():  # Ensure response is not empty
                logging.info(f"Jeff: {response}")
                self.conversation_memory.append('Response from Jeff:'+response)
                code = CodingUtils.extract_python_code(response)
                if code:
                    is_valid = CodingUtils.is_code_valid(code)
                    if is_valid:
                        success, formatted_code = CodingUtils.format_python_code(code)
                        if success:
                            logging.info("Python code formatting successful.")
                            save_path = "main.py"
                            with open(save_path, "w") as file:
                                file.write(formatted_code)
                            print("python file saved as main.py")

                            #subprocess.run(["python", "main.py"])
                            #logging.info(f"Formatted Python code:\n{formatted_code}")
                        else:
                            logging.error(f"Failed to format Python code: {formatted_code}")
                    else:
                        logging.error("Invalid Python code detected. Skipping formatting.")
                gpt4all_done.set()
                
            else:
                logging.warning("GPT4All did not generate a valid response. Retrying...")
                
            
            if response.lower() == 'quit':
                break

# Synchronization Events
openai_done = threading.Event()
gpt4all_done = threading.Event()

# Initialize ConversationManager and threads
manager = ConversationManager()
thread1 = threading.Thread(target=manager.openai_thread)
thread2 = threading.Thread(target=manager.fred_thread)

# Initial prompt
initial_prompt = """
Let us create a new algorithm in python(never created and useful while being creative and helpful in real human life or health extending.
 We can use this template as our skeleton start without any meaningful code to actually just use as a structure only:
```python
class example_class:
<docstrings>
    def __init__(self):
    <actual logic>
    return 0

    def sample(self):
    <actual logic>
    return 0
```
"""
manager.conversation_memory.append(initial_prompt)
gpt4all_done.set()

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
