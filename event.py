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

def add_event():
    """
    Add a new event to the database. Prompts the user for event details and inserts them into the EVENTS table.
    """
    print("\n--- Add New Event ---")
    event_name = input("Enter event name: ")
    room_info = input("Enter room information: ")
    booking_datetime = input("Enter booking date and time (YYYY-MM-DD HH:MM): ")
    try:
        cost = float(input("Enter event cost: "))
    except ValueError:
        print("Cost must be a number.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO EVENTS (event_name, room_info, booking_datetime, cost)
        VALUES (?, ?, ?, ?)
    """, (event_name, room_info, booking_datetime, cost))
    conn.commit()
    conn.close()
    print("Event added successfully.")

def view_events():
    """
    Display a list of all events in the database, including their details.
    """
    print("\n--- List of Events ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENTS")
    for event in cursor:
        print(event)  # Display each event as a tuple
    conn.close()

def update_event():
    """
    Update the details of an existing event.
    Prompts the user for updated details and allows blank input to retain current values.
    """
    event_id = input("\nEnter event ID to update: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENTS WHERE event_id = ?", (event_id,))
    event = cursor.fetchone()
    if event:
        print("Leave blank to keep the current details.")
        new_event_name = input(f"Event name ({event[1]}): ") or event[1]
        new_room_info = input(f"Room information ({event[2]}): ") or event[2]
        new_booking_datetime = input(f"Booking date and time ({event[3]}): ") or event[3]
        try:
            new_cost = float(input(f"Cost ({event[4]}): ")) or event[4]
        except ValueError:
            print("Cost must be a number.")
            return
        cursor.execute("""
            UPDATE EVENTS
            SET event_name = ?, room_info = ?, booking_datetime = ?, cost = ?
            WHERE event_id = ?
        """, (new_event_name, new_room_info, new_booking_datetime, new_cost, event_id))
        conn.commit()
        print("Event updated successfully.")
    else:
        print("Event not found.")
    conn.close()

def delete_event():
    """
    Delete an event from the database. Ensures the event is not referenced in other tables before deletion.
    """
    event_id = input("\nEnter event ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the event is linked to donations
    cursor.execute("SELECT * FROM DONATIONS WHERE event_id = ?", (event_id,))
    donation_link = cursor.fetchone()

    if donation_link:
        print("Cannot delete this event. It has existing donations.")
    else:
        cursor.execute("DELETE FROM EVENTS WHERE event_id = ?", (event_id,))
        conn.commit()
        print("Event deleted successfully.")
    conn.close()

def event_menu():
    """
    Display the event menu and execute user-selected operations.
    """
    while True:
        print("\n========== Event Operations ==========")
        print("1. Add Event")
        print("2. View Events")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. Return to Main Menu")
        choice = input("Select an option (1-5): ")
        if choice == "1":
            add_event()
        elif choice == "2":
            view_events()
        elif choice == "3":
            update_event()
        elif choice == "4":
            delete_event()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")