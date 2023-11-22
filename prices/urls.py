# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('view/', views.view_laptop_price_list, name='view_price_list'),
    path('upload/', views.upload_price_list, name='upload_price_list'),
    path('upload_coloursoft/', views.upload_coloursoft_price_list, name='upload_coloursoft_price_list'),
    path('upload_fellowes/', views.upload_fellowes_price_list, name='upload_fellowes_price_list'),
    path('create_supplier/', views.create_supplier, name='create-supplier'),
    path('create_brand/', views.create_brand, name='create_brand'),
    path('create_equipment/', views.create_equipment, name='create-equipment'),
    path('list_suppliers/', views.list_suppliers, name='list-suppliers'),
    path('list_brands/', views.list_brands, name='list_brands'),
    path('list_equipment/', views.list_equipment, name='list-equipment'),
    path('search/', views.search_laptops, name='search_laptops'),
    path('search_coloursoft/', views.search_coloursoft, name='search_coloursoft'),
    path('search_fellowes/', views.search_fellowes, name='search_fellowes'),
    path('exchange/', views.edit_exchange, name='edit_exchange'),
    # Add other URLs as needed
]
