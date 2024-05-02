from encoder import Encoder
import argparse
import os

encoder = Encoder()


def create_admin(username, password):
    if os.path.exists("Admin.txt"):
        print("Error: Admin Already Exists")

    output = "%s,%s" % (username, encoder.encrypt(password).decode())
    with open("Admin.txt", "w") as file:
        file.write(output)


parser = argparse.ArgumentParser()
parser.add_argument("--username", type=str, default="admin", help= "defines the username of the admin")
parser.add_argument("--password", type=str, default="admin", help="defines the password of the admin")

args = parser.parse_args()


create_admin(args.username, args.password)
