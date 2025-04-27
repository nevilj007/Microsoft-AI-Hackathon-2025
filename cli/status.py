import argparse
from agent.status_checker import check_status

def main():
    parser = argparse.ArgumentParser(description="Check status of a GitHub Actions run.")
    parser.add_argument("--run-id", required=True, help="The workflow run ID to check.")

    args = parser.parse_args()
    run_id = args.run_id

    try:
        info = check_status(run_id)

        print(f" Workflow: {info['workflow']}")
        print(f" Branch: {info['branch']}")
        print(f" View on GitHub: {info['url']}")
        print(f" Status: {info['status']}")

        if info["status"] == "completed":
            if info["conclusion"] == "success":
                print(" Build completed successfully.")
            elif info["conclusion"] == "failure":
                print(" Build failed.")
            else:
                print(f"⚠ Build finished with conclusion: {info['conclusion']}")
        else:
            print(" Build still in progress...")

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
