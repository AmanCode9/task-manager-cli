from dataclasses import dataclass, asdict, field
from typing import Optional, List
import json
from datetime import datetime

DATA_FILE = "tasks.json"
DATE_FORMAT = "%Y-%m-%d"

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    due_date: Optional[str] = None  
    status: str = "Pending"         
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Task(**d)

class TaskManager:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.tasks: List[Task] = []
        self._load()

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def add_task(self, title, description="", due_date=None):
        task = Task(id=self._next_id(), title=title, description=description, due_date=due_date)
        self.tasks.append(task)
        self.save()
        return task

    def get_all(self):
        return list(self.tasks)

    def find(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def mark_complete(self, task_id):
        t = self.find(task_id)
        if t:
            t.status = "Completed"
            self.save()
            return True
        return False

    def delete(self, task_id):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < before:
            self.save()
            return True
        return False

    def update(self, task_id, title=None, description=None, due_date=None):
        t = self.find(task_id)
        if not t:
            return False
        if title is not None:
            t.title = title
        if description is not None:
            t.description = description
        if due_date is not None:
            t.due_date = due_date
        self.save()
        return True

    def search(self, keyword):
        k = keyword.lower()
        return [t for t in self.tasks if k in t.title.lower() or k in t.description.lower()]
