#main.py
import sys
import os
from OrderPlacement.order import makeOrder
from OrderPlacement.favorites import viewFaves 
from RefundManagement.refund_manager import RefundManager
from ContentEditing.content_editor import edit_content_menu 

def mainMenu():
    """Main menu to let the user interact with the system."""
    while True:
        print("\n1. Make Order")
        print("2. View Favorite Orders")
        print("3. Request Refund")
        print("4. Cancel Delivery")
        print("5. Edit Content")
        print("6. Exit")
        choice = input("Choose an option (1/2/3/4/5/6): ").strip()

        if choice == '1':
            makeOrder()
        elif choice == '2':
            viewFaves()
        elif choice == '3':
            refund_manager = RefundManager()
            refund_manager.request_refund()
        elif choice == '4':
            from OrderPlacement.delivery import cancel_delivery  # Import as needed
            cancel_delivery()
        elif choice == '5':
            edit_content_menu()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    mainMenu()
