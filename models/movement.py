from dataclasses import dataclass


@dataclass
class Movement:
    id: int
    equipment_id: int
    movement_type: str
    quantity: int
    movement_date: str