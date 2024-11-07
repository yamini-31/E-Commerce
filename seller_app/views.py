from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import OrderSerializer, SellerSerializer
from .models import Order, Seller
from customer_app.models import Customer,Cart
from django.db.models import F, Sum


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password, check_password


@api_view(['POST'])
def seller_signup(request):
    data = request.data
    data['password'] = make_password(data['password'])  
    serializer = SellerSerializer(data=data)

    if serializer.is_valid():
        seller = serializer.save()  
        return Response({'seller': serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def get_order(request):
    orders=Order.objects.all()
    ser=OrderSerializer(orders, many=True)
    return Response(ser.data)

# Below 3 functions are for customer to access his order. 1st by customer_id, 2nd by order_id, 3rd by status.

def calculate_final_price(customer_id):
    order = Order.objects.filter(customer_id=customer_id)
    
    
    total_price = order.annotate(
        final_price=F('total_bill')
    ).aggregate(total=Sum('final_price'))
    
    return total_price['total'] or 0


@api_view(['GET'])
def get_order_by_customer_id(request, customer_id):
    try:
        # Filter orders by customer_id
        orders = Order.objects.filter(customer_id=customer_id)
        if not orders.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the queryset
        total = calculate_final_price(customer_id)

        ser = OrderSerializer(orders, many=True)
        return Response({"orders":ser.data, "final_bill":total})
    
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_order_by_order_id(request,order_id):
    try:
        order=Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(OrderSerializer(order).data)


@api_view(['GET'])
def get_order_by_status(request):
    status_param = request.GET.get("status")  # Renamed to avoid conflict with imported status
    customer_id = request.GET.get("id")

    try:
        # Filter orders by status and customer ID
        orders = Order.objects.filter(status=status_param, customer_id=customer_id)
        if not orders.exists():  # Check if no orders are found
            return Response({"detail": "Orders not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize multiple orders, hence many=True
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        return Response({"detail": "Orders not found."}, status=status.HTTP_404_NOT_FOUND)


# This is for customer to delete his order by using customer_id and product_id.
@api_view(['DELETE'])
def cancel_order(request,customer_id,product_id):
    order=Order.objects.get(customer_id=customer_id,product_id=product_id)
    try:
        order.delete()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_405_NOT_FOUND)
    return Response("Order cancelled",status=status.HTTP_200_OK)



# This function is for seller. jiska purpose hai to get orders assigned to them.
@api_view(['GET'])

def get_orders_by_seller(request, id):
    try:
        orders = Order.objects.filter(seller_id=id)  
        if not orders.exists():
            return Response({"message": "No orders found for this seller."}, status=status.HTTP_404_NOT_FOUND)
        
        ser = OrderSerializer(orders, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)



# This function is for seller to delete a particular order.
# doubtful-- rakhe ki delete kare inko?????? Answer: only for development
@api_view(['DELETE'])

def remove_order(request,seller_id,order_id):
    order=Order.objects.get(seller_id=seller_id,order_id=order_id)
    try:
        order.delete()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response("Order cancelled",status=status.HTTP_200_OK)



# This function is for seller to update the status of a particular order.
@api_view(['PUT'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found or seller not authorized to update this order."}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the request is correct or not. (kahi kuch aur toh change nahi kr raha seller.)
    if 'status' not in request.data:
        return Response({"detail": "Status field is required."}, status=status.HTTP_400_BAD_REQUEST)

    new_status = request.data['status']
    
    # validationg the new choice to be present in the available choices or not.
    if new_status not in dict(Order.STATUS_CHOICES).keys():
        return Response({"detail": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)
    
    order.status = new_status
    order.save() 
    ser=OrderSerializer(order)
    return Response(ser.data, status=status.HTTP_200_OK)




