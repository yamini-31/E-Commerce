from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', customer_signup, name='customer-signup'),
    path('login/', customer_login, name='customer-login'),
    #path('protected/', protected_view, name='protected-route'),
    path('customers/', list_customers, name='list_customers'),
    path('customer/<int:customer_id>/', get_customer_by_id, name='get_customer_by_id'),
    path('customer/update/<int:customer_id>/', update_customer, name='update_customer'),
    
    
    #cart urls
    path('cart/add/', add_product_to_cart, name='add_product_to_cart'),
    path('cart/remove/', remove_product_from_cart, name='remove_product_from_cart'),
    path('cart/total/<int:customer_id>/', get_cart_total, name='get_cart_total'),
    path('cart/place_order_from_cart/', place_order_from_cart, name='place_order_from_cart'),
    path('cart/show_cart/<int:customer_id>', show_cart, name='place_order_from_cart'),



    #JWT token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    
]