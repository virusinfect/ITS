from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket-list'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('edit-ticket/<int:ticket_id>/', views.edit_ticket, name='edit-ticket'),
    path('create_delivery/<int:ticket_id>/', views.create_delivery, name='create_delivery'),
    path('view_delivery/<int:ticket_id>/', views.view_delivery, name='view_delivery'),
    path('list_deliveries/', views.list_deliveries, name='list_deliveries'),
    path('requisitions/', views.list_requisitions, name='list_requisitions'),
    path('requisitions/add/', views.add_requisition, name='add_requisition'),
    path('requisitions/<int:requisition_id>/change_status/', views.change_requisition_status,
         name='change_requisition_status'),
    path('requisitions/<int:requisition_id>/edit/', views.edit_requisition, name='edit_requisition'),
    path('requisition/delete/<int:requisition_id>/', views.delete_requisition, name='delete_requisition'),
    path('active-call-cards/', views.active_call_cards, name='active_call_cards'),
    path('add-call-card/', views.add_call_card, name='add_call_card'),
    path('edit_call_card/<int:cc_id>/', views.edit_call_card, name='edit_call_card'),
    path('call-card/delete/<int:cc_id>/', views.delete_call_card, name='delete_call_card'),
    path('get-clients/<int:company_id>/', views.get_clients, name='get_clients'),
    path('service/', views.service, name='service'),
    path('get-events/', views.get_events, name='get_events'),
    path('create-service-schedule/', views.create_service_schedule, name='create_service_schedule'),
    path('edit-service-schedule/<int:schedule_id>/', views.edit_service_schedule, name='edit_service_schedule'),
    path('service/delete/<int:schedule_id>/', views.delete_service, name='delete_service'),
    path('sign/<int:delivery_id>/', views.sign, name='sign'),
    path('sign_call/<int:cc_id>/', views.sign_call, name='sign_call'),
    path('get_clients/', views.get_clients, name='get_clients'),
    path('get_products/', views.get_products, name='get_products'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('create-delivery', views.create_delivery_normal, name='create_delivery_normal'),
    path('view_delivery_normal/<int:delivery_id>/', views.view_delivery_normal, name='view_delivery_normal'),
    path('dashboard1/', views.helpdesk_dash, name='helpdesk_dashboard'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
    path('sourcing_ticket/<int:ticket_id>/delete/', views.sourcing_tickets, name='sourcing_ticket'),
    path('quote_ticket/<int:ticket_id>/delete/', views.quote_tickets, name='quote_ticket'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete-entry'),
    path('copy-to-quote/<int:entry_id>/', views.copy_to_quote, name='copy-to-quote'),
    path('report/<int:ticket_id>/', views.report, name='report'),
    path('checklist/<int:client_id>/', views.fill_checklist, name='fill_checklist'),
    path('create_format_approval/<int:ticket_id>/', views.create_format_approval, name='create_format_approval'),
    path('format-approval/<int:format_approval_id>/', views.format_approval_detail, name='format_approval_detail'),
    path('send-format-email/<int:format_approval_id>/', views.send_format_email, name='send_format_email'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
