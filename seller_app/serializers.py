from rest_framework import serializers
from .models import Order, Seller
from ..customer_app.models import Customer
from ..product_app.models import Product

class OrderSerializer(serializers.ModelSerializer):
    # Optionally, you can show related `Customer` and `Product` details
    cust_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['id', 'cust_id', 'product_id', 'quantity', 'status', 'total_bill']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'shop_address', 'phone_number', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hash the password before saving the seller instance
        seller = Seller(
            name=validated_data['name'],
            email=validated_data['email'],
            shop_address=validated_data['shop_address'],
            phone_number=validated_data['phone_number'],
            username=validated_data['username']
        )
        seller.set_password(validated_data['password'])  # Hash password
        seller.save()
        return seller
