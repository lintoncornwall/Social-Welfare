# payment.py

def processPayment(total_cost):
    """
    Process the payment by asking the customer to select an online payment option
    and enter the necessary information. Returns True if payment is successful,
    False otherwise.
    """
    print(f"\nYour total amount due is: ${total_cost:.2f}")
    print("Select a payment method:")
    print("1. Credit Card")
    print("2. PayPal")
    
    method = input("Enter the number of your chosen payment method: ").strip()
    
    if method == '1':
        # Process Credit Card Payment
        card_number = input("Enter your credit card number: ").strip()
        expiry_date = input("Enter the expiration date (MM/YY): ").strip()
        cvv = input("Enter the CVV: ").strip()
        print("Processing your credit card payment...")
    elif method == '2':
        # Process PayPal Payment
        paypal_email = input("Enter your PayPal email: ").strip()
        print("Processing your PayPal payment...")
    else:
        print("Invalid payment method selected.")
        return False
    
    # Simulate payment confirmation
    confirmation = input("Confirm payment? (y/n): ").strip().lower()
    if confirmation == 'y':
        print("Payment successful!")
        return True
    else:
        print("Payment canceled.")
        return False
