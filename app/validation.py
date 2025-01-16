from datetime import datetime


def validate_task_name(name):
    """Validate the task name."""
    if not name.strip():
        raise ValueError("Task name cannot be empty!")
    if len(name) > 100:
        raise ValueError("Task name is too long! Maximum 100 characters.")


def validate_due_date(due_date):
    """Validate the due date."""
    if due_date:
        try:
            date = datetime.strptime(due_date, "%Y-%m-%d").date()
            if date < datetime.now().date():
                raise ValueError("Due date cannot be in the past!")
        except ValueError:
            raise ValueError("Invalid due date format! Use YYYY-MM-DD.")


def validate_priority(priority):
    """Validate task priority, defaulting to 'Medium' if not provided."""
    valid_priorities = ["High", "Medium", "Low"]
    if not priority:  # Empty or None input
        return "Medium"
    priority = priority.strip().title()
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority! Choose from {', '.join(valid_priorities)}.")
    return priority


def validate_recurrence(recurrence):
    """Validate task recurrence, defaulting to 'None' if not provided."""
    valid_recurrences = ["None", "Daily", "Weekly", "Monthly"]
    if not recurrence:  # Empty or None input
        return "None"
    recurrence = recurrence.strip().title()
    if recurrence not in valid_recurrences:
        raise ValueError(f"Invalid recurrence! Choose from {', '.join(valid_recurrences)}.")
    return recurrence
