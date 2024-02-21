import subprocess
import tempfile
import os
import logging
from openai import OpenAI
import ast



logging.basicConfig(level=logging.INFO)


gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"
ft3 = "ft:gpt-3.5-turbo-1106:personal::8uLu2E19"
model = gpt3
smartmodel = gpt4
idea_prompt = """
Generate a profitable Python program idea with zero startup and upkeep costs that can be developed in 1 file. 
The program should be able to run on any computer with Python installed and should make profit in a reasonable amount of time. 
use openai calls to create complex outputs that are not easily understood by humans but provide valuable profitable outputs.
we need to make an autonomous agent specefic to a certain niche that can output profitable content.
We need to use this to describe the new openai api calls:
from openai import OpenAI

    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI() # never add api_key here
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content
make sure your idea is robust and profitable. If I can sell the output content such as programs it creates or content like full chapterbooks to sell online or anything else like that.
"""
code_prompt = """
Develop Python code for the following idea. Please note, do not include placeholders such as 'pass' in the Python code. The code should follow this structure:

```python
# Import necessary libraries
import os
import sys

# Define necessary classes
class MyClass:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def method1(self):
        # Implement method1
        pass

    def method2(self):
        # Implement method2
        pass

# Define main function
def main():
    # Create an instance of MyClass
    my_class = MyClass('param1', 'param2')

    # Call methods of MyClass
    my_class.method1()
    my_class.method2()

# Call the main function
if __name__ == "__main__":
    main()
```
proper openai calls that you cant change if using openai:
from openai import OpenAI
    gpt4 = "gpt-4-0125-preview"
    gpt3 = "gpt-3.5-turbo-0125" # good model for testing purposes.
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI() # never add api_key here
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content
never change these openai core functions(they are even case-sensative, dont include models I didnt list) while improving the programs extended functionalities for automation of content creation. All outputs from your program must directly profit with content creation or other means of profit where the user can sell the output like program code, stories, images, ect.
"""
class CodeExecutor:
    '''
    Class to execute Python code and return the output.
    This class is used to execute Python code and return the output. It uses the subprocess module to run the code in a separate process and capture the output. 
    The code is written to a temporary file and then executed using the Python interpreter. 
    The output is then returned to the caller. If there is an error, an exception is raised and the error message is returned.
    The temporary file is then deleted.
    the flow of the code is as follows:
    1. Write the code to a temporary file
    2. Execute the code using the Python interpreter
    3. Capture the output and return it to the caller
    4. If there is an error, raise an exception and return the error message
    5. Delete the temporary file
    
    '''
    @staticmethod
    def execute_python_code(code, input_simulation=""):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode())
            tmp_name = tmp.name
        try:
            result = subprocess.run(['python', tmp_name], input=input_simulation.encode(), capture_output=True, text=True, timeout=30)
            output = result.stdout
            error = result.stderr
            if error:
                raise Exception(error)
            return output
        except Exception as e:
            return f"Error executing Python code: {e}"
        finally:
            os.remove(tmp_name)
    def save_code(self, code, filename):
        with open(filename, "w") as file:
            file.write(code)    
        print(f"Code saved to {filename}")
    def read_code(self, filename):
        with open(filename, "r") as file:
            code = file.read()
        print(f"Code read from {filename}")
        return code
    def execute_code(self, code, input_simulation=""):
        result = subprocess.run(['python', code], input=input_simulation.encode(), capture_output=True, text=True, timeout=30)
        output = result.stdout
        error = result.stderr
        if error:
            raise Exception(error)
        return output

    

class ConversationManager:
    '''
    this class is used to manage the conversation and development process.
    It uses the OpenAI API to generate responses and execute the code.
    The conversation is managed in a loop, with the initial idea generation, code development, and iterative refinement.
    steps in process are:
    1. Initial idea generation
    2. Development of the project
    3. Iterative refinement and completion check
    4. Execute and test the generated code
    5. Further refine the code based on feedback
    6. Finalize the project
    7. Output the final project code
    8. Log the conversation and development process

    '''
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI()
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content

    def extract_valid_python_code(self, response):
        """Extracts valid Python code from the response."""
        try:
            ast.parse(response)
            return response
        except SyntaxError:
            return ""

    def iterate_development(self):
        self.project_idea = self.generate_response(smartmodel, idea_prompt, "Generating extremely real profitable project idea that an LLM can create in one response...")
        self.project_code = self.generate_response(smartmodel, code_prompt+f"{self.project_idea}", "Developing project code(full robust verbose complex logic without placeholders)...I am a python programming superstar")
        
        completion = "no"
        iteration = 0
        while completion == "no":
            execution_result = CodeExecutor.execute_python_code(self.project_code)
            feedback = self.generate_response(smartmodel, f"Execution result: {execution_result}\nIs the program complete and profitable either directly or indirectly using the original idea of {self.project_idea}? Answer yes or no.", "Evaluating program completion...")
            
            if "yes" in feedback.lower():
                CodeExecutor.save_code(self.project_code, f"project_{iteration}.py")
                completion = "yes"
                logging.info("Project deemed complete and potentially profitable.")
            else:
                # Further refine the code based on feedback
                CodeExecutor.save_code(self.project_code, f"project_{iteration}.py")
                refined_code = self.generate_response(smartmodel, f"Refine the Python code to ensure profitability and completion.{self.project_code} as it was rejected by another AI", "Refining project code to meet acedemic standards and beyond...")
                valid_code = self.extract_valid_python_code(refined_code)
                if valid_code:
                    self.project_code = valid_code
                    CodeExecutor.save_code(self.project_code, f"project_{iteration}.py")
                    print(f"Refined code saved to project_{iteration}.py")
                    iteration += 1
    def conversation_thread(self):
        self.iterate_development()
        if self.project_code:
            logging.info("Final Project Code:\n" + self.project_code)
        else:
            logging.warning("Failed to develop a profitable project.")

# Initialize ConversationManager
manager = ConversationManager()

# Run the development process
manager.conversation_thread()
