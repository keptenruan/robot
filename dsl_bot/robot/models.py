# models.py
from passlib.hash import pbkdf2_sha256

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

class Account:
    def __init__(self, id, user_id, account_number, balance):
        self.id = id
        self.user_id = user_id
        self.account_number = account_number
        self.balance = balance