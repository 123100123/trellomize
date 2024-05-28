from menu import UserMenu,LoginMenu

def main():
    while True:
        user = LoginMenu.get_user()
        if user == None:
            break
        user_menu = UserMenu(user)
        user_menu.menu()
        
    
    

if __name__ == "__main__":
    main()

