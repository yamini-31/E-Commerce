from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken
from .models import *
from django.http import JsonResponse
from django.db.models import F, Sum
from .serializer import CustomerSerializer, CartSerializer
from seller_app.serializer import OrderSerializer
from django.shortcuts import get_object_or_404


 #JWT token
def get_access_token(customer):
    access = AccessToken.for_user(customer)
    return str(access)

# Signup view
@api_view(['POST'])
def customer_signup(request):
    data = request.data
    data['customer_password'] = make_password(data['customer_password'])  # Hash the password
    serializer = CustomerSerializer(data=data)

    if serializer.is_valid():
        customer = serializer.save()  
        access_token = get_access_token(customer)  
        return Response({'customer': serializer.data, 'access': access_token}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
@api_view(['POST'])
def customer_login(request):
    username = request.data.get('customer_username')
    password = request.data.get('customer_password')

   
    customers = Customer.objects.filter(customer_username=username)

   
    if customers.exists():
        customer = customers.first()  

        if check_password(password, customer.customer_password):
            access_token = get_access_token(customer)  # Use the same function to get the access token
            return Response({'message': 'Login successful', 'access': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
#protected route
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def protected_view(request):
#    return Response({"message": "You have accessed a protected route!"}, status=status.HTTP_200_OK)


#get all the customer
@api_view(['GET'])
def list_customers(request):
    
    customers = Customer.objects.all()
    
    
    serializer =CustomerSerializer(customers, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)



#get customer by id
@api_view(['GET'])
def get_customer_by_id(request, customer_id):
    try:
        
        customer = Customer.objects.get(id=customer_id)
        
        
        serializer = CustomerSerializer(customer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        
        return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
#update the customer details


@api_view(['PUT'])
def update_customer(request, customer_id):
    try:
        
        customer = Customer.objects.get(id=customer_id)
        
        
        serializer = CustomerSerializer(customer, data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Customer.DoesNotExist:
        
        return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)



#add item to the cart

@api_view(['POST'])
def add_product_to_cart(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    customer = get_object_or_404(Customer, customer_id=customer_id)
    product = get_object_or_404(Product, product_id=product_id)

    price = product.product_price
   
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': quantity, 'price': price}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'message': 'Product added to cart successfully', 'cart_item_id': cart_item.id})



#remove item from the cart
@api_view(['DELETE'])
def remove_product_from_cart(request):
    cart_item_id = request.data.get('cart_item_id')

    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()

    return JsonResponse({'message': 'Product removed from cart successfully'})



@api_view(['POST'])
def place_order_from_cart(request):
    customer_id = request.data.get('customer_id')
    cartObjects=Cart.objects.filter(customer_id=customer_id)
    
    # serializer = CartSerializer(cartObjects, many=True)
    seller_ids = [cart_item.product.seller_id for cart_item in cartObjects]

    # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    # seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    # quantity = models.IntegerField()

    for index,cartob in enumerate(cartObjects):

        data={
            "customer_id":cartob.customer.customer_id,
            "product_id":cartob.product.product_id,
            "seller_id":seller_ids[index],
            "quantity":cartob.quantity,
            "total_bill":(cartob.quantity*cartob.price),
            "status":"pending"
        }

        print(data)

        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order_serializer.save()
        else:
            return Response({'message': 'Some problem'}, status=400)
    return Response({"message":f"added all items to cart {len(seller_ids)}"}, status=201)

    
@api_view(['GET'])
def show_cart(request, customer_id):
    try:
    # Filter orders by customer_id
        cartItems = Cart.objects.filter(customer_id=customer_id)
        if not cartItems.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the queryset
        ser = CartSerializer(cartItems, many=True)
        return Response(ser.data)

    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



#calculate the final bill of the cart 

# Function to calculate the total price of the cart
def calculate_final_price(customer_id):
    cart_items = Cart.objects.filter(customer_id=customer_id)
    
    
    total_price = cart_items.annotate(
        final_price=F('quantity') * F('price')
    ).aggregate(total=Sum('final_price'))
    
    return total_price['total'] or 0


@api_view(['GET'])
def get_cart_total(request, customer_id):
    total = calculate_final_price(customer_id)
    return Response({'total_price': total})