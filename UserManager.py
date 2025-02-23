class UserManager:
    def __init__(self):
        self.users = {}
        self.admin_code = "Kod@Code"

    def add_user(self):
        admin_code = input("Enter admin code: ")
        if admin_code != self.admin_code:
            print("Invalid admin code. Access denied.")
            return

        username = input("Enter new username: ")
        password = input("Enter password: ")
        self.users[username] = password
        print(f"User '{username}' added successfully.")

    def view_users(self):
        admin_code = input("Enter admin code: ")
        if admin_code != self.admin_code:
            print("Invalid admin code. Access denied.")
            return

        if not self.users:
            print("No users found.")
        else:
            print("Registered users:")
            for username in self.users:
                print(f"- {username}")

    def remove_user(self):
        admin_code = input("Enter admin code: ")
        if admin_code != self.admin_code:
            print("Invalid admin code. Access denied.")
            return

        username = input("Enter username to remove: ")
        if username in self.users:
            del self.users[username]
            print(f"User '{username}' removed successfully.")
        else:
            print(f"User '{username}' not found.")


# דוגמת שימוש
manager = UserManager()

while True:
    print("\n--- User Manager Menu ---")
    print("1. Add user")
    print("2. View users")
    print("3. Remove user")
    print("4. Exit")

    choice = input("Choose an option (1-4): ")

    if choice == "1":
        manager.add_user()
    elif choice == "2":
        manager.view_users()
    elif choice == "3":
        manager.remove_user()
    elif choice == "4":
        print("Exiting User Manager.")
        break
    else:
        print("Invalid choice. Please select a valid option.")