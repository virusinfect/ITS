from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket-list'),
    path('inhouse_tickets/', views.inhouse_ticket_list, name='inhouse-ticket-list'),
    path('create_inhouse_ticket/', views.create_Inhouse_ticket, name='create_inhouse_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('inhouse-ticket/<int:ticket_id>/delete/', views.delete_inhouse_ticket, name='delete_inhouse_ticket'),
    path('edit-ticket/<int:ticket_id>/', views.edit_ticket, name='edit-ticket'),
    path('edit-inhouse-ticket/<int:ticket_id>/', views.edit_inhouse_ticket, name='edit_inhouse_ticket'),
    path('print-ticket/<int:ticket_id>/', views.ticket_print, name='ticket_print'),
    path('inhouse-print-ticket/<int:ticket_id>/', views.inhouse_ticket_print, name='inhouse_ticket_print'),
    path('create_delivery/<int:ticket_id>/', views.create_delivery, name='create_delivery'),
    path('create_inhouse_delivery/<int:ticket_id>/', views.create_inhouse_delivery, name='create_inhouse_delivery'),
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
    path('dashboard3/', views.tech_dash, name='tech_dashboard'),
    path('dashboard4/', views.store_dash, name='store_dashboard'),
    path('dashboard5/', views.acc_dash, name='acc_dashboard'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
    path('sourcing_ticket/<int:ticket_id>/delete/', views.sourcing_tickets, name='sourcing_ticket'),
    path('sourcing_inhouseticket/<int:ticket_id>/delete/', views.sourcing_inhousetickets, name='sourcing_inhouseticket'),
    path('quote_ticket/<int:ticket_id>/delete/', views.quote_tickets, name='quote_ticket'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete-entry'),
    path('delete-entry-quote/<int:entry_id>/', views.delete_entry_quote, name='delete-entry-quote'),
    path('copy-to-quote/<int:entry_id>/', views.copy_to_quote, name='copy-to-quote'),
    path('report/<int:report_id>/', views.report, name='report'),
    path('create_format_approval/<int:ticket_id>/', views.create_format_approval, name='create_format_approval'),
    path('format-approval/<int:format_approval_id>/', views.format_approval_detail, name='format_approval_detail'),
    path('send-format-email/<int:format_approval_id>/', views.send_format_email, name='send_format_email'),
    path('tr_status/<str:tr_status>/', views.tr_status_tickets, name='tr_status_tickets'),
    path('pending_requisitions/<str:status>/', views.pending_requisitions, name='pending_requisitions'),
    path('bench_status/<str:type>/<str:title>/<str:bench_status>/', views.bench_status_tickets,
         name='bench_status_tickets'),
    path('inhouse_bench_status_tickets/<str:title>/<str:bench_status>/', views.inhouse_bench_status_tickets,
         name='inhouse_bench_status_tickets'),
    path('status/<str:status>/<str:title>/', views.status_tickets, name='status_tickets'),
    path('remark/<str:remark>/<str:title>/', views.remark_tickets, name='remark_tickets'),
    path('tickets-created-monthly/', views.tickets_created_monthly_this_year, name='tickets_created_monthly_this_year'),
    path('tickets-created-monthly-tech/', views.tickets_created_monthly_this_year_tech,
         name='tickets_created_monthly_this_year_tech'),
    path('tr-status-pie-chart/', views.tr_status_pie_chart, name='tr_status_pie_chart'),
    path('service-schedules-yearly/', views.service_schedules_yearly, name='service_schedules_yearly'),
    path('service-schedules-yearly-tech/', views.service_schedules_yearly_tech, name='service_schedules_yearly_tech'),
    path('remark-pie-chart/', views.remark_pie_chart, name='remark_pie_chart'),
    path('bench-status-pie-chart/', views.bench_status_pie_chart, name='bench_status_pie_chart'),
    path('status-pie-chart/', views.status_pie_chart, name='status_pie_chart'),
    path('requisitions-created-monthly/', views.requisitions_created_monthly, name='requisitions_created_monthly'),
    path('requisitions_returned/', views.requisitions_returned, name='requisitions_returned'),
    path('requisitions-created-monthly-tec/', views.requisitions_created_monthly_tech,
         name='requisitions_created_monthly_tech'),
    path('generate_report/<int:ticket_id>/', views.generate_report, name='generate_report'),
    path('approve_report/<int:report_id>/', views.approve_report, name='approve_report'),
    path('mark_sent_for_approval/<int:report_id>/', views.mark_sent_for_approval, name='mark_sent_for_approval'),
    path('technical_reports/', views.TechnicalReportListView.as_view(), name='technical_report_list'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('save-signature-view-ticket/', views.save_signature_view_ticket, name='save-signature-view-ticket'),
    path('save-signature-view-inhouse-ticket/', views.save_signature_view_inhouse_ticket,
         name='save-signature-view-inhouse-ticket'),
    path('add-client/', views.add_client, name='add_client'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('edit_delivery/<int:delivery_id>/', views.edit_delivery, name='edit_delivery'),
    path('delete_item/<int:delivery_id>/<int:item_id>/', views.delete_item, name='delete_item'), ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
