from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, SellerSerializer
from .models import Order, Seller


@api_view(['GET'])
def get_order(request):
    orders=Order.objects.all()
    ser=OrderSerializer(orders, many=True)
    return Response(ser.data)


@api_view(['GET'])
def get_order_by_id(request,id):
    try:
        order=Order.objects.get(pk=id)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(OrderSerializer(order).data)


@api_view(['DELETE'])
def cancel_order(request,id):
    order=Order.objects.get(pk=id)
    try:
        order.delete()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response("Order cancelled",status=status.HTTP_200_OK)

@api_view(['GET'])
def get_order_by_status(request,status):
    order=Order.objects.get(status)
    try:
        order=Order.objects.get('status')
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(OrderSerializer(order).data)







