from user import User
from user import UserController

while True:
    print("1. Sign in")
    print("2. Log in")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        while True:
            username = input("Enter your username: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            if UserController.exists(username):
                print("Username already exists. Please try again.")
                continue

            if not UserController.email_check(email):
                print("Invalid email. Please try again.")
                continue

            if not UserController.password_check(password):
                print("Invalid password. Password should be at least 8 characters long. Please try again.")
                continue

            user = User(username, password, email, True, [])
            UserController.add_user(user)
            print("User signed in successfully!")
            break

    elif choice == '2':
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            users = UserController.get_users()
            for user in users:
                if user.username == username and user.password == password:
                    print("User logged in successfully!")
                    break
            else:
                print("Invalid username or password. Please try again.")
                continue
            break

    else:
        print("Invalid choice. Please enter 1 or 2.")
