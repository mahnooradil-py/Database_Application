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

def add_donation():
    """
    Add a new donation to the database. Prompts the user for donation details and inserts them into the DONATIONS table.
    """
    print("\n--- Add New Donation ---")
    donor_id = input("Enter donor ID: ")
    event_id = input("Enter event ID (optional): ")
    volunteer_id = input("Enter volunteer ID (optional): ")
    try:
        amount = float(input("Enter donation amount: "))
    except ValueError:
        print("Amount must be a valid number.")
        return
    donation_date = input("Enter donation date (YYYY-MM-DD): ")
    gift_aid = input("Gift Aid? (yes/no): ").strip().lower() in ["yes", "y"]
    notes = input("Enter additional notes (optional): ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DONATIONS (donor_id, event_id, volunteer_id, amount, donation_date, gift_aid, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (donor_id, event_id or None, volunteer_id or None, amount, donation_date, gift_aid, notes))
    conn.commit()
    conn.close()
    print("Donation added successfully.")

def view_donations():
    """
    Display a list of all donations in the database, including their details.
    """
    print("\n--- List of Donations ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONATIONS")
    for donation in cursor:
        print(donation)  # Display each donation as a tuple
    conn.close()

def delete_donation():
    """
    Delete a donation from the database using its donation ID.
    """
    donation_id = input("Enter the donation ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DONATIONS WHERE donation_id = ?", (donation_id,))
    conn.commit()
    conn.close()
    print("Donation deleted successfully.")

def donation_menu():
    """
    Display the donation menu and execute user-selected operations.
    """
    while True:
        print("\n========== Donation Operations ==========")
        print("1. Add Donation")
        print("2. View Donations")
        print("3. Delete Donation")
        print("4. Return to Main Menu")
        choice = input("Select an option (1-4): ")
        if choice == "1":
            add_donation()
        elif choice == "2":
            view_donations()
        elif choice == "3":
            delete_donation()
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")