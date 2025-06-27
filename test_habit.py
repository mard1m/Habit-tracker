import unittest
import os
import tempfile
import shutil
from datetime import date, timedelta
from habit import Habit, HabitTracker, load_predefined_habits
import analytics

class TestHabit(unittest.TestCase):
    """Test the Habit class functionality."""
    
    def test_habit_creation(self):
        """Test habit creation with basic attributes."""
        habit = Habit('Test Habit', 'daily')
        self.assertEqual(habit.name, 'Test Habit')
        self.assertEqual(habit.periodicity, 'daily')
        self.assertIsInstance(habit.creation_date, str)
        self.assertEqual(len(habit.completions), 0)
    
    def test_habit_creation_with_custom_date(self):
        """Test habit creation with custom creation date."""
        custom_date = '2024-01-01'
        habit = Habit('Test', 'weekly', creation_date=custom_date)
        self.assertEqual(habit.creation_date, custom_date)
    
    def test_check_off_daily_habit(self):
        """Test checking off a daily habit."""
        habit = Habit('Test', 'daily')
        today = date.today().isoformat()
        
        # Check off for the first time
        habit.check_off()
        self.assertIn(today, habit.completions)
        self.assertEqual(len(habit.completions), 1)
        
        # Check off again (should not duplicate)
        habit.check_off()
        self.assertEqual(len(habit.completions), 1)
    
    def test_check_off_weekly_habit(self):
        """Test checking off a weekly habit."""
        habit = Habit('Test', 'weekly')
        today = date.today().isoformat()
        
        habit.check_off()
        self.assertIn(today, habit.completions)
    
    def test_serialization(self):
        """Test habit serialization to and from dictionary."""
        habit = Habit('Test Habit', 'daily')
        habit.check_off()
        
        # Serialize
        data = habit.to_dict()
        self.assertIn('name', data)
        self.assertIn('periodicity', data)
        self.assertIn('creation_date', data)
        self.assertIn('completions', data)
        
        # Deserialize
        habit2 = Habit.from_dict(data)
        self.assertEqual(habit2.name, habit.name)
        self.assertEqual(habit2.periodicity, habit.periodicity)
        self.assertEqual(habit2.creation_date, habit.creation_date)
        self.assertEqual(habit2.completions, habit.completions)
    
    def test_current_streak_daily(self):
        """Test streak calculation for daily habits."""
        habit = Habit('Test', 'daily')
        
        # No completions
        self.assertEqual(habit.current_streak(), 0)
        
        # Add some completions
        today = date.today()
        habit.completions = [
            (today - timedelta(days=i)).isoformat() for i in range(3)
        ]
        self.assertEqual(habit.current_streak(), 3)
    
    def test_current_streak_weekly(self):
        """Test streak calculation for weekly habits."""
        habit = Habit('Test', 'weekly')
        
        # Add weekly completions
        today = date.today()
        habit.completions = [
            (today - timedelta(weeks=i)).isoformat() for i in range(2)
        ]
        self.assertEqual(habit.current_streak(), 2)

class TestHabitTracker(unittest.TestCase):
    """Test the HabitTracker class functionality."""
    
    def setUp(self):
        """Set up test environment with temporary file."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_habits.json')
        self.tracker = HabitTracker(self.test_file)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_add_habit(self):
        """Test adding a habit to the tracker."""
        habit = Habit('Test', 'daily')
        self.tracker.add_habit(habit)
        
        self.assertEqual(len(self.tracker.habits), 1)
        self.assertEqual(self.tracker.habits[0].name, 'Test')
    
    def test_delete_habit(self):
        """Test deleting a habit from the tracker."""
        habit1 = Habit('Test1', 'daily')
        habit2 = Habit('Test2', 'weekly')
        self.tracker.add_habit(habit1)
        self.tracker.add_habit(habit2)
        
        self.assertEqual(len(self.tracker.habits), 2)
        
        self.tracker.delete_habit('Test1')
        self.assertEqual(len(self.tracker.habits), 1)
        self.assertEqual(self.tracker.habits[0].name, 'Test2')
    
    def test_check_off_existing_habit(self):
        """Test checking off an existing habit."""
        habit = Habit('Test', 'daily')
        self.tracker.add_habit(habit)
        
        result = self.tracker.check_off('Test')
        self.assertTrue(result)
        self.assertEqual(len(habit.completions), 1)
    
    def test_check_off_nonexistent_habit(self):
        """Test checking off a habit that doesn't exist."""
        result = self.tracker.check_off('Nonexistent')
        self.assertFalse(result)
    
    def test_persistence(self):
        """Test saving and loading habits from file."""
        habit = Habit('Test', 'daily')
        self.tracker.add_habit(habit)
        
        # Create new tracker instance to test loading
        tracker2 = HabitTracker(self.test_file)
        self.assertEqual(len(tracker2.habits), 1)
        self.assertEqual(tracker2.habits[0].name, 'Test')
    
    def test_load_empty_file(self):
        """Test loading when file doesn't exist."""
        tracker = HabitTracker('nonexistent_file.json')
        self.assertEqual(len(tracker.habits), 0)

