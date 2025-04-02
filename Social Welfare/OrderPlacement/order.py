#order.py
import datetime
import os
import json
from .menu import load_menu
from .receipt import genReceipt
from .favorites import editFaves
from .delivery import requestDelivery
from RefundManagement.refund_manager import RefundManager  # Assuming this exists

def get_meal_choices(menu, day, is_lunch_time=False):
    """Display and get meal choices for a specific day."""
    if day not in menu:
        print(f"Error: No menu available for {day}.")
        return None, None, None, None
    
    choices = menu[day]
    print(f"Available meals for {day}:")
    
    main_choices = [choices.get(f'Main {i}') for i in range(1, 6) if choices.get(f'Main {i}')]
    side_choices = [choices.get(f'Side {i}') for i in range(1, 6) if choices.get(f'Side {i}')]
    
    print("Main options:")
    for idx, item in enumerate(main_choices, 1):
        print(f"{idx}. {item}")
    
    print("\nSide options:")
    for idx, item in enumerate(side_choices, 1):
        print(f"{idx}. {item}")
    
    # Get user selections with error handling for main and side choices
    main_choice = None
    while main_choice is None:
        try:
            main_choice = int(input("Choose the number of the Main course: ")) - 1
            if main_choice < 0 or main_choice >= len(main_choices):
                raise ValueError("Invalid choice, please select a valid main course number.")
        except ValueError as e:
            print(e)
            main_choice = None
    
    side_choice = None
    while side_choice is None:
        try:
            side_choice = int(input("Choose the number of the Side dish: ")) - 1
            if side_choice < 0 or side_choice >= len(side_choices):
                raise ValueError("Invalid choice, please select a valid side dish number.")
        except ValueError as e:
            print(e)
            side_choice = None

    daily_special_input = input(f"Would you like the Daily Special: {choices.get('Daily Special', 'None')}? (y/n): ").strip().lower()
    special = choices.get('Daily Special', '') if daily_special_input == 'y' else None
    
    customize = input(f"Do you want to customize your {main_choices[main_choice]} meal? (y/n): ").strip().lower()
    if customize == 'y':
        customization = input(f"How would you like to customize your {main_choices[main_choice]} meal?: ")
    else:
        customization = "No customization"
    
    return main_choices[main_choice], side_choices[side_choice], special, customization

def get_beverage_choice(meal_type):
    """Get beverage choice based on meal time."""
    if meal_type == 'breakfast':
        beverages = ['Tea', 'Coffee', 'Orange Juice', 'Water']
        prices = {'Tea': 150, 'Coffee': 150, 'Orange Juice': 200, 'Water': 100}
    elif meal_type == 'lunch':
        beverages = ['Soda', 'Fruit Juice', 'Iced Tea', 'Water']
        prices = {'Soda': 150, 'Fruit Juice': 250, 'Iced Tea': 200, 'Water': 100}
    else:
        return None, 0
    
    print("\nAvailable Beverages:")
    for idx, beverage in enumerate(beverages, 1):
        print(f"{idx}. {beverage} - ${prices[beverage]}")
    
    choice = None
    while choice is None:
        try:
            choice_input = int(input(f"Choose your beverage (1-{len(beverages)}), or 0 for none: "))
            if choice_input == 0:
                return None, 0
            choice = choice_input - 1
            if 0 <= choice < len(beverages):
                selected_beverage = beverages[choice]
                return selected_beverage, prices[selected_beverage]
            else:
                raise ValueError("Invalid choice. Please try again.")
        except ValueError as e:
            print(e)
            choice = None

def confirmOrder(order_details):
    """Confirm the order with the user."""
    print("\nYour order details:")
    print("Main Course: ", order_details['main'])
    print("Side Dish: ", order_details['side'])
    print("Daily Special: ", order_details.get('special') or "None")
    print("Customization: ", order_details.get('customization'))
    if order_details.get('beverage'):
        print("Beverage: ", order_details['beverage'])
    
    is_correct = input("\nIs your order correct? (y/n): ").strip().lower()
    if is_correct == 'n':
        print("Let's redo your order.")
        return False
    
    confirm = input("\nDo you want to confirm this order? (y/n): ").strip().lower()
    if confirm == 'y':
        print("Your order has been completed, thank you!")
        add_to_faves = input("Would you like to add this order to your favorites? (y/n): ").strip().lower()
        if add_to_faves == 'y':
            editFaves(order_details)
        delivery_choice = input("Would you like delivery or pickup? (Enter 'delivery' or 'pickup'): ").strip().lower()
        if delivery_choice == 'delivery':
            requestDelivery()
        else:
            print("Thank you! Your pickup order has been confirmed.")
        return True
    else:
        cancelOrder(order_details)
        return False

def cancelOrder(order_details):
    """Cancel the order."""
    print("\nYour order has been canceled.")
    # Additional cancellation logic can be implemented here

def makeOrder():
    """Create an order based on time of day."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    all_orders = []
    refund_manager = RefundManager()

    if "08:00" <= current_time <= "11:30":
        print("It's breakfast time!")
        day = now.strftime("%A")
        breakfast_menu = load_menu('menuitems/breakfast.csv')
        if day in breakfast_menu:
            num_orders = int(input("How many breakfasts would you like to order? "))
            for i in range(num_orders):
                print(f"\nOrder #{i+1}:")
                size = input("Choose size (SML/MED/LRG): ").strip().upper()
                while size not in ['SML', 'MED', 'LRG']:
                    print("Invalid size, please choose SML, MED, or LRG.")
                    size = input("Choose size (SML/MED/LRG): ").strip().upper()
                
                main, side, special, customization = get_meal_choices(breakfast_menu, day)
                beverage, beverage_price = get_beverage_choice('breakfast')
                
                order = {
                    'main': main,
                    'side': side,
                    'special': special,
                    'customization': customization,
                    'size': size,
                    'beverage': beverage,
                    'beverage_price': beverage_price
                }
                
                if confirmOrder(order):
                    all_orders.append(order)
                else:
                    print("Let's redo your order.")
                    return makeOrder()  # Restart the order flow
            genReceipt(all_orders, 'breakfast')
        else:
            print(f"No breakfast menu found for {day}.")
    elif "11:30" <= current_time <= "18:00":
        print("It's lunch time!")
        day = now.strftime("%A")
        lunch_menu = load_menu('menuitems/lunch.csv')
        if day in lunch_menu:
            num_orders = int(input("How many lunch orders would you like? "))
            for i in range(num_orders):
                print(f"\nOrder #{i+1}:")
                size = input("Choose size (SML/MED/LRG): ").strip().upper()
                while size not in ['SML', 'MED', 'LRG']:
                    print("Invalid size, please choose SML, MED, or LRG.")
                    size = input("Choose size (SML/MED/LRG): ").strip().upper()
                
                main, side, special, customization = get_meal_choices(lunch_menu, day, is_lunch_time=True)
                beverage, beverage_price = get_beverage_choice('lunch')
                
                order = {
                    'main': main,
                    'side': side,
                    'special': special,
                    'customization': customization,
                    'size': size,
                    'beverage': beverage,
                    'beverage_price': beverage_price
                }
                
                if confirmOrder(order):
                    all_orders.append(order)
                else:
                    print("Let's redo your order.")
                    return makeOrder()
            genReceipt(all_orders, 'lunch')
        else:
            print(f"No lunch menu found for {day}.")
    else:
        print("It's neither breakfast nor lunch time. Please try again later.")
