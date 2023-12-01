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
    path('search_js/', views.search_laptops_js, name='search_laptops_js'),
    path('search_coloursoft/', views.search_coloursoft, name='search_coloursoft'),
    path('search_fellowes/', views.search_fellowes, name='search_fellowes'),
    path('exchange/', views.edit_exchange, name='edit_exchange'),
    path('equipment/<int:equipment_id>/', views.price_rules_for_equipment, name='price_rules_for_equipment'),
    path('types/', views.type_list, name='type_list'),
    path('types/create/', views.create_type, name='create_type'),
    path('types/edit/<int:type_id>/', views.edit_type, name='edit_type'),
    path('types/delete/<int:type_id>/', views.delete_type, name='delete_type'),
    path('api/get_types/', views.get_types, name='get_types'),
    path('laptop_prices/edit/<int:laptop_price_id>/', views.edit_laptop_price, name='edit_laptop_price'),
    path('laptop_prices/delete/<int:laptop_price_id>/', views.delete_laptop_price, name='delete_laptop_price'),
    # Add other URLs as needed
]
