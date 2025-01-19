import random
import string
from datetime import datetime
import africastalking # type: ignore
from django.conf import settings # type: ignore

from myproject.db_exceptions import DataBaseException # type: ignore

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
        

africastalking.initialize(
    username=settings.SMS_USERNAME,
    api_key=settings.SMS_API_KEY
)

sms = africastalking.SMS

class send_sms:

    @staticmethod
    def sending(recipient_number, recipient_name, order_no, item, price):
        recipients = [str(recipient_number)]
        
        message = f"Dear {recipient_name}! Your order {order_no}, price: {price}, item: {item}"
        
        sender = settings.SHORT_CODE
        try:
            
            response = sms.send(message, recipients, sender)
            return response
        except Exception as ex:
            raise DataBaseException(message=ex)
