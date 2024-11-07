from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields="__all__"
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"