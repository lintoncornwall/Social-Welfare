#favorites.py
import os
import json

def editFaves(order_details):
    """Add, edit, or delete an order from favorites."""
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
    
    action = input("\nWhat would you like to do? (add/edit/delete): ").strip().lower()
    
    if action == 'add':
        favorites.append(order_details)
        print("Order added to favorites!")
    elif action == 'edit':
        fave_idx = None
        while fave_idx is None:
            try:
                fave_idx = int(input("Enter the number of the favorite to edit: ")) - 1
                if 0 <= fave_idx < len(favorites):
                    favorites[fave_idx] = order_details
                    print("Favorite updated!")
                else:
                    raise ValueError("Invalid choice.")
            except (ValueError, IndexError):
                print("Invalid choice.")
                fave_idx = None
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
    
    try:
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f, indent=4)
    except Exception as e:
        print(f"Error saving favorites: {e}")

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
        print(f"Additional Side: {favorite.get('additional_side', 'None')}")
        print(f"Daily Special: {favorite.get('special', 'None')}")
        print(f"Customization: {favorite.get('customization', 'No customization')}")
        if favorite.get('beverage'):
            print(f"Beverage: {favorite['beverage']}")

    action = input("\nWould you like to (edit/delete/place) a favorite, or go back? (edit/delete/place/back): ").strip().lower()
    if action in ['edit', 'delete', 'place']:
        favorite_idx = None
        while favorite_idx is None:
            try:
                favorite_idx = int(input("Enter the number of the favorite to modify: ")) - 1
                if 0 <= favorite_idx < len(favorites):
                    if action == 'edit':
                        editFaves(favorites[favorite_idx])
                    elif action == 'delete':
                        deleted = favorites.pop(favorite_idx)
                        print(f"Favorite deleted: {deleted['main']} with {deleted['side']}")
                        with open(favorites_file, 'w') as f:
                            json.dump(favorites, f, indent=4)
                    elif action == 'place':
                        print("Placing order from favorites...")
                        # You can call order confirmation here if desired.
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
