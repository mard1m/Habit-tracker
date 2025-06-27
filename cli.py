from habit import Habit, HabitTracker, load_predefined_habits
import analytics

def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("           HABIT TRACKER")
    print("="*50)
    print("1. Create a new habit")
    print("2. Delete a habit")
    print("3. Check off a habit (mark as completed)")
    print("4. List all habits")
    print("5. View habit statistics")
    print("6. Load predefined habits (for testing)")
    print("7. Exit")
    print("="*50)

def create_habit(tracker):
    """Interactive habit creation."""
    print("\n--- Create New Habit ---")
    name = input("Enter habit name: ").strip()
    if not name:
        print("Habit name cannot be empty!")
        return
    
    print("Select periodicity:")
    print("1. Daily")
    print("2. Weekly")
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        periodicity = "daily"
    elif choice == "2":
        periodicity = "weekly"
    else:
        print("Invalid choice! Please enter 1 or 2.")
        return
    
    habit = Habit(name=name, periodicity=periodicity)
    tracker.add_habit(habit)
    print(f"✅ Habit '{name}' created successfully!")

def delete_habit(tracker):
    """Interactive habit deletion."""
    if not tracker.habits:
        print("No habits to delete!")
        return
    
    print("\n--- Delete Habit ---")
    print("Current habits:")
    for i, habit in enumerate(tracker.habits, 1):
        print(f"{i}. {habit.name} ({habit.periodicity})")
    
    try:
        choice = int(input("Enter the number of the habit to delete: "))
        if 1 <= choice <= len(tracker.habits):
            habit = tracker.habits[choice - 1]
            tracker.delete_habit(habit.name)
            print(f"✅ Habit '{habit.name}' deleted successfully!")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number!")

def check_off_habit(tracker):
    """Interactive habit check-off."""
    if not tracker.habits:
        print("No habits to check off!")
        return
    
    print("\n--- Check Off Habit ---")
    print("Current habits:")
    for i, habit in enumerate(tracker.habits, 1):
        print(f"{i}. {habit.name} ({habit.periodicity})")
    
    try:
        choice = int(input("Enter the number of the habit to check off: "))
        if 1 <= choice <= len(tracker.habits):
            habit = tracker.habits[choice - 1]
            if tracker.check_off(habit.name):
                print(f"✅ '{habit.name}' marked as completed!")
            else:
                print("❌ Failed to check off habit!")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number!")

def list_habits(tracker):
    """Display all habits with their details."""
    if not tracker.habits:
        print("No habits found!")
        return
    
    print("\n--- Your Habits ---")
    for i, habit in enumerate(tracker.habits, 1):
        streak = habit.current_streak()
        print(f"{i}. {habit.name}")
        print(f"   Periodicity: {habit.periodicity}")
        print(f"   Created: {habit.creation_date}")
        print(f"   Current streak: {streak}")
        print(f"   Total completions: {len(habit.completions)}")
        print()

def view_statistics(tracker):
    """Display habit statistics and analytics."""
    if not tracker.habits:
        print("No habits to analyze!")
        return
    
    print("\n--- Habit Statistics ---")
    
    # Basic stats
    total_habits = len(tracker.habits)
    daily_habits = len(analytics.filter_by_periodicity(tracker.habits, "daily"))
    weekly_habits = len(analytics.filter_by_periodicity(tracker.habits, "weekly"))
    
    print(f"Total habits: {total_habits}")
    print(f"Daily habits: {daily_habits}")
    print(f"Weekly habits: {weekly_habits}")
    print()
    
    # Streak analysis
    longest_streak = analytics.longest_streak(tracker.habits)
    print(f"Longest current streak: {longest_streak}")
    print()
    
    # Per-habit streaks
    print("Current streaks by habit:")
    streaks = analytics.longest_streak_per_habit(tracker.habits)
    for habit_name, streak in streaks.items():
        print(f"  {habit_name}: {streak}")

def load_predefined(tracker):
    """Load predefined habits for testing."""
    print("\n--- Loading Predefined Habits ---")
    predefined_habits = load_predefined_habits()
    
    print("Loading 5 predefined habits with 4 weeks of example data:")
    for habit in predefined_habits:
        print(f"  • {habit.name} ({habit.periodicity}) - {len(habit.completions)} completions")
    
    tracker.habits = predefined_habits
    tracker.save()
    print("\n✅ Predefined habits loaded successfully!")
    print("You can now view, check off, and analyze these example habits.")

def main():
    """Main interactive loop."""
    tracker = HabitTracker()
    
    print("Welcome to Habit Tracker!")
    print("This app helps you build and track your daily and weekly habits.")
    
    # Auto-load predefined habits if no habits exist
    if not tracker.habits:
        print("\nNo habits found. Loading predefined example habits...")
        load_predefined(tracker)
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            create_habit(tracker)
        elif choice == "2":
            delete_habit(tracker)
        elif choice == "3":
            check_off_habit(tracker)
        elif choice == "4":
            list_habits(tracker)
        elif choice == "5":
            view_statistics(tracker)
        elif choice == "6":
            load_predefined(tracker)
        elif choice == "7":
            print("Thank you for using Habit Tracker!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main() 