"""
This module is used for task management. It allows users to register, add tasks, 
view tasks, generate reports, and display statistics.
"""

# Import necessary libraries
import os
from datetime import datetime, date

# Define the format for datetime strings
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

# Read task data from tasks.txt
with open("tasks.txt", "r", encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Parse task data into a list of dictionaries
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["username"] = task_components[0]
    curr_t["title"] = task_components[1]
    curr_t["description"] = task_components[2]
    curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t["completed"] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# Login Section
# This code reads usernames and password from the user.txt file to allow a user to login.

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user data
with open("user.txt", "r", encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert user data to a dictionary
username_password = {}
for user in user_data:
    if ";" in user:
        username, password = user.split(";")
        username_password[username] = password
    else:
        print(f"Invalid line in user.txt: {user}")

# User login loop
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password:
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def save_tasks():
    """
    Writes tasks from "task_list" to "tasks.txt", one task per line.
    """
    # Open the file in write mode
    with open("tasks.txt", "w", encoding="utf-8") as new_task_file:
        task_list_to_write = []
        # Iterate over each task in the task list
        for t in task_list:
            # Prepare the attributes of the task for writing
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No"
            ]
            # Join the attributes with a semicolon and add to the list
            task_list_to_write.append(";".join(str_attrs))
        # Write the tasks to the file, one per line
        new_task_file.write("\n".join(task_list_to_write))

def reg_user():
    """Allow a user to register new user to user.txt file
        Prompt a user for the following: 
         - Username of new user,
         - Resubmission if user exists,
         - Password of new user with confirmation and 
         - Resubmission if password incorrect."""
    while True:
        # Request input of a new username
        new_username = input("New Username: ")
        # If the username already exists, prompt for a different username
        if new_username in username_password:
            print("Username already exists. Please try a different username.")
            continue
        else:
            while True:
                # Request input of a new password
                new_password = input("New Password: ")

                # Request input for password confirmation
                confirm_password = input("Confirm Password: ")

                # If new password and confirmed password are the same, add them to user.txt file
                if new_password == confirm_password:
                    print("New user added")
                    username_password[new_username] = new_password

                    # Open the user.txt file in write mode
                    with open("user.txt", "w", encoding="utf-8") as out_file:
                        new_user_data = []
                        # Iterate over each user in the username_password dictionary
                        for k, v in username_password.items():
                            # Prepare the user data for writing
                            new_user_data.append(f"{k};{v}")
                        # Write the user data to the file, one per line
                        out_file.write("\n".join(new_user_data))
                    return
                else:
                    # If the passwords do not match, present a relevant message
                    print("Passwords do not match. Please try again.")

def add_task():
    """Allow a user to add a new task to task.txt file
        Prompt a user for the following with errors if done wrong: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - The due date of the task."""
    while True:
        # Request input for the name of the person assigned to the task
        task_username = input("Name of person assigned to task: ")

        # If the username does not exist, present a relevant message
        if task_username not in username_password:
            print("User does not exist. Please enter a valid username")
        else:
            break

    # Request input for the title of the task
    task_title = input("Title of Task: ")

    # Request input for the description of the task
    task_description = input("Description of Task: ")

    while True:
        try:
            # Request input for the due date of the task
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            # Convert the due date to a datetime object
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            # If the datetime format is invalid, present a relevant message
            print("Invalid datetime format. Please use the format specified")

    # Get the current date
    curr_date = date.today()

    # Prepare the new task data
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add the new task to the task list
    task_list.append(new_task)

    # Save the tasks to the file
    save_tasks()

    # Confirm that the task was successfully added
    print("Task successfully added.")

def view_all():
    """Reads all tasks from task.txt file and prints to the console including spacing 
    and labelling 
    """
    # Iterate over each task in the task list
    for t in task_list:
        # Prepare the display string for the task
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        # Print the display string
        print(disp_str)

def view_mine():
    """Allow a user to view assigned tasks from task.txt file
        They can then choose to do the following and will receive prompts if done incorrectly: 
         - Select a specific task,
         - Mask task as complete,
         - Edit task due date and 
         - Edit task assigned user."""
    # Filter tasks assigned to the current user
    user_tasks = [t for t in task_list if t["username"] == curr_user]

    # Iterate over each task assigned to the current user
    for i, t in enumerate(user_tasks):
        # Prepare the display string for the task
        disp_str = f"Task {i+1}: \t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        # Print the display string
        print(disp_str)

    task_updated = False
    while True:
        # Prompt the user to select a task number to edit or '-1' to return to the main menu
        print("Select a task number to edit, or '-1' to return to the main menu.")
        task_num = int(input())
        if task_num == -1:
            # If a task was updated, save the tasks
            if task_updated:
                save_tasks()
            # Return to the main menu
            return "back_to_menu"
        elif task_num < 1 or task_num > len(user_tasks):
            # If the task number is invalid, present a relevant message
            print("Invalid task number. Please try again.")
        else:
            # Select the task
            selected_task = user_tasks[task_num-1]
            print("Selected Task: ", selected_task["title"])
            # If the task is already completed, it cannot be edited
            if selected_task["completed"]:
                print("This task is already completed and cannot be edited.")
                break
            # Present the options to the user
            print("1. Mark task as complete")
            print("2. Edit task due date")
            print("3. Edit task assigned user")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                # Mark the task as complete
                selected_task["completed"] = True
                print("Task marked as complete.")
                task_updated = True
            elif choice == 2:
                while True:
                    try:
                        # Request input for the new due date
                        new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                        # Convert the input string to a datetime object
                        new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        # Assign the datetime object to the task's due date
                        selected_task["due_date"] = new_due_date
                    except ValueError:
                        # If the input is not a valid date, print an error message
                        print("Invalid date format or date does not exist. Please try again.")
                    else:
                        # If the input is a valid date, update the task due date and break the loop
                        print("Task due date updated.")
                        task_updated = True
                        break
            elif choice == 3:
                # Request input for the new assigned user
                new_assigned_user = input("Enter new assigned user: ")
                # If the username does not exist, present a relevant message
                if new_assigned_user not in username_password:
                    print("User does not exist. Please enter a valid username")
                else:
                    # Update the assigned user of the task
                    selected_task["username"] = new_assigned_user
                    print("Task assigned user updated.")
                    task_updated = True
            else:
                # If the choice is invalid, present a relevant message
                print("Invalid choice. Please try again.")
        # If a task was updated, save the tasks
        if task_updated:
            save_tasks()

def display_statistics():
    """This function displays statistics about the number of users and tasks. 
    It should only be called if the user is an admin."""

    # Check if the report files exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        # If they don't exist, generate them using the generate_reports function
        generate_reports()

    # Read the report files
    with open("task_overview.txt", "r", encoding="utf-8") as task_file_local:
        task_report = task_file_local.read()
    with open("user_overview.txt", "r", encoding="utf-8") as user_file_local:
        user_report = user_file_local.read()

    # Print the reports
    print("Task Overview:\n", task_report)
    print("User Overview:\n", user_report)

def generate_reports():
    """Generate reports when the user selects this option.
       Two text files, called task_overview.txt and user_overview.txt, are generated.
       The task overview includes the total number of tasks, the number of completed tasks, etc.
       The user overview includes the total number of users, the tasks assigned to each user, etc.
       Both these text files output data in a user-friendly, easy to read manner.
    """
    # task_overview.txt
    # task_list is a list of all tasks
    total_tasks = len(task_list)
    if total_tasks > 0:  # Check if there are tasks before calculating percentages
        completed_tasks = len([t for t in task_list if t["completed"]])
        uncompleted_tasks = total_tasks - completed_tasks
        # Count tasks that are overdue and not completed
        overdue_tasks = len([
            t for t in task_list
            if t["due_date"].date() < date.today() and not t["completed"]
            ])
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100
    else:
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        incomplete_percentage = 0
        overdue_percentage = 0

    # Writing task overview to file
    with open("task_overview.txt", "w", encoding="utf-8") as task_overview:
        task_overview.write(f"Total tasks: {total_tasks}\n")
        task_overview.write(f"Completed tasks: {completed_tasks}\n")
        task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview.write(f"Percentage of tasks that are incomplete: "
                            f"{round(incomplete_percentage, 2)}%\n")
        task_overview.write(f"Percentage of tasks that are overdue: "
                            f"{round(overdue_percentage, 2)}%\n")

    # user_overview.txt
    # username_password is a dictionary with usernames as keys and passwords as values
    total_users = len(username_password)
    # Creating a dictionary with usernames as keys and their tasks as values
    user_tasks = {
        username: [
            t for t in task_list
            if t["username"] == username
            ]
        for username in username_password
    }

    # Writing user overview to file
    with open("user_overview.txt", "w", encoding="utf-8") as user_overview:
        user_overview.write(f"Total users: {total_users}\n")
        user_overview.write(f"Total tasks: {total_tasks}\n")
        for user_name, tasks in user_tasks.items():
            assigned_tasks = len(tasks)
            if assigned_tasks > 0:  # Check if there are tasks before calculating percentages
                completed_tasks = len([t for t in tasks if t["completed"]])
                uncompleted_tasks = assigned_tasks - completed_tasks
                # Count tasks that are overdue and not completed
                overdue_tasks = len([
                    t for t in tasks
                    if t["due_date"].date() < date.today() and not t["completed"]
                    ])
                # Calculate percentages for assigned, completed, uncompleted, and overdue tasks
                assigned_percentage = round((assigned_tasks / total_tasks) * 100, 2)
                completed_percentage = round((completed_tasks / assigned_tasks) * 100, 2)
                uncompleted_percentage = round((uncompleted_tasks / assigned_tasks) * 100, 2)
                overdue_percentage = round((overdue_tasks / assigned_tasks) * 100, 2)
            else:
                completed_tasks = 0
                uncompleted_tasks = 0
                overdue_tasks = 0
                assigned_percentage = 0
                completed_percentage = 0
                uncompleted_percentage = 0
                overdue_percentage = 0

            user_overview.write(f"\nUser: {user_name}\n")
            user_overview.write(f"Total tasks assigned to user: {assigned_tasks}\n")
            user_overview.write(
                f"Percentage of total tasks assigned to user: "
                f"{assigned_percentage}%\n"
                )
            user_overview.write(
                f"Percentage of tasks assigned to user that have been completed: "
                f"{completed_percentage}%\n"
                )
            user_overview.write(
                f"Percentage of tasks assigned to user that must still be completed: "
                f"{uncompleted_percentage}%\n"
                )
            user_overview.write(
                f"Percentage of tasks assigned to user that are overdue: "
                f"{overdue_percentage}%\n"
                )

    print("Reports generated.")

while True:
    # Presenting the menu to the user and converting the user input to lower case.
    print()
    # curr_user is the currently logged in user
    if curr_user == "admin":
        # Displaying admin menu
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: """).lower()
    else:
        # Displaying non-admin menu
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
e - Exit
: """).lower()

    # Executing the function based on the user's choice
    if menu == "r":
        reg_user()
    elif menu == "a":
        add_task()
    elif menu == "va":
        view_all()
    elif menu == "vm":
        result = view_mine()
        if result == "back_to_menu":
            continue  # If the user chooses to go back, skip the rest of the loop
    elif menu == "gr":
        generate_reports()
    elif menu == "ds" and curr_user == "admin":
        display_statistics()  # Display statistics option only available for admin
    elif menu == "e":
        print("Goodbye!!!")
        exit()
    else:
        print("You have made a wrong choice, Please Try again")  # Handle invalid input

    # Pause the program and wait for the user to press any key to return to the main menu
    input("Press any key to return to the main menu...")
