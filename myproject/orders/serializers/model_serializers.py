from rest_framework import serializers # type: ignore
from orders.models.orders import Order  

class OrderSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer() 

    class Meta:
        model = Order
        fields = [
            'order_id',
            'customer',
            'item',
            'price',
            'order_number',
            'created_at',
            'modified_at',
        ]


class OrderDeserializer(serializers.Serializer):
    item= serializers.CharField(required=True)
    price = serializers.FloatField(required=True, min_value=1)
    customer_code= serializers.CharField(required=True)
     

class UpdateOrderDeserializer(serializers.Serializer):
    item= serializers.CharField(required=False)
    price = serializers.FloatField(required=False, min_value=1)