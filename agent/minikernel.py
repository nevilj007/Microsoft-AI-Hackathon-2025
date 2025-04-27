import time
import os
from agent.intent_parser import parse_intent
from agent.build_trigger import trigger_workflow
from agent.status_checker import check_status
from agent.log_summarizer import summarize_logs
from summarize_ci_logs import get_log_for_run, extract_error_chunks
from agent.ai_summarizer import summarize_log_with_kernel
from agent.github_workflows import list_workflows_in_repo
from agent.github_branches import list_branches_in_repo



class MiniKernel:

    def __init__(self):
        self.skills = {
            "trigger": self.trigger_workflow,
            "wait": self.wait_for_status,
            "summarize": self.summarize_logs
        }

    def run(self, command: str):
        print(f" MiniKernel received intent: {command}")
        intent = parse_intent(command)

        # List all valid workflows in repo
        valid_workflows = list_workflows_in_repo()

        # Step 1: Check if LLM output contains valid workflow
        chosen_file = None
        if intent and "workflow_file" in intent:
            if intent["workflow_file"] in valid_workflows:
                chosen_file = intent["workflow_file"]
            else:
                print(f" LLM suggested invalid or missing workflow: {intent['workflow_file']}")

        # Step 2: If not, prompt user
        if not chosen_file:
            print(" Falling back to interactive workflow selection...\n")
            chosen_file = self.ask_for_workflow()
            if not chosen_file:
                return

        #  Validate branch
        available_branches = list_branches_in_repo()
        if intent and "ref" in intent and intent["ref"] in available_branches:
            branch = intent["ref"]
        else:
            print(f" LLM-suggested branch not found: {intent.get('ref', 'none')}")
            branch = self.ask_for_branch()
            if not branch:
                return

        # Proceed as normal
        run_id = self.skills["trigger"](chosen_file, branch)
        result = self.skills["wait"](run_id)

        if result == "failure":
            self.skills["summarize"](run_id)
        else:
            print(" Build succeeded!")
    def trigger_workflow(self, workflow_file, branch):
        print(f" Triggering `{workflow_file}` on branch `{branch}`")
        trigger_workflow(workflow_file, ref=branch)
        time.sleep(5)  # Let GitHub catch up
        from summarize_ci_logs import get_latest_run_id
        run_id = get_latest_run_id()
        print(f" Run ID: {run_id}")
        return run_id

    def wait_for_status(self, run_id):
        print(" Waiting for build to finish...\n")
        while True:
            status = check_status(run_id)
            if status["status"] == "completed":
                conclusion = status["conclusion"]
                print(f"\n Final Result: {conclusion.upper()}")
                return conclusion
            print(" Still running...")
            time.sleep(10)

    def summarize_logs(self, run_id):
        print(" Build failed. Fetching logs...\n")
        log_text = get_log_for_run(run_id)
        summary = summarize_log_with_kernel(log_text)
        print(" Summary:\n", summary)

    def ask_for_workflow(self):
        print(" Scanning .github/workflows...")
        workflows = list_workflows_in_repo()

        if not workflows:
            print(" No workflows found in the repository.")
            return None

        print("\n Available workflows:")
        for idx, wf in enumerate(workflows):
            print(f"[{idx + 1}] {wf}")

        while True:
            try:
                choice = int(input("\n Select a workflow to run (enter number): "))
                if 1 <= choice <= len(workflows):
                    return workflows[choice - 1]
                print(" Invalid choice. Try again.")
            except ValueError:
                print(" Please enter a number.")

    def ask_for_branch(self):
        print(" Scanning GitHub branches...")
        branches = list_branches_in_repo()

        if not branches:
            print(" No branches found in this repo.")
            return None

        print("\n Available branches:")
        for idx, b in enumerate(branches):
            print(f"[{idx + 1}] {b}")

        while True:
            try:
                choice = int(input("\n Select a branch to deploy (enter number): "))
                if 1 <= choice <= len(branches):
                    return branches[choice - 1]
                print(" Invalid choice. Try again.")
            except ValueError:
                print(" Please enter a number.")
