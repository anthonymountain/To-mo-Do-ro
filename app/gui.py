from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from task_manager import add_task, complete_task, save_tasks, load_tasks

# Global Variables
tasks = load_tasks()  # Load existing tasks
timer_running = False
timer_seconds = 25 * 60  # Default: 25 minutes


def refresh_task_list():
    """Refresh the task list display."""
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        task_listbox.insert(tk.END, f"{task['name']} [{status}]")


def add_task_to_list():
    """Add a task from user input."""
    task_name = simpledialog.askstring("Add Task", "Enter task name:")
    if not task_name:
        messagebox.showerror("Error", "Task name cannot be empty!")
        return
    due_date = simpledialog.askstring("Add Task",
                                      "Enter due date (YYYY-MM-DD) "
                                      "or leave blank:")
    priority = simpledialog.askstring("Add Task", "Enter priority "
                                                  "(High, Medium, Low) "
                                                  "or leave blank:")
    recurrence = simpledialog.askstring("Add Task", "Enter "
                                                    "recurrence (None, Daily, "
                                                    "Weekly, Monthly) or leave "
                                                    "blank:")

    try:
        add_task(tasks, task_name, due_date, priority, recurrence)
        refresh_task_list()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def complete_selected_task():
    """Mark the selected task as completed."""
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No task selected!")
        return
    task_id = selected[0] + 1
    complete_task(tasks, task_id)
    refresh_task_list()


def delete_selected_task():
    """Delete the selected task."""
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No task selected!")
        return
    task_id = selected[0] + 1
    tasks.pop(task_id - 1)
    save_tasks(tasks)
    refresh_task_list()


def start_timer():
    """Start the Pomodoro timer."""
    global timer_running
    timer_running = True
    countdown()


def pause_timer():
    """Pause the Pomodoro timer."""
    global timer_running
    timer_running = False


def reset_timer():
    """Reset the Pomodoro timer."""
    global timer_running, timer_seconds
    timer_running = False
    timer_seconds = 25 * 60
    update_timer_display()


def countdown():
    """Handle the countdown for the timer."""
    global timer_seconds, timer_running
    if timer_running and timer_seconds > 0:
        minutes, seconds = divmod(timer_seconds, 60)
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        timer_seconds -= 1
        root.after(1000, countdown)
    elif timer_seconds == 0:
        messagebox.showinfo("Pomodoro Timer", "Time's up!")


def update_timer_display():
    """Update the timer display."""
    minutes, seconds = divmod(timer_seconds, 60)
    timer_label.config(text=f"{minutes:02}:{seconds:02}")


def show_tasks_for_date():
    """Show tasks for the selected date."""
    # Get the selected date from the calendar
    selected_date = calendar.get_date()

    try:
        formatted_date = (datetime.strptime(selected_date, "%m/%d/%y")
                          .strftime("%Y-%m-%d"))
    except ValueError:
        # Handle unexpected formats (fallback for MM/DD/YYYY)
        formatted_date = (datetime.strptime(selected_date, "%m/%d/%Y")
                          .strftime("%Y-%m-%d"))

    # Filter tasks for the selected date
    tasks_for_date = [task for task in tasks if task.get("due_date") ==
                      formatted_date]

    # Update the task listbox
    task_listbox.delete(0, tk.END)
    if tasks_for_date:
        for task in tasks_for_date:
            status = "✓" if task["completed"] else "✗"
            task_listbox.insert(tk.END, f"{task['name']} [{status}]")
    else:
        messagebox.showinfo("No Tasks", f"No tasks scheduled for "
                                        f"{formatted_date}.")


def main():
    global root, task_listbox, timer_label, calendar

    root = tk.Tk()
    root.title("To-mo-Do-ro")
    root.geometry("550x700")

    # Task List Frame
    task_frame = ttk.Frame(root)
    task_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
    ttk.Label(task_frame, text="Tasks").grid(row=0, column=0, padx=5, pady=5)
    task_listbox = tk.Listbox(task_frame, height=15, width=40)
    task_listbox.grid(row=1, column=0, padx=5, pady=5)
    (ttk.Button(task_frame, text="Add Task", command=add_task_to_list)
     .grid(row=2, column=0, padx=5, pady=5))
    (ttk.Button(task_frame, text="Complete Task",
                command=complete_selected_task)
     .grid(row=3, column=0, padx=5, pady=5))
    (ttk.Button(task_frame, text="Delete Task", command=delete_selected_task)
     .grid(row=4, column=0, padx=5, pady=5))

    # Pomodoro Timer Frame
    timer_frame = ttk.Frame(root)
    timer_frame.grid(row=0, column=1, sticky="n", padx=10, pady=5)
    ttk.Label(timer_frame, text="Pomodoro Timer").grid(row=0, column=0, padx=5,
                                                       pady=5)
    timer_label = ttk.Label(timer_frame, text="25:00", font=("Helvetica", 24))
    timer_label.grid(row=1, column=0, padx=5, pady=5)
    (ttk.Button(timer_frame, text="Start", command=start_timer)
     .grid(row=2,column=0, padx=5, pady=5))
    (ttk.Button(timer_frame, text="Pause", command=pause_timer)
     .grid(row=3, column=0, padx=5, pady=5))
    (ttk.Button(timer_frame, text="Reset", command=reset_timer)
     .grid(row=4, column=0, padx=5, pady=5))

    # Calendar Frame
    calendar_frame = ttk.Frame(root)
    calendar_frame.grid(row=1, column=1, padx=10, pady=5, sticky="n")
    ttk.Label(calendar_frame, text="Calendar View").grid(row=0, column=0,
                                                         padx=5, pady=5)
    calendar = Calendar(calendar_frame, selectmode="day")
    calendar.grid(row=1, column=0, padx=5, pady=5)
    calendar.bind("<<CalendarSelected>>", lambda e: show_tasks_for_date())

    refresh_task_list()  # Load tasks into the listbox on startup
    root.mainloop()


if __name__ == "__main__":
    main()
