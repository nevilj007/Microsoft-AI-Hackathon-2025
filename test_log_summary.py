'''from agent.log_summarizer import summarize_logs

if __name__ == "__main__":
    log = """
    Step 1: install deps
    Successfully installed packages.

    Step 2: run tests
    test_model.py .....
    test_data.py ..F

    =================================== FAILURES ===================================
    test_data.py::test_data_format - AssertionError: Data format invalid
    """

    summary = summarize_logs(log)
    print("\n Build Summary:\n", summary)'''
