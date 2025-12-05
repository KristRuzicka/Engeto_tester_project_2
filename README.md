 # Task Manager

Task Manager which stores data in a MySQL database. The program allows you to: add tasks, view, tasks (according to status), update task status and remove tasks.
The project also includesautomated possitive and negative tests using pytest and a test MySQL database covering functions: add task, update task and remove taks.

## Requirments
- dotenv
- pytest
- mysql-connector-python
- rich

### dotenv
Plugin for loading configuration from `.env` file
##### Windows
`pip install python-dotenv`
`python -m pip install python-dotenv`
##### MacOS
`python3 -m pip install python-dotenv`
`pip3 install python-dotenv` -> Windows 

### pyTest
##### Windows
`pip install pytest`
`python -m pip install pytest`
##### MacOS
`pip3 install pytest`
`python3 -m pip install pytest`

### mysql-connector-python
##### Windows
`pip install mysql-connector-python`
`python -m pip install mysql-connector-python`

##### MacOS
`pip3 install mysql-connector-python`
`python3 -m pip install mysql-connector-python`

### rich
##### Windows
`pip install rich`
`python -m pip install rich`
##### MacOS
`pip3 install rich`
`python3 -m pip install rich`


## Configuration
In the main folder in the `.env` file configure the necessary login information to connect to the db

```
DB_HOST=localhost
DB_USER=root
DB_PASS=1111
DB_NAME=tasks
```

## Launch

Run `main.py`

## Test
in the terminal in the root folder run the command `pytest`

## Program directory structure
```
project/
├─ src/
│ ├─ __init_.py
│ ├─ db.py <-- Contains all functions for working with the db
│ └─ tasks.py <-- Contains all functions managing the application logic
├─ tests/
│ ├─ __init_.py
│ └─ test_tasks.py <-- Contains all tests
├─ main.py <-- Entry point to the application
└─ README.md <-- Introductory documentation
```