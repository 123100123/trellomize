from encoder import Encoder
import argparse
import os

def create_admin(username, password):
    if os.path.exists("Admin.txt"):
        print("Error: Admin Already Exists")
        exit(1)

    output = "%s,%s" % (username, Encoder.encrypt(password))
    with open("Admin.txt", "w") as file:
        file.write(output)

parser = argparse.ArgumentParser()
parser.add_argument("action",type=str)
parser.add_argument("--username", type=str, default="admin", help= "defines the username of the admin",required=True)
parser.add_argument("--password", type=str, default="admin", help="defines the password of the admin")

args = parser.parse_args()

if args.action == "create-admin":
    create_admin(args.username, args.password)
else:
    print("Error: Unknown action. Use 'create-admin' to create an admin user.")
