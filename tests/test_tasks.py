import pytest
from mysql.connector import MySQLConnection
from src.db import table, task_statuses, db_connection, create_table, add_task_db, update_task_db, remove_task_db, create_data
import random

@pytest.fixture(scope="function")
def conn():
    print("Connect to database.")
    conn = db_connection("test_")
    # Create table and data
    print("Table and data created.")
    create_table(conn)
    create_data(conn)
    yield conn

    # Delete test table
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    print("\nTable and data deleted.")
    conn.close()

def return_random_task(conn):
    """pomocna funkce na vyber nahodneho ID knihy pro testy"""

    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT id from {table}")
        tasks_ids = cursor.fetchall()
    task_id = random.choice(tasks_ids)
    return task_id["id"]

def test_add_task_positive(conn):
    """This test tests the task is added."""
    # Arrange - get task name and description
    task_name = "Christmas preparations"
    task_description = "Decorate the house and bake cookies."

    # Act 
    add_task_db(conn, name = task_name, description = task_description)

    # Assert 
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"""
                SELECT * FROM {table}
                WHERE name = %s AND description = %s
                """, (task_name, task_description))
        test_task = cursor.fetchone()

    assert test_task != None
    assert test_task['status'] == task_statuses[1]
    assert test_task['name'] == task_name, f"The task name should be {task_name} and it is {test_task['name']}."
    assert test_task['description'] == task_description, f"The task description should be {task_description} and it is {test_task['description']}."
    assert test_task['date'] == None

def test_add_task_negative(conn):
    """This test tests Exception return when the name and description is empty."""

    # Act 
    with pytest.raises(Exception) as e:
        result = add_task_db(conn, name = "", description = "")
    
    print(e.value)


def test_update_task_positive(conn):
    """This test tests if the task status is updated."""
    # Arrange - get random task
    task_id = return_random_task(conn)
    
    # Act 
    result = update_task_db(conn, task_id, task_statuses[2])
    
    # Assert 
    with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"""SELECT id, status, date 
                        FROM {table} 
                        WHERE id = %s""", (task_id,))
            tasks = cursor.fetchall()
            sum_tasks = len(tasks)
            task_status = tasks[0]["status"]
            date = tasks[0]["date"]

    assert sum_tasks == 1
    assert result == True
    assert task_status == task_statuses[2]
    assert date != None


def test_update_task_negative(conn):
    """This test tests Exception return when the status number is empty."""
    # Arrange - ger random task
    task_id = return_random_task(conn)
    
    # Act 
    with pytest.raises(Exception) as e:
        result = update_task_db(conn, task_id, status = "")
    
    print(e.value)

def test_remove_task_positive(conn):
    """This test tests if the task is removed."""
    # Arrange - get random task
    task_id = return_random_task(conn)
    
    # Act 
    result = remove_task_db(conn, task_id)
    
    # Assert 
    with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"""DELETE FROM {table} 
                        WHERE id = %s""", (task_id,))
            tasks = cursor.fetchall()
    assert result == True

def test_remove_task_negative(conn):
    """This test tests if the task is removed."""
    # Arrange - get random task
    task_id = return_random_task(conn)
    
    # Act 
    with pytest.raises(Exception) as e:
        result = remove_task_db(conn, task_id = "")
    
    print(e.value)


