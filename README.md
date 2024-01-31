# AI Algorithm Development and Testing Framework
![image](https://github.com/Drlordbasil/SelfImprovAlgoBot/assets/126736516/b2a167a2-e887-49aa-9ba6-49097f45117b)

![image](https://github.com/Drlordbasil/SelfImprovAlgoBot/assets/126736516/2529ab29-3dbb-4057-8453-4c97be6097aa)

![image](https://github.com/Drlordbasil/SelfImprovAlgoBot/assets/126736516/cf868c65-42a9-4f72-8aa3-88832d9d4d4b)


## Overview
This project presents an automated framework for the development, testing, and improvement of AI algorithms using OpenAI's GPT models. It's designed to iteratively develop and refine AI algorithms based on feedback and error analysis.

## Features
- **Automated Algorithm Development**: Utilizes OpenAI's GPT models for generating and improving AI algorithms.
- **Dynamic Testing**: Employs subprocesses to test the algorithms and capture output and errors.
- **Error Handling and Logging**: Comprehensive logging and error handling for tracking the development process.
- **Performance Metrics**: Collection and logging of performance metrics for each iteration.
- **Data Storage**: Saves the final algorithm and conversation history for review and further use.

## Components
1. **OpenAIHandler**: Manages interactions with the OpenAI API for algorithm generation and improvement.
2. **AlgoDeveloper**: Develops and refines algorithms based on current code and feedback.
3. **AlgoTester**: Tests algorithms and captures feedback.
4. **CodingUtils**: Validates Python code and extracts code blocks from text.
5. **FileManager**: Handles file operations, saving scripts and conversation data.

## Usage
To use this framework:
1. Set up your environment with necessary OpenAI API keys.
2. Run the main script to start the iterative development and testing process.
3. Review the saved algorithm and conversation history for insights.

## Requirements
- Python
- OpenAI API key
- Subprocess and Logging modules

## Installation
Clone the repository and install the required dependencies.

```bash
git clone https://github.com/Drlordbasil/SelfImprovAlgoBot/
cd your-repository
pip install -r requirements.txt
