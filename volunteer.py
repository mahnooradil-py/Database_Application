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

def add_volunteer():
    """
    Add a new volunteer to the database. Prompts the user for details and inserts them into the VOLUNTEERS table.
    """
    print("\n--- Add New Volunteer ---")
    first_name = input("Enter volunteer's first name: ")
    surname = input("Enter volunteer's surname: ")
    phone_number = input("Enter volunteer's phone number: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO VOLUNTEERS (first_name, surname, phone_number)
        VALUES (?, ?, ?)
    """, (first_name, surname, phone_number))
    conn.commit()
    conn.close()
    print("Volunteer added successfully.")

def view_volunteers():
    """
    Display a list of all volunteers in the database, including their details.
    """
    print("\n--- List of Volunteers ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VOLUNTEERS")
    for volunteer in cursor:
        print(volunteer)  # Display each volunteer as a tuple
    conn.close()

def update_volunteer():
    """
    Update the details of an existing volunteer.
    Prompts the user for updated details and allows blank input to retain current values.
    """
    volunteer_id = input("\nEnter volunteer ID to update: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VOLUNTEERS WHERE volunteer_id = ?", (volunteer_id,))
    volunteer = cursor.fetchone()
    if volunteer:
        print("Leave blank to keep the current details.")
        new_first_name = input(f"First name ({volunteer[1]}): ") or volunteer[1]
        new_surname = input(f"Surname ({volunteer[2]}): ") or volunteer[2]
        new_phone_number = input(f"Phone number ({volunteer[3]}): ") or volunteer[3]
        cursor.execute("""
            UPDATE VOLUNTEERS
            SET first_name = ?, surname = ?, phone_number = ?
            WHERE volunteer_id = ?
        """, (new_first_name, new_surname, new_phone_number, volunteer_id))
        conn.commit()
        print("Volunteer updated successfully.")
    else:
        print("Volunteer not found.")
    conn.close()

def delete_volunteer():
    """
    Delete a volunteer from the database. Ensures the volunteer is not referenced elsewhere before deletion.
    """
    volunteer_id = input("\nEnter volunteer ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the volunteer is linked to events or donations
    cursor.execute("SELECT * FROM EVENT_VOLUNTEERS WHERE volunteer_id = ?", (volunteer_id,))
    event_link = cursor.fetchone()
    cursor.execute("SELECT * FROM DONATIONS WHERE volunteer_id = ?", (volunteer_id,))
    donation_link = cursor.fetchone()

    if event_link or donation_link:
        print("Cannot delete this volunteer. They are referenced in other tables.")
    else:
        cursor.execute("DELETE FROM VOLUNTEERS WHERE volunteer_id = ?", (volunteer_id,))
        conn.commit()
        print("Volunteer deleted successfully.")
    conn.close()

def volunteer_menu():
    """
    Display the volunteer menu and execute user-selected operations.
    """
    while True:
        print("\n========== Volunteer Operations ==========")
        print("1. Add Volunteer")
        print("2. View Volunteers")
        print("3. Update Volunteer")
        print("4. Delete Volunteer")
        print("5. Return to Main Menu")
        choice = input("Select an option (1-5): ")
        if choice == "1":
            add_volunteer()
        elif choice == "2":
            view_volunteers()
        elif choice == "3":
            update_volunteer()
        elif choice == "4":
            delete_volunteer()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")