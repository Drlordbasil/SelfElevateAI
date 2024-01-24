import logging
from OpenAIHandler import OpenAIHandler

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Initialize the OpenAIHandler with your API key and preferred model
    api_key = 'your-api-key-here'  # Replace with your actual API key
    model = 'gpt-3.5-turbo-1106'  # Replace with your actual model
    openai_handler = OpenAIHandler(api_key, model)

    # Create a message
    system_content = 'Your system message here'
    user_content = 'Your user message here'
    assistant_content = 'Your assistant message here (optional)'
    messages = openai_handler.create_message(system_content, user_content, assistant_content)

    # Get a response from the OpenAI API
    response = openai_handler.get_response(messages)
    if response:
        logging.info(f"Received response: {response}")
    else:
        logging.error("Failed to receive a response.")

if __name__ == '__main__':
    main()
