from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializer import ProductSerializer
from rest_framework.decorators import api_view
from project.utils import generate_jwt_token, decode_jwt_token
from project.utils import auth_required

@api_view(["GET"])
# @auth_required
def get_all_products(request):
    payload = getattr(request, 'payload', {})  # This will default to an empty dictionary if 'payload' does not exist

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"data":serializer.data})

@api_view(["POST"])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product added successfully', 'product_id': serializer.data['product_id']}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def get_product_by_id(request):
    
    
    product_id = request.GET.get('product_id')
    if not product_id:
        return Response({'error': 'id parameter is required'}, status=400)
    
    try:
        product = Product.objects.get(product_id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(["GET"])
def get_product_by_name(request):
    name = request.GET.get('name')
    if not name:
        return Response({'error': 'name parameter is required'}, status=400)

    products = Product.objects.filter(product_name__icontains=name)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_product_by_category(request):
    category = request.GET.get('category')
    if not category:
        return Response({'error': 'category parameter is required'}, status=400)

    products = Product.objects.filter(product_category__iexact=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_product_by_seller_id(request):
    seller_id = request.GET.get('seller_id')
    if not seller_id:
        return Response({'error': 'seller_id parameter is required'}, status=400)

    products = Product.objects.filter(seller_id=seller_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
