# tables.py
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

def create_tables():
    """
    Create all necessary tables with appropriate relationships in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create DONORS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DONORS (
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        business_name TEXT,
        postcode TEXT NOT NULL,
        house_number TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )
    """)

    # Create DONATIONS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DONATIONS (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        donation_date TEXT NOT NULL,
        gift_aid BOOLEAN NOT NULL,
        notes TEXT,
        event_id INTEGER,
        volunteer_id INTEGER,
        FOREIGN KEY (donor_id) REFERENCES DONORS(donor_id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES EVENTS(event_id) ON DELETE CASCADE,
        FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEERS(volunteer_id)
    )
    """)

    # Create VOLUNTEERS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS VOLUNTEERS (
        volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )
    """)

    # Create EVENTS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EVENTS (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        room_info TEXT NOT NULL,
        booking_datetime TEXT NOT NULL,
        cost REAL NOT NULL
    )
    """)

    # Create EVENT_VOLUNTEERS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EVENT_VOLUNTEERS (
        event_id INTEGER NOT NULL,
        volunteer_id INTEGER NOT NULL,
        PRIMARY KEY (event_id, volunteer_id),
        FOREIGN KEY (event_id) REFERENCES EVENTS(event_id),
        FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEERS(volunteer_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")