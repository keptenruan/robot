# main.py
from db_utils import init_db, register, login, logout, get_db_connection

def main_menu(user):
    while True:
        print("\nMain Menu")
        print("1. Add Account")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter account number: ")
            initial_balance = float(input("Enter initial balance (default is 0): ") or 0)
            add_account(user.id, account_number, initial_balance)
        elif choice == '2':
            account_number = input("Enter account number: ")
            balance = check_balance(user.id, account_number)
            if balance is not None:
                print(f"Balance: {balance}")
        elif choice == '3':
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to deposit: "))
            deposit(user.id, account_number, amount)
        elif choice == '4':
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to withdraw: "))
            withdraw(user.id, account_number, amount)
        elif choice == '5':
            logout(user)
            break
        else:
            print("Invalid choice. Please try again.")

def add_account(user_id, account_number, initial_balance=0.0):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Accounts (user_id, account_number, balance) VALUES (%s, %s, %s)', (user_id, account_number, initial_balance))
        conn.commit()
        print(f"Account {account_number} added successfully.")

def check_balance(user_id, account_number):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM Accounts WHERE user_id = %s AND account_number = %s', (user_id, account_number))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Account does not exist.")
            return None

def deposit(user_id, account_number, amount):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Accounts SET balance = balance + %s WHERE user_id = %s AND account_number = %s', (amount, user_id, account_number))
        conn.commit()
        print(f"Deposited {amount} to the account {account_number}.")

def withdraw(user_id, account_number, amount):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM Accounts WHERE user_id = %s AND account_number = %s', (user_id, account_number))
        current_balance = cursor.fetchone()[0]
        if current_balance >= amount:
            cursor.execute('UPDATE Accounts SET balance = balance - %s WHERE user_id = %s AND account_number = %s', (amount, user_id, account_number))
            conn.commit()
            print(f"Withdrew {amount} from the account {account_number}.")
        else:
            print("Insufficient funds.")

def main():
    init_db()  # 初始化数据库
    while True:
        print("\nBank System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = login(username, password)
            if user:
                main_menu(user)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()