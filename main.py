# main.py
from tables import create_tables
from insert_data import insert_data
from donor import donor_menu
from event import event_menu
from donation import donation_menu
from volunteer import volunteer_menu
from search import search_menu

def main():
    """
    Main function for the charity donation management application.
    Provides an interactive menu to access various operations.
    """
    # Create the database tables and insert s data
    create_tables()  # Ensures the database schema is created
    insert_data()    # Populates the tables with data for testing

    while True:
        print("\n========== Charity Donation Management ==========")
        print("Please select an option:")
        print("1. Donors")
        print("2. Events")
        print("3. Donations")
        print("4. Volunteers")
        print("5. Search Donations")
        print("6. Exit Application")
        choice = input("Enter your choice (1-6): ")

        # Navigate to the appropriate menu based on user input
        if choice == "1":
            donor_menu()
        elif choice == "2":
            event_menu()
        elif choice == "3":
            donation_menu()
        elif choice == "4":
            volunteer_menu()
        elif choice == "5":
            search_menu()
        elif choice == "6":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()