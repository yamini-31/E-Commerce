from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken
from .models import Customer
from .serializers import CustomerSerializer

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





