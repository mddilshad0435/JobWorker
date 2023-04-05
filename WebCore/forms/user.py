from typing import List, Optional
from fastapi import Request


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.full_name: str = None
        self.email: str = None
        self.password: str = None
        self.username: Optional[str] = None

    async def load_data(self):
        form = self.request
        self.full_name = form.get("full_name")
        self.email = form.get("email")
        self.password = form.get("password")
        self.username = form.get("username")

    async def is_valid(self):
        if not self.full_name or not len(self.full_name) > 3:
            self.errors.append("Username should be >  3chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("password must be > 4char")
        if not self.errors:
            return True
        return False


class UserLoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = self.request
        self.email = form.get("email")
        self.password = form.get("password")
