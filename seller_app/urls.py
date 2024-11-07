from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('show_all_orders/', get_order, name='get_order'),
    path('orders_custid/<int:customer_id>/', get_order_by_customer_id, name='get_order_by_customer_id'),
    path('orders_odr_id/<int:order_id>/', get_order_by_order_id, name='get_order_by_order_id'),
    path('orders_stat/', get_order_by_status, name='get_order_by_status'),
    path('orders_cancel/<int:customer_id>/<int:product_id>/', cancel_order, name='cancel_order'),
    path('orders_seller/<int:id>/', get_orders_by_seller, name='get_order_by_seller'),
    path('orders_delete/<int:seller_id>/<int:order_id>/', remove_order, name='remove_order'),
    path('orders_update_stat/<int:order_id>/', update_order_status, name='update_order_status'),

    
    path('seller_signup/', seller_signup, name='update_order_status'),

]
