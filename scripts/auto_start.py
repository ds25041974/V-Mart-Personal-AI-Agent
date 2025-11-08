"""
Script to auto-start and monitor the V-Mart Personal AI Agent.
This is a conceptual example. A robust implementation would use a process manager like systemd or supervisord.
"""

import os
import subprocess
import time


def start_agent():
    """Starts the agent application."""
    print("Starting V-Mart Personal AI Agent...")
    # Use absolute path to main.py
    main_py_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "main.py"
    )
    process = subprocess.Popen(["python", main_py_path])
    return process


def main():
    """Main loop to monitor and restart the agent if it crashes."""
    process = start_agent()
    while True:
        time.sleep(10)
        poll = process.poll()
        if poll is not None:
            print("Agent has crashed. Restarting...")
            process = start_agent()


if __name__ == "__main__":
    main()
