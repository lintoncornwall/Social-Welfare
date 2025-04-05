#favorites.py
import os
import json


def addOrderToFaves(order_details):
    """Add an order to the favorites list without prompting for add/delete."""
    favorites_file = 'favorites.json'
    if os.path.exists(favorites_file):
        try:
            with open(favorites_file, 'r') as f:
                favorites = json.load(f)
        except json.JSONDecodeError:
            print("Error reading the favorites file. It may be corrupted.")
            favorites = []
    else:
        favorites = []

    # Simply append the new order
    favorites.append(order_details)
    print("Order added to favorites!")

    # Save the updated favorites list
    try:
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f, indent=4)
    except Exception as e:
        print(f"Error saving favorites: {e}")


def editFaves(order_details):
    """Add or delete an order from favorites."""
    favorites_file = 'favorites.json'
    if os.path.exists(favorites_file):
        try:
            with open(favorites_file, 'r') as f:
                favorites = json.load(f)
        except json.JSONDecodeError:
            print("Error reading the favorites file. It may be corrupted.")
            favorites = []
    else:
        favorites = []
    
    print("\nCurrent Favorites:")
    for idx, fave in enumerate(favorites, 1):
        print(f"{idx}. {fave['main']} with {fave['side']}")
    
    action = input("\nWhat would you like to do? (add/delete): ").strip().lower()
    
    if action == 'add':
        favorites.append(order_details)
        print("Order added to favorites!")
    elif action == 'delete':
        fave_idx = None
        while fave_idx is None:
            try:
                fave_idx = int(input("Enter the number of the favorite to delete: ")) - 1
                if 0 <= fave_idx < len(favorites):
                    deleted = favorites.pop(fave_idx)
                    print(f"{deleted['main']} with {deleted['side']} has been deleted from favorites.")
                else:
                    raise ValueError("Invalid choice.")
            except (ValueError, IndexError):
                print("Invalid choice.")
                fave_idx = None
    else:
        print("Invalid action. No changes made.")
    
    try:
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f, indent=4)
    except Exception as e:
        print(f"Error saving favorites: {e}")

def placeFavoriteOrder(favorite_order):
    """Place an order directly from a favorite order shortcut with online payment."""
    print("\nSelected Favorite Order:")
    print(f"\nMain Course: {favorite_order['main']}")
    print(f"Side Dish: {favorite_order['side']}")
    print(f"Daily Special: {favorite_order.get('special', 'None')}")
    print(f"Customization: {favorite_order.get('customization', 'No customization')}")
    if favorite_order.get('beverage'):
        print(f"Beverage: {favorite_order['beverage']}")
    
    confirm = input("\nDo you want to place this order? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Order placement cancelled.")
        return

    # Prompt for meal type.
    meal_type = None
    while meal_type not in ['breakfast', 'lunch']:
        meal_type = input("Enter meal type for this order (breakfast/lunch): ").strip().lower()
        if meal_type not in ['breakfast', 'lunch']:
            print("Invalid meal type. Please enter 'breakfast' or 'lunch'.")
    
    # Ask for delivery or pickup.
    delivery_choice = input("Would you like delivery or pickup for your order? (Enter 'delivery' or 'pickup'): ").strip().lower()
    if delivery_choice == 'delivery':
        from .delivery import requestDelivery
        requestDelivery()
    else:
        print("Thank you! Your pickup order has been confirmed.")
    
    # Update the order with the order type.
    favorite_order['order_type'] = delivery_choice

    final_confirm = input("Would you like to confirm and proceed to payment? (y/n): ").strip().lower()
    if final_confirm != 'y':
        print("Order canceled.")
        return

    # Import the payment processing function.
    from .payment import processPayment
    # Import the total cost calculator from receipt.
    from .receipt import calculateTotal

    # Calculate the total cost for this single order.
    total_cost = calculateTotal([favorite_order], meal_type)
    
    if processPayment(total_cost):
        from .receipt import genReceipt
        genReceipt([favorite_order], meal_type)
        print("Your favorite order has been completed, thank you!")
    else:
        print("Payment was not successful. Order canceled.")



def viewFaves():
    """View the list of favorite orders and allow actions on them."""
    favorites_file = 'favorites.json'
    if not os.path.exists(favorites_file):
        print("\nNo favorites found.")
        return

    try:
        with open(favorites_file, 'r') as f:
            favorites = json.load(f)
    except json.JSONDecodeError:
        print("Error reading the favorites file. It may be corrupted.")
        return

    if not favorites:
        print("\nNo favorites found.")
        return

    print("\n---- Favorite Orders ----")
    for idx, favorite in enumerate(favorites, 1):
        print(f"\nFavorite #{idx}:")
        print(f"Main Course: {favorite['main']}")
        print(f"Side Dish: {favorite['side']}")
        print(f"Daily Special: {favorite.get('special', 'None')}")
        print(f"Customization: {favorite.get('customization', 'No customization')}")
        if favorite.get('beverage'):
            print(f"Beverage: {favorite['beverage']}")

    action = input("\nWould you like to (delete/order) a favorite, or go back? (delete/order/back): ").strip().lower()
    if action in ['delete', 'order']:
        favorite_idx = None
        while favorite_idx is None:
            try:
                favorite_idx = int(input("Enter the number of the favorite to select: ")) - 1
                if 0 <= favorite_idx < len(favorites):
                    if action == 'delete':
                        deleted = favorites.pop(favorite_idx)
                        print(f"Favorite deleted: {deleted['main']} with {deleted['side']}")
                        with open(favorites_file, 'w') as f:
                            json.dump(favorites, f, indent=4)
                    elif action == 'order':
                        placeFavoriteOrder(favorites[favorite_idx])
                    break
                else:
                    raise ValueError("Invalid choice.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
                favorite_idx = None
    elif action == 'back':
        return
    else:
        print("Invalid action. Returning to main menu.")
