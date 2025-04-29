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

def add_donor():
    """
    Add a new donor to the database. Prompts the user for donor information and inserts it into the DONORS table.
    """
    print("\n--- Add New Donor ---")
    first_name = input("Enter donor's first name: ")
    surname = input("Enter donor's surname: ")
    business_name = input("Enter donor's business name (optional): ")
    postcode = input("Enter donor's postcode: ")
    house_number = input("Enter donor's house number: ")
    phone_number = input("Enter donor's phone number: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DONORS (first_name, surname, business_name, postcode, house_number, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (first_name, surname, business_name, postcode, house_number, phone_number))
    conn.commit()
    conn.close()
    print("Donor added successfully.")

def view_donors():
    """
    Display a list of all donors in the database, including their details.
    """
    print("\n--- List of Donors ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONORS")
    for donor in cursor:
        print(donor)  # Display each donor as a tuple
    conn.close()

def update_donor():
    """
    Update the details of an existing donor.
    Prompts the user for updated details and allows blank input to retain current values.
    """
    donor_id = input("\nEnter donor ID to update: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DONORS WHERE donor_id = ?", (donor_id,))
    donor = cursor.fetchone()
    if donor:
        print("Leave blank to keep the current details.")
        new_first_name = input(f"First name ({donor[1]}): ") or donor[1]
        new_surname = input(f"Surname ({donor[2]}): ") or donor[2]
        new_business_name = input(f"Business name ({donor[3]}): ") or donor[3]
        new_postcode = input(f"Postcode ({donor[4]}): ") or donor[4]
        new_house_number = input(f"House number ({donor[5]}): ") or donor[5]
        new_phone_number = input(f"Phone number ({donor[6]}): ") or donor[6]
        cursor.execute("""
            UPDATE DONORS
            SET first_name = ?, surname = ?, business_name = ?, postcode = ?, house_number = ?, phone_number = ?
            WHERE donor_id = ?
        """, (new_first_name, new_surname, new_business_name, new_postcode, new_house_number, new_phone_number, donor_id))
        conn.commit()
        print("Donor updated successfully.")
    else:
        print("Donor not found.")
    conn.close()

def delete_donor():
    """
    Delete a donor from the database. Ensures the donor is not referenced in other tables before deletion.
    """
    donor_id = input("\nEnter donor ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the donor is linked to donations
    cursor.execute("SELECT * FROM DONATIONS WHERE donor_id = ?", (donor_id,))
    donation_link = cursor.fetchone()

    if donation_link:
        print("Cannot delete this donor. They have existing donations.")
    else:
        cursor.execute("DELETE FROM DONORS WHERE donor_id = ?", (donor_id,))
        conn.commit()
        print("Donor deleted successfully.")
    conn.close()

def donor_menu():
    """
    Display the donor menu and execute user-selected operations.
    """
    while True:
        print("\n========== Donor Operations ==========")
        print("1. Add Donor")
        print("2. View Donors")
        print("3. Update Donor")
        print("4. Delete Donor")
        print("5. Return to Main Menu")
        choice = input("Select an option (1-5): ")
        if choice == "1":
            add_donor()
        elif choice == "2":
            view_donors()
        elif choice == "3":
            update_donor()
        elif choice == "4":
            delete_donor()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")