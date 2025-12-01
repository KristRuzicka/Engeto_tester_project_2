from src.db import task_statuses, return_tasks, return_one_task, add_task_db, update_task_db, remove_task_db, view_task_db

sep_short = "="*40
sep_long = "_"*80

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
        print(f"{sep_short}\nNo task found.")
        return
    
    print_tasks(tasks)
    
def print_tasks(tasks):
    print(sep_long,
          "\n{:<5} {:<20} {:<25} {:<12} {:<19}"
            .format("ID","Name","Description","Status","Date"), 
        )
    print(sep_long)

    for task in tasks:
        id = task['id']
        name = (task['name'][:20] + "...") if len(task['name']) > 20 else task['name']
        description = (task['description'][:20] + "...") if len(task['description']) > 20 else task['description']
        status = task['status']
        date = task['date'].strftime("%Y-%m-%d") if task['date'] else ""
        print(
            "{:<5} {:<20} {:<25} {:<12} {:<19}"
            .format(id,name,description,status,date,)
        )
    print(sep_long)

def print_all_tasks(conn):
    tasks = view_task_db(conn, "1")
    print_tasks(tasks)

def update_status(conn):
    """Function update task status."""
    
    print_all_tasks(conn)

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
    """Function update task status."""
    
    print_all_tasks(conn)
    # Task removal
    try:
        selected_id = int(input("""\nEnter number of task to be removed: """).strip())
       # Check for id of non existing task.
    
        # if not return_one_task(conn, selected_id):
        # print(f"Error: Task ID {selected_id} doesn't exist.")
        # return
        
        remove_task_db(conn, selected_id)
        print(f"{sep_short}\nTask {selected_id} has been removed.")
    
    # Check for invalid task number
    except ValueError:
        print(f"{sep_short}\nError: Invalid entry.")
    except Exception as e:
        print(f"{sep_short}\nError: Task not removed: {e}.")