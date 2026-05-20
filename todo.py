import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


def is_valid_task_list(tasks):
    """Return True if the loaded JSON data is a valid task list."""
    if not isinstance(tasks, list):
        return False

    for task in tasks:
        if not isinstance(task, dict):
            return False
        if not isinstance(task.get("title"), str):
            return False
        if not isinstance(task.get("completed"), bool):
            return False

    return True


def load_tasks():
    """Load tasks from the JSON storage file."""
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        print("Warning: tasks.json is not valid JSON. Starting with an empty list.")
        return []
    except OSError as error:
        print(f"Warning: could not read tasks.json: {error}")
        return []

    if not is_valid_task_list(tasks):
        print("Warning: tasks.json has an invalid format. Starting with an empty list.")
        return []

    return tasks


def save_tasks(tasks):
    """Save tasks to the JSON storage file."""
    try:
        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        print(f"Error: could not save tasks: {error}")
        return False

    return True


def display_menu():
    """Print the main menu options."""
    print("\n===== ToDo List Menu =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Exit")


def get_menu_choice():
    """Read and validate the user's menu choice."""
    choice = input("Choose an option (1-5): ").strip()

    if not choice:
        print("Menu selection cannot be empty.")
        return None

    if not choice.isdigit():
        print("Invalid selection. Please enter a number from 1 to 5.")
        return None

    choice_number = int(choice)
    if choice_number < 1 or choice_number > 5:
        print("Invalid selection. Please choose a number from 1 to 5.")
        return None

    return choice_number


def add_task(tasks):
    """Add a new task to the list."""
    title = input("Enter task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    tasks.append({"title": title, "completed": False})
    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    """Display all tasks with their completion status."""
    if not tasks:
        print("No tasks found.")
        return

    print("\nYour Tasks:")
    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["completed"] else "Pending"
        print(f"{index}. [{status}] {task['title']}")


def get_task_number(tasks, prompt):
    """Read and validate a task number from the user."""
    if not tasks:
        print("No tasks available.")
        return None

    view_tasks(tasks)
    choice = input(prompt).strip()

    if not choice:
        print("Task number cannot be empty.")
        return None

    if not choice.isdigit():
        print("Invalid task number. Please enter a positive number.")
        return None

    task_number = int(choice)
    if task_number < 1 or task_number > len(tasks):
        print(f"Task number must be between 1 and {len(tasks)}.")
        return None

    return task_number - 1


def mark_completed(tasks):
    """Mark a selected task as completed."""
    task_index = get_task_number(tasks, "Enter task number to mark as completed: ")

    if task_index is None:
        return

    tasks[task_index]["completed"] = True
    save_tasks(tasks)
    print("Task marked as completed.")


def delete_task(tasks):
    """Delete a selected task from the list."""
    task_index = get_task_number(tasks, "Enter task number to delete: ")

    if task_index is None:
        return

    deleted_task = tasks.pop(task_index)
    save_tasks(tasks)
    print(f"Deleted task: {deleted_task['title']}")


def main():
    """Run the ToDo List application."""
    tasks = load_tasks()

    try:
        while True:
            display_menu()
            choice = get_menu_choice()

            if choice is None:
                continue

            if choice == 1:
                add_task(tasks)
            elif choice == 2:
                view_tasks(tasks)
            elif choice == 3:
                mark_completed(tasks)
            elif choice == 4:
                delete_task(tasks)
            elif choice == 5:
                print("Goodbye!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
