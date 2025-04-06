#order.py
import datetime
import os
import json
from .menu import load_menu
from .receipt import genReceipt
from .delivery import requestDelivery
from RefundManagement.refund_manager import RefundManager  # Assuming this exists
from .prices import get_size_price, get_side_price, get_special_cost, get_beverage_price
from .favorites import addOrderToFaves  

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
    
    # Get user selections with error handling
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

def cancelOrder(order_details):
    """Cancel the order."""
    print("\nYour order has been canceled.")

def show_order_summary(all_orders, meal_type):
    """
    Show a cost breakdown for each order in all_orders without finalizing a receipt.
    Returns the total cost for all orders.
    """
    print("\n-- Order Summary (Preview) --")
    total_cost = 0
    for idx, order in enumerate(all_orders, start=1):
        print(f"\nOrder #{idx}:")
        print(f"  Main: {order['main']} ({order['size']})")
        print(f"  Side: {order['side']}")
        print(f"  Daily Special: {order.get('special') or 'None'}")
        print(f"  Customization: {order.get('customization')}")
        print(f"  Beverage: {order.get('beverage') or 'None'}")

        # Calculate costs similarly to receipt.py
        main_cost = get_size_price(meal_type, order['size'])
        side_cost = get_side_price()
        special_cost = get_special_cost(meal_type) if order.get('special') else 0
        beverage_cost = 0
        if order.get('beverage'):
            beverage_cost = get_beverage_price(meal_type, order['beverage'])

        item_total = main_cost + side_cost + special_cost + beverage_cost
        total_cost += item_total

        print(f"  -> Subtotal: ${item_total:.2f}")
    print(f"\nOverall Total: ${total_cost:.2f}")
    print("-- End of Summary --\n")
    return total_cost

def finalizeOrder(all_orders, meal_type):
    """
    (CLI version)
    1) Display full order details with cost breakdown.
    2) Ask if the overall order is correct.
    3) Ask if they'd like delivery or pickup.
    4) Process the online payment if the order is confirmed.
    5) If payment is successful, generate the final receipt; otherwise, cancel.
    """
    total_cost = show_order_summary(all_orders, meal_type)

    is_correct = input("Is your order correct? (y/n): ").strip().lower()
    if is_correct != 'y':
        print("Order not confirmed. Let's cancel.")
        return

    # Ask if they'd like delivery or pickup.
    delivery_choice = input("Would you like delivery or pickup? (Enter 'delivery' or 'pickup'): ").strip().lower()
    if delivery_choice == 'delivery':
        from .delivery import requestDelivery
        requestDelivery()
    else:
        print("Thank you! Your pickup order has been noted.")

    # Update each order with the order type.
    for order in all_orders:
        order['order_type'] = delivery_choice

    # Ask if they'd like to confirm and proceed to payment.
    final_confirm = input("Would you like to confirm and proceed to payment? (y/n): ").strip().lower()
    if final_confirm == 'y':
        from .payment import processPayment
        if processPayment(total_cost):
            from .receipt import genReceipt
            genReceipt(all_orders, meal_type)
            print("Your order has been completed, thank you!")
        else:
            print("Payment was not successful. Order canceled.")
    else:
        print("Order canceled.")

def process_order_data(order_data, meal_type, payment_processor=None, receipt_callback=None):
    """
    Process an order given its data as a dictionary.
    Calculates total cost, processes payment, and generates a receipt.
    If a `payment_processor` function is provided, it will be used to process payment.
    If a `receipt_callback` function is provided, it will be called with the receipt text.
    Returns True if the order is successfully completed, False otherwise.
    """
    main_cost = get_size_price(meal_type, order_data['size'])
    side_cost = get_side_price()
    special_cost = get_special_cost(meal_type) if order_data.get('special') else 0
    beverage_cost = get_beverage_price(meal_type, order_data['beverage']) if order_data.get('beverage') else 0
    total_cost = main_cost + side_cost + special_cost + beverage_cost

    # Process payment using the provided payment_processor (GUI) or default CLI method.
    if payment_processor:
        success = payment_processor(total_cost)
    else:
        from .payment import processPayment
        success = processPayment(total_cost)

    if success:
        # Capture the receipt output instead of printing to terminal.
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        from .receipt import genReceipt
        genReceipt([order_data], meal_type)
        sys.stdout = old_stdout
        receipt_text = mystdout.getvalue()
        if receipt_callback:
            receipt_callback(receipt_text)
        else:
            print(receipt_text)
        print("Your order has been completed, thank you!")
        return True
    else:
        print("Payment was not successful. Order canceled.")
        return False

def makeOrder():
    """Create an order based on time of day (CLI version)."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    all_orders = []
    refund_manager = RefundManager()

    if "00:00" <= current_time <= "11:30":
        print("It's breakfast time!")
        day = now.strftime("%A")
        breakfast_menu = load_menu('ContentEditing/breakfast.csv')
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
                
                add_to_faves = input("Would you like to add this order to your favorites? (y/n): ").strip().lower()
                if add_to_faves == 'y':
                    addOrderToFaves(order)

                all_orders.append(order)

            finalizeOrder(all_orders, 'breakfast')
        else:
            print(f"No breakfast menu found for {day}.")
    elif "11:31" <= current_time <= "23:59":
        print("It's lunch time!")
        day = now.strftime("%A")
        lunch_menu = load_menu('ContentEditing/lunch.csv')
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

                add_to_faves = input("Would you like to add this order to your favorites? (y/n): ").strip().lower()
                if add_to_faves == 'y':
                    addOrderToFaves(order)

                all_orders.append(order)

            finalizeOrder(all_orders, 'lunch')
        else:
            print(f"No lunch menu found for {day}.")
    else:
        print("It's neither breakfast nor lunch time. Please try again later.")
