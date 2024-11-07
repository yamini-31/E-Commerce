from rest_framework import serializers
from .models import Customer,Cart

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields="__all__"
    def create(self, validated_data):
        # Hash the password before saving it
        password = validated_data.pop('customer_password', None)
        customer = Customer(**validated_data)

        if password:
            customer.set_password(password)  # Hash the password
        customer.save()
        return customer

class CustomerLoginSerializer(serializers.Serializer):
    customer_username = serializers.CharField()
    password = serializers.CharField()

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"
