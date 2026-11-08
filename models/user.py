from dataclasses import dataclass


@dataclass
class User:
    id: int
    login: str
    password_hash: str
    role: str