from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Task:
    title: str
    description: str = ""
    priority: str = "medium"
    deadline: Optional[str] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    completed: bool = False
    task_id: str = ""

    def __post_init__(self):
        self.title = self.title.strip()

        if not self.title:
            raise ValueError("Task title cannot be empty.")

        self.priority = self.priority.lower().strip()

        if self.priority not in {"low", "medium", "high"}:
            raise ValueError(
                "Priority must be low, medium, or high."
            )

        if self.estimated_hours < 0 or self.actual_hours < 0:
            raise ValueError("Hours cannot be negative.")

        if not self.task_id:
            self.task_id = str(uuid4())

        if self.deadline:
            try:
                datetime.strptime(self.deadline, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError(
                    "Deadline must use YYYY-MM-DD format."
                ) from exc

    def mark_completed(self):
        self.completed = True

    def update_actual_hours(self, hours: float):
        if hours < 0:
            raise ValueError("Hours cannot be negative.")

        self.actual_hours = hours

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)