#!/usr/bin/env python3

import subprocess
import time
import re
import argparse
import sys
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import LangChain modules
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Configure logging
logger = logging.getLogger(__name__)

# Set logging level from environment variable or default to DEBUG
log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
numeric_log_level = getattr(logging, log_level, logging.DEBUG)
logger.setLevel(numeric_log_level)

# Set logging handler
log_handler = os.getenv("LOG_HANDLER", "stream").lower()
if log_handler == "file":
    log_file = os.getenv("LOG_FILE", "app.log")
    handler = logging.FileHandler(log_file)
else:
    handler = logging.StreamHandler()

# Set logging format
log_format = os.getenv("LOG_FORMAT", '%(asctime)s [%(levelname)s] %(message)s')
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_current_branch():
    METHOD_NAME = "get_current_branch"
    logger.debug(f" > {METHOD_NAME}")
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        branch_name = result.stdout.strip()
        logger.debug(f" < {METHOD_NAME} {branch_name}")
        return branch_name
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting current branch: {e.stderr.strip()}")
        sys.exit(1)

def extract_ticket_id(branch_name, prefix_regex):
    METHOD_NAME = "extract_ticket_id"
    logger.debug(f" > {METHOD_NAME} {branch_name} {prefix_regex}")
    match = re.match(prefix_regex, branch_name)
    if match:
        ticket_id = match.group(1)
        logger.debug(f" < {METHOD_NAME} {ticket_id}")
        return ticket_id
    else:
        logger.error("Could not extract ticket ID from branch name.")
        sys.exit(1)

def get_git_diff():
    METHOD_NAME = "get_git_diff"
    logger.debug(f" > {METHOD_NAME}")
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],  # Use '--cached' to get staged changes
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        diff_text = result.stdout.strip()
        logger.debug(f" < {METHOD_NAME} diff length: {len(diff_text)}")
        return diff_text
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting git diff: {e.stderr.strip()}")
        sys.exit(1)

def generate_commit_message(diff_text, model_name):
    METHOD_NAME = "generate_commit_message"
    logger.debug(f" > {METHOD_NAME} diff length: {len(diff_text)}")
    if not diff_text:
        message = "No changes detected."
        logger.debug(f" < {METHOD_NAME} {message}")
        return message
    try:
        # Get OLLAMA_LLM_TEMPERATURE from environment variable or default to 0.0
        temperature = float(os.getenv("OLLAMA_LLM_TEMPERATURE", "0.0"))
        logger.debug(f" >> {METHOD_NAME} model_name: {model_name}, temperature: {temperature}")

        # Get base_url from environment variable or default to "http://localhost:11434"
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        llm = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
        )

        prompt_template = PromptTemplate(
            input_variables=["diff"],
            template="""Please summarize the following code changes into a clear and concise commit message. 
The commit message should accurately reflect the changes made and follow best practices in less that 15 words.

Examples:

- "Fix login issue by correcting variable typo in authentication module"
- "Add unit tests for user registration functionality"
- "Refactor database connection logic for improved performance"
- "Update README with installation instructions"
- "Remove unused import statements and clean up code style"
- "Implement password reset feature via email"
- "Upgrade project to use React 17"

Important: Output ONLY the commit message without any additional text or preamble.'

<CHANGES>
{diff}
</CHANGES>
"""
        )

        chain = LLMChain(llm=llm, prompt=prompt_template)
        inputs = {"diff": diff_text}
        logger.debug(f" >> {METHOD_NAME} inputs: {inputs}")

        result = chain.run(inputs)
        result = result.replace("\"", "")
        
        logger.debug(f" < {METHOD_NAME} {result[:30]}...")
        return result.strip()
    except Exception as e:
        message = f" E ERROR: Unexpected error, caused by: '{e}'."
        logger.error(message)
        raise Exception(message)

def stage_all_changes():
    METHOD_NAME = "stage_all_changes"
    logger.debug(f" > {METHOD_NAME}")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        logger.debug(f" < {METHOD_NAME}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error staging changes: {e.stderr.strip()}")
        sys.exit(1)

def commit_changes(commit_message):
    METHOD_NAME = "commit_changes"
    logger.debug(f" > {METHOD_NAME} {commit_message}")
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        logger.debug(f" < {METHOD_NAME}")
    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr.strip()
        if 'nothing to commit' in stderr_output:
            logger.info("Nothing to commit.")
        else:
            logger.error(f"Error committing changes: {stderr_output}")
            sys.exit(1)

def main():
    METHOD_NAME = "main"
    logger.debug(f" > {METHOD_NAME}")
    parser = argparse.ArgumentParser(description='Periodic Git Commit Script')
    parser.add_argument('period', type=int, nargs='?', default=os.getenv("PERIOD", 60), help='Period in seconds between commits')
    parser.add_argument('--prefix-regex', type=str, default=os.getenv("PREFIX_REGEX", r'(INSTA-\d+)'),
                        help='Regular expression to extract ticket ID from branch name')
    parser.add_argument('--model-name', type=str, default=os.getenv("OLLAMA_LLM_MODEL_NAME", 'llama3.1:8b'),
                        help='Name of the Ollama model to use (default from environment variable or "llama3.1:8b")')
    args = parser.parse_args()

    period = int(args.period)
    prefix_regex = args.prefix_regex
    model_name = args.model_name

    logger.debug(f"Script started with period: {period}, prefix_regex: {prefix_regex}, model_name: {model_name}")

    while True:
        logger.debug(f"Sleeping for {period} seconds")
        time.sleep(period)
        branch_name = get_current_branch()
        ticket_id = extract_ticket_id(branch_name, prefix_regex)
        stage_all_changes()
        diff_text = get_git_diff()
        if not diff_text:
            logger.info("No changes detected. Continuing to next iteration.")
            continue
        commit_message_body = generate_commit_message(diff_text, model_name)
        commit_message = f"[{ticket_id}] {commit_message_body}"
        commit_changes(commit_message)
        logger.info(f"Committed changes with message: {commit_message}")

if __name__ == "__main__":
    main()
