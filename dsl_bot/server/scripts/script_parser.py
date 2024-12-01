import re
from ..db.models import User, Account
from ..db.db_utils import db

def parse_script(script):
    """
    解析并执行脚本中的命令。
    """
    commands = script.split(';')
    user = None
    responses = []

    for command in commands:
        command = command.strip()
        if not command:
            continue

        # 正则表达式匹配命令
        register_pattern = r'register\s+(\w+)\s+(".*?")'
        login_pattern = r'login\s+(\w+)\s+(".*?")'
        add_account_pattern = r'add_account\s+(\w+)\s+(\d+(\.\d+)?)'
        check_balance_pattern = r'check_balance\s+(\w+)'
        deposit_pattern = r'deposit\s+(\w+)\s+(\d+(\.\d+)?)'
        withdraw_pattern = r'withdraw\s+(\w+)\s+(\d+(\.\d+)?)'

        if re.match(register_pattern, command):
            match = re.match(register_pattern, command)
            username = match.group(1)
            password = match.group(2).strip('"')
            result = register(username, password)
            responses.append(result)

        elif re.match(login_pattern, command):
            match = re.match(login_pattern, command)
            username = match.group(1)
            password = match.group(2).strip('"')
            user = login(username, password)
            if user:
                responses.append(f"Logged in as {user.username}")
            else:
                responses.append("Login failed.")

        elif re.match(add_account_pattern, command):
            if not user:
                responses.append("You must be logged in to add an account.")
                continue
            match = re.match(add_account_pattern, command)
            account_number = match.group(1)
            initial_balance = float(match.group(2))
            result = add_account(user, account_number, initial_balance)
            responses.append(result)

        elif re.match(check_balance_pattern, command):
            if not user:
                responses.append("You must be logged in to check balance.")
                continue
            match = re.match(check_balance_pattern, command)
            account_number = match.group(1)
            balance = check_balance(user, account_number)
            if balance is not None:
                responses.append(f"Balance: {balance}")
            else:
                responses.append("Account does not exist.")

        elif re.match(deposit_pattern, command):
            if not user:
                responses.append("You must be logged in to deposit.")
                continue
            match = re.match(deposit_pattern, command)
            account_number = match.group(1)
            amount = float(match.group(2))
            result = deposit(user, account_number, amount)
            responses.append(result)

        elif re.match(withdraw_pattern, command):
            if not user:
                responses.append("You must be logged in to withdraw.")
                continue
            match = re.match(withdraw_pattern, command)
            account_number = match.group(1)
            amount = float(match.group(2))
            result = withdraw(user, account_number, amount)
            responses.append(result)

        else:
            responses.append("Unknown command. Available commands: register, login, add_account, check_balance, deposit, withdraw")

    return responses

def register(username, password):
    """
    注册新用户。
    """
    if User.query.filter_by(username=username).first():
        return "Username already exists."
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return "User registered successfully."

def login(username, password):
    """
    登录用户。
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    else:
        return None

def add_account(user, account_number, initial_balance=0.0):
    """
    为用户添加新的账户。
    """
    if Account.query.filter_by(account_number=account_number).first():
        return "Account number already exists."
    
    new_account = Account(user_id=user.id, account_number=account_number, balance=initial_balance)
    db.session.add(new_account)
    db.session.commit()
    return f"Account {account_number} added successfully."

def check_balance(user, account_number):
    """
    检查账户余额。
    """
    account = Account.query.filter_by(user_id=user.id, account_number=account_number).first()
    if account:
        return account.balance
    else:
        return None

def deposit(user, account_number, amount):
    """
    存款到账户。
    """
    account = Account.query.filter_by(user_id=user.id, account_number=account_number).first()
    if account:
        account.balance += amount
        db.session.commit()
        return f"Deposited {amount} to the account {account_number}."
    else:
        return "Account does not exist."

def withdraw(user, account_number, amount):
    """
    从账户取款。
    """
    account = Account.query.filter_by(user_id=user.id, account_number=account_number).first()
    if account and account.balance >= amount:
        account.balance -= amount
        db.session.commit()
        return f"Withdrew {amount} from the account {account_number}."
    else:
        return "Insufficient funds."