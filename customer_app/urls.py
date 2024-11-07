from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', register_customer, name='customer-signup'),
    path('login/', login_customer, name='customer-login'),
    path('protected/',protected_route, name='protected-route'),
    path('', list_customers, name='list_customers'),
    path('<int:customer_id>/', get_customer_by_id, name='get_customer_by_id'),
    path('update/<int:customer_id>/', update_customer, name='update_customer'),
    
    
    #cart urls
    path('cart/add/', add_product_to_cart, name='add_product_to_cart'),
    path('cart/remove/', remove_product_from_cart, name='remove_product_from_cart'),
    path('cart/total/<int:customer_id>/', get_cart_total, name='get_cart_total'),
    
]
