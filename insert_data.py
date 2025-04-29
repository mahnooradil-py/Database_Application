# insert_data.py
import sqlite3
from tables import get_connection

def insert_data():
    """
    Populate the database tables with sample data for donors, events, volunteers, and donations.
    """
    conn = get_connection()
    cursor = conn.cursor()

    #Data for DONORS table
    donors = [
        ("Alice", "Smith", "Smith Co.", "AB12XY", "25", "07123456789"),
        ("Bob", "Jones", None, "CD34ZT", "12", "07234567890"),
        ("Charlie", "Brown", "Charlie Designs", "EF56OP", "89", "07345678901")
    ]
    cursor.executemany("""
        INSERT INTO DONORS (first_name, surname, business_name, postcode, house_number, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, donors)

    #Data for EVENTS table
    events = [
        ("Fundraising Dinner", "Banquet Hall", "2025-11-01 18:00", 500.0),
        ("Food Drive", "Town Centre", "2025-12-15 10:00", 100.0),
        ("Charity Concert", "Theatre", "2026-01-10 19:00", 800.0)
    ]
    cursor.executemany("""
        INSERT INTO EVENTS (event_name, room_info, booking_datetime, cost)
        VALUES (?, ?, ?, ?)
    """, events)

    #Data for VOLUNTEERS table
    volunteers = [
        ("Lucy", "Green", "07456789012"),
        ("Tom", "Black", "07567890123"),
        ("Emma", "White", "07678901234")
    ]
    cursor.executemany("""
        INSERT INTO VOLUNTEERS (first_name, surname, phone_number)
        VALUES (?, ?, ?)
    """, volunteers)

    #Data for DONATIONS table
    donations = [
        (1, None, 1, 100.0, "2025-11-02", True, "Donation during dinner"),
        (2, 2, None, 50.0, "2025-12-16", False, "Charity donation"),
        (3, None, None, 200.0, "2026-01-11", True, None)
    ]
    cursor.executemany("""
        INSERT INTO DONATIONS (donor_id, event_id, volunteer_id, amount, donation_date, gift_aid, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, donations)

    conn.commit()
    conn.close()
    print("Data inserted successfully.")