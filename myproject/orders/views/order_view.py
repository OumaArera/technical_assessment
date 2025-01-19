from rest_framework.authentication import SessionAuthentication  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from myproject.responses import APIResponse
from myproject.validate_params import validate_query_params
from orders.services.order_service import OrderService
from orders.serializers.model_serializers import OrderDeserializer, OrderSerializer, UpdateOrderDeserializer


class OrderView(APIView):

    def post(self, request):
        """Handles creating a new order."""
        try:
            deserializer = OrderDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                new_order = OrderService.create_order(order_data=validated_data)
                serialized_order = OrderSerializer(instance=new_order)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Order created successfully",
                        data=serialized_order.data
                    ),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating the order",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request, order_id=None):
        """Handles fetching orders."""
        try:
            if order_id:
                order = OrderService.get_order_by_id(order_id=order_id)
                serialized_order = OrderSerializer(instance=order)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Order fetched successfully",
                        data=serialized_order.data
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                query_params = validate_query_params(
                    query_params=request.query_params,
                    valid_query_params={"order_number", "customer_code"}
                )
                orders = OrderService.get_all_orders(query_params=query_params)
                serialized_orders = OrderSerializer(orders, many=True)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Orders fetched successfully",
                        data=serialized_orders.data
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching orders",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, order_id):
        """Handles updating an order."""
        try:
            deserializer = UpdateOrderDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                updated_order = OrderService.update_order(order_id=order_id, order_data=validated_data)
                serialized_order = OrderSerializer(instance=updated_order)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Order updated successfully",
                        data=serialized_order.data
                    ),
                    status=status.HTTP_200_OK
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating order",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, order_id):
        """Handles deleting an order."""
        try:
            if OrderService.delete_order(order_id=order_id):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Order deleted successfully",
                        data={"order_id": order_id}
                    ),
                    status=status.HTTP_200_OK
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Failed to delete order",
                    error="Order not found or already deleted"
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting order",
                    error=str(ex)
                ),
                status=ex.status_code
            )
