from src.db import db_connection, create_table
from src.tasks import view_tasks, update_status, add_task, remove_task

sep_short = "="*50

def main_function(conn):
    while True:
        print(f"{sep_short}\nTask manager - Main menu\n" 
        "1. Add new task\n"
        "2. View tasks\n"
        "3. Update task\n"
        "4. Remove task\n"
        "5. End program\n"
        )
        print(sep_short)
        
        choice = input("Choose option (1-5):" ).strip()
    
        if choice == "1":
            add_task(conn)
        elif choice == "2":
            view_tasks(conn)
        elif choice == "3":
            update_status(conn)
        elif choice == "4":
            remove_task(conn)
        elif choice == "5":
            print("\nEnding program.")
            break
        else: 
            print(f"{sep_short}\nError - Choose valid option (1-5).")

if __name__ == "__main__":
    conn = db_connection()
    if conn:
        create_table(conn)

        main_function(conn)
        conn.close()

