from src.db import task_statuses, return_tasks, return_one_task, add_task_db, update_task_db, remove_task_db, view_task_db
from rich.table import Table
from rich.console import Console

sep_short = "="*50
sep_long = "_"*80

console = Console()

def color_for_status(status: str) -> str:
    status = status.lower()
    if status == "not started":
        return "red"
    elif status == "in progress":
        return "yellow"
    elif status == "done":
        return "green"
    return "white"  # default

def print_tasks(tasks):
    table = Table(title="Tasks", header_style="white")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Status")
    table.add_column("Date")

    for task in tasks:
        id = str(task["id"])
        name = (task["name"][:20] + "...") if len(task["name"]) > 20 else task["name"]
        description = (task["description"][:25] + "...") if len(task["description"]) > 25 else task["description"]
        status = task["status"]
        date = task["date"].strftime("%Y-%m-%d") if task["date"] else ""
        
        row_style = color_for_status(status)

        table.add_row(
            id, name, description, status, date,
            style=row_style)

    console.print(table)


def view_tasks(conn):
    """Function prints all tasks from the database."""

    print("Choose option: \n 1. View all tasks."
    "\n 2. View 'Not started' tasks." 
    "\n 3. View tasks 'In progress'.")
    
    filter_option = input("Enter number: ").strip()
    
    if filter_option not in ("1", "2", "3"):
        print(f"{sep_short}\nError: Invalid number.")
        return  
    
    tasks = view_task_db(conn, filter_option)

    if not tasks:
        print(f"{sep_short}\nThere are no saved tasks 'In progress'.")
        return
    
    print_tasks(tasks)
    
def print_all_tasks(conn):

    try:
        tasks = view_task_db(conn, "1")

        if not tasks:
            print(f"{sep_short}\nNo task found.")
            return False
        
        print_tasks(tasks)
        return True

    except Exception as e:
        print(f"{sep_short}\nError: {e}.")
        return False

def update_status(conn):
    """Function update task status."""
    
    if not print_all_tasks(conn):
        print("There are no saved tasks yet.")
        return

    # User enters task id which should be amended.
    try:
        id = int(input("Enter task ID: ").strip())
    except ValueError:
        print(f"{sep_short}\nError: Invalid ID.")
        return

    # Check for id of non existing task.
    if not return_one_task(conn, id):
        print(f"{sep_short}\nError: Task ID {id} doesn't exist.")
        return

    # Status change
    try:
        new_status = int(input("""Statuses: \n1 - Not started \n2 - In progress \n3 - Done \nEnter number of status: """).strip())

        if new_status not in task_statuses:
            print(f"{sep_short}\nError: Invalid status number.")
            return
        
        update_task_db(conn, id, task_statuses[new_status])
        print(f"{sep_short}\nTask status has been updated to '{task_statuses[new_status]}'.")
    
    
    # Check for valid status number
    except ValueError:
        print(f"{sep_short}\nError: Invalid entry.")
    except Exception as e:
        print(f"{sep_short}\nError: Task status not udpated: {e}.")


def add_task(conn):
    '''Function takes input from user and add new tasks to database'''

    name = get_input("Enter task name: ")
    if name is None:
        print(f"{sep_short}\nError - taks name not entered.")
        return
    
    description = get_input("Enter task description: ")
    if description is None:

        print(f"{sep_short}\nError - taks description not entered.")
        return
    
    try:
        add_task_db(conn, name, description)
    except Exception as e:
        print(f"{sep_short}\nError - task not added: {e}")


def get_input(entry):
    '''Function takes input from user. 
    Checks for empty and interupted entry.'''
    while True:
        try:
            value = input(entry).strip()
            if value:
                return value
            print(f"{sep_short}\nError: Empty entry")
            
        except KeyboardInterrupt:
            print(f"{sep_short}\nProcess interupted by user.")
            return None

def remove_task(conn):
    """Function removes selected task."""
    if not print_all_tasks(conn):
        print("There are no saved tasks yet.")
        return
    
    # Task removal
    try:
        selected_id = get_input("""\nEnter number of task to be removed: """)
        
        if selected_id is None:
            print(f"{sep_short}\nError - ID not entered.")
            return
        try: 
            selected_id = int(selected_id)
        except ValueError:
            print(f"{sep_short}\nError: Invalid entry.")
            return
        
        task = return_one_task(conn, selected_id)
        if not task:
            print(f"{sep_short}\nError: Task with ID {selected_id} does not exist.")
            return

        remove_task_db(conn, selected_id)
        print(f"{sep_short}\nTask {selected_id} has been removed.")

    # Check for invalid task number
    except Exception as e:
        print(f"{sep_short}\nError: Task not removed: {e}.")