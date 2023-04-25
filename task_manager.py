# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

# This lines define a string format for date-time objects
DATETIME_STRING_FORMAT = "%Y-%m-%d"


def read_task_data():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

        # Red task data from task.txt
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        # Filter out empty string from task_data
        task_data = [t for t in task_data if t != ""]

    # process the task data and store them as  dictionaries in a list
    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(
            task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(
            task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)
    return task_list


# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''


def read_user_data():
    # check if user.txt exists, if not create it
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read user data from user.txt
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Process user data and store them as a dictionary
    username_password = {}
    for user in user_data:
        # This line checks if the semicolon (;) is not present in the current line
        if ';' not in user:
            continue
        username, password = user.split(';')
        username_password[username] = password

    return username_password


def reg_user(username_password):
    # Register new user
    new_username = input("New Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task(task_list, username_password):
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all_tasks(task_list):
    '''Reads the task from task.txt file and prints to the console in the format of Output 2 presented in the task pdf (i.e. includes spacing and labelling)'''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_my_tasks(task_list, curr_user):
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)


def display_statistics(username_password, task_list):
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


def generate_reports(task_list, username_password):
    # create and write to task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        total_tasks = len(task_list)
        completed_tasks = sum([1 for task in task_list if task['completed']])
        uncompleted_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(
            [1 for task in task_list if not task["completed"] and task["due_date"] < datetime.now()])
        incomplete_percentage = (overdue_tasks/total_tasks) * 100
        overdue_percentage = (overdue_tasks/total_tasks) * 100
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(
            f"Incomplete tasks percentage: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(
            f"Overdue tasks percentage: {overdue_percentage:.2f}%\n")


def main():
    task_list = read_task_data()
    username_password = read_user_data()
    logged_in = False

    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    while True:
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Get reports
ds - Display statistics
e - Exit
: ''').lower()

        if menu == 'r':
            reg_user(username_password)
        elif menu == 'a':
            add_task(task_list, username_password)
        elif menu == 'va':
            view_all_tasks(task_list)
        elif menu == 'vm':
            view_my_tasks(task_list, curr_user)
        elif menu == "gr" and curr_user == "admin":
            generate_reports(task_list, username_password)
            print("Reports generated successfully.")
        elif menu == 'ds' and curr_user == 'admin':
            display_statistics(username_password, task_list)
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")


if __name__ == "__main__":
    main()
