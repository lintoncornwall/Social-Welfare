"""
This module centralizes all pricing logic for the restaurant ordering system.
It defines prices for meal sizes, daily specials, sides, and beverages for different meal types.
"""

# Pricing definitions
SIZE_PRICES = {
    'breakfast': {'SML': 500, 'MED': 650, 'LRG': 750},
    'lunch': {'SML': 700, 'MED': 800, 'LRG': 900}
}

SPECIAL_COST = {
    'breakfast': 250,
    'lunch': 500
}

BEVERAGE_PRICES = {
    'breakfast': {'Tea': 150, 'Coffee': 150, 'Orange Juice': 200, 'Water': 100},
    'lunch': {'Soda': 150, 'Fruit Juice': 250, 'Iced Tea': 200, 'Water': 100}
}

# New constant: Equal pricing for all sides
SIDE_PRICE = 300

def get_size_price(meal_type, size):
    """
    Return the price for a given meal type and size.
    If no price is defined, returns 0.
    """
    return SIZE_PRICES.get(meal_type, {}).get(size, 0)

def get_special_cost(meal_type):
    """
    Return the cost for the daily special for a given meal type.
    """
    return SPECIAL_COST.get(meal_type, 0)

def get_beverage_price(meal_type, beverage):
    """
    Return the price for a given beverage based on the meal type.
    """
    return BEVERAGE_PRICES.get(meal_type, {}).get(beverage, 0)

def get_side_price():
    """
    Return the price for a side dish.
    """
    return SIDE_PRICE