class TestAnalytics(unittest.TestCase):
    """Test the analytics module functionality."""
    
    def setUp(self):
        """Set up test habits for analytics testing."""
        self.habits = [
            Habit('Daily1', 'daily'),
            Habit('Daily2', 'daily'),
            Habit('Weekly1', 'weekly'),
            Habit('Weekly2', 'weekly')
        ]
        
        # Add some completion data
        today = date.today()
        self.habits[0].completions = [(today - timedelta(days=i)).isoformat() for i in range(5)]
        self.habits[1].completions = [(today - timedelta(days=i)).isoformat() for i in range(3)]
        self.habits[2].completions = [(today - timedelta(weeks=i)).isoformat() for i in range(2)]
        self.habits[3].completions = [(today - timedelta(weeks=i)).isoformat() for i in range(4)]
    
    def test_get_all_habits(self):
        """Test getting all habits."""
        result = analytics.get_all_habits(self.habits)
        self.assertEqual(len(result), 4)
        self.assertEqual(result, self.habits)
    
    def test_filter_by_periodicity_daily(self):
        """Test filtering habits by daily periodicity."""
        result = analytics.filter_by_periodicity(self.habits, 'daily')
        self.assertEqual(len(result), 2)
        for habit in result:
            self.assertEqual(habit.periodicity, 'daily')
    
    def test_filter_by_periodicity_weekly(self):
        """Test filtering habits by weekly periodicity."""
        result = analytics.filter_by_periodicity(self.habits, 'weekly')
        self.assertEqual(len(result), 2)
        for habit in result:
            self.assertEqual(habit.periodicity, 'weekly')
    
    def test_longest_streak(self):
        """Test finding the longest streak among all habits."""
        result = analytics.longest_streak(self.habits)
        self.assertEqual(result, 5)  # Daily1 has the longest streak
    
    def test_longest_streak_empty_list(self):
        """Test longest streak with empty habit list."""
        result = analytics.longest_streak([])
        self.assertEqual(result, 0)
    
    def test_longest_streak_per_habit(self):
        """Test getting streaks for each habit."""
        result = analytics.longest_streak_per_habit(self.habits)
        self.assertIn('Daily1', result)
        self.assertIn('Weekly2', result)
        self.assertEqual(result['Daily1'], 5)
        self.assertEqual(result['Weekly2'], 4)

class TestPredefinedHabits(unittest.TestCase):
    """Test the predefined habits functionality."""
    
    def test_load_predefined_habits(self):
        """Test loading predefined habits."""
        habits = load_predefined_habits()
        
        # Should have 5 habits
        self.assertEqual(len(habits), 5)
        
        # Should have at least one daily and one weekly habit
        daily_habits = [h for h in habits if h.periodicity == 'daily']
        weekly_habits = [h for h in habits if h.periodicity == 'weekly']
        
        self.assertGreaterEqual(len(daily_habits), 1)
        self.assertGreaterEqual(len(weekly_habits), 1)
        
        # Check specific habits exist
        habit_names = [h.name for h in habits]
        self.assertIn('Drink Water', habit_names)
        self.assertIn('Call Parents', habit_names)
        self.assertIn('Exercise', habit_names)
        self.assertIn('Read Book', habit_names)
        self.assertIn('Clean Room', habit_names)
        
        # Check that all habits have completion data
        for habit in habits:
            self.assertGreater(len(habit.completions), 0)
            self.assertIsInstance(habit.creation_date, str)

if __name__ == '__main__':
    unittest.main() 