from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', customer_signup, name='customer-signup'),
    path('login/', customer_login, name='customer-login'),
    path('protected/', protected_view, name='protected-route'),
    path('customers/', list_customers, name='list_customers'),
    path('customer/<int:customer_id>/', get_customer_by_id, name='get_customer_by_id'),
    path('customer/update/<int:customer_id>/', update_customer, name='update_customer'),
    
]
