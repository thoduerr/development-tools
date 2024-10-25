# Periodic Git Commit Script

This Python script automates periodic commits to your Git repository, generating meaningful commit messages based on your changes using the `llama3.1-8b` model from Ollama.

## Features

- **Periodic Commits**: Automatically commit changes at user-defined intervals.
- **Intelligent Commit Messages**: Uses AI to generate descriptive commit messages based on your code changes.
- **Customizable Ticket ID Extraction**: Optionally specify a regular expression to extract the ticket ID from your branch name.

## Requirements

- **Python 3.6+**
- **Git** installed and accessible from the command line.
- **Ollama** installed locally with the `llama3.1-8b` model.

## Installation

### 1. Clone the Repository

```bash
git clone https://your-repo-url.git
cd your-repo
```

### 2. Install Ollama and the Llama Model

Install Ollama

Visit the Ollama website and follow the installation instructions for your operating system.

Install the Llama Model

Once Ollama is installed, download the llama3.1-8b model:

```bash
ollama pull llama3.1-8b
```

### 3. Make the Script Executable

```bash
chmod +x periodic_git_commit.py
```

## Usage

Run the script with the desired period (in seconds) between commits:

```bash
./periodic_git_commit.py 3600
```

Optionally, you can provide a custom prefix regular expression:

```bash
./periodic_git_commit.py 3600 --prefix-regex '(FEATURE-\d+)'
```

### Command-Line Arguments

- period: (Required) The time in seconds between commits.
- --prefix-regex: (Optional) A regular expression to extract the ticket ID from the branch name. The default is `'(INSTA-\d+)'`.

## How It Works

1. Periodically Executes:

   - The script sleeps for the specified period before each execution.

2. Extracts Ticket ID:

   - Reads the current Git branch name.
   - Uses the provided regular expression to extract the ticket ID.

3. Generates Commit Message:

   - Stages all changes using git add ..
   - Performs a git diff --staged to get the changes.
   - Sends the diff to the llama3.1-8b model via Ollama to generate a descriptive commit message.

4. Commits Changes:

   - Commits the changes with the message "[<ticket_id>] <generated_message>".

## Branch Naming Convention

By default, the script expects the branch name to start with `INSTA-<number>`, for example:

- INSTA-1234-new-feature
- INSTA-5678-bug-fix
-

If your project uses a different naming convention, you can specify a custom regular expression using the `--prefix-regex` argument.

## Example

Suppose you're on branch FEATURE-789-add-payment-processing and use the following command:

```bash
./periodic_git_commit.py 3600 --prefix-regex '(FEATURE-\d+)'
```

The script will:

1. Wait for the specified period.
2. Extract FEATURE-789 as the ticket ID.
3. Generate a commit message like [FEATURE-789] Implemented payment gateway integration.
4. Commit the changes to your repository.

## Troubleshooting

Error getting current branch: Ensure you're inside a Git repository.
Could not extract ticket ID from branch name: Make sure your branch name matches the provided regular expression.
Error generating commit message: Verify that Ollama is installed and the llama3.1-8b model is correctly set up.
Nothing to commit: There are no staged changes to commit; the script will wait for the next interval.

## Security Considerations

The script uses subprocess.run with check=True and text=True for secure command execution.
Inputs and outputs are handled carefully to prevent injection attacks.
Regular expressions provided via command-line arguments are used cautiously to avoid security risks.

## License

This project is licensed under the MIT License.
