from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_view, name='home'),
    path('get_clients/', views.get_clients, name='get_clients'),
    path('parts-categories/', views.parts_categories_list, name='parts-categories-list'),
    path('parts/', views.parts_list, name='parts-list'),
    path('add-category/', views.add_category, name='add-category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit-category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete-category'),
    path('add-part/', views.add_part, name='add-part'),
    path('edit-part/<int:part_id>/', views.edit_part, name='edit-part'),
    path('delete-part/<int:part_id>/', views.delete_part, name='delete-part'),
    path('companies/', views.company_list, name='company-list'),
    path('companies_create/', views.create_company, name='create-company'),
    path('companies_edit/<int:company_id>/', views.edit_company, name='edit-company'),
    path('companies_delete/<int:company_id>/', views.delete_company, name='delete-company'),
    path('companies/<int:company_id>/clients/', views.client_list, name='client-list'),
    path('companies/<int:company_id>/clients/create/', views.create_client, name='create-client'),
    path('user_list/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('create_user/', views.create_user, name='create_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('tasks/', views.Tasks, name='tasks'),
    path('task/<int:task_id>/', views.view_task_details, name='view_task_details'),
    path('push/', views.pushjs, name='push'),
    path('save-signature-view/', views.save_signature_view, name='save_signature'),
    path('save-signature-view-call/', views.save_signature_view_call, name='save_signature_call'),
    path('save-signature-view-format/', views.save_signature_view_format, name='save_signature_format'),
    path('form/<uuid:token>/', views.form_with_uuid, name='form_with_uuid'),
    path('form_not_found/', views.form_not_found, name='form_not_found'),
    path('get_personal/', views.get_personal, name='get_personal'),
    path('personal_task/', views.personal_task, name='personal_task'),
    path('create_personal_task/', views.create_personal_task, name='create_personal_task'),
    path('personal/delete/<int:task_id>/', views.delete_personal_task, name='delete_personal_task'),

]
