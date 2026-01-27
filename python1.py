# user_management.py

import uuid
import hashlib
from datetime import datetime


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, name, email):
        user_id = self._generate_user_id(email)
        user = User(user_id, name, email)
        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def list_users(self):
        return [user.to_dict() for user in self.users.values()]

    def _generate_user_id(self, email):
        raw = f"{email}-{uuid.uuid4()}"
        return hashlib.sha256(raw.encode()).hexdigest()


class AuthService:
    def __init__(self):
        self.credentials = {}

    def register(self, email, password):
        hashed = self._hash_password(password)
        self.credentials[email] = hashed
        return True

    def login(self, email, password):
        if email not in self.credentials:
            return False
        return self.credentials[email] == self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


# ---------- Utility Functions ----------

def validate_email(email):
    return "@" in email and "." in email


def format_user_output(user: User):
    if not user:
        return None
    return f"{user.name} <{user.email}> | ID: {user.user_id}"


def system_health_check():
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    }


# ---------- Main Simulation ----------

if __name__ == "__main__":
    user_service = UserService()
    auth_service = AuthService()

    # Create users
    u1 = user_service.create_user("Alice", "alice@example.com")
    u2 = user_service.create_user("Bob", "bob@example.com")

    # Register auth
    auth_service.register("alice@example.com", "password123")

    # Login attempt
    login_status = auth_service.login("alice@example.com", "password123")

    # Output
    print("Login success:", login_status)
    print("All users:", user_service.list_users())
    print("System health:", system_health_check())
