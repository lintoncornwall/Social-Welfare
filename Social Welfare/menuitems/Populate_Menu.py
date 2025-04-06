#Populate_Menu.py
import csv

    
breakfast = {
    "Monday": {"Main 1": "Kidney", "Main 2": "Stewed Chicken", "Main 3": "Callaloo & saltfish", "Main 4": "Ackee & Saltfish", "Side 1": "Boiled food", "Side 2": "Fried Dumplings", "Side 3": "Breadfruit & Plantain", "Daily Special": "Peanut porridge", "Beverage 1": "Tea", "Beverage 2": "Coffee", "Beverage 3": "Orange juice", "Beverage 4": "Water"},
    "Tuesday": {"Main 1": "Steamed Cabbage", "Main 2": "Curried Chicken", "Main 3": "Liver", "Main 4": "Baked beans & Saltfish", "Side 1": "Boiled food", "Side 2": "Fried Dumplings", "Side 3": "Breadfruit & Plantain", "Daily Special": "Cornmeal porridge", "Beverage 1": "Tea", "Beverage 2": "Coffee", "Beverage 3": "Orange juice", "Beverage 4": "Water"},
    "Wednesday": {"Main 1": "Kidney", "Main 2": "Stewed Chicken", "Main 3": "Callaloo & Saltfish", "Main 4": "Ackee & Saltfish", "Side 1": "Boiled food", "Side 2": "Fried Dumplings", "Side 3": "Breadfruit & Plantain", "Daily Special": "Oatmeal porridge", "Beverage 1": "Tea", "Beverage 2": "Coffee", "Beverage 3": "Orange juice", "Beverage 4": "Water"},
    "Thursday": {"Main 1": "Steamed Cabbage", "Main 2": "Curried Chicken", "Main 3": "Liver", "Main 4": "Baked beans & Saltfish", "Side 1": "Boiled food", "Side 2": "Fried Dumplings", "Side 3": "Breadfruit & Plantain", "Daily Special": "Hominy Corn porridge", "Beverage 1": "Tea", "Beverage 2": "Coffee", "Beverage 3": "Orange juice", "Beverage 4": "Water"},
    "Friday": {"Main 1": "Salt Mackerel", "Main 2": "Ackee & Corned pork", "Main 3": "Roasted Saltfish", "Main 4": "Baked beans & Sausages", "Side 1": "Boiled food", "Side 2": "Fried Dumplings", "Side 3": "Breadfruit & Plantain", "Daily Special": "Peanut porridge", "Beverage 1": "Tea", "Beverage 2": "Coffee", "Beverage 3": "Orange juice", "Beverage 4": "Water"}
}
    
