#content_editor.py
import csv
import json
import os

def edit_menu():
    """Allow the user to edit the breakfast or lunch menu CSV file."""
    print("\nEdit Menu Content")
    print("1. Edit Breakfast Menu")
    print("2. Edit Lunch Menu")
    choice = input("Select an option (1 or 2): ").strip()
    
    if choice == '1':
        filename = 'Breakfast.csv'
    elif choice == '2':
        filename = 'Lunch.csv'
    else:
        print("Invalid choice.")
        return

    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return

    # Read the current CSV content
    with open(filename, 'r', newline='') as csvfile:
        reader = list(csv.reader(csvfile))
    
    # Display the content with row numbers
    print("\nCurrent Menu Content:")
    for idx, row in enumerate(reader):
        print(f"{idx}: {row}")

    try:
        row_num = int(input("\nEnter the row number you want to edit: "))
        if row_num < 0 or row_num >= len(reader):
            print("Invalid row number.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Get new data for the selected row
    new_row = input("Enter new row data as comma-separated values: ")
    new_row = [val.strip() for val in new_row.split(',')]
    reader[row_num] = new_row

    # Write the updated content back to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(reader)
    
    print("Menu updated successfully.")

def edit_opening_hours():
    """Allow the user to change the restaurant's opening hours."""
    filename = 'hours.json'
    # Load existing hours if available
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                hours = json.load(f)
            except json.JSONDecodeError:
                hours = {}
    else:
        hours = {}

    print("\nCurrent Opening Hours:")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        print(f"{day}: {hours.get(day, 'Not set')}")
    
    print("\nEnter new opening hours for each day (press Enter to leave unchanged):")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        new_hours = input(f"{day}: ").strip()
        if new_hours:
            hours[day] = new_hours

    with open(filename, 'w') as f:
        json.dump(hours, f, indent=4)
    
    print("Opening hours updated successfully.")

def edit_content_menu():
    """Provide a sub-menu to choose which content to edit."""
    while True:
        print("\n--- Edit Content ---")
        print("1. Edit Menu Items (Breakfast/Lunch)")
        print("2. Edit Opening Hours")
        print("3. Return to Main Menu")
        choice = input("Select an option (1/2/3): ").strip()

        if choice == '1':
            edit_menu()
        elif choice == '2':
            edit_opening_hours()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
