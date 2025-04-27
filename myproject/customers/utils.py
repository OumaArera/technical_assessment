from datetime import datetime
import random
import string

def generate_unique_customer_code():
        """
        Generates the time stamp
        Generates a unique 8-character customer_code consisting of uppercase letters and numbers.
        Join the time stamp and the unique code
        Ensures the code is unique by checking the database.
        """
        while True:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            customer_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            customer_code = f"{timestamp}-{customer_code}"
            return customer_code