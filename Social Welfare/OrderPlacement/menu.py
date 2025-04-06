#menu.py
import csv

def load_menu(filename):
    """Load the menu from a CSV file and return it as a dictionary."""
    menu = {}
    try:
        with open(filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                day = row['Day']
                menu[day] = {key: row[key] for key in row.keys() if key != 'Day'}
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return {}
    except Exception as e:
        print(f"Error loading menu from {filename}: {e}")
        return {}
    return menu