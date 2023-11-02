from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('service_tickets/', views.ticket_list, name='service-tickets'),
    path('service_ticket/delete/<int:schedule_id>/', views.delete_service_ticket, name='delete_service_ticket'),
    path('service_ticket_view/<int:schedule_id>/', views.ticket_view, name='service_ticket_view'),
    path('client_view/<int:client_id>/', views.client_view, name='client_view'),
    path('add_equipment/<int:client_id>/', views.add_equipment, name='add_equipment'),
    path('add_software/<int:client_id>/', views.add_software, name='add_software'),
    path('edit_software/<int:client_id>/', views.edit_software, name='edit_software'),
    path('equipment/<int:equipment_id>/edit_specs/', views.create_or_edit_equipment_specs,
         name='create_or_edit_equipment_specs'),
    path('equipment/<int:equipment_id>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<int:equipment_id>/delete/', views.delete_equipment, name='delete_equipment'),
    path('create-service-form/<int:client_id>/<int:ticket_id>/', views.create_service_form, name='create_service_form'),
    path('create-or-edit-monitor-checklist/<int:equipment_id>/<int:service_id>/<int:client_id>/<int:ticket_id>/',
         views.create_or_edit_monitor_checklist, name='create_or_edit_monitor_checklist'),
    path('create-or-edit-printer-checklist/<int:equipment_id>/<int:service_id>/<int:client_id>/<int:ticket_id>/',
         views.create_or_edit_printer_checklist, name='create_or_edit_printer_checklist'),
    path('create-or-edit-ups-checklist/<int:equipment_id>/<int:service_id>/<int:client_id>/<int:ticket_id>/', views.create_or_edit_ups_checklist,
         name='create_or_edit_ups_checklist'),
    path('service_report/<int:schedule_id>/',views.service_report,name='service_report')
]
