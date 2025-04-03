import os
import json
from .prices import get_size_price, get_special_cost, get_beverage_price, get_side_price

RECEIPT_FILE = "receipts.json"
RECEIPT_NUMBER_FILE = "receipt_number.txt"

def load_receipt_number():
    """Load the last used receipt number, starting at 00000000."""
    if os.path.exists(RECEIPT_NUMBER_FILE):
        with open(RECEIPT_NUMBER_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def save_receipt_number(receipt_number):
    """Save the new receipt number to a file."""
    with open(RECEIPT_NUMBER_FILE, 'w') as f:
        f.write(str(receipt_number))

def load_cashed_receipts():
    """Load all previously cashed receipts from a file."""
    if os.path.exists(RECEIPT_FILE):
        try:
            with open(RECEIPT_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error reading receipts file. It may be corrupted.")
            return []
    return []

def save_cashed_receipts(cashed_receipts):
    """Save all cashed receipts to a file."""
    with open(RECEIPT_FILE, 'w') as f:
        json.dump(cashed_receipts, f, indent=4)

def genReceipt(all_orders, meal_type):
    """
    Generate the receipt with cost calculation for all confirmed orders.
    :param all_orders: List of confirmed orders
    :param meal_type: 'breakfast' or 'lunch' to determine pricing
    """
    receipt_number = load_receipt_number()
    formatted_receipt_number = f"{receipt_number:08d}"
    total_cost = 0

    width = 40
    print("\n---- Order Receipt ----")
    print(f"Receipt Number: {formatted_receipt_number}")
    for idx, order in enumerate(all_orders, 1):
        print(f"\nOrder #{idx}:")
        item_total = 0
        
        # Calculate main course cost based on meal type and selected size.
        main_cost = get_size_price(meal_type, order['size'])
        item_total += main_cost
        order['main_price'] = main_cost
        print(f"Main Course ({order['size']}): {order['main']}".ljust(width) + f"${main_cost:.2f}")
        
        # Calculate side dish cost.
        side_price = get_side_price()
        order['side_price'] = side_price
        print(f"Side Dish: {order['side']}".ljust(width) + f"${side_price:.2f}")
        item_total += side_price
        
        # Apply daily special cost if available.
        if order.get('special'):
            special_cost = get_special_cost(meal_type)
            order['special_cost'] = special_cost
            item_total += special_cost
            print(f"Daily Special: {order['special']}".ljust(width) + f"${special_cost:.2f}")
        else:
            order['special_cost'] = 0
            print("Daily Special: None".ljust(width) + "$0.00")
        
        order['customization_price'] = 0
        print(f"Customization: {order['customization']}".ljust(width) + "$0.00")
        
        if order.get('beverage'):
            beverage_price = get_beverage_price(meal_type, order['beverage'])
            order['beverage_price'] = beverage_price
            item_total += beverage_price
            print(f"Beverage: {order['beverage']}".ljust(width) + f"${beverage_price:.2f}")
        else:
            order['beverage_price'] = 0
            print("Beverage: None".ljust(width) + "$0.00")
        
        print(f"Order Total:".ljust(width) + f"${item_total:.2f}")
        total_cost += item_total
    
    print("\n" + "-" * (width + 10))
    print(f"Total:".rjust(width) + f"${total_cost:.2f}")
    print("-" * (width + 10))
    print("\n---- Thank You! ----")

    cashed_receipts = load_cashed_receipts()
    receipt = {
        'receipt_number': formatted_receipt_number,
        'orders': all_orders,
        'total_cost': total_cost
    }
    cashed_receipts.append(receipt)
    save_cashed_receipts(cashed_receipts)
    save_receipt_number(receipt_number + 1)
