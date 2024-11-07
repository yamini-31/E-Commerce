from rest_framework import serializers
from .models import Order, Seller
from customer_app.models import Customer
from product_app.models import Product
from django.contrib.auth.hashers import make_password


class OrderSerializer(serializers.ModelSerializer):
    # Optionally, you can show related `Customer` and `Product` details
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = '__all__'



class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['seller_id', 'name', 'email', 'shop_address', 'phone_number', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Password will not be included in the response
        }

    def create(self, validated_data):
        # Hash the password using Django's make_password utility
        validated_data['password'] = make_password(validated_data['password'])
        # Create and save the Seller instance with the hashed password
        seller = Seller.objects.create(**validated_data)
        return seller