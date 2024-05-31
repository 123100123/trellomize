from encoder import Encoder
from user import UserController
import argparse
import os
import shutil

def authenticate(username, password):
    if not os.path.exists("Admin.txt"):
        print("Error: Admin does not exist.")
        exit(1)
    
    stored_username, stored_password = read_admin()
    if username != stored_username or password != stored_password:
        print("Error: Invalid username or password.")
        exit(1)

def create_admin(username, password):
    if os.path.exists("Admin.txt"):
        print("Error: Admin Already Exists")
        exit(1)

    output = "%s,%s" % (username, Encoder.encrypt(password))
    with open("Admin.txt", "w") as file:
        file.write(output)

def read_admin():
    with open("Admin.txt", "r") as file:
        username, password = file.readline().strip().split(",")
        password = Encoder.decrypt(password)
        
        return username, password

def reset():
    if os.path.exists("users.json"):
        os.remove("users.json")
    
    if os.path.exists("projects.json"):
        os.remove("projects.json")
        
    if os.path.exists("tasks"):
        shutil.rmtree("tasks")
    
    if os.path.exists("loggerFile.log"):
        os.remove("loggerFile.log")

def activate_user(username: str):
    if not UserController.exists(username):
        print("Error: User doesn't exist")
        exit(1)
    user = UserController.get_user(username)
    user.enabled = True
    UserController.update_user(user)

def deactivate_user(username: str):
    if not UserController.exists(username):
        print("Error: User doesn't exist")
        exit(1)
    user = UserController.get_user(username)
    user.enabled = False
    UserController.update_user(user)

parser = argparse.ArgumentParser()

parser.add_argument("action", type=str, choices=["create-admin", "purge-data", "activate-user", "deactivate-user"])
parser.add_argument("--username", type=str, required=True, help="Username for authentication or action")
parser.add_argument("--password", type=str, required=True, help="Password for authentication or action")


args, remaining_args = parser.parse_known_args()


if args.action in ["activate-user", "deactivate-user"]:
    parser.add_argument("--user", type=str, required=True, help="Defines the username of the user to activate/deactivate")

args = parser.parse_args()

if args.action != "create-admin":
    authenticate(args.username, args.password)

if args.action == "create-admin":
    create_admin(args.username, args.password)
elif args.action == "purge-data":
    confirm = input("Are You Sure?(Y/N): ")
    if confirm == "Y" or confirm == "y":
        reset()
elif args.action == "activate-user":
    activate_user(args.user)
elif args.action == "deactivate-user":
    deactivate_user(args.user)
else:
    print("Error: Unknown action.")
