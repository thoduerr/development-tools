# Periodic Git Commit Script

This Python script automates periodic commits to your Git repository, generating meaningful commit messages based on your staged changes using a model from Ollama. It utilizes LangChain's Ollama integration and includes detailed logging for debugging and monitoring purposes.

## Features

- **Periodic Commits**: Automatically commit changes at user-defined intervals.
- **Intelligent Commit Messages**: Uses AI to generate descriptive commit messages based on your staged code changes.
- **Customizable Configuration via Environment Variables**: Configure various aspects of the script using environment variables or a `.env` file.
- **Detailed Logging**: Entry and exit logs for all methods, including parameters and results.

## Requirements

- **Python 3.8+**
- **Git** installed and accessible from the command line.
- **Ollama** installed locally with your desired model.
- **Python Packages**: Install via `pip install -r requirements.txt`

## Installation

### 1. Clone the Repository

```bash
git clone https://your-repo-url.git
cd your-repo
```

### 2. Install Ollama and the Llama Model

#### Install Ollama

Visit the Ollama website and follow the installation instructions for your operating system.

#### Install the Llama Model

Once Ollama is installed, download the model you wish to use, for example:

``` bash
ollama pull llama3.1:8b
```

### 3. Install Python Dependencies
Create a requirements.txt file with the following content:

```text
langchain
langchain-ollama
python-dotenv
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

1. Make the Script Executable
bash
Copy code
chmod +x periodic_git_commit.py
Configuration

You can configure the script using environment variables. You can set these variables directly in your environment or by creating a .env file in the same directory as the script.

Available Environment Variables
LOG_LEVEL: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is DEBUG.
LOG_HANDLER: Set to file to log to a file or stream to log to the console. Default is stream.
LOG_FILE: If LOG_HANDLER is file, set the filename. Default is app.log.
LOG_FORMAT: Set the logging format. Default is '%(asctime)s [%(levelname)s] %(message)s'.
OLLAMA_BASE_URL: Base URL for the Ollama LLM. Default is http://localhost:11434.
TEMPERATURE: Temperature parameter for the LLM. Default is 0.0.
MODEL_NAME: Default model name for the LLM. Default is 'llama3.1:8b'.
PERIOD: Default period in seconds between commits. Default is 3600 (1 hour).
PREFIX_REGEX: Default regular expression to extract the ticket ID from the branch name. Default is '(INSTA-\d+)'.
Example .env File
env
Copy code
# Logging configuration
LOG_LEVEL=INFO
LOG_HANDLER=file
LOG_FILE=commit_script.log
LOG_FORMAT=%(asctime)s %(levelname)s %(message)s

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
TEMPERATURE=0.1
MODEL_NAME=llama2

# Script configuration
PERIOD=1800  # 30 minutes
PREFIX_REGEX=(TASK-\d+)
Usage

Run the script with or without command-line arguments:

bash
Copy code
./periodic_git_commit.py
Command-line arguments override environment variables:

bash
Copy code
./periodic_git_commit.py 3600 --prefix-regex '(FEATURE-\d+)' --model-name 'llama3.1:8b'
Command-Line Arguments
period: (Optional) The time in seconds between commits. Overrides PERIOD environment variable.
--prefix-regex: (Optional) A regular expression to extract the ticket ID from the branch name. Overrides PREFIX_REGEX environment variable.
--model-name: (Optional) The name of the Ollama model to use for generating commit messages. Overrides MODEL_NAME environment variable.
How It Works

Configuration: The script loads configuration from environment variables or a .env file.
Periodically Executes: The script sleeps for the specified period before each execution.
Extracts Ticket ID:
Reads the current Git branch name.
Uses the provided regular expression to extract the ticket ID.
Stages All Changes: Uses git add . to stage all changes.
Generates Commit Message:
Performs a git diff --cached to get the diff of staged changes.
Sends the diff to the specified Ollama model via LangChain's Ollama integration to generate a descriptive commit message.
The prompt template instructs the model to return only the commit message without any additional text or introduction.
Commits Changes:
Commits the staged changes with the message "[<ticket_id>] <generated_message>".
Logging

The script includes detailed logging for each method:

Entry Logs: Display method name and input parameters.
Exit Logs: Display method name and output results (if available).
Error Logs: Capture and display errors with detailed messages.
Logs can be configured to output to the console or a file, with customizable formats and levels.

Example

Suppose you're on branch TASK-123456-fix-bug and have the following .env file:

env
Copy code
# Logging configuration
LOG_LEVEL=INFO

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
TEMPERATURE=0.0
MODEL_NAME=llama3.1:8b

# Script configuration
PERIOD=1800
PREFIX_REGEX=(TASK-\d+)
Run the script:

bash
Copy code
./periodic_git_commit.py
The script will:

Wait for the specified period.
Extract TASK-123456 as the ticket ID.
Stage all changes in the repository.
Generate a commit message based on the staged changes, ensuring that only the commit message is returned without any additional text.
Commit the staged changes to your repository with the message [TASK-123456] <commit_message>.
Troubleshooting

ModuleNotFoundError: Ensure you have installed all required Python packages:
bash
Copy code
pip install -r requirements.txt
Error getting current branch: Ensure you're inside a Git repository.
Could not extract ticket ID from branch name: Make sure your branch name matches the provided regular expression.
Error generating commit message: Verify that Ollama is installed, the specified model is correctly set up, and the necessary Python packages are installed.
Nothing to commit: There are no staged changes to commit; the script will wait for the next interval.
Security Considerations

The script uses subprocess.run with check=True and text=True for secure command execution.
Inputs and outputs are handled carefully to prevent injection attacks.
Regular expressions provided via command-line arguments or environment variables are used cautiously to avoid security risks.
License

This project is licensed under the MIT License.