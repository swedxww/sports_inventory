from dataclasses import dataclass


@dataclass
class Equipment:
    id: int
    name: str
    quantity: int
    condition: str
    category_id: int