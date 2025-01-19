from customers.repositories.users_repo import UserRepository
from orders.models.orders import Order
from rest_framework.test import APITestCase # type: ignore
from customers.models.user import User
from django.contrib.auth import authenticate # type: ignore

from myproject.tokens_utils import generate_jwt_token 

def create_customer_setup(self, user_model):

    """Customer creation test setup function"""
    
    test_customers = [
        {
            "username": "Ouma", 
            "phone_number": "+254748800714", 
            "password": "Test1234#", 
            "first_name": "Ouma",
            "last_name": "Arera",
            "email": "ouma@example.com",
            'customer_code': "Test123"
        },
        {
            "username": "Ouma1", 
            "phone_number": "+254748800716", 
            "password": "Test1234#", 
            "first_name": "Rambung'",
            "last_name": "Fee",
            "email": "fee@example.com",
            'customer_code': "Test124"
        }
    ]
    
    self.customers = []
    for customer_data in test_customers:
        password = customer_data.pop("password")
        customer = user_model.objects.create(**customer_data)
        customer.set_password(password)
        customer.save()
        self.customers.append(customer)


def login_setUp():
	"""Login Test setup function for protected endpoints"""
	test_customer = {
		'username': 'Ouma',
		'password': 'Test1234#'
	}
	customer = authenticate(
		username=test_customer['username'],
		password=test_customer['password'],
	)
	
	if customer:
		token = generate_jwt_token(customer)
		return token
	else:
		return None
     

def create_order(self, order_model):

    """Order creation test setup function"""
    
    test_orders = [
        {"item": "Test Item 1", "price": 400, "customer_code": "Test124", "order_number": "OD1239"  },
        {"item": "Test Item 2", "price": 500, "customer_code": "Test124", "order_number": "OD1238"  },
        {"item": "Test Item 3", "price": 700, "customer_code": "Test124", "order_number": "OD1237"  },

        {"item": "Test Item 1", "price": 400, "customer_code": "Test123", "order_number": "OD1236"  },
        {"item": "Test Item 2", "price": 500, "customer_code": "Test123", "order_number": "OD1235"  },
        {"item": "Test Item 3", "price": 700, "customer_code": "Test123", "order_number": "OD1234" },
    ]
    
    self.orders = []
    for order_data in test_orders:
        
        customer = UserRepository.get_user_by_customer_code(
             customer_code=order_data.pop("customer_code")
        )
        
        order_data['customer'] = customer
        order = order_model.objects.create(**order_data)
        self.orders.append(order)


class GlobalAPITestCase(APITestCase):

  def setUp(self):
    super().setUp()
    
  @classmethod
  def setUpTestData(cls):
    # 1. Set up customers
    create_customer_setup(self=cls, user_model=User)
    # 2. Login customer
    cls.token = login_setUp()
    # 3. Order setup
    create_order(self=cls, order_model=Order)