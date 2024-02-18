import subprocess
import logging
import sys
import time
import ast
import re
import json
import requests
from openai import OpenAI
import black

# Configuration
idea = "create a video creation factory using AI"
gpt_models = {
    "gpt4": "gpt-4-0125-preview",
    "gpt3": "gpt-3.5-turbo-0125",
    "ft3": "ft:gpt-3.5-turbo-1106:personal::8tGk0TIP"
}

def search(idea):
    """Simulate searching for an idea."""
    try:
        search_results = requests.get(f"https://www.google.com/search?q=\"{idea}\"").json()
        return search_results
    except Exception as e:
        logging.error(f"Search failed: {e}")
        return {}

class OpenAIHandler:
    def __init__(self, model=gpt_models["gpt3"]):
        self.client = OpenAI()
        self.model = model

    def get_response_with_message(self, system_content, user_content, assistant_content=None):
        """Generate a response from OpenAI based on the given content."""
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        if assistant_content:
            messages.append({"role": "assistant", "content": assistant_content})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0.5,
                messages=messages
            )
            response_content = completion.choices[0].message.content
            # Clean the response content
            cleaned_content = self.clean_code(response_content)
            return True, cleaned_content
        except Exception as e:
            logging.error(f"OpenAIHandler error: {e}")
            return False, "Failed to get a response from OpenAI."

    def clean_code(self, code):
        """Remove comments and 'pass' placeholders from the code."""
        cleaned_lines = []
        for line in code.split('\n'):
            if not line.strip().startswith("#") and 'pass' not in line:
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

class AlgoTester:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler

    def test_algo(self, algo_code):
        """Test a given algorithm code and provide feedback."""
        try:
            process = subprocess.Popen(
                [sys.executable, "-c", algo_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=15)
            if stderr:
                return False, stderr
            return True, stdout
        except subprocess.TimeoutExpired:
            return False, "Timeout during execution."
        except Exception as e:
            return False, f"Testing error: {e}"

class AlgoDeveloper:
    def __init__(self, openai_handler, algo_tester):
        self.openai_handler = openai_handler
        self.algo_tester = algo_tester

    def develop_algo(self, algo_code=None):
        """Develop an algorithm with iterative refinement based on testing feedback."""
        system_content = "System request for algorithm development."
        user_content = f"Idea: {idea}. Develop an initial algorithm."

        if not algo_code:
            success, response = self.openai_handler.get_response_with_message(system_content, user_content)
            if success:
                algo_code = response
            else:
                logging.error("Failed to generate initial algorithm.")
                return None

        for iteration in range(5):  # Limited number of iterations for refinement
            success, feedback = self.algo_tester.test_algo(algo_code)
            if success:
                logging.info("Algorithm passed testing.")
                break
            else:
                # Refine based on feedback
                logging.info(f"Refining based on feedback: {feedback}")
                _, algo_code = self.openai_handler.get_response_with_message(system_content, feedback, algo_code)

        return algo_code

def main():
    logging.basicConfig(level=logging.INFO)
    openai_handler = OpenAIHandler()
    algo_tester = AlgoTester(openai_handler)
    algo_developer = AlgoDeveloper(openai_handler, algo_tester)

    algo_code = ""
    for iteration in range(10):  # Example iteration count for development
        logging.info(f"Iteration {iteration+1}: Algorithm development cycle.")
        algo_code = algo_developer.develop_algo(algo_code)
        if algo_code is None:
            logging.error("Stopping due to a critical failure in algorithm development.")
            break

        # Example: Save the current version of the algorithm
        logging.info("Algorithm development successful for this iteration.")

    logging.info("Algorithm development process completed.")

if __name__ == "__main__":
    main()
