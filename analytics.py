from typing import List
from habit import Habit

def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """Return all tracked habits."""
    return habits

def filter_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Filter habits by periodicity ('daily' or 'weekly')."""
    return [h for h in habits if h.periodicity == periodicity]

def longest_streak(habits: List[Habit]) -> int:
    """Return the longest streak among all habits."""
    if not habits:
        return 0
    return max((h.current_streak() for h in habits), default=0)

def longest_streak_per_habit(habits: List[Habit]) -> dict:
    """Return the longest streak for each habit by name."""
    return {h.name: h.current_streak() for h in habits} 