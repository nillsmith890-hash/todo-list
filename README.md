# Command-Line ToDo List

A simple menu-based ToDo List application written in Python.

## Features

- Add new tasks
- View all tasks
- Mark tasks as completed
- Delete tasks
- Save tasks automatically to `tasks.json`
- Load saved tasks automatically when the program starts
- Validate empty input, invalid menu choices, and invalid task numbers
- Handle JSON file errors gracefully

## Files

- `todo.py`: Main Python program
- `tasks.json`: Stores saved tasks
- `test_todo.py`: Unit tests for storage and input validation

## How to Run

Open a terminal in this folder and run:

```bash
python3 todo.py
```

If your system uses `python` instead of `python3`, run:

```bash
python todo.py
```

## Menu Options

When the program starts, you will see:

```text
===== ToDo List Menu =====
1. Add task
2. View tasks
3. Mark task as completed
4. Delete task
5. Exit
```

Enter the number of the option you want to use.

## Data Storage

Tasks are saved in `tasks.json` using JSON format.

Example:

```json
[
    {
        "title": "Study Python",
        "completed": false
    }
]
```

If `tasks.json` does not exist, the program starts with an empty task list.

## Requirements

- Python 3

No external libraries are required.

## Error Handling

The program handles common errors gracefully:

- Missing `tasks.json`: starts with an empty task list
- Invalid JSON in `tasks.json`: shows a warning and starts with an empty task list
- Invalid task data format: shows a warning and starts with an empty task list
- File save errors: shows an error message instead of crashing
- `Ctrl+C` or unexpected input ending: exits cleanly

## Running Tests

Run the unit tests with:

```bash
python3 -m unittest test_todo.py
```

Or, if your system uses `python`:

```bash
python -m unittest test_todo.py
```
