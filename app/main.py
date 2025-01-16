from task_manager import (load_tasks, save_tasks, add_task, delete_task,
                          complete_task, list_tasks, view_completed_tasks)
from pomodoro import timer


def main():
    tasks = load_tasks()

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Start Pomodoro Timer")
        print("6. Exit")
        print("7. View Completed Tasks")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter task name: ")
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            priority = input("Enter priority (High, Medium, Low): ")
            recurrence = input("Is this a recurring task? (None, Daily, Weekly,"
                               " Monthly): ")
            add_task(tasks, name, due_date, priority, recurrence)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            task_id = int(input("Enter task ID to complete: "))
            complete_task(tasks, task_id)
        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            tasks = delete_task(tasks, task_id)
        elif choice == "5":
            work_time = int(input("Enter work time in minutes (default 25): ")
                            or 25)
            break_time = int(input("Enter break time in minutes (default 5): ")
                             or 5)
            timer(work_time, break_time)
        elif choice == "6":
            break
        elif choice == "7":
            view_completed_tasks()
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