lunch = {
    "Monday": {"Main 1": "Baked Chicken", "Main 2": "Pineapple Chicken", "Main 3": "Steamed Fish", "Main 4": "Peppered Steak", "Main 5": "Curried Goat", "Side 1": "Rice & peas", "Side 2": "Callaloo rice", "Side 3": "Boiled food", "Side 4": "White rice", "Side 5": "Pumpkin rice", "Additional side 1": "Pasta", "Additional side 2": "Raw vegetables","Additional side 3": "Mashed potatoes", "Daily Special": "Chef's salad", "Beverage 1": "Soda", "Beverage 2": "Fruit juice", "Beverage 3": "Iced tea", "Beverage 4": "Water"},
    "Tuesday": {"Main 1": "Cow Foot", "Main 2": "Curried Chicken", "Main 3": "Ackee & Saltfish", "Main 4": "Barbi-fried Chicken", "Main 5": "Stewed peas w/ Chicken", "Side 1": "Rice & peas", "Side 2": "Callaloo rice", "Side 3": "Boiled food", "Side 4": "White rice", "Side 5": "Pumpkin rice", "Additional side 1": "Pasta", "Additional side 2": "Raw vegetables","Additional side 3": "Mashed potatoes", "Daily Special": "Chicken Alfredo", "Beverage 1": "Soda", "Beverage 2": "Fruit juice", "Beverage 3": "Iced tea", "Beverage 4": "Water"},
    "Wednesday": {"Main 1": "Roast Chicken", "Main 2": "Fried Chicken", "Main 3": "Fried Fish", "Main 4": "Barbi-fried Chicken", "Main 5": "Stewed peas w/ Pigstail", "Side 1": "Rice & peas", "Side 2": "Callaloo rice", "Side 3": "Boiled food", "Side 4": "White rice", "Side 5": "Pumpkin rice", "Additional side 1": "Pasta", "Additional side 2": "Raw vegetables","Additional side 3": "Mashed potatoes", "Daily Special": "Spaghetti & Meatballs", "Beverage 1": "Soda", "Beverage 2": "Fruit juice", "Beverage 3": "Iced tea", "Beverage 4": "Water"},
    "Thursday": {"Main 1": "Fried Chicken", "Main 2": "Curried Chicken", "Main 3": "Turkey Neck", "Main 4": "Barbi-fried Chicken", "Main 5": "Stewed Pork", "Side 1": "Rice & peas", "Side 2": "Callaloo rice", "Side 3": "Boiled food", "Side 4": "White rice", "Side 5": "Pumpkin rice", "Additional side 1": "Pasta", "Additional side 2": "Raw vegetables","Additional side 3": "Mashed potatoes", "Daily Special": "Chef's salad", "Beverage 1": "Soda", "Beverage 2": "Fruit juice", "Beverage 3": "Iced tea", "Beverage 4": "Water"},
    "Friday": {"Main 1": "Jerked Chicken", "Main 2": "Fried Chicken", "Main 3": "Jerked Pork", "Main 4": "Barbi-fried Chicken", "Main 5": "Roast Beef", "Side 1": "Rice & peas", "Side 2": "Callaloo rice", "Side 3": "Boiled food", "Side 4": "White rice", "Side 5": "Pumpkin rice", "Additional side 1": "Pasta", "Additional side 2": "Raw vegetables","Additional side 3": "Mashed potatoes", "Daily Special": "Shrimp Pasta", "Beverage 1": "Soda", "Beverage 2": "Fruit juice", "Beverage 3": "Iced tea", "Beverage 4": "Water"}
}

try:
    # Writing breakfast data to CSV
    with open('Breakfast.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Day', 'Main 1', 'Main 2', 'Main 3', 'Main 4', 'Side 1', 'Side 2', 'Side 3', 'Daily Special', 'Beverage 1', 'Beverage 2', 'Beverage 3', 'Beverage 4'])
        for day, menu in breakfast.items():
            row = [day] + [menu.get(f"Main {i}", "") for i in range(1, 5)] + \
                  [menu.get(f"Side {i}", "") for i in range(1, 4)] + \
                  [menu.get("Daily Special", "")] + \
                  [menu.get(f"Beverage {i}", "") for i in range(1, 5)]
            writer.writerow(row)

    # Writing lunch data to CSV
    with open('Lunch.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Day', 'Main 1', 'Main 2', 'Main 3', 'Main 4', 'Main 5', 'Side 1', 'Side 2', 'Side 3', 'Side 4', 'Side 5', 'Additional side 1', 'Additional side 2', 'Additional side 3', 'Daily Special', 'Beverage 1', 'Beverage 2', 'Beverage 3', 'Beverage 4'])
        for day, menu in lunch.items():
            row = [day] + [menu.get(f"Main {i}", "") for i in range(1, 6)] + \
                  [menu.get(f"Side {i}", "") for i in range(1, 6)] + \
                  [menu.get(f"Additional side {i}", "") for i in range(1, 4)] + \
                  [menu.get("Daily Special", "")] + \
                  [menu.get(f"Beverage {i}", "") for i in range(1, 5)]
            writer.writerow(row)

    print("Data written to CSV files: Breakfast.csv and Lunch.csv")

except Exception as e:
    print(f"An error occurred: {e}")
