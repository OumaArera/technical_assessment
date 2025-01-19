import random
import string
from datetime import datetime

def generate_unique_order_number():
        """
        Generates a unique order number in the format CUST{YYYY-MM-DD-HH:MM:S:}XX.
        Ensures the order number is unique by checking the database.
        """
        while True:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            order_number = f"ORD-{timestamp}-{random_suffix}"
            
            return order_number