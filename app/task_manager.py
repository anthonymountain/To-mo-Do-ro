import json
import os
from datetime import datetime, timedelta
from validation import (validate_task_name, validate_due_date,
                        validate_priority, validate_recurrence)

# File to save tasks
DATA_FILE = "data.json"
COMPLETED_TASKS_FILE = "completed_tasks.json"


def load_tasks():
    """Load tasks from a file, creating the file if it doesn't exist, and handle
    recurring tasks."""
    # Check if the file exists; if not, create and initialize it
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump([], f)
    if not os.path.exists("completed_tasks.json"):
        with open("completed_tasks.json", "w") as f:
            json.dump([], f)

    # Try loading tasks from the file
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if content:  # File is not empty
                tasks = json.loads(content)
                return generate_recurring_tasks(tasks)  # Add recurring tasks
            else:
                return []  # Return an empty list if the file is empty
    except json.JSONDecodeError:
        print("Error: data.json contains invalid JSON. Starting with an empty"
              "task list.")
        return []


def save_tasks(tasks):
    """Save tasks to a file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)


def add_task(tasks, name, due_date=None, priority="Medium", recurrence=None):
    """Add a new task with a recurrence interval."""
    try:
        validate_task_name(name)
        validate_due_date(due_date)
        priority = validate_priority(priority)
        recurrence = validate_recurrence(recurrence)
    except ValueError as e:
        # If validation fails, print the error and stop
        print(f"Error adding task: {e}")
        return

    task = {
        "id": len(tasks) + 1,
        "name": name,
        "completed": False,
        "due_date": due_date,
        "priority": priority,
        "recurrence": recurrence
    }
    tasks.append(task)
    save_tasks(tasks)


def generate_recurring_tasks(tasks):
    """Generate future tasks for recurring tasks."""
    new_tasks = []
    today = datetime.now().date()

    for task in tasks:
        if task.get("recurrence", "None") != "None" and task.get("due_date"):
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

            # Generate tasks for future dates
            while due_date <= today:
                if task["recurrence"] == "Daily":
                    due_date += timedelta(days=1)
                elif task["recurrence"] == "Weekly":
                    due_date += timedelta(weeks=1)
                elif task["recurrence"] == "Monthly":
                    # Add one month (handling month/year boundaries)
                    due_date = ((due_date.replace(day=1) + timedelta(days=32))
                                .replace(day=1))

            # Create a new task for the future date
            new_task = task.copy()
            new_task["id"] = len(tasks) + len(new_tasks) + 1
            new_task["due_date"] = due_date.strftime("%Y-%m-%d")
            new_task["completed"] = False
            new_tasks.append(new_task)

    tasks.extend(new_tasks)
    save_tasks(tasks)  # Save updated task list
    return tasks


def delete_task(tasks, task_id):
    """Delete a task and update task IDs."""
    # Remove the task with the given ID
    tasks = [task for task in tasks if task["id"] != task_id]

    # Reassign IDs to the remaining tasks
    for i, task in enumerate(tasks, start=1):
        task["id"] = i

    # Save the updated task list
    save_tasks(tasks)
    return tasks


def complete_task(tasks, task_id):
    """Mark a task as completed and log it."""
    # Find the task by ID
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True

            # Log the completed task
            log_completed_task(task)

            # Save the updated tasks list
            save_tasks(tasks)
            print(f"Task '{task['name']}' marked as completed!")
            return
    print(f"No task found with ID {task_id}.")


def log_completed_task(task):
    """Log the completed task to a separate file."""
    # Remove the "id" field for the completed log
    completed_task = task.copy()
    completed_task.pop("id", None)

    try:
        with open(COMPLETED_TASKS_FILE, "r") as f:
            completed_tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        completed_tasks = []

    completed_tasks.append(completed_task)

    with open(COMPLETED_TASKS_FILE, "w") as f:
        json.dump(completed_tasks, f, indent=4)


def list_tasks(tasks):
    """List all tasks with priorities."""
    if not tasks:
        print("No tasks, add some!")
    tasks_sorted = sorted(tasks, key=lambda t: ["High", "Medium", "Low"]
                          .index(t["priority"].title()))
    for task in tasks_sorted:
        status = "✓" if task["completed"] else "✗"
        due = f" (Due: {task['due_date']})" if task["due_date"] else ""
        print(f"{task['id']}. {task['name']} [{status}]"
              ""f"[Priority: {task['priority']}] {due} "
              ""f"[Recurrence: {task['recurrence']}]")


def view_completed_tasks():
    """Display all completed tasks."""
    try:
        with open(COMPLETED_TASKS_FILE, "r") as f:
            completed_tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No completed tasks logged yet.")
        return

    if not completed_tasks:
        print("No completed tasks logged yet.")
        return

    print("Completed Tasks:")
    for i, task in enumerate(completed_tasks, start=1):
        due = f" (Due: {task['due_date']})" if task.get("due_date") else ""
        print(f"{i}. {task['name']} [Priority: {task['priority']}] {due}")

