import argparse
import csv
import sqlite3
from os import remove, path

DB_NAME = 'example.db'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Parses path to csv files to fill the database')
    parser.add_argument('-projects', type=str, help='path to csv with projects')
    parser.add_argument('-tasks', type=str, help='path to csv with tasks')
    return parser.parse_args()


def input_check(user_input, list_len):
    return user_input.isdigit() and not (int(user_input) > list_len or int(user_input) < 1)


def print_tasks(task_list):
    for task in task_list:
        task_string = "{:<5}{:<3}{:<13}{:<13}{:<13}{:<13}{:<13}".format(*task)
        print(task_string)


def choose_project(project_list):
    for i, project in enumerate(project_list):
        print(i + 1, project)
    project_name = ''
    if len(task_projects) < 1:
        print('The task table is empty ')
    else:
        message = "Choose one of projects to look at its task: "
        project_number = input(message)
        while not input_check(project_number, len(task_projects)):
            print('There no such number in the nf list! try again ')
            project_number = input(message)
        project_name = task_projects[int(project_number) - 1]
    return project_name


def create_tables(cursor):
    cursor.executescript('''CREATE TABLE Project
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     Name text NOT NULL,
                     Description text, 
                     Deadline date);
                     
                     CREATE TABLE Tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      priority INTEGER,
                      details text, 
                      status text, 
                      deadline date, 
                      completed date, 
                      Project text NOT NULL)''')


if __name__ == '__main__':

    if path.isfile(DB_NAME):
        remove(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    args = parse_arguments()
    create_tables(c)

    with open(args.tasks) as f:
        d = csv.DictReader(f)
        for row in d:
            task = (row['priority'], row['details'], row['status'], row['deadline'], row['completed'], row['Project'])
            c.execute("""INSERT INTO Tasks  ( priority, details, status, deadline, completed, 
                  Project) VALUES (?,?,?,?,?,?)""", task)

    with open(args.projects) as f:
        d = csv.DictReader(f)
        for row in d:
            project = (row['Name'], row['description'], row['deadline'])
            c.execute("""INSERT INTO Project  (Name, description, deadline) VALUES (?,?,?)""", project)

    c.execute("""select distinct project from tasks""")

    task_projects = c.fetchmany(5)
    project_name = choose_project(task_projects)
    c.execute("""select * from tasks where project = (?)  """, project_name)
    conn.commit()

    print_tasks(c.fetchall())
    conn.close()
