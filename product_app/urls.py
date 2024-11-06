from django.urls import path
from .views import (
    get_all_products,
    add_product,
    get_product_by_id,
    get_product_by_name,
    get_product_by_category,
    get_product_by_seller_id
)

urlpatterns = [
    path('', get_all_products, name='get_all_products'),
    path('add_product/', add_product, name='add_product'),
    path('product_id/', get_product_by_id, name='get_product_by_id'),
    path('name/', get_product_by_name, name='get_product_by_name'),
    path('category/', get_product_by_category, name='get_product_by_category'),
    path('seller/', get_product_by_seller_id, name='get_product_by_seller_id'),
]
