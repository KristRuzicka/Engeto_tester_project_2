
import mysql.connector
from mysql.connector import MySQLConnection

from dotenv import load_dotenv
import os 


load_dotenv()

sep_short = "="*40

table = "tasks"
task_statuses = {
    1: "Not started",
    2: "In progress",
    3: "Done"
}

def db_connection(prefix = ""):
    """Creates connection to mysql
    and creates database. Checks for error"""
    try:
        conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS")
        )
        cursor = conn.cursor(dictionary=True)
        db_name = prefix + os.getenv("DB_NAME")

        create_db(cursor, db_name)

        cursor.execute(f"USE {db_name}")
        cursor.close()
        conn.commit()
        
        print(f"{sep_short}\nConnected to database {db_name}.")
        return conn
    
    except mysql.connector.Error as err:
        print (f"{sep_short}\nNot connected: {err}.")
        return None

 
def create_db(cursor, db_name):
    """Creates database if not exists."""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")

def create_table(conn):
    """Creates table for saving tasks. Checks for error."""
    try:
        with conn.cursor() as cursor:
            # status ENUM('Not started', 'In progress','Done') DEFAULT 'Not started',
            enum_values = ", ".join(f"'{status}'" for status in task_statuses.values())

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    status ENUM({enum_values}) DEFAULT '{task_statuses[1]}',
                    date DATE
                    );
                """)
            conn.commit()
            print(f"{sep_short}\nTable created.")

    except mysql.connector.Error as e:
        print(f"{sep_short}\nError - table not created: {e}")


def create_data(conn):
    """Inserts data into table."""
    tasks = [
        ("Fix time machine", ""
        "It keeps sending me to Monday mornings", 
        "Not started"),
        ("Untangle Christmas lights", 
         "Current knot may be a new form of life", 
         "Not started"),
        ("Write New Year resolutions",
         "Try to make at least one realistic this time", 
         "Not started"),
         ]

    try:
        with conn.cursor() as cursor:
            # Checks if table is empty
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sum = cursor.fetchone()[0]

            if sum > 0:
                print(f"There are already {sum} tasks.")
                return False

            cursor.executemany(f"""
                INSERT INTO {table} (name, description, status)
                VALUES (%s, %s, %s)
            """, tasks)
        conn.commit()
        print(f"{len(tasks)} tasks have been inserted.")

    except mysql.connector.Error as e:
        print(f"Error - no tasks in the table: {e}")

def add_task_db(conn, name, description):
    """ Adds task to the database. Checks for empty entry."""

    if not name or not description:
        raise Exception("Error - Name and description cannot be empty.")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table} (name, description) VALUES (%s, %s)""",
                (name, description)
            )
        conn.commit()
        print(f"{sep_short}\nThe task {name} has been added.")

    except mysql.connector.Error as e:
        conn.rollback()
        raise Exception(f"Error - the task has not been added: {e}")

def view_task_db(conn: MySQLConnection, filter_option=None):
    """Returns task according to selected option. Checks for empty entry."""
    try:
        with conn.cursor(dictionary=True) as cursor:
            if filter_option == "1" or filter_option is None:
                cursor.execute(f"""
                    SELECT id, name, description, status, date
                    FROM {table}
                """)

            elif filter_option == "2":
                cursor.execute(f"""
                    SELECT id, name, description, status, date
                    FROM {table} WHERE status = "Not started"
                """)
            
            elif filter_option == "3":
                cursor.execute(f"""
                    SELECT id, name, description, status, date
                    FROM {table} WHERE status = "In progress"
                """)
            return cursor.fetchall()

    except Exception as e:
        print(f"{sep_short}\nError - tasks cannot be viewed.")
        return
        

def return_tasks(conn: MySQLConnection):
    """Returns all tasks form the database as a list dictionary."""
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT id, name, description, status, date FROM {table}")
            tasks = cursor.fetchall()
            return tasks
    except Exception:
        print(f"{sep_short}\nError - tasks cannot be viewed.")

def return_one_task(conn: MySQLConnection, id):
    """Return one task according to selected Task ID."""
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT id, name, description, status, date FROM {table} WHERE id = %s", (id,))
            task = cursor.fetchone()
            return task
    except Exception:
        print(f"{sep_short}\nError - Task doesn't exist.")
    
    
def update_task_db(conn: MySQLConnection, id, new_status):
    """Updates task status. If changed to 'In progress', date is added."""
    if new_status not in task_statuses.values():
        raise Exception(f"Invalid status: {new_status}")
    
    try:
        with conn.cursor() as cursor:
            if new_status == task_statuses[2]: 
                cursor.execute(f"""UPDATE {table} SET status = %s, date = CURRENT_TIMESTAMP WHERE id = %s""", (new_status, id))
            else:
                cursor.execute(f"""UPDATE {table} SET status = %s, date = NULL WHERE id = %s""", (new_status, id))
        conn.commit()
        return True
    
    except Exception as e:
        print(f"{sep_short}\nError - Task status not updated {id}: {e}")
        return None

def remove_task_db(conn: MySQLConnection, id):
    """Removes selected task."""
 #   if selected_id not in id.values():
  #      raise Exception(f"Invalid id: {selected_id}")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""DELETE FROM {table} WHERE id = %s""", (id,))
        conn.commit()
        return True
    
    except Exception as e:
        print(f"{sep_short}\nError - task not removed: {e}")
        return None