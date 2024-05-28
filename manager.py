from encoder import Encoder
from user import UserController
import argparse
import os

def create_admin(username, password):
    if os.path.exists("Admin.txt"):
        print("Error: Admin Already Exists")
        exit(1)

    output = "%s,%s" % (username, Encoder.encrypt(password))
    with open("Admin.txt", "w") as file:
        file.write(output)

def reset():
    if os.path.exists("users.json"):
        os.remove("users.json")
    
    if os.path.exists("projects.json"):
        os.remove("projects.json")

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

if "create-admin" in parser.parse_known_args()[0].action:
    parser.add_argument("--username", type=str, default="admin", help="defines the username of the admin")
    parser.add_argument("--password", type=str, default="admin", help="defines the password of the admin")

elif "activate-user" in parser.parse_known_args()[0].action or "deactivate-user" in parser.parse_known_args()[0].action:
    parser.add_argument("--username", type=str, help="defines the username of the user to activate/deactivate")

args = parser.parse_args()

if args.action == "create-admin":
    create_admin(args.username, args.password)
elif args.action == "purge-data":
    reset()
elif args.action == "activate-user":
    activate_user(args.username)
elif args.action == "deactivate-user":
    deactivate_user(args.username)
else:
    print("Error: Unknown action.")
