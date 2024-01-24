import logging
import time
from openai import OpenAI
import json

class OpenAIHandler:
    """
    A handler class for interacting with OpenAI's API.
    
    Attributes:
        client (OpenAI): The OpenAI client.
        model (str): The model to use for generating responses.
        delay (int): The delay between API calls to throttle requests.
    """
    
    def __init__(self, api_key, model, delay=10):
        """
        The constructor for OpenAIHandler class.
        
        Parameters:
            api_key (str): The API key for authenticating with the OpenAI API.
            model (str): The model to use for generating responses.
            delay (int): The delay between API calls to throttle requests.
        """
        self.client = OpenAI() 
        self.model = model
        self.delay = delay

    def create_message(self, system_content, user_content, assistant_content=None):
        """
        Create structured messages for the OpenAI API.
        
        Parameters:
            system_content (str): The content for the system's role in the conversation.
            user_content (str): The content for the user's role in the conversation.
            assistant_content (str, optional): The content for the assistant's role in the conversation.
            
        Returns:
            list: A list of structured messages.
        """
        structured_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        if assistant_content:
            structured_messages.append({"role": "assistant", "content": assistant_content})
        return structured_messages

    def get_response(self, messages):
        """
        Get a response from the OpenAI API based on the input messages.
        
        Parameters:
            messages (list): A list of structured messages.
            
        Returns:
            str: The response content from the OpenAI API.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            response_content = completion.choices[0].message.content
            logging.info(f"OpenAI Response Received: {response_content}")
            time.sleep(self.delay)
            return response_content
        except Exception as e:
            logging.error(f"Failed to get response from OpenAI: {e}")
            return None
