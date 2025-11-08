"""
Scheduler for automated tasks in V-Mart Personal AI Agent
"""

import threading
import time
from datetime import datetime
from typing import Callable, Dict, List

import schedule


class TaskScheduler:
    def __init__(self):
        """
        Initializes the Task Scheduler.
        """
        self.tasks: List[Dict] = []
        self.running = False
        self.thread = None

    def add_daily_task(self, time_str: str, task: Callable, name: str = None):
        """
        Adds a daily task to the scheduler.

        Args:
            time_str (str): Time in HH:MM format (24-hour)
            task (Callable): The function to execute
            name (str): Optional name for the task
        """
        job = schedule.every().day.at(time_str).do(task)
        self.tasks.append(
            {
                "name": name or f"daily_task_{len(self.tasks)}",
                "job": job,
                "schedule": f"Daily at {time_str}",
                "task": task,
            }
        )
        return job

    def add_interval_task(self, minutes: int, task: Callable, name: str = None):
        """
        Adds an interval task to the scheduler.

        Args:
            minutes (int): Interval in minutes
            task (Callable): The function to execute
            name (str): Optional name for the task
        """
        job = schedule.every(minutes).minutes.do(task)
        self.tasks.append(
            {
                "name": name or f"interval_task_{len(self.tasks)}",
                "job": job,
                "schedule": f"Every {minutes} minutes",
                "task": task,
            }
        )
        return job

    def add_weekly_task(
        self, day: str, time_str: str, task: Callable, name: str = None
    ):
        """
        Adds a weekly task to the scheduler.

        Args:
            day (str): Day of week (monday, tuesday, etc.)
            time_str (str): Time in HH:MM format (24-hour)
            task (Callable): The function to execute
            name (str): Optional name for the task
        """
        day_methods = {
            "monday": schedule.every().monday,
            "tuesday": schedule.every().tuesday,
            "wednesday": schedule.every().wednesday,
            "thursday": schedule.every().thursday,
            "friday": schedule.every().friday,
            "saturday": schedule.every().saturday,
            "sunday": schedule.every().sunday,
        }

        job = day_methods[day.lower()].at(time_str).do(task)
        self.tasks.append(
            {
                "name": name or f"weekly_task_{len(self.tasks)}",
                "job": job,
                "schedule": f"Every {day} at {time_str}",
                "task": task,
            }
        )
        return job

    def list_tasks(self) -> List[Dict]:
        """
        Lists all scheduled tasks.

        Returns:
            List of task dictionaries
        """
        return [
            {
                "name": task["name"],
                "schedule": task["schedule"],
                "next_run": task["job"].next_run,
            }
            for task in self.tasks
        ]

    def start(self):
        """
        Starts the scheduler in a background thread.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            print("Scheduler started")

    def stop(self):
        """
        Stops the scheduler.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        print("Scheduler stopped")

    def _run_scheduler(self):
        """
        Internal method to run the scheduler loop.
        """
        while self.running:
            schedule.run_pending()
            time.sleep(1)
