#delivery.py
import datetime
import json

def requestDelivery():
    """Handle the process of requesting delivery for an order."""
    order_time = datetime.datetime.now()
    print("\n--- Delivery Request ---")
    address = input("Enter your delivery address: ").strip()
    phone = input("Enter your phone number: ").strip()
    email = input("Enter your email address: ").strip()
    
    print("\nPlease review your delivery details:")
    print(f"Address: {address}")
    print(f"Phone: {phone}")
    print(f"Email: {email}")
    
    confirm_delivery = input("Would you like to confirm the delivery? (y/n): ").strip().lower()
    if confirm_delivery == 'y':
        delivery_details = {
            "address": address,
            "phone": phone,
            "email": email,
            "order_time": order_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_delivery_details(delivery_details)
        print(f"\nDelivery has been confirmed!")
    else:
        print("Delivery request canceled.")
        return

def save_delivery_details(details):
    """Mock function to save delivery details."""
    with open("delivery_requests.json", "a") as file:
        json.dump(details, file)
        file.write("\n")

def allow_cancellation(order_time):
    """Allow cancellation of the delivery within a 20-minute window."""
    cancel_time_limit = order_time + datetime.timedelta(minutes=20)
    print(f"\nYou can cancel your delivery up to {cancel_time_limit.strftime('%Y-%m-%d %H:%M:%S')}.")
    cancel_delivery_choice = input("Do you want to cancel the delivery within 20 minutes? (y/n): ").strip().lower()
    current_time = datetime.datetime.now()
    if current_time <= cancel_time_limit and cancel_delivery_choice == 'y':
        cancel_delivery()
    elif current_time > cancel_time_limit:
        print("\nSorry, the 20-minute cancellation window has expired.")
    else:
        print("\nDelivery not canceled.")

def cancel_delivery():
    """Cancel the delivery based on receipt number."""
    print("\n--- Cancel Delivery ---")
    receipt_number = input("Please enter your receipt number to cancel the delivery: ").strip()
    
    try:
        with open("receipts.json", "r") as file:
            receipts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading receipts: {e}")
        return
    
    receipt_found = False
    for receipt in receipts:
        if receipt.get("receipt_number") == receipt_number:
            receipt_found = True
            receipt["status"] = "canceled"
            break
    
    if receipt_found:
        print(f"Delivery for receipt number {receipt_number} has been canceled successfully.")
        with open("receipts.json", "w") as file:
            json.dump(receipts, file, indent=4)
    else:
        print(f"The receipt number {receipt_number} is invalid or not found. Please check and try again.")
