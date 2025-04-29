import sqlite3

def get_connection():
    """
    Establish a connection to the charity donations database and enable foreign key constraints.
    Returns:
        Connection object for the database.
    """
    conn = sqlite3.connect("charity_donations.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def search_donations_by_donor():
    """
    Search and display donations linked to a specific donor by their donor ID.
    """
    donor_id = input("\nEnter donor ID to search for donations: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONATIONS WHERE donor_id = ?", (donor_id,))
    results = cursor.fetchall()
    if results:
        print(f"\nDonations by Donor ID {donor_id}:")
        for donation in results:
            print(donation)  # Display each donation as a tuple
    else:
        print("No donations found for this donor.")
    conn.close()

def search_donations_by_event():
    """
    Search and display donations linked to a specific event by its event ID.
    """
    event_id = input("\nEnter event ID to search for donations: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONATIONS WHERE event_id = ?", (event_id,))
    results = cursor.fetchall()
    if results:
        print(f"\nDonations for Event ID {event_id}:")
        for donation in results:
            print(donation)  # Display each donation as a tuple
    else:
        print("No donations found for this event.")
    conn.close()

def search_donations_by_volunteer():
    """
    Search and display donations linked to a specific volunteer by their volunteer ID.
    """
    volunteer_id = input("\nEnter volunteer ID to search for donations: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONATIONS WHERE volunteer_id = ?", (volunteer_id,))
    results = cursor.fetchall()
    if results:
        print(f"\nDonations linked to Volunteer ID {volunteer_id}:")
        for donation in results:
            print(donation)  # Display each donation as a tuple
    else:
        print("No donations found for this volunteer.")
    conn.close()

def search_menu():
    """
    Display the search menu and execute user-selected search operations.
    """
    while True:
        print("\n========== Search Donations ==========")
        print("1. Search Donations by Donor")
        print("2. Search Donations by Event")
        print("3. Search Donations by Volunteer")
        print("4. Return to Main Menu")
        choice = input("Select an option (1-4): ")
        if choice == "1":
            search_donations_by_donor()
        elif choice == "2":
            search_donations_by_event()
        elif choice == "3":
            search_donations_by_volunteer()
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")