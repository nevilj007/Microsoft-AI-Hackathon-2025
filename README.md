

---

# BuildBot: Zero-Cost CI/CD Assistant

BuildBot is a lightweight AI-powered assistant designed to integrate with GitHub Actions. It helps automate build triggering, status monitoring, and log summarization with zero cost, making your CI/CD workflows smarter and faster -all for $0 !. 

## Features:
- **Trigger workflows** on GitHub via AI-based commands.
- **Monitor GitHub Actions build status** and receive detailed feedback.
- **Summarize CI/CD logs** using AI to identify errors and suggest actionable fixes.
- **Seamlessly integrate** with your existing GitHub repository and workflows.

## Requirements

### Prerequisites:
- GitHub repository with Actions set up.
- GitHub Personal Access Token (PAT) with required permissions.
- Python 3.8 or above.
- Required permissions in the workflow for auto dispatch in GitHub:

```yaml
on:
  workflow_dispatch:
    inputs:
      tag:
        description: "Docker image tag"
        required: false
        default: "latest"
```



## Setup

### 1. Clone the repository

Clone this repository to your local machine into your project directory for eg:buildbot :

```bash
git clone https://github.com/nevilj007/Microsoft-AI-Hackathon-2025.git
```

### 2. Set up a virtual environment

Navigate to the project directory and set up a virtual environment:

```bash
cd buildbot
python3 -m venv venv
```

Activate the virtual environment:

#### On Windows:
```bash
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up GitHub API token

Create a `secrets.env` file in the `config/` directory with the following content:

```bash
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your_github_username/repo_name
```

Replace `your_github_personal_access_token` with your GitHub token and `your_github_username/repo_name` with your GitHub repository details.

### 5. Run DeepSeek-Coder Model

Ensure the `deepseek-coder:6.7b-instruct` model from Ollama is running:

```bash
ollama run deepseek-coder:6.7b-instruct
```

The AI will process CI logs and summarize them based on the prompts given.

## Usage

Once everything is set up, you can trigger workflows with the following command:

```bash
python -m cli.minibot --say "Deploy my app"
```

### Optional Parameters:

- If you want to specify the **branch** and **workflow filename** directly, include them inside the quotation marks:

```bash
python -m cli.minibot --say "Deploy my app on main branch with deploy.yml"
```

- If no branch or workflow filename is provided, the AI will prompt you to input the necessary information.

### Workflow Dispatch Permissions Example

In your GitHub workflow YAML file, ensure you have the following snippet to enable manual workflow dispatch:

```yaml
on:
  workflow_dispatch:
    inputs:
      tag:
        description: "Docker image tag"
        required: false
        default: "latest"
```

This ensures the workflows can be triggered by external requests, such as the one from the `BuildBot` AI.

## Project Structure

Here’s a breakdown of the file structure:

```
buildbot/
│
├── agent/
│   ├── __init__.py
│   ├── ai_summarizer.py
│   ├── build_trigger.py
│   ├── github_branches.py
│   ├── github_workflows.py
│   ├── intent_parser.py
│   ├── log_summarizer.py
│   ├── minikernel.py
│   ├── status_checker.py
│
├── cli/
│   ├── minibot.py
│   └── status.py
│
├── config/
│   └── secrets.env
│
├── summarize_ci_logs.py
└── requirements.txt
```

### File Descriptions:

- **agent/**: Contains the core logic for interacting with GitHub Actions and processing logs.
  - `build_trigger.py`: Triggers workflows via GitHub's API.
  - `ai_summarizer.py`: Summarizes CI/CD logs and suggests actionable steps.
  - `status_checker.py`: Checks the status of a workflow run.
  - `github_branches.py`: Retrieves branches from the repository.
  - `github_workflows.py`: Retrieves available workflows from the repository.
  - `log_summarizer.py`: Extracts and summarizes error logs.
  - `minikernel.py`: Handles the AI reasoning and interaction flow.
  
- **cli/**: Provides the command-line interface for users to interact with the BuildBot.
  - `minibot.py`: Main script to trigger AI-based workflow actions.
  - `status.py`: Allows users to check the status of a workflow run.

- **config/**: Contains the configuration files like secrets for accessing GitHub.

- **summarize_ci_logs.py**: Fetches the latest workflow logs and sends them for summarization.
- **requirements.txt**: Lists the Python dependencies.

## Contributing

Feel free to fork the project, submit issues, and create pull requests. Your contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

