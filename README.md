# AI Algorithm Development and Testing Framework

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
