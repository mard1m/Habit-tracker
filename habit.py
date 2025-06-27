"""
Habit Tracker Backend

A modular, testable, and extensible habit tracker backend in Python 3.7+.

Core features:
- OOP for habit modeling (Habit class)
- Functional analytics (analytics module)
- JSON file storage for persistence
- CLI interface (cli.py)
- Unit tests for validation

Components:
- Habit: Represents a single habit, supports check-off, serialization, and streak calculation
- HabitTracker: Manages habits, handles persistence, delegates analytics
- analytics: Pure functions for analytics (to be implemented)
- cli.py: Command-line interface (to be implemented)
- data/habits.json: JSON storage for all habits
"""

import json
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict
import os

class Habit:
    def __init__(self, name: str, periodicity: str, creation_date: Optional[str] = None, completions: Optional[List[str]] = None):
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.creation_date = creation_date or date.today().isoformat()
        self.completions = completions or []  # List of ISO-format date strings

    def check_off(self):
        today = date.today().isoformat()
        if today not in self.completions:
            self.completions.append(today)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'periodicity': self.periodicity,
            'creation_date': self.creation_date,
            'completions': self.completions
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data['name'],
            periodicity=data['periodicity'],
            creation_date=data.get('creation_date'),
            completions=data.get('completions', [])
        )

    def current_streak(self) -> int:
        # Calculate current streak based on completions and periodicity
        if not self.completions:
            return 0
        dates = sorted([datetime.strptime(d, '%Y-%m-%d').date() for d in self.completions], reverse=True)
        streak = 0
        today = date.today()
        delta = 1 if self.periodicity == 'daily' else 7
        for i, d in enumerate(dates):
            expected = today if i == 0 else dates[i-1] - timedelta(days=delta)
            if d == expected:
                streak += 1
                today = d
            else:
                break
        return streak

class HabitTracker:
    def __init__(self, storage_path: str = 'data/habits.json'):
        self.storage_path = storage_path
        self.habits: List[Habit] = []
        self._ensure_data_dir()
        self.load()

    def _ensure_data_dir(self):
        directory = os.path.dirname(self.storage_path)
        if directory:  # Only create directory if there is one
            os.makedirs(directory, exist_ok=True)

    def add_habit(self, habit: Habit):
        self.habits.append(habit)
        self.save()

    def delete_habit(self, name: str):
        self.habits = [h for h in self.habits if h.name != name]
        self.save()

    def check_off(self, name: str):
        for habit in self.habits:
            if habit.name == name:
                habit.check_off()
                self.save()
                return True
        return False

    def save(self):
        data = [habit.to_dict() for habit in self.habits]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            self.habits = [Habit.from_dict(h) for h in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.habits = []

def load_predefined_habits() -> list:
    """Return a list of predefined Habit objects with 4 weeks of example data."""
    habits = []
    # Daily habit: Drink Water
    daily = Habit(
        name='Drink Water',
        periodicity='daily',
        creation_date=(date.today() - timedelta(weeks=4)).isoformat(),
        completions=[
            (date.today() - timedelta(days=i)).isoformat() for i in range(28)
        ]
    )
    # Weekly habit: Call Parents
    weekly = Habit(
        name='Call Parents',
        periodicity='weekly',
        creation_date=(date.today() - timedelta(weeks=4)).isoformat(),
        completions=[
            (date.today() - timedelta(weeks=i)).isoformat() for i in range(4)
        ]
    )
    # More habits for diversity
    exercise = Habit(
        name='Exercise',
        periodicity='daily',
        creation_date=(date.today() - timedelta(weeks=4)).isoformat(),
        completions=[
            (date.today() - timedelta(days=i*2)).isoformat() for i in range(14)
        ]
    )
    read = Habit(
        name='Read Book',
        periodicity='daily',
        creation_date=(date.today() - timedelta(weeks=4)).isoformat(),
        completions=[
            (date.today() - timedelta(days=i*3)).isoformat() for i in range(10)
        ]
    )
    clean = Habit(
        name='Clean Room',
        periodicity='weekly',
        creation_date=(date.today() - timedelta(weeks=4)).isoformat(),
        completions=[
            (date.today() - timedelta(weeks=i)).isoformat() for i in range(4)
        ]
    )
    habits.extend([daily, weekly, exercise, read, clean])
    return habits

# Placeholder for analytics module
# def get_all_habits(habits: List[Habit]) -> List[Habit]: ...
# def filter_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]: ...
# def longest_streak(habits: List[Habit]) -> int: ...

# CLI entry point will be implemented in cli.py
