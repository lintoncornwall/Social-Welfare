#refund_manager.py
import json
import os
import datetime


class RefundManager:
    def __init__(self, receipt_file="receipts.json", refund_log_file="refunds.json"):
        """Initialize the RefundManager with file paths."""
        self.receipt_file = receipt_file
        self.refund_log_file = refund_log_file

    def load_cashed_receipts(self):
        """Load all previously cashed receipts from a file."""
        if os.path.exists(self.receipt_file):
            with open(self.receipt_file, 'r') as f:
                return json.load(f)
        return []  # Return an empty list if no receipts file exists

    def save_cashed_receipts(self, cashed_receipts):
        """Save all cashed receipts to a file."""
        with open(self.receipt_file, 'w') as f:
            json.dump(cashed_receipts, f, indent=4)

    
    def request_refund(self):
        """Allow the user to request a refund for a previously confirmed order."""
        # Ask the user for the receipt number
        receipt_number = input("Enter your receipt number to request a refund: ").strip()

        # Load the list of cashed receipts
        cashed_receipts = self.load_cashed_receipts()

        # Search for the receipt by receipt number
        receipt_to_refund = None
        for receipt in cashed_receipts:
            if receipt['receipt_number'] == receipt_number:
                receipt_to_refund = receipt
                break

        # If the receipt is found, process the refund
        if receipt_to_refund:
            print("\nRefund Request Details:")
            print(f"Receipt Number: {receipt_to_refund['receipt_number']}")
            print("\nOrder Details:")

            width = 40  # Adjust alignment
            for idx, order in enumerate(receipt_to_refund['orders'], 1):
                print(f"\nOrder #{idx}:")

                # Main Course
                main_price = order.get('main_price', 0.00)
                print(f"Main Course ({order['size']}): {order['main']}".ljust(width) + f"${main_price:.2f}")

                # Side Dish
                side_price = order.get('side_price', 0.00)
                print(f"Side Dish: {order['side']}".ljust(width) + f"${side_price:.2f}")  # Ensure the side price is accessed properly

                # Additional Side
                additional_side_price = order.get('additional_side_price', 0.00)
                if order['additional_side']:
                    print(f"Additional Side: {order['additional_side']}".ljust(width) + f"${additional_side_price:.2f}")
                
                # Daily Special
                special_cost = order.get('special_cost', 0.00)
                if order['special']:
                    print(f"Daily Special: {order['special']}".ljust(width) + f"${special_cost:.2f}")
                else:
                    print("Daily Special: None".ljust(width) + "$0.00")

                # Customization (No price, just description)
                print(f"Customization: {order['customization']}".ljust(width) + "$0.00")

                # Beverage
                beverage_price = order.get('beverage_price', 0.00)
                if order['beverage']:
                    print(f"Beverage: {order['beverage']}".ljust(width) + f"${beverage_price:.2f}")
                else:
                    print("Beverage: None".ljust(width) + "$0.00")

                # Order Total
                item_total = main_price + side_price + special_cost + additional_side_price + beverage_price
                print(f"Order Total:".ljust(width) + f"${item_total:.2f}")

            # Total Refund Amount
            print("\n" + "-" * (width + 10))
            print(f"Total Refund Amount:".rjust(width) + f"${receipt_to_refund['total_cost']:.2f}")
            print("-" * (width + 10))

            # Confirm refund with the user
            confirm = input("\nAre you sure you want to request a refund for this order? (y/n): ").strip().lower()

            if confirm == 'y':
                # Process the refund (just print a confirmation for now)
                print(f"\nYour refund for receipt {receipt_number} is being processed.")
                
                # Generate a transaction reference number
                transaction_reference = self.generate_transaction_reference()

                # Log the refund (log refund details including the transaction reference)
                self.log_refund(receipt_to_refund, transaction_reference)

                # Remove the refunded receipt from the list
                cashed_receipts.remove(receipt_to_refund)
                self.save_cashed_receipts(cashed_receipts)

                # Provide refund confirmation to the user
                print(f"Refund has been successfully processed!")
                print(f"Your transaction reference number is {transaction_reference}.")
            else:
                print("\nRefund request canceled.")
        else:
            print("No order found with that receipt number.")




    def log_refund(self, receipt, transaction_reference):
        """Log the refunded order to a file or database."""
        refund_entry = {
            'receipt_number': receipt['receipt_number'],
            'total_cost': receipt['total_cost'],
            'transaction_reference': transaction_reference,
            'date_refunded': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Load current refunds if any
        if os.path.exists(self.refund_log_file):
            try:
                with open(self.refund_log_file, 'r') as f:
                    refunds = json.load(f)
            except json.JSONDecodeError:
                print("Error reading the refund log. It may be corrupted.")
                refunds = []
        else:
            refunds = []

        # Log the refund details
        refunds.append(refund_entry)

        # Save the updated refunds log
        try:
            with open(self.refund_log_file, 'w') as f:
                json.dump(refunds, f, indent=4)
        except Exception as e:
            print(f"Error saving refund log: {e}")

    def generate_transaction_reference(self):
        """Generate a unique transaction reference for the refund."""
        return f"REF-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(4).hex().upper()}"
