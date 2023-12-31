import base64
import datetime
import math
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.http import HttpResponseNotFound, Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from its.models import Company, Clients, Parts, PartsCategory, Task
from service.models import Equipment

from .forms import TsourcingForm
from .models import Tickets, ProductDetail, Delivery, Items, Requisition, CallCards, ServiceSchedules, ServiceTickets, \
    Deliverys, Tsourcing, tQuote, FormatApproval, UniqueToken, FSignature, TechnicalReport, TSignature, TicketImage, \
    TechSignature, InhouseTickets, InhouseTSignature, InhouseTicketImage, InhouseTsourcing, inhousetQuote, \
    InhouseProductDetail


@login_required
def helpdesk_dash(request):
    tickets = ServiceSchedules.objects.filter(is_active=1).order_by('-created')
    ticket_count = tickets.count()
    # Define the list of statuses you want to count
    statuses_to_count = [
        "Open",
    ]

    # Initialize a dictionary to store the counts for each status
    status_counts = {}

    # Loop through each status and count the tickets with that status
    for status in statuses_to_count:
        count = Tickets.objects.filter(status=status, is_active=1).count()
        status_counts[status] = count

    req_statuses_to_count = [
        "Pending",
    ]

    # Initialize a dictionary to store the counts for each status
    req_status_counts = {}

    # Loop through each status and count the tickets with that status
    for status in req_statuses_to_count:
        count = Requisition.objects.filter(req_status=status, is_active=1).count()
        req_status_counts[status] = count

    # Define the list of remarks you want to count
    remarks_to_count = [
        "Awaiting feedback",
        "Awaiting parts",
        "Repairs",
        "LPO follow up",
        "MD LPO follow up",
        "To be collected",
        "To be delivered",
        "Warranty",
    ]

    # Initialize a dictionary to store the counts for each remark
    remark_counts = {}

    # Loop through each remark and count the tickets with that remark
    for remark in remarks_to_count:
        count = Tickets.objects.filter(remark=remark, is_active=1).count()
        remark_counts[remark] = count

    bench_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    bench_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for bench_status in bench_statuses_to_count:
        count = Tickets.objects.filter(bench_status=bench_status, type="Bench", is_active=1).count()
        bench_status_counts[bench_status] = count

    inhouse_bench_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    inhouse_bench_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for bench_status in inhouse_bench_statuses_to_count:
        count = InhouseTickets.objects.filter(bench_status=bench_status, is_active=1).count()
        inhouse_bench_status_counts[bench_status] = count

    site_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    site_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for site_status in site_statuses_to_count:
        count = Tickets.objects.filter(bench_status=site_status, type="On-site", is_active=1).count()
        site_status_counts[site_status] = count

        # Define the list of tr_statuses you want to count
    tr_statuses_to_count = [
        "Follow up",
        "Awaiting LPO",
        "On hold",
        "Not interested",
        "Done",
    ]

    # Initialize a dictionary to store the counts for each tr_status
    tr_status_counts = {}

    # Loop through each tr_status and count the tickets with that tr_status
    for tr_status in tr_statuses_to_count:
        count = Tickets.objects.filter(tr_status=tr_status, is_active=1).count()
        tr_status_counts[tr_status] = count

    return render(request, "technical/helpdesk_dashboard.html",
                  {'remark_counts': remark_counts, 'site_status_counts': site_status_counts,
                   'bench_status_counts': bench_status_counts,
                   'status_counts': status_counts, 'req_status_counts': req_status_counts,
                   'tr_status_counts': tr_status_counts, 'inhouse_bench_status_counts': inhouse_bench_status_counts,
                   'ticket_count': ticket_count})


@login_required
def tech_dash(request):
    # Define the list of statuses you want to count
    statuses_to_count = [
        "Open",
    ]

    # Initialize a dictionary to store the counts for each status
    status_counts = {}

    # Loop through each status and count the tickets with that status
    for status in statuses_to_count:
        count = Tickets.objects.filter(status=status, is_active=1).count()
        status_counts[status] = count
    # Define the list of remarks you want to count
    remarks_to_count = [
        "Awaiting feedback",
        "Awaiting parts",
        "Repairs",
        "LPO follow up",
        "MD LPO follow up",
        "To be collected",
        "To be delivered",
        "Warranty",
    ]

    # Initialize a dictionary to store the counts for each remark
    remark_counts = {}

    # Loop through each remark and count the tickets with that remark
    for remark in remarks_to_count:
        count = Tickets.objects.filter(remark=remark, is_active=1).count()
        remark_counts[remark] = count

    bench_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    bench_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for bench_status in bench_statuses_to_count:
        count = Tickets.objects.filter(bench_status=bench_status, type="Bench", is_active=1, tech=request.user).count()
        bench_status_counts[bench_status] = count

    site_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    site_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for site_status in site_statuses_to_count:
        count = Tickets.objects.filter(bench_status=site_status, type="On-site", is_active=1, tech=request.user).count()
        site_status_counts[site_status] = count

        # Define the list of tr_statuses you want to count
    tr_statuses_to_count = [
        "Follow up",
        "Awaiting LPO",
        "On hold",
        "Not interested",
        "Done",
    ]

    # Initialize a dictionary to store the counts for each tr_status
    tr_status_counts = {}

    # Loop through each tr_status and count the tickets with that tr_status
    for tr_status in tr_statuses_to_count:
        count = Tickets.objects.filter(tr_status=tr_status, is_active=1).count()
        tr_status_counts[tr_status] = count

    return render(request, "technical/tech_dashboard.html",
                  {'remark_counts': remark_counts, 'bench_status_counts': bench_status_counts,
                   'status_counts': status_counts, 'tr_status_counts': tr_status_counts})


@login_required
def store_dash(request):
    returned_requisitions_count = Requisition.objects.filter(issue_status="returned",
                                                             return_status__isnull=True).count()
    pending_approved_requisitions_count = Requisition.objects.filter(req_status="Approved",
                                                                     issue_status="Pending").count()
    # Define the list of statuses you want to count
    statuses_to_count = [
        "Open",
    ]

    # Initialize a dictionary to store the counts for each status
    status_counts = {}

    # Loop through each status and count the tickets with that status
    for status in statuses_to_count:
        count = Tickets.objects.filter(status=status, is_active=1).count()
        status_counts[status] = count
    # Define the list of remarks you want to count
    remarks_to_count = [
        "Awaiting feedback",
        "Awaiting parts",
        "Repairs",
        "LPO follow up",
        "MD LPO follow up",
        "To be collected",
        "To be delivered",
        "Warranty",
    ]

    # Initialize a dictionary to store the counts for each remark
    remark_counts = {}

    # Loop through each remark and count the tickets with that remark
    for remark in remarks_to_count:
        count = Tickets.objects.filter(remark=remark, is_active=1).count()
        remark_counts[remark] = count

    bench_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    bench_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for bench_status in bench_statuses_to_count:
        count = Tickets.objects.filter(bench_status=bench_status, type="Bench", is_active=1, tech=request.user).count()
        bench_status_counts[bench_status] = count

    site_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    site_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for site_status in site_statuses_to_count:
        count = Tickets.objects.filter(bench_status=site_status, type="On-site", is_active=1, tech=request.user).count()
        site_status_counts[site_status] = count

        # Define the list of tr_statuses you want to count
    tr_statuses_to_count = [
        "Follow up",
        "Awaiting LPO",
        "On hold",
        "Not interested",
        "Done",
    ]

    # Initialize a dictionary to store the counts for each tr_status
    tr_status_counts = {}

    # Loop through each tr_status and count the tickets with that tr_status
    for tr_status in tr_statuses_to_count:
        count = Tickets.objects.filter(tr_status=tr_status, is_active=1).count()
        tr_status_counts[tr_status] = count

    return render(request, "technical/store_dashboard.html",
                  {'remark_counts': remark_counts, 'bench_status_counts': bench_status_counts,
                   'status_counts': status_counts, 'tr_status_counts': tr_status_counts,
                   'returned_requisitions_count': returned_requisitions_count,
                   'pending_approved_requisitions_count': pending_approved_requisitions_count})


@login_required
def acc_dash(request):
    reports = TechnicalReport.objects.filter(active=1, is_approved="approved").order_by('-created')
    reports_count = reports.count()

    returned_requisitions_count = Requisition.objects.filter(issue_status="returned",
                                                             return_status__isnull=True).count()
    pending_approved_requisitions_count = Requisition.objects.filter(req_status="Approved",
                                                                     issue_status="Pending").count()
    # Define the list of statuses you want to count
    statuses_to_count = [
        "Open",
    ]

    # Initialize a dictionary to store the counts for each status
    status_counts = {}

    # Loop through each status and count the tickets with that status
    for status in statuses_to_count:
        count = Tickets.objects.filter(status=status, is_active=1).count()
        status_counts[status] = count
    # Define the list of remarks you want to count
    remarks_to_count = [
        "Awaiting feedback",
        "Awaiting parts",
        "Repairs",
        "LPO follow up",
        "MD LPO follow up",
        "To be collected",
        "To be delivered",
        "Warranty",
    ]

    # Initialize a dictionary to store the counts for each remark
    remark_counts = {}

    # Loop through each remark and count the tickets with that remark
    for remark in remarks_to_count:
        count = Tickets.objects.filter(remark=remark, is_active=1).count()
        remark_counts[remark] = count

    bench_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    bench_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for bench_status in bench_statuses_to_count:
        count = Tickets.objects.filter(bench_status=bench_status, type="Bench", is_active=1, tech=request.user).count()
        bench_status_counts[bench_status] = count

    site_statuses_to_count = [
        "Pending"
    ]

    # Initialize a dictionary to store the counts for each bench status
    site_status_counts = {}

    # Loop through each bench status and count the tickets with that status
    for site_status in site_statuses_to_count:
        count = Tickets.objects.filter(bench_status=site_status, type="On-site", is_active=1, tech=request.user).count()
        site_status_counts[site_status] = count

        # Define the list of tr_statuses you want to count
    tr_statuses_to_count = [
        "Follow up",
        "Awaiting LPO",
        "On hold",
        "Not interested",
        "Done",
    ]

    # Initialize a dictionary to store the counts for each tr_status
    tr_status_counts = {}

    # Loop through each tr_status and count the tickets with that tr_status
    for tr_status in tr_statuses_to_count:
        count = Tickets.objects.filter(tr_status=tr_status, is_active=1).count()
        tr_status_counts[tr_status] = count

    return render(request, "technical/acc_dashboard.html",
                  {'remark_counts': remark_counts, 'bench_status_counts': bench_status_counts,
                   'status_counts': status_counts, 'tr_status_counts': tr_status_counts,
                   'returned_requisitions_count': returned_requisitions_count,
                   'pending_approved_requisitions_count': pending_approved_requisitions_count,
                   'reports_count': reports_count})


@login_required
def remark_tickets(request, remark, title):
    title = title
    # Filter tickets with the specified remark and that are active
    tickets = Tickets.objects.filter(remark=remark, is_active=1)

    return render(request, 'technical/ticket_list.html', {'tickets': tickets, 'title': title})


@login_required
def approved_technical_reports(request):
    reports = TechnicalReport.objects.filter(active=1, is_approved="approved").order_by('-created')
    return render(request, 'technical/technical_report_list.html', {'reports': reports})


@login_required
def status_tickets(request, status, title):
    title = title
    # Filter tickets with the specified status and that are active
    tickets = Tickets.objects.filter(status=status, is_active=1)

    return render(request, 'technical/ticket_list.html', {'tickets': tickets, 'title': title})


@login_required
def pending_requisitions(request, status):
    requisitions = Requisition.objects.filter(req_status=status, is_active=True).order_by('-created')
    return render(request, 'technical/list_requisitions.html', {'requisitions': requisitions})


@login_required
def bench_status_tickets(request, type, bench_status, title):
    title = title
    if request.user.groups.filter(name='Technician').exists():
        # If the user belongs to the "Technician" group, show only their assigned tickets
        tickets = Tickets.objects.filter(tech=request.user, is_active=1, bench_status=bench_status, type=type).order_by(
            '-created')
    else:
        # If the user doesn't belong to the "Technician" group, show all tickets
        tickets = Tickets.objects.filter(is_active=1, bench_status=bench_status, type=type).order_by('-created')

    return render(request, 'technical/ticket_list.html', {'tickets': tickets, 'title': title})


def inhouse_bench_status_tickets(request, bench_status, title):
    title = title
    if request.user.groups.filter(name='Technician').exists():
        # If the user belongs to the "Technician" group, show only their assigned tickets
        tickets = InhouseTickets.objects.filter(tech=request.user, is_active=1, bench_status=bench_status).order_by(
            '-created')
    else:
        # If the user doesn't belong to the "Technician" group, show all tickets
        tickets = InhouseTickets.objects.filter(is_active=1, bench_status=bench_status).order_by('-created')

    return render(request, 'technical/inhouse_ticket_list.html', {'tickets': tickets, 'title': title})


@login_required
def tr_status_tickets(request, tr_status):
    # Filter tickets with the specified tr_status and that are active
    tickets = Tickets.objects.filter(tr_status=tr_status, is_active=1)

    return render(request, 'technical/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_list(request):
    title = "Ticket List"
    if request.user.groups.filter(name='Technician').exists():
        # If the user belongs to the "Technician" group, show only their assigned tickets
        tickets = Tickets.objects.filter(tech=request.user, is_active=1).order_by('-created')[:50]
    else:
        # If the user doesn't belong to the "Technician" group, show all tickets
        tickets = Tickets.objects.filter(is_active=1).order_by('-created')

    return render(request, 'technical/ticket_list.html', {'tickets': tickets, 'title': title})


@login_required
def inhouse_ticket_list(request):
    title = "Inhouse Ticket List"
    if request.user.groups.filter(name='Technician').exists():
        # If the user belongs to the "Technician" group, show only their assigned tickets
        tickets = InhouseTickets.objects.filter(tech=request.user, is_active=1).order_by('-created')
    else:
        # If the user doesn't belong to the "Technician" group, show all tickets
        tickets = InhouseTickets.objects.filter(is_active=1).order_by('-created')

    return render(request, 'technical/inhouse_ticket_list.html', {'tickets': tickets, 'title': title})


@login_required
def sign(request, delivery_id):
    return render(request, "sign.html", {'delivery_id': delivery_id})


def sign_call(request, cc_id):
    return render(request, "sign_call.html", {'cc_id': cc_id})


@login_required
def delivery_list(request):
    deliveries = Deliverys.objects.all()
    return render(request, 'sign3.html', {'deliveries': deliveries})


@login_required
def ticket_print(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)

    try:
        # Try to get the TechSignature for the ticket
        signature = TSignature.objects.get(ticket=ticket)
    except TSignature.DoesNotExist:
        # If TechSignature does not exist, provide a default value or handle it as needed
        signature = None  # You can set a default value or leave it as None

    try:
        # Try to get the TechSignature for the ticket
        tech_signature = TechSignature.objects.get(tech=ticket.tech)
    except TechSignature.DoesNotExist:
        # If TechSignature does not exist, provide a default value or handle it as needed
        tech_signature = None  # You can set a default value or leave it as None
    return render(request, 'technical/ticket_print.html',
                  {'ticket': ticket, 'signature': signature, 'tech_signature': tech_signature})


@login_required
def inhouse_ticket_print(request, ticket_id):
    ticket = get_object_or_404(InhouseTickets, ticket_id=ticket_id)

    try:
        # Try to get the TechSignature for the ticket
        signature = InhouseTSignature.objects.get(ticket=ticket)
    except TSignature.DoesNotExist:
        # If TechSignature does not exist, provide a default value or handle it as needed
        signature = None  # You can set a default value or leave it as None

    try:
        # Try to get the TechSignature for the ticket
        tech_signature = TechSignature.objects.get(tech=ticket.tech)
    except TechSignature.DoesNotExist:
        # If TechSignature does not exist, provide a default value or handle it as needed
        tech_signature = None  # You can set a default value or leave it as None
    return render(request, 'technical/inhouse_ticket_print.html',
                  {'ticket': ticket, 'signature': signature, 'tech_signature': tech_signature})


@login_required
def edit_ticket(request, ticket_id):
    technician_group = Group.objects.get(name='Technician')
    users = technician_group.user_set.filter(is_active=True)
    sales_group = Group.objects.get(name='Sales')
    sales = sales_group.user_set.all()
    companies = Company.objects.all().order_by("name")
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    product_details = ProductDetail.objects.filter(ticket=ticket.ticket_id)
    tsourcing_data = Tsourcing.objects.filter(ticket=ticket)
    tquote_data = tQuote.objects.filter(ticket=ticket)
    action_images = TicketImage.objects.filter(ticket=ticket, tag="action")
    diagnosis_images = TicketImage.objects.filter(ticket=ticket, tag="diagnosis")
    recommendation_images = TicketImage.objects.filter(ticket=ticket, tag="recommendation")

    try:
        requisitions = Requisition.objects.filter(ticket=ticket, is_active=True)
    except Requisition.DoesNotExist:
        requisitions = None

    try:
        parts = Requisition.objects.filter(ticket=ticket, is_active=True, issue_status="Issue")
    except Requisition.DoesNotExist:
        parts = None

    if request.method == 'POST':
        # Handle form submission and update ticket details here
        # Example:
        form_type = request.POST.get('form_type')
        if form_type == 'form1':
            selected_technician_id = request.POST.get('tech')
            print("data")
            print(selected_technician_id)
            saved_technician = ticket.tech
            ticket.type = request.POST.get('type')
            client = request.POST.get('client')
            ticket.recommendation = request.POST.get('recommendation')
            ticket.equipment = request.POST.get('equipment')
            ticket.serial_no = request.POST.get('serial_no')
            ticket.fault = request.POST.get('fault')
            ticket.notes = request.POST.get('notes')
            ticket.diagnosis = request.POST.get('diagnosis')
            ticket.action = request.POST.get('action')
            ticket.accessories = request.POST.get('accessories')
            if selected_technician_id:
                ticket.tech_id = selected_technician_id
            ticket.updated = timezone.now()
            ticket.accessories = request.POST.get('accessories')
            ticket.updated = timezone.now()
            # Update other fields similarly
            if ticket.client != client:
                ticket.client_id = client

            # Save the changes
            ticket.save()
            image1 = request.FILES.get('action_image')
            image2 = request.FILES.get('diagnosis_image')
            image3 = request.FILES.get('recommendation_image')

            if image1:  # Check if image1 is not empty
                TicketImage.objects.create(ticket=ticket, tag="action", image=image1)

            if image2:  # Check if image2 is not empty
                TicketImage.objects.create(ticket=ticket, tag="diagnosis", image=image2)

            if image3:  # Check if image3 is not empty
                TicketImage.objects.create(ticket=ticket, tag="recommendation", image=image3)

            #if selected_technician != saved_technician:
                #if ticket.task:  # Check if a task exists for the ticket
                    #ticket.task.user = selected_technician
                    #ticket.task.save()

            messages.success(request, 'Ticket Edited successfully')
            return redirect('edit-ticket', ticket_id=ticket_id)

        elif form_type == 'form2':
            status = request.POST.get('status')
            status1 = ticket.status
            ticket.status = status
            ticket.bench_status = request.POST.get('bench_status')
            ticket.remark = request.POST.get('remark')
            ticket.tr_status = request.POST.get('tr_status')
            ticket.more = request.POST.get('more')
            ticket.lpo_no = request.POST.get('lpo_no')
            ticket.tr_approval = request.POST.get('tr_approval')
            ticket.updated = timezone.now()
            ticket.save()

            messages.success(request, 'Ticket Edited successfully')
            if status1 == 'Open' and status == 'Closed':
                ticket.task.status = 'Completed'
                ticket.task.save()
                subject = "TICKET ITL/TN/" + str(ticket.ticket_id) + " CLOSED - ITS"
                message = "Dear {0},\n\nWe are pleased to inform you that your ticket ITL/TN/{1} has been successfully closed. Our team has reviewed the details and has taken the necessary actions to ensure a prompt and effective resolution.\n\nIf you have any further questions or concerns, please don't hesitate to reach out to us at support@intellitech.co.ke. We are here to assist you.\n\nThank you for your patience and understanding throughout this process. We value your business and look forward to serving you in the future.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.".format(
                    ticket.company, ticket.ticket_id)
                recipient_list = [ticket.company.email]
                from_email = 'its-noreply@intellitech.co.ke'
                # send_mail(subject, message, from_email, recipient_list)

            # Redirect back to the edit view
            return redirect('edit-ticket', ticket_id=ticket_id)

        elif form_type == 'form3':
            machine_yom = request.POST.get('machine_yom')
            ram = request.POST.get('ram')
            rom = request.POST.get('rom')
            processor = request.POST.get('processor')
            os = request.POST.get('os')
            office_suite = request.POST.get('office_suite')
            printer_yom = request.POST.get('printer_yom')
            printer_type = request.POST.get('printer_type')
            catridge = request.POST.get('catridge')

            if machine_yom:
                ticket.machine_yom = machine_yom
            if ram:
                ticket.ram = ram
            if rom:
                ticket.rom = rom
            if processor:
                ticket.processor = processor
            if os:
                ticket.os = os
            if office_suite:
                ticket.office_suite = office_suite
            if printer_yom:
                ticket.printer_yom = printer_yom
            if printer_type:
                ticket.printer_type = printer_type
            if catridge:
                ticket.catridge = catridge
            ticket.save()
            messages.success(request, 'Equipment Specs successfully')
            return redirect('edit-ticket', ticket_id=ticket_id)

        # Render the edit form
    return render(request, 'technical/edit_ticket.html',
                  {'ticket': ticket, 'users': users, 'product_details': product_details, 'companies': companies,
                   'requisitions': requisitions, 'tsourcing_data': tsourcing_data, 'tquote_data': tquote_data,
                   'parts': parts, 'action_images': action_images, 'diagnosis_images': diagnosis_images,
                   'recommendation_images': recommendation_images, 'sales': sales})


@login_required
def edit_inhouse_ticket(request, ticket_id):
    technician_group = Group.objects.get(name='Technician')
    users = technician_group.user_set.filter(is_active=True)
    sales_group = Group.objects.get(name='Sales')
    sales = sales_group.user_set.all()
    companies = Company.objects.all().order_by("name")
    ticket = get_object_or_404(InhouseTickets, ticket_id=ticket_id)
    product_details = InhouseProductDetail.objects.filter(ticket=ticket.ticket_id)
    tsourcing_data = InhouseTsourcing.objects.filter(ticket=ticket)
    tquote_data = inhousetQuote.objects.filter(ticket=ticket)
    action_images = InhouseTicketImage.objects.filter(ticket=ticket, tag="action")
    diagnosis_images = InhouseTicketImage.objects.filter(ticket=ticket, tag="diagnosis")
    recommendation_images = InhouseTicketImage.objects.filter(ticket=ticket, tag="recommendation")

    # try:
    #     requisitions = Requisition.objects.filter(ticket=ticket, is_active=True)
    # except Requisition.DoesNotExist:
    requisitions = None
    #
    # try:
    #     parts = Requisition.objects.filter(ticket=ticket, is_active=True, issue_status="Issue")
    # except Requisition.DoesNotExist:
    parts = None

    if request.method == 'POST':
        # Handle form submission and update ticket details here
        # Example:
        form_type = request.POST.get('form_type')
        if form_type == 'form1':
            selected_technician_id = request.POST.get('tech')
            selected_technician = User.objects.get(pk=selected_technician_id)
            saved_technician = ticket.tech
            # Update the ticket fields based on the POST data
            ticket.company = request.POST.get('company')
            ticket.email = request.POST.get('email')
            ticket.recommendation = request.POST.get('recommendation')
            ticket.equipment = request.POST.get('equipment')
            ticket.serial_no = request.POST.get('serial_no')
            ticket.fault = request.POST.get('fault')
            ticket.diagnosis = request.POST.get('diagnosis')
            ticket.action = request.POST.get('action')
            ticket.accessories = request.POST.get('accessories')
            ticket.tech = selected_technician
            ticket.updated = timezone.now()

            ticket.accessories = request.POST.get('accessories')
            ticket.updated = timezone.now()

            # Save the changes
            ticket.save()
            image1 = request.FILES.get('action_image')
            image2 = request.FILES.get('diagnosis_image')
            image3 = request.FILES.get('recommendation_image')

            if image1:  # Check if image1 is not empty
                InhouseTicketImage.objects.create(ticket=ticket, tag="action", image=image1)

            if image2:  # Check if image2 is not empty
                InhouseTicketImage.objects.create(ticket=ticket, tag="diagnosis", image=image2)

            if image3:  # Check if image3 is not empty
                InhouseTicketImage.objects.create(ticket=ticket, tag="recommendation", image=image3)

            if selected_technician != saved_technician:
                if ticket.task:  # Check if a task exists for the ticket
                    ticket.task.user = selected_technician
                    ticket.task.save()

            messages.success(request, 'Ticket Edited successfully')
            return redirect('edit_inhouse_ticket', ticket_id=ticket_id)

        elif form_type == 'form2':
            status = request.POST.get('status')
            status1 = ticket.status
            ticket.status = status
            ticket.bench_status = request.POST.get('bench_status')
            ticket.remark = request.POST.get('remark')
            ticket.tr_status = request.POST.get('tr_status')
            ticket.more = request.POST.get('more')
            ticket.lpo_no = request.POST.get('lpo_no')
            ticket.tr_approval = 2
            ticket.updated = timezone.now()
            ticket.save()

            messages.success(request, 'Ticket Edited successfully')
            if status1 == 'Open' and status == 'Closed':
                ticket.task.status = 'Completed'
                ticket.task.save()
                subject = "TICKET ITL/IHTN/" + str(ticket.ticket_id) + " CLOSED - ITS"
                message = "Dear {0},\n\nWe are pleased to inform you that your ticket ITL/IHTN/{1} has been successfully closed. Our team has reviewed the details and has taken the necessary actions to ensure a prompt and effective resolution.\n\nIf you have any further questions or concerns, please don't hesitate to reach out to us at support@intellitech.co.ke. We are here to assist you.\n\nThank you for your patience and understanding throughout this process. We value your business and look forward to serving you in the future.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.".format(
                    ticket.company, ticket.ticket_id)
                recipient_list = [ticket.email]
                from_email = 'its-noreply@intellitech.co.ke'
                # send_mail(subject, message, from_email, recipient_list)

            # Redirect back to the edit view
            return redirect('edit_inhouse_ticket', ticket_id=ticket_id)

        elif form_type == 'form3':
            form = TsourcingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('edit_inhouse_ticket', ticket_id=ticket_id)  # Redirect after saving
            else:
                form = TsourcingForm()

        # Render the edit form
    return render(request, 'technical/edit_inhouse_ticket.html',
                  {'ticket': ticket, 'users': users, 'product_details': product_details, 'companies': companies,
                   'requisitions': requisitions, 'tsourcing_data': tsourcing_data, 'tquote_data': tquote_data,
                   'parts': parts, 'action_images': action_images, 'diagnosis_images': diagnosis_images,
                   'recommendation_images': recommendation_images, 'sales': sales})


def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            image = TicketImage.objects.get(pk=image_id)
            image.delete()
            return JsonResponse({'message': 'Image deleted successfully.'})
        except TicketImage.DoesNotExist:
            return JsonResponse({'message': 'Image not found.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)


@require_GET
def get_clients(request):
    company_id = request.GET.get('company_id')

    if company_id is not None:
        # Your code to retrieve clients based on the company_id
        clients = Clients.objects.filter(company_id=company_id).values('id', 'f_name', 'l_name')

        # Return clients in JSON format
        return JsonResponse(list(clients), safe=False)
    else:
        # Handle the case where company_id is not provided
        return JsonResponse([], safe=False)


@login_required
def create_delivery(request, ticket_id):
    ticket_id = ticket_id
    try:
        ticket = Tickets.objects.get(pk=ticket_id)
    except Tickets.DoesNotExist:
        return HttpResponseNotFound("Ticket not found")

    accessories_list = [item.strip() for item in ticket.accessories.split(',')]
    # Check if a delivery already exists for this ticket
    existing_delivery = Delivery.objects.filter(ticket=ticket, is_active=True).first()

    if existing_delivery:
        # Redirect to another page or show a message if a delivery already exists
        return redirect('view_delivery', ticket_id=ticket_id)

    if request.method == 'POST':
        # Process the form data and create a new delivery
        client = ticket.company
        delivery_type = 'Returns'
        lpo = request.POST.get('lpo')
        collected_by = request.POST.get('collected_by')
        currency = request.POST.get('currency')
        vat_status = request.POST.get('vat_status') == 'on'  # Convert the checkbox value to a boolean
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        department = request.POST.get('department')
        # Create the new delivery and associate it with the ticket
        new_delivery = Delivery(
            ticket=ticket,
            client=client,
            type=delivery_type,
            lpo=lpo,
            collected_by=collected_by,
            currency=currency,
            vat_status=vat_status,
            status=status,
            remarks=remarks,
            department=department,
            created_by=request.user,
        )
        new_delivery.save()

        quantity_list = request.POST.getlist('quantity_[]')
        serial_no_list = request.POST.getlist('serial_no_[]')
        particulars_list = request.POST.getlist('particulars_[]')

        for i in range(len(particulars_list)):
            if (particulars_list[i]):
                items = Items(
                    delivery=new_delivery,
                    quantity=quantity_list[i],
                    serial_no=serial_no_list[i],
                    particulars=particulars_list[i],

                )
                items.save()

        messages.success(request, 'Delivery Created successfully')
        # Redirect to the ticket details page or a success page
        return redirect('view_delivery', ticket_id=ticket_id)

    return render(request, 'create_delivery.html', {'ticket': ticket, 'accessories_list': accessories_list, })


@login_required
def create_inhouse_delivery(request, ticket_id):
    ticket_id = ticket_id
    try:
        ticket = InhouseTickets.objects.get(pk=ticket_id)
    except InhouseTickets.DoesNotExist:
        return HttpResponseNotFound("Ticket not found")

        # Check if a delivery already exists for this ticket
    # existing_delivery = Delivery.objects.filter(ticket=ticket, is_active=True).first()

    if request.method == 'POST':
        # Process the form data and create a new delivery
        client = ticket.company
        delivery_type = 'Returns'
        lpo = request.POST.get('lpo')
        collected_by = request.POST.get('collected_by')
        currency = request.POST.get('currency')
        vat_status = request.POST.get('vat_status') == 'on'  # Convert the checkbox value to a boolean
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        department = request.POST.get('department')
        # Create the new delivery and associate it with the ticket
        new_delivery = Delivery(
            ticket=ticket,
            client=client,
            type=delivery_type,
            lpo=lpo,
            collected_by=collected_by,
            currency=currency,
            vat_status=vat_status,
            status=status,
            remarks=remarks,
            department=department,
            created_by=request.user,
        )
        new_delivery.save()

        quantity_list = request.POST.getlist('quantity_[]')
        serial_no_list = request.POST.getlist('serial_no_[]')
        particulars_list = request.POST.getlist('particulars_[]')

        # Assuming you have a Ticket model
        for quantity, serial_no, particulars in zip(quantity_list, serial_no_list, particulars_list):
            if particulars:
                Items.objects.create(delivery=new_delivery, quantity=quantity, serial_no=serial_no,
                                     particulars=particulars)

        messages.success(request, 'Delivery Created successfully')
        # Redirect to the ticket details page or a success page
        return redirect('view_delivery', ticket_id=ticket_id)

    return render(request, 'create_delivery.html', {'ticket': ticket})


@login_required
def create_delivery_normal(request):
    if request.method == 'POST':
        # Process the form data and create a new delivery
        client = request.POST.get('client')
        address = request.POST.get('address')
        delivery_type = request.POST.get('type')
        lpo = request.POST.get('lpo')
        collected_by = request.POST.get('collected_by')
        currency = request.POST.get('currency')
        vat_status = request.POST.get('vat_status')  # Convert the checkbox value to a boolean
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        department = request.POST.get('department')
        new_delivery = Delivery(
            ticket=None,
            client=client,
            type=delivery_type,
            lpo=lpo,
            collected_by=collected_by,
            currency=currency,
            vat_status=vat_status,
            status=status,
            remarks=remarks,
            department=department,
            address=address,
            created_by=request.user,

        )

        new_delivery.save()

        for i in range(1, 11):  # Example: Create up to 10 items
            quantity = request.POST.get(f'quantity_{i}')
            serial_no = request.POST.get(f'serial_no_{i}')
            amount = request.POST.get(f'amount_{i}')
            particulars = request.POST.get(f'particulars_{i}')

            if particulars:
                item = Items(
                    delivery=new_delivery,
                    quantity=quantity,
                    amount=amount,
                    serial_no=serial_no,
                    particulars=particulars
                )
                item.save()

        messages.success(request, 'Delivery Created successfully')
        # Redirect to the ticket details page or a success page
        return redirect('list_deliveries')

    return render(request, 'create_delivery_normal.html')


@login_required
def view_delivery(request, ticket_id):
    try:
        ticket = get_object_or_404(Tickets, pk=ticket_id)
        delivery = Delivery.objects.filter(ticket=ticket, is_active=True).last()
        signature = delivery.signatures.last()
        items = delivery.items.all()
    except (Tickets.DoesNotExist, Delivery.DoesNotExist):
        return HttpResponseNotFound("Ticket or Delivery not found")

    return render(request, 'view_delivery.html',
                  {'ticket': ticket, 'delivery': delivery, 'signature': signature, 'items': items})


@login_required
def print_delivery(request, ticket_id):
    try:
        ticket = get_object_or_404(Tickets, pk=ticket_id)
        delivery = Delivery.objects.filter(ticket=ticket, is_active=True).last()
        signature = delivery.signatures.last()
        items = delivery.items.all()
    except (Tickets.DoesNotExist, Delivery.DoesNotExist):
        return HttpResponseNotFound("Ticket or Delivery not found")

    return render(request, 'print_delivery.html',
                  {'ticket': ticket, 'delivery': delivery, 'signature': signature, 'items': items})


@login_required
def view_delivery_normal(request, delivery_id):
    delivery = Delivery.objects.get(pk=delivery_id)

    # Check if the ticket is not None
    if delivery.ticket is not None:
        # Ticket is not None, redirect to the 'view_delivery' view with the 'ticket_id' parameter
        return redirect('view_delivery', ticket_id=delivery.ticket.ticket_id)

    items = Items.objects.filter(delivery=delivery)

    subtotals = 0
    vat = 0

    for item in items:
        item.total = item.amount * item.quantity

        if delivery.vat_status == "Inclusive":
            item.amount -= math.ceil((item.amount / 1.16) * 0.16)  # Deduct VAT from item.amount
            item.total -= math.ceil((item.total / 1.16) * 0.16)
            subtotals += item.total
            vat = math.ceil(subtotals * 0.16)
            total_amount = math.ceil(subtotals + vat)

        if delivery.vat_status == "Exclusive":
            subtotals += item.total
            vat = math.ceil(subtotals * 0.16)
            total_amount = math.ceil(subtotals + vat)

        elif delivery.vat_status == "Exempted":
            subtotals += item.total
            vat = 0
            total_amount = subtotals + vat

    try:
        signature = delivery.signatures.last()
    except (Delivery.DoesNotExist):
        return HttpResponseNotFound("Ticket or Delivery not found")

    return render(request, 'view_delivery_normal.html',
                  {'delivery': delivery, 'signature': signature, 'items': items, 'subtotals': subtotals, 'vat': vat,
                   'total_amount': total_amount, })


def edit_delivery(request, delivery_id):
    try:
        delivery = Delivery.objects.get(pk=delivery_id)
    except Delivery.DoesNotExist:
        raise Http404("Delivery does not exist")

    if request.method == 'POST':
        # Update Delivery details
        delivery.client = request.POST.get('client')
        delivery.type = request.POST.get('type')
        delivery.lpo = request.POST.get('lpo')
        delivery.collected_by = request.POST.get('collected_by')
        delivery.currency = request.POST.get('currency')
        delivery.vat_status = request.POST.get('vat_status')
        delivery.status = request.POST.get('status')
        delivery.remarks = request.POST.get('remarks')
        delivery.department = request.POST.get('department')
        delivery.updated = timezone.now()
        delivery.address = request.POST.get('address')
        delivery.save()

        # Update Items
        quantity_list = request.POST.getlist('quantity[]')
        amount_list = request.POST.getlist('amount[]')
        serial_no_list = request.POST.getlist('serial_no[]')
        particulars_list = request.POST.getlist('particulars[]')

        for quantity, amount, serial_no, particulars in zip(quantity_list, amount_list, serial_no_list,
                                                            particulars_list):
            if particulars:
                item, created = Items.objects.get_or_create(delivery=delivery, serial_no=serial_no)
                item.quantity = quantity
                item.amount = amount
                item.particulars = particulars
                item.save()
        messages.success(request, 'Delivery Edited successfully')
        return redirect('view_delivery_normal',
                        delivery.id)  # Replace 'your_success_url' with the actual URL you want to redirect to after editing

    return render(request, 'edit_delivery.html', {'delivery': delivery})


def delete_item(request, delivery_id, item_id):
    # Get the delivery
    delivery = get_object_or_404(Delivery, pk=delivery_id)

    # Get the item to delete
    item = get_object_or_404(Items, pk=item_id, delivery=delivery)

    if request.method == 'POST':
        # Delete the item
        item.delete()
        messages.warning(request, 'Item Deleted successfully')
        # Redirect to    the delivery edit page or any other desired URL
        return redirect('edit_delivery', delivery_id=delivery.id)

    return render(request, 'delete_item.html', {'item': item, 'delivery': delivery})


@login_required
def list_deliveries(request):
    user = request.user
    deliveries = Delivery.objects.filter(is_active=1).order_by('-id')
    return render(request, 'list_deliveries.html', {'deliveries': deliveries})


@login_required
def list_requisitions(request):
    requisitions = Requisition.objects.filter(is_active=True).order_by('-created')
    return render(request, 'technical/list_requisitions.html', {'requisitions': requisitions})


@login_required
def add_requisition(request):
    active_tickets = Tickets.objects.filter(is_active=True).order_by('-created')
    # Initialize variables for product selection
    active_categories = PartsCategory.objects.all()
    selected_category_id = None
    products = []
    technician_group = Group.objects.get(name='Technician')
    collected_by_users = technician_group.user_set.all()

    if request.method == 'POST':
        # Get the data from the POST request
        ticket_id = request.POST.get('ticket_id')
        part_id = request.POST.get('selected_product')
        serial_no = request.POST.get('serial_no')
        collected_by = request.POST.get('collected_by')
        remarks = request.POST.get('remarks')
        req_status = 'Pending'
        issue_status = 'Pending'
        quantity = request.POST.get('quantity')
        collected_by_user = User.objects.get(id=collected_by)

        # Create a new Requisition object
        requisition = Requisition(
            ticket_id=ticket_id,
            part_id=part_id,
            serial_no=serial_no,
            collected_by=collected_by_user,
            remarks=remarks,
            req_status=req_status,
            quantity=quantity,
            issue_status=issue_status
        )

        requisition.save()
        helpdesk_group = Group.objects.get(name='helpdesk')
        users_in_helpdesk_group = User.objects.filter(groups=helpdesk_group)
        created_by = request.user

        messages.success(request, 'Requisition Created successfully')
        return redirect('list_requisitions')

    elif 'selected_category' in request.GET:
        selected_category_id = int(request.GET['selected_category'])
        products = Parts.objects.filter(category=selected_category_id)
        # Save the new requisition to the database

        # Redirect to a success page or the requisitions list page

        return redirect('list_requisitions')

    return render(request, 'technical/add_requisition.html',
                  {'active_tickets': active_tickets, 'active_categories': active_categories,
                   'selected_category_id': selected_category_id,
                   'products': products,
                   'collected_by_users': collected_by_users, })


@login_required
def get_products(request):
    category_id = request.GET.get('category_id')
    products = Parts.objects.filter(category_id=category_id).values('part_id', 'description')

    return JsonResponse(list(products), safe=False)


@login_required
def change_requisition_status(request, requisition_id):
    requisition = get_object_or_404(Requisition, pk=requisition_id)

    if request.method == 'POST':
        # Get the current status
        current_status = requisition.req_status

        # Determine the new status based on the current status
        new_status = "Pending" if current_status == "Approved" else "Approved"

        # Update the requisition status
        requisition.req_status = new_status
        requisition.approved_by = request.user
        requisition.save()

        return redirect('list_requisitions')

    return render(request, 'technical/change_status.html', {'requisition': requisition})


@login_required
def edit_requisition(request, requisition_id):
    requisition = get_object_or_404(Requisition, pk=requisition_id)
    active_categories = PartsCategory.objects.all()
    technician_group = Group.objects.get(name='Technician')
    users = technician_group.user_set.all()
    if request.method == 'POST':
        # Process the form submission and update the requisition fields
        if 'serial_no' in request.POST and request.POST['serial_no']:
            requisition.serial_no = request.POST.get('serial_no')
        if 'invoice' in request.POST and request.POST['invoice']:
            requisition.invoice = request.POST.get('invoice')
        if 'selected_product' in request.POST and request.POST['selected_product']:
            requisition.part_id = request.POST.get('selected_product')
        if 'company' in request.POST and request.POST['company']:
            requisition.company = request.POST.get('company')
        if 'remarks' in request.POST and request.POST['remarks']:
            requisition.remarks = request.POST.get('remarks')
        if 'req_status' in request.POST and request.POST['req_status']:
            requisition.req_status = request.POST.get('req_status')
        if 'issue_status' in request.POST and request.POST['issue_status']:
            requisition.issue_status = request.POST.get('issue_status')
        if 'tech' in request.POST and request.POST['tech']:
            user_id =request.POST.get('tech')
            user = User.objects.get(id=user_id)
            requisition.collected_by = user
        if 'return_status' in request.POST and request.POST['return_status']:
            requisition.return_status = request.POST.get('return_status')
            requisition.return_approved_by = request.user

        # Save the updated requisition
        requisition.save()
        messages.success(request, 'Requisition Edited successfully')
        return redirect('list_requisitions')

    return render(request, 'technical/edit_requisition.html',
                  {'requisition': requisition, 'active_categories': active_categories,'users':users })


@login_required
def delete_requisition(request, requisition_id):
    requisition = get_object_or_404(Requisition, req_id=requisition_id)
    requisition.is_active = False
    requisition.save()
    messages.warning(request, 'Requisition Deleted successfully')
    return redirect('list_requisitions')


@login_required
def active_call_cards(request):
    call_cards = CallCards.objects.filter(is_active=True).order_by('-created')
    return render(request, 'technical/active_call_cards.html', {'call_cards': call_cards})


@login_required
def add_call_card(request):
    companies = Company.objects.all().order_by('name')
    technician_group = Group.objects.get(name='Technician')
    technicians = technician_group.user_set.all()
    if request.method == 'POST':
        # Get data from the POST request
        company_id = request.POST.get('company')
        client_id = request.POST.get('client')
        tech_user = request.POST.get('tech_id')
        equipment = request.POST.get('equipment')
        fault = request.POST.get('fault')
        remarks = request.POST.get('remarks')
        status = "Pending"
        call_type = request.POST.get('call_type')
        tech_id = get_object_or_404(User, id=tech_user)

        # Create a new CallCards instance
        call_card = CallCards(
            company_id=company_id,
            client_id=client_id,
            tech_id=tech_id,
            equipment=equipment,
            fault=fault,
            remarks=remarks,
            status=status,
            type=call_type,
            is_active=True,  # Assuming it's active when added
            created=timezone.now(),
            updated=timezone.now(),
        )

        # Save the new call card to the database
        call_card.save()
        messages.success(request, 'Call Card Created successfully')
        return redirect('active_call_cards')  # Redirect to the list of active call cards

    return render(request, 'technical/add_call_card.html', {'companies': companies, 'technicians': technicians})


@login_required
def get_clients(request, company_id):
    clients = Clients.objects.filter(company_id=company_id)
    clients_data = [{'id': client.id, 'f_name': client.f_name} for client in clients]
    return JsonResponse({'clients': clients_data})


@login_required
def service(request):
    events = ServiceSchedules.objects.filter(is_active=True).order_by('from_date')
    return render(request, 'technical/service.html', {'events': events})


@login_required
def get_events(request):
    status_colors = {
        "Awaiting confirmation": "red",
        "Confirmed": "green",
        "Postponed": "orange",
        # Add more status-color mappings as needed
    }
    events = ServiceSchedules.objects.filter(is_active=True)

    data = []
    for event in events:
        if event.status in status_colors:
            # Assign the appropriate color based on the status
            color = status_colors[event.status]
        else:
            # Default to a color if the status is not in the dictionary
            color = "blue"
        company = event.company.name
        event_to_date = event.to_date
        # Add one day to the date
        new_date = event_to_date + datetime.timedelta(days=1)
        data.append({
            'title': company,
            'start': event.from_date.isoformat(),
            'end': event.to_date.isoformat(),
            'color': color,
        })

    return JsonResponse(data, safe=False)


@login_required
def create_service_schedule(request):
    if request.method == 'POST':
        # Get data from the request
        company_id = request.POST.get('company_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        notes = request.POST.get('notes')
        status = 'Awaiting confirmation'
        servers = request.POST.get('servers')
        cpus = request.POST.get('cpus')
        laptops = request.POST.get('laptops')
        printers = request.POST.get('printers')
        scanners = request.POST.get('scanners')
        ups = request.POST.get('ups')
        large_ups = request.POST.get('large_ups')
        aios = request.POST.get('aios')
        biometrics = request.POST.get('biometrics')
        cctvs = request.POST.get('cctvs')
        highend_machines = request.POST.get('highend_machines')
        nas = request.POST.get('nas')
        more = request.POST.get('more')
        remark = request.POST.get('remark')
        tech_ids = request.POST.getlist('techs')

        company_instance = Company.objects.get(pk=company_id)

        # Create a new ServiceSchedules instance
        with transaction.atomic():
            # Create a new ServiceSchedules instance
            service_schedule = ServiceSchedules(
                company_id=company_id,
                from_date=from_date,
                to_date=to_date,
                notes=notes,
                status=status,
                is_active=1,  # You can set the default value here
                created=timezone.now(),
                updated=timezone.now()
            )
            service_schedule.save()

            for tech_id in tech_ids:
                tech = User.objects.get(pk=tech_id)
                service_schedule.techs.add(tech)
            # Save ServiceSchedules instance

            # Create a new ServiceTickets instance associated with the ServiceSchedules instance
            service_ticket = ServiceTickets(
                ticket_id=service_schedule,  # Associate the ticket with the ServiceSchedules instance
                servers=servers,
                cpus=cpus,
                laptops=laptops,
                printers=printers,
                scanners=scanners,
                ups=ups,
                large_ups=large_ups,
                aios=aios,
                biometrics=biometrics,
                cctvs=cctvs,
                highend_machines=highend_machines,
                nas=nas,
                more=more,
                remark=remark,

                # Add other fields...
            )
            service_ticket.save()

            # Assuming you are in a view function, you can access the current user through the request object
            user = request.user
            # Create a new Task instance without saving it
            new_task = Task(
                title="Service for " + str(company_instance),
                description="You have been assigned to do  service for  " + str(company_instance) + " on " + str(
                    from_date) + " to " + str(to_date),
                # Assuming company_instance is an object or variable
                is_active=True,
                status="Pending",
                user=user,
                created_by=user,
            )

            # Save the new_task instance
            new_task.save()

            # Add users to the cc_users many-to-many relationship
            for user_id in tech_ids:
                user = User.objects.get(id=user_id)  # Replace with your actual user lookup logic
                new_task.cc_users.add(user)

        messages.success(request, 'Service Schedule created successfully')
        # Redirect to a success page or any other appropriate action
        return redirect('service')  # Replace 'success_page' with your success page URL

    # Retrieve companies for the dropdown
    companies = Company.objects.all().order_by('name')
    technicians = User.objects.all()

    return render(request, 'technical/create_service_schedule.html',
                  {'companies': companies, 'technicians': technicians})


@login_required
def edit_service_schedule(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    service_ticket = get_object_or_404(ServiceTickets, ticket_id=service_schedule)

    if request.method == 'POST':
        # Get data from the request
        company_id = request.POST.get('company_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        notes = request.POST.get('notes')
        status = request.POST.get('status')
        tech_ids = request.POST.getlist('techs')
        company_instance = Company.objects.get(pk=company_id)
        active_status = request.POST.get('active_status')

        # Update both ServiceSchedules and ServiceTickets instances within a transaction
        with transaction.atomic():
            # Update ServiceSchedules instance
            service_schedule.company_id = company_instance
            service_schedule.from_date = from_date
            service_schedule.to_date = to_date
            service_schedule.notes = notes
            service_schedule.status = status
            service_schedule.status = status
            service_schedule.updated = timezone.now()
            service_schedule.is_active = active_status
            service_schedule.save()
            service_schedule.techs.clear()
            for tech_id in tech_ids:
                tech = User.objects.get(pk=tech_id)
                service_schedule.techs.add(tech)

            # Update ServiceTickets instance
            service_ticket.servers = request.POST.get('servers')
            service_ticket.cpus = request.POST.get('cpus')
            service_ticket.laptops = request.POST.get('laptops')
            service_ticket.printers = request.POST.get('printers')
            service_ticket.scanners = request.POST.get('scanners')
            service_ticket.ups = request.POST.get('ups')
            service_ticket.large_ups = request.POST.get('large_ups')
            service_ticket.aios = request.POST.get('aios')
            service_ticket.biometrics = request.POST.get('biometrics')
            service_ticket.highend_machines = request.POST.get('highend_machines')
            service_ticket.nas = request.POST.get('nas')
            service_ticket.more = request.POST.get('more')
            service_ticket.remark = request.POST.get('remark')
            service_ticket.cctvs = request.POST.get('cctvs')
            service_ticket.serversdone = request.POST.get('serversdone')
            service_ticket.cpusdone  = request.POST.get('cpusdone')
            service_ticket.laptopsdone  = request.POST.get('laptopsdone')
            service_ticket.printersdone  = request.POST.get('printersdone')
            service_ticket.scannersdone  = request.POST.get('scannersdone')
            service_ticket.upsdone  = request.POST.get('upsdone')
            service_ticket.large_upsdone  = request.POST.get('large_upsdone')
            service_ticket.aiosdone  = request.POST.get('aiosdone')
            service_ticket.biometricsdone  = request.POST.get('biometricsdone')
            service_ticket.highend_machinesdone  = request.POST.get('highend_machinesdone')
            service_ticket.nasdone  = request.POST.get('nasdone')
            service_ticket.cctvsdone  = request.POST.get('cctvsdone')

            # Update other fields...
            service_ticket.save()

        messages.success(request, 'Service Schedule edited successfully')
        # Redirect to a success page or any other appropriate action
        return redirect('service')  # Replace 'success_page' with your success page URL

    # Retrieve companies for the dropdown
    companies = Company.objects.all().order_by('name')
    technicians = User.objects.all()

    return render(request, 'technical/edit_service_schedule.html',
                  {'service_schedule': service_schedule, 'service_ticket': service_ticket, 'companies': companies,
                   'technicians': technicians})


@login_required
def delete_service(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    service_schedule.is_active = False
    service_schedule.save()
    messages.warning(request, 'Service Schedule Deleted successfully')
    return redirect('service')


@login_required
def edit_call_card(request, cc_id):
    call_card = get_object_or_404(CallCards, pk=cc_id)
    signature = call_card.signatures.last()
    status1 = call_card.status
    if request.method == 'POST':
        # Handle form submission and update the call card
        call_card.time_in = request.POST.get('time_in')
        call_card.tech_id_id = request.POST.get('tech_id')
        call_card.time_out = request.POST.get('time_out')
        call_card.equipment = request.POST.get('equipment')
        call_card.fault = request.POST.get('fault')
        call_card.remarks = request.POST.get('remarks')
        status2 = request.POST.get('status')
        call_card.status = status2
        call_card.type = request.POST.get('type')

        call_card.save()

        if status1 == "Pending" and status2 == "Done":
            management_group = Group.objects.get(name='Helpdesk')

            # Get all users in the "management" group
            management_users = management_group.user_set.all()

            # Extract email addresses
            management_emails = [user.email for user in management_users]

            # Your existing code to create new_sourcing_data objects
            url = "http://146.190.61.23:8500/technical/edit_call_card/" + str(call_card.cc_id) + "/"  # Replace with your actual URL
            clickable_url = f"<a href='{url}'>#" + str(call_card.cc_id) + "  " + str(call_card.company) + "</a>"
            # Use the 'table' string in the email message
            message = (
                f"Dear Sir/Madam,<br><br>"
                f"Our technician has closed Call Card  for {clickable_url} . <br><br>"
                "This is an auto-generated email | © 2023 ITS. All rights reserved."
            )
            subject = f"Call card closed for {call_card.company}"
            recipient_list = management_emails
            from_email = 'its-noreply@intellitech.co.ke'

            # Create an EmailMessage instance for HTML content
            email_message = EmailMessage(subject, message, from_email, recipient_list)
            email_message.content_subtype = 'html'  # Set content type to HTML
            email_message.send()

        messages.success(request, 'Call Card Edited successfully')
        return redirect('active_call_cards')

    technician_group = Group.objects.get(name='Technician')
    technicians = technician_group.user_set.all()

    return render(request, 'technical/edit_call_card.html',
                  {'call_card': call_card, 'technicians': technicians, 'signature': signature})


@login_required
def delete_call_card(request, cc_id):
    call_card = get_object_or_404(CallCards, pk=cc_id)
    call_card.is_active = False
    call_card.save()
    messages.warning(request, 'Call card Deleted successfully')
    return redirect('active_call_cards')


def create_ticket(request):
    if request.method == 'POST':
        # Handle form submission
        type = request.POST.get('type')
        company = request.POST.get('company')
        client = request.POST.get('client')
        equipment = request.POST.get('equipment')
        serial_no = request.POST.get('serial_no')
        fault = request.POST.get('fault')
        accessories = request.POST.get('accessories')
        notes = request.POST.get('notes')
        brought_by = request.POST.get('brought_by')
        tech_id = request.POST.get('tech')
        company_id = Company.objects.get(id=company)
        client_id = Clients.objects.get(id=client)

        # Create the ticket
        ticket = Tickets.objects.create(
            company=company_id,
            client=client_id,
            equipment=equipment,
            serial_no=serial_no,
            fault=fault,
            accessories=accessories,
            notes=notes,
            tech_id=tech_id,
            type=type,
            brought_by=brought_by,
        )

        if type == "On-site":

            tech_user = get_object_or_404(User, id=tech_id)
            # Create a CallCards instance for on-site tickets
            call_card = CallCards.objects.create(
                company=company_id,
                client=client_id,
                tech_id=tech_user,
                equipment=equipment,
                fault=fault,
                type=type,
                # Add any other fields as needed
            )
            messages.success(request, 'Ticket and Call Card Created successfully')
        else:
            messages.success(request, 'Ticket Created successfully')

            # Assuming you are in a view function, you can access the current user through the request object
        user = request.user
        # Create a new Task instance without saving it
        new_task = Task(
            title="Ticket for " + str(company_id) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
            description="You have been allocated Ticket for " + str(company_id) + " with fault " + str(fault),
            is_active=True,
            status="In Progress",
            user=get_object_or_404(User, id=tech_id),
            created_by=user,

        )

        # Save the new_task instance
        new_task.save()

        ticket.task = new_task
        ticket.save()

        created_by = request.user

        subject = "TICKET ITL/TN/" + str(ticket.ticket_id) + " OPENED - ITS"
        message = "Dear {0},\n\nA ticket ITL/TN/{1} has been raised for your work order, and our team is now reviewing the details to ensure a prompt and effective resolution.\n\nNote: You can reach out to us at support@intellitech.co.ke if you have any questions or concerns.\n\nThank you for your patience and understanding.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.".format(
            company_id, ticket.ticket_id)
        recipient_list = [company_id.email]
        from_email = 'its-noreply@intellitech.co.ke'
        # send_mail(subject, message, from_email, recipient_list)
        # Redirect to a success page or any other desired action
        return redirect('edit-ticket', ticket.ticket_id)  # Replace 'success_page' with the actual success page URL

    else:
        # Handle GET request, render the form
        companies = Company.objects.all().order_by('name')
        clients = Clients.objects.all()
        technician_group = Group.objects.get(name='Technician')
        users = technician_group.user_set.all()

        return render(request, 'technical/create_ticket.html',
                      {'companies': companies, 'clients': clients, 'users': users})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)

    # Set is_active to 0 to mark the ticket as deleted
    ticket.is_active = 0
    messages.warning(request, 'Ticket Deleted successfully')
    ticket.save()

    return redirect('ticket-list')  # Redirect to the list of tickets after deletion


@login_required
def delete_inhouse_ticket(request, ticket_id):
    ticket = get_object_or_404(InhouseTickets, ticket_id=ticket_id)

    # Set is_active to 0 to mark the ticket as deleted
    ticket.is_active = 0
    messages.warning(request, 'Ticket Deleted successfully')
    ticket.save()

    return redirect('inhouse-ticket-list')  # Redirect to the list of tickets after deletion


@login_required
def delete_delivery(request, delivery_id):
    try:
        delivery = Delivery.objects.get(id=delivery_id)
        delivery.is_active = 0  # Set is_active to 0 to mark it as deleted
        delivery.save()
    except Delivery.DoesNotExist:
        # Handle the case where the ticket does not exist
        pass
    messages.warning(request, 'Delivery Succefully Deleted.')
    return redirect('list_deliveries')


@login_required
def quote_tickets(request, ticket_id):
    if request.method == 'POST':
        ticket = Tickets.objects.get(ticket_id=ticket_id)
        ticket.labour = request.POST.get('labour')
        ticket.save()

        for req_id, price in request.POST.items():
            if req_id.startswith('req_price_'):
                req_id = req_id[len('req_price_'):]
                requisition = Requisition.objects.get(req_id=req_id)
                requisition.price = price
                requisition.save()

        part_no_list = request.POST.getlist('part_no[]')
        description_list = request.POST.getlist('description[]')
        quantity_list = request.POST.getlist('quantity[]')
        currency_list = request.POST.getlist('currency[]')
        price_list = request.POST.getlist('price[]')
        layout_list = request.POST.getlist('layout[]')

        # Create a list to hold the new tQuote objects
        new_quote_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and description_list[i]):
                quote = tQuote(
                    part_no=part_no_list[i],
                    description=description_list[i],
                    quantity=quantity_list[i],
                    currency=currency_list[i],
                    price=price_list[i],
                    ticket=ticket,
                    layout=layout_list[i]
                )
                new_quote_data.append(quote)

        # Delete old tQuote data
        tQuote.objects.filter(ticket=ticket).delete()

        # Insert the new data
        tQuote.objects.bulk_create(new_quote_data)

        messages.success(request, 'Quotation Products Updated.')

    return redirect('edit-ticket', ticket_id=ticket_id)


@login_required
def sourcing_tickets(request, ticket_id):
    if request.method == 'POST':
        ticket = Tickets.objects.get(ticket_id=ticket_id)
        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('desc[]')
        qty_list = request.POST.getlist('qty[]')
        availability_list = request.POST.getlist('availability[]')
        supplier_list = request.POST.getlist('supplier[]')
        currency_list = request.POST.getlist('currency[]')
        price_list = request.POST.getlist('price[]')
        attach_list = request.POST.get('attach[]')
        handler = request.POST.get('handler')
        attachment_list = request.FILES.getlist('att[]')
        handler_id = User.objects.get(pk=handler)
        ticket.sourcing_parts = handler_id
        ticket.save()
        created_by = request.user
        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and desc_list[i]):
                z = i + 1
                attachment_list = request.FILES.getlist(f'att_{z}')
                if attachment_list:
                    attachment = attachment_list[0]
                else:
                    attachment = None

                sourcing = Tsourcing(
                    part_no=part_no_list[i],
                    desc=desc_list[i],
                    qty=qty_list[i],
                    availability=availability_list[i],
                    supplier=supplier_list[i],
                    currency=currency_list[i],
                    price=price_list[i],
                    ticket=ticket,
                    attachment=attachment,
                )
                new_sourcing_data.append(sourcing)

        # Delete old Tsourcing data
        Tsourcing.objects.filter(ticket=ticket).delete()

        # Insert the new data
        Tsourcing.objects.bulk_create(new_sourcing_data)

        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Part No</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Description</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Availability</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Currency</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Price</th>"
            "</tr>"
        )

        for i in range(len(desc_list)):
            if desc_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{part_no_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{desc_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{qty_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{availability_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{currency_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{price_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/technical/edit-ticket/" + str(
            ticket.ticket_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>ITL/TN/" + str(ticket.ticket_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler_id},<br><br>"
            f"Our Technical team has made a sourcing request, {clickable_url} on your behalf. Here are the details and summary of the order:<br><br>"
            f"Company: {ticket.company};<br><br>"
            f"Client :{ticket.client};<br><br>"
            f"Kindly order for below::<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"SOURCING FOR ITL/TN/{ticket.ticket_id}"
        recipient_list = [ticket.sourcing_parts.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        user = request.user
        # Create a new Task instance without saving it
        if ticket.task is None:
            new_task = Task(
                title="Sourcing Items for " + str(ticket.company) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                description="Help in sourcing for items in Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                is_active=True,
                status="In Progress",
                user_id=handler_id.id,  # Correctly set the user_id
                created_by=user,
            )
            # Save the new_task instance
            new_task.save()
        elif ticket.task.user_id != handler_id:  # Check if the user_id is different
            ticket.task.user_id = handler_id  # Correctly set the user_id
            ticket.task.save()  # Save the task

        messages.success(request, 'Sourcing Products Updated.')

    return redirect('edit-ticket', ticket_id=ticket_id)


@login_required
def sourcing_inhousetickets(request, ticket_id):
    if request.method == 'POST':
        ticket = InhouseTickets.objects.get(ticket_id=ticket_id)
        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('desc[]')
        qty_list = request.POST.getlist('qty[]')
        availability_list = request.POST.getlist('availability[]')
        supplier_list = request.POST.getlist('supplier[]')
        currency_list = request.POST.getlist('currency[]')
        price_list = request.POST.getlist('price[]')
        attach_list = request.POST.get('attach[]')
        handler = request.POST.get('handler')
        handler_id = User.objects.get(pk=handler)
        ticket.sourcing_parts_id = handler_id.id
        ticket.save()
        created_by = request.user
        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and desc_list[i]):
                z = i + 1
                attachment_list = request.FILES.getlist(f'att_{z}')
                if attachment_list:
                    attachment = attachment_list[0]
                else:
                    attachment = None

                sourcing = InhouseTsourcing(
                    part_no=part_no_list[i],
                    desc=desc_list[i],
                    qty=qty_list[i],
                    availability=availability_list[i],
                    supplier=supplier_list[i],
                    currency=currency_list[i],
                    price=price_list[i],
                    ticket=ticket,
                    attachment=attachment,
                )
                new_sourcing_data.append(sourcing)

        # Delete old Tsourcing data
        InhouseTsourcing.objects.filter(ticket=ticket).delete()

        # Insert the new data
        InhouseTsourcing.objects.bulk_create(new_sourcing_data)

        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Part No</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Description</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Availability</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Currency</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Price</th>"
            "</tr>"
        )

        for i in range(len(desc_list)):
            if desc_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{part_no_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{desc_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{qty_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{availability_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{currency_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{price_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/technical/edit-inhouse-ticket/" + str(
            ticket.ticket_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>ITL/IHTN/" + str(ticket.ticket_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler_id},<br><br>"
            f"Our Technical team has made a inhouse sourcing request, {clickable_url} on your behalf. Here are the details and summary of the order:<br><br>"
            f"Company: {ticket.company};<br><br>"
            f"Kindly order for below::<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"SOURCING FOR INHOUSE TICKET ITL/IHTN/{ticket.ticket_id}"
        recipient_list = [ticket.sourcing_parts.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        user = request.user
        # Create a new Task instance without saving it
        if ticket.task is None:
            new_task = Task(
                title="Sourcing Items for " + str(ticket.company) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                description="Help in sourcing for items in Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                is_active=True,
                status="In Progress",
                user_id=handler_id.id,  # Correctly set the user_id
                created_by=user,
            )
            # Save the new_task instance
            new_task.save()
        elif ticket.task.user_id != handler_id:  # Check if the user_id is different
            ticket.task.user_id = handler_id  # Correctly set the user_id
            ticket.task.save()  # Save the task

        messages.success(request, 'Sourcing Products Updated.')

    return redirect('edit_inhouse_ticket', ticket_id=ticket_id)


@login_required
def delete_entry(request, entry_id):
    try:
        entry = Tsourcing.objects.get(id=entry_id)  # Replace YourModel with the appropriate model name
        entry.delete()
        return JsonResponse({'message': 'Entry deleted successfully'})
    except Tsourcing.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)


@login_required
def delete_entry_quote(request, entry_id):
    try:
        entry = tQuote.objects.get(id=entry_id)  # Replace YourModel with the appropriate model name
        entry.delete()
        return JsonResponse({'message': 'Entry deleted successfully'})
    except Tsourcing.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)


@login_required
def copy_to_quote(request, entry_id):
    try:
        tsourcing_entry = Tsourcing.objects.get(id=entry_id)
        tquote_entry = tQuote(
            part_no=tsourcing_entry.part_no,
            description=tsourcing_entry.desc,
            price=tsourcing_entry.price,
            quantity=tsourcing_entry.qty,
            currency=tsourcing_entry.currency,
            ticket=tsourcing_entry.ticket,
            availability=tsourcing_entry.availability
        )
        tquote_entry.save()
        return JsonResponse({'message': 'Product copied to tQuote successfully'})
    except Tsourcing.DoesNotExist:
        return JsonResponse({'error': 'Product not found in Tsourcing'}, status=404)


def approve_report(request, report_id):
    # Retrieve the technical report associated with the given report_id
    report = get_object_or_404(TechnicalReport, pk=report_id)
    user = request.user
    if request.method == 'POST':
        # Check if the request is a POST request (e.g., a form submission)
        status = request.POST.get('approval_status')
        # If the report is not already approved, mark it as approved
        report.is_approved = status
        report.approved_by = user
        report.approval_date = datetime.datetime.now()

        report.save()  # You can pass the currently logged-in user

        management_group = Group.objects.get(name='Helpdesk')

        # Get all users in the "management" group
        management_users = management_group.user_set.all()

        # Extract email addresses
        management_emails = [user.email for user in management_users]

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/technical/report/" + str(report.id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(report.id) + " " + str(report.ticket.company) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear Sir/Madam,<br><br>"
            f"{user} has approved   {clickable_url} Technical Report from ticket  ITL/TN/{report.ticket.ticket_id} on your behalf. <br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"Report approval for {report.ticket.company}"
        recipient_list = management_emails
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        messages.success(request, 'Report Approved successfully')
    # Redirect back to the report's detail page (or wherever you prefer)
    return redirect('report', report_id=report_id)


def mark_sent_for_approval(request, report_id):
    # Retrieve the technical report associated with the given report_id
    report = get_object_or_404(TechnicalReport, pk=report_id)

    if not report.sent_approval:
        # If the report is not marked as sent for approval, set it to True
        report.sent_approval = True
        report.save()
        # Assuming you have a "management" group
        management_group = Group.objects.get(name='Management')

        # Get all users in the "management" group
        management_users = management_group.user_set.all()

        # Extract email addresses
        management_emails = [user.email for user in management_users]

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/technical/report/" + str(report.id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(report.id) + " " + str(report.ticket.company) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear Sir,<br><br>"
            f"Our technical Team has raised approval request of Technical Report for {clickable_url} from ticket  ITL/TN/{report.ticket.ticket_id} on your behalf. <br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"Report approval for {report.ticket.company}"
        recipient_list = management_emails
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

    # Redirect back to the report's detail page (or wherever you prefer)
    return redirect('report', report_id=report.id)


def generate_report(request, ticket_id):
    # Retrieve the ticket associated with the given ticket_id
    ticket = get_object_or_404(Tickets, pk=ticket_id)

    try:
        report = TechnicalReport.objects.get(ticket=ticket)
    except TechnicalReport.DoesNotExist:
        # If no report exists, generate one (you can customize this logic)
        report = TechnicalReport.objects.create(ticket=ticket, report_text="Generated report text", is_approved=0)
        messages.success(request, 'Report Generated successfully')

    # Redirect to the ticket's URL
    return redirect('report', report_id=report.id)


from itertools import groupby


@login_required
def report(request, report_id):
    # Retrieve the technical report associated with the given report_id
    report = get_object_or_404(TechnicalReport, pk=report_id)
    ticket = report.ticket
    action_images = TicketImage.objects.filter(ticket=ticket, tag="action")
    diagnosis_images = TicketImage.objects.filter(ticket=ticket, tag="diagnosis").last()
    recommendation_images = TicketImage.objects.filter(ticket=ticket, tag="recommendation").last()
    layout_2_count =0
    # Retrieve the associated ticket
    subtotals = 0
    ticket = report.ticket
    subtotals = 0
    vat = 0
    grouped_tquote_data = {}
    group_vat = {}
    group_total_amount = {}

    try:
        tquote_data = tQuote.objects.filter(ticket=ticket)

        # Sort the tquote_data by layout
        tquote_data = sorted(tquote_data, key=lambda x: x.layout)
        print("data")
        print(tquote_data)

        # Group tquote_data by layout
        grouped_tquote_data = {key: list(group) for key, group in groupby(tquote_data, key=lambda x: x.layout)}

        # Dictionary to store totals for each group
        group_totals = {}
        for layout, items in grouped_tquote_data.items():
            group_total = 0  # Initialize total for the current group
            for item in items:
                item.total = item.quantity * item.price
                group_total += item.total
                if item.layout == "1":
                    subtotals += item.total
                    layout_2_count += 1
            group_totals[layout] = group_total

            group_vat[layout] = round(group_total * 0.16)
            group_total_amount[layout] = group_totals[layout] + group_vat[layout]

    except tQuote.DoesNotExist:
        tquote_data = None

    # Your existing code...

    try:
        parts = Requisition.objects.filter(ticket=ticket, is_active=True, issue_status="Issue")

        # No need to sort or group since there is no 'layout' field

        for requisition in parts:
            if requisition.quantity is not None and requisition.price is not None:
                requisition.total = requisition.quantity * requisition.price
                layout_2_count += 1
            else:
                # Handle the case where either quantity or price is None
                requisition.total = 0  # or set it to some default value or handle it according to your requirements
            subtotals += requisition.total

    except Requisition.DoesNotExist:
        parts = None

    if isinstance(ticket.labour, int):
        subtotals += ticket.labour
        if ticket.labour != 0:
            layout_2_count += 1
    elif isinstance(ticket.labour, str) and ticket.labour.isdigit():
        subtotals += int(ticket.labour)
        if int(ticket.labour) != 0:
            layout_2_count += 1
    if ticket.company.id == 55:
        vat = 0
        total_amount = subtotals + vat
    else:
        vat = round(subtotals * 0.16)
        total_amount = subtotals + vat


    print(layout_2_count)
    return render(request, 'technical/report.html',
                  {'ticket': ticket, 'tquote_data': tquote_data, 'parts': parts, 'vat': vat,
                   'total_amount': total_amount, 'subtotals': subtotals, 'report': report,
                   'diagnosis_images': diagnosis_images,
                   'recommendation_images': recommendation_images, 'grouped_tquote_data': grouped_tquote_data,
                   'group_totals': group_totals, 'group_vat': group_vat, 'group_total_amount': group_total_amount,'layout_2_count':layout_2_count})


class TechnicalReportListView(ListView):
    model = TechnicalReport
    template_name = 'technical/technical_report_list.html'
    context_object_name = 'reports'


@login_required
def delete_report(request, report_id):
    report = get_object_or_404(TechnicalReport, pk=report_id)

    if request.method == 'POST':
        report.delete()
        messages.warning(request, 'Report Deleted    successfully')
        return redirect('technical_report_list')  # Redirect to the report list after deletion

    return render(request, 'technical/report_confirm_delete.html', {'report': report})


@login_required
def create_format_approval(request, ticket_id):
    try:
        # Get the Ticket object based on the ticket_id
        ticket = Tickets.objects.get(pk=ticket_id)

        # Check if a FormatApproval already exists for this Ticket
        format_approval = FormatApproval.objects.filter(ticket=ticket).first()

        if format_approval:
            # Redirect to the existing FormatApproval
            return redirect('format_approval_detail', format_approval_id=format_approval.pk)

        if request.method == "POST":
            # Process the form submission
            app_info = request.POST.get('app_info')
            data_info = request.POST.get('data_info')

            # Create a new FormatApproval
            format_approval = FormatApproval(
                ticket=ticket,
                app_info=app_info,
                data_info=data_info
            )
            format_approval.save()

            # Generate a UniqueToken and associate it with FormatApproval
            unique_token = UniqueToken(
                token=uuid.uuid4(),
                FormatApproval=format_approval
            )
            unique_token.save()

            # Redirect to the created FormatApproval
            return redirect('format_approval_detail', format_approval_id=format_approval.pk)

        # Render the form for creating a FormatApproval
        return render(request, 'technical/create_format.html', {'ticket': ticket})
    except Tickets.DoesNotExist:
        raise Http404("Ticket does not exist")


@login_required
def format_approval_detail(request, format_approval_id):
    try:
        format_approval = FormatApproval.objects.get(pk=format_approval_id)
        signature = FSignature.objects.filter(format=format_approval).last()
        return render(request, 'technical/format_approval.html',
                      {'format_approval': format_approval, 'signature': signature})
    except FormatApproval.DoesNotExist:
        # Handle the case where the FormatApproval does not exist
        # You can raise an Http404 or render an error page.
        pass


from django.utils.safestring import mark_safe


@login_required
def send_format_email(request, format_approval_id):
    # Retrieve the FormatApproval object
    format_approval = get_object_or_404(FormatApproval, pk=format_approval_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')  # Get the recipient's email from the form
        # Ensure recipient_email is valid and not empty before proceeding

        # Generate a unique UUID for this email
        token = uuid.uuid4()

        # Check if there's an existing UniqueToken associated with the FormatApproval
        existing_token = UniqueToken.objects.filter(FormatApproval=format_approval).first()

        # Check if the existing token is still valid (e.g., not expired)
        if existing_token:
            # Use the existing token
            unique_token = existing_token.token
        else:
            # Create a new UniqueToken and associate it with the FormatApproval
            existing_token = UniqueToken.objects.create(token=token, FormatApproval=format_approval)
            unique_token = existing_token.token

        # Construct the URL using reverse with the UUID as a parameter
        url1 = request.build_absolute_uri(reverse('form_with_uuid', args=[str(token)]))
        # Assuming 'format_approval', 'recipient_email', and 'token' are defined elsewhere in your code
        url = "http://146.190.61.23:8500/form/" + str(unique_token) + "/"
        clickable_url = mark_safe(f"<a href='{url}'>URL</a>")
        subject = 'Format Approval Request'
        message = (
            f"Dear {format_approval.ticket.company},<br><br>"
            f"We have created a Format Approval request for: {format_approval.ticket.equipment}, Serial Number: {format_approval.ticket.serial_no}.<br><br>"
            f"Please click this {clickable_url} to preview and sign the document<br><br>"
            f"Note: You can reach out to us at support@intellitech.co.ke if you have any questions or concerns.<br><br>"
            f"Thank you for your patience and understanding.<br><br>"
            f"Regards,<br>"
            f"Intellitech Limited.<br><br>"
            f"This is an auto-generated email | © 2023 ITS. All rights reserved."
        )

        recipient_list = [recipient_email]  # Use the recipient's email from the form input
        from_email = 'its-noreply@intellitech.co.ke'

        # Creating EmailMessage instance
        email = EmailMessage(subject, message, from_email, recipient_list)

        # Setting content type to HTML
        email.content_subtype = 'html'

        # Sending the email

        try:
            email.send()

            signature = FSignature.objects.filter(format=format_approval).last()
            messages.success(request, 'Format Approval Sent Successfully.')
            return render(request, 'technical/format_approval.html',
                          {'format_approval': format_approval, 'signature': signature})
            # Email sent successfully, do something here
        except Exception as e:
            # An error occurred while sending the email, handle it here
            # You can print the error message for debugging
            signature = FSignature.objects.filter(format=format_approval).last()
            messages.error(request, 'There was an error sending the email.')
            return render(request, 'technical/format_approval.html',
                          {'format_approval': format_approval, 'signature': signature})
            # You can also perform other actions when the email sending fails
        # Handle GET request or form display
    signature = FSignature.objects.filter(format=format_approval).last()
    return render(request, 'technical/format_approval.html',
                  {'format_approval': format_approval, 'signature': signature})


def tickets_created_monthly_this_year(request):
    current_year = timezone.now().year

    monthly_ticket_counts = Tickets.objects.filter(
        created__year=current_year,
        is_active=1  # Filter by active tickets if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('ticket_id')
    ).order_by('month')

    data = list(monthly_ticket_counts)

    return JsonResponse(data, safe=False)


def tickets_created_monthly_this_year_tech(request):
    current_year = timezone.now().year

    monthly_ticket_counts = Tickets.objects.filter(
        created__year=current_year,
        is_active=1, tech=request.user  # Filter by active tickets if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('ticket_id')
    ).order_by('month')

    data = list(monthly_ticket_counts)

    return JsonResponse(data, safe=False)


def tr_status_pie_chart(request):
    tr_status_counts = Tickets.objects.values('tr_status').annotate(count=Count('ticket_id'))
    data = [{'label': item['tr_status'], 'count': item['count']} for item in tr_status_counts]

    return JsonResponse(data, safe=False)


def service_schedules_yearly(request):
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of service schedules created each month this year
    monthly_schedule_counts = ServiceSchedules.objects.filter(
        from_date__year=current_year,
        is_active=1  # Filter by active schedules if needed
    ).annotate(
        month=ExtractMonth('from_date')
    ).values(
        'month'
    ).annotate(
        count=Count('ss_id')
    ).order_by('month')

    data = list(monthly_schedule_counts)

    return JsonResponse(data, safe=False)


def service_schedules_yearly_tech(request):
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of service schedules created each month this year
    monthly_schedule_counts = ServiceSchedules.objects.filter(
        from_date__year=current_year,
        is_active=1,
    ).annotate(
        month=ExtractMonth('from_date')
    ).values(
        'month'
    ).annotate(
        count=Count('ss_id')
    ).order_by('month')

    data = list(monthly_schedule_counts)

    return JsonResponse(data, safe=False)


def remark_pie_chart(request):
    remark_counts = Tickets.objects.values('remark').annotate(count=Count('ticket_id'))
    data = [{'label': item['remark'], 'count': item['count']} for item in remark_counts]

    return JsonResponse(data, safe=False)


def bench_status_pie_chart(request):
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year

    ticket_counts = Tickets.objects.filter(
        created__month=current_month,
        created__year=current_year
    ).values('bench_status').annotate(count=Count('ticket_id'))

    total_tickets = sum(item['count'] for item in ticket_counts)

    data = [{'label': item['bench_status'], 'count': item['count'], 'percentage': (item['count'] / total_tickets) * 100}
            for item in ticket_counts]

    return JsonResponse(data, safe=False)


def status_pie_chart(request):
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year

    ticket_counts = Tickets.objects.filter(
        created__month=current_month,
        created__year=current_year
    ).values('status').annotate(count=Count('ticket_id'))

    total_tickets = sum(item['count'] for item in ticket_counts)

    data = [{'label': item['status'], 'count': item['count'], 'percentage': (item['count'] / total_tickets) * 100} for
            item in ticket_counts]

    return JsonResponse(data, safe=False)


def requisitions_created_monthly(request):
    current_year = timezone.now().year

    monthly_requisition_counts = Requisition.objects.filter(
        created__year=current_year,
        is_active=True  # Filter by active requisitions if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('req_id')
    ).order_by('month')

    data = list(monthly_requisition_counts)

    return JsonResponse(data, safe=False)


def requisitions_created_monthly_tech(request):
    current_year = timezone.now().year

    monthly_requisition_counts = Requisition.objects.filter(
        created__year=current_year,
        is_active=True,
        collected_by=request.user  # Filter by active requisitions if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('req_id')
    ).order_by('month')

    data = list(monthly_requisition_counts)

    return JsonResponse(data, safe=False)


def requisitions_returned(request):
    current_year = timezone.now().year

    monthly_requisition_counts = Requisition.objects.filter(
        created__year=current_year,
        is_active=True,
        return_approved_by__isnull=False,  # Filter by active requisitions if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('req_id')
    ).order_by('month')

    data = list(monthly_requisition_counts)

    return JsonResponse(data, safe=False)


def requisitions_rejected(request):
    current_year = timezone.now().year

    monthly_requisition_counts = Requisition.objects.filter(
        created__year=current_year,
        is_active=True,
        return_approved_by__isnull=False,  # Filter by active requisitions if needed
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('req_id')
    ).order_by('month')

    data = list(monthly_requisition_counts)

    return JsonResponse(data, safe=False)


@csrf_exempt
def save_signature_view_ticket(request):
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        type = request.POST.get('type')
        client = request.POST.get('client')
        equipment = request.POST.get('equipment')
        serial_no = request.POST.get('serial_no')
        fault = request.POST.get('fault')
        accessories = request.POST.get('accessories')
        notes = request.POST.get('notes')
        tech_id = request.POST.get('tech')
        eqpass = request.POST.get('eqpass')
        client_id = Clients.objects.get(id=client)
        brought_by = request.POST.get('brought_by')

        # Create the ticket
        ticket = Tickets.objects.create(
            company=client_id.company,
            client=client_id,
            equipment=equipment,
            serial_no=serial_no,
            fault=fault,
            accessories=accessories,
            notes="notes",
            tech_id=tech_id,
            type=type,
            eqpass=eqpass,
            brought_by=brought_by,

        )
        if type == "On-site":

            tech_user = get_object_or_404(User, id=tech_id)
            # Create a CallCards instance for on-site tickets
            call_card = CallCards.objects.create(
                company=client_id.company,
                client=client_id,
                tech_id=tech_user,
                equipment=equipment,
                fault=fault,
                type=type,
                # Add any other fields as needed
            )
            messages.success(request, 'Ticket and Call Card Created successfully')
        else:
            messages.success(request, 'Ticket Created successfully')

            # Assuming you are in a view function, you can access the current user through the request object
        user = request.user
        # Create a new Task instance without saving it
        new_task = Task(
            title="Ticket for " + str(client_id.company) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
            description="You have been allocated Ticket for " + str(client_id.company) + " with fault " + str(fault),
            is_active=True,
            status="In Progress",
            user=get_object_or_404(User, id=tech_id),
            created_by=user,

        )

        # Save the new_task instance
        new_task.save()

        ticket.task = new_task
        ticket.save()

        subject = "TICKET ITL/TN/" + str(ticket.ticket_id) + " OPENED - ITS"
        message = "Dear {0},\n\nA ticket ITL/TN/{1} has been raised for your work order, and our team is now reviewing the details to ensure a prompt and effective resolution.\n\nNote: You can reach out to us at support@intellitech.co.ke if you have any questions or concerns.\n\nThank you for your patience and understanding.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.".format(
            client_id.company, ticket.ticket_id)
        recipient_list = [client_id.company.email]
        from_email = 'its-noreply@intellitech.co.ke'
        # send_mail(subject, message, from_email, recipient_list)
        # Redirect to a success page or any other desired action

        # Extract the Base64 data after the comma
        base64_data = signature_data.split(',')[1]

        # Decode the Base64 data
        signature_binary = base64.b64decode(base64_data)

        # Create a Signature object and save it to the database
        signature = TSignature()

        # Update the corresponding Delivery object with the signature
        try:
            signature.ticket = ticket  # Associate the delivery with the signature
            signature.signature_image.save('signature.png', ContentFile(signature_binary), save=True)
            return JsonResponse({'success': True})
        except Tickets.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Format Approval not found'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def save_signature_view_inhouse_ticket(request):
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        company = request.POST.get('company')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        equipment = request.POST.get('equipment')
        serial_no = request.POST.get('serial_no')
        fault = request.POST.get('fault')
        accessories = request.POST.get('accessories')
        notes = request.POST.get('notes')
        tech_id = request.POST.get('tech')
        eqpass = request.POST.get('eqpass')
        brought_by = request.POST.get('brought_by')
        # Create the ticket
        ticket = InhouseTickets.objects.create(
            type="White",
            company=company,
            equipment=equipment,
            email=email,
            telephone=telephone,
            serial_no=serial_no,
            fault=fault,
            accessories=accessories,
            notes="notes",
            tech_id=tech_id,
            eqpass=eqpass,
            brought_by=brought_by,
        )

        messages.success(request, 'Ticket Created successfully')

        # Extract the Base64 data after the comma
        base64_data = signature_data.split(',')[1]

        # Decode the Base64 data
        signature_binary = base64.b64decode(base64_data)

        # Create a Signature object and save it to the database
        signature = InhouseTSignature()

        # Update the corresponding Delivery object with the signature
        try:
            signature.ticket = ticket  # Associate the delivery with the signature
            signature.signature_image.save('signature.png', ContentFile(signature_binary), save=True)
            return JsonResponse({'success': True})
        except Tickets.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Format Approval not found'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


def create_Inhouse_ticket(request):
    if request.method == 'POST':
        # Handle form submission
        type = request.POST.get('type')
        company = request.POST.get('company')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        equipment = request.POST.get('equipment')
        serial_no = request.POST.get('serial_no')
        fault = request.POST.get('fault')
        accessories = request.POST.get('accessories')
        notes = request.POST.get('notes')
        brought_by = request.POST.get('brought_by')
        tech_id = request.POST.get('tech')

        # Create the ticket
        ticket = Tickets.objects.create(
            company=company,
            email=email,
            telephone=telephone,
            equipment=equipment,
            serial_no=serial_no,
            fault=fault,
            accessories=accessories,
            notes=notes,
            tech_id=tech_id,
            type=type,
            brought_by=brought_by,
        )

        messages.success(request, 'Ticket Created successfully')

        # Assuming you are in a view function, you can access the current user through the request object
        user = request.user
        # Create a new Task instance without saving it
        new_task = Task(
            title="Ticket for " + str(company) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
            description="You have been allocated Ticket for " + str(company) + " with fault " + str(fault),
            is_active=True,
            status="In Progress",
            user=get_object_or_404(User, id=tech_id),
            created_by=user,

        )

        # Save the new_task instance
        new_task.save()

        ticket.task = new_task
        ticket.save()

        return redirect('edit-ticket', ticket.ticket_id)  # Replace 'success_page' with the actual success page URL

    else:
        # Handle GET request, render the form
        companies = Company.objects.all().order_by('name')
        clients = Clients.objects.all()
        technician_group = Group.objects.get(name='Technician')
        users = technician_group.user_set.all()

        return render(request, 'technical/create_inhouse_ticket.html',
                      {'companies': companies, 'clients': clients, 'users': users})


def add_client(request):
    if request.method == 'POST':
        # Extract form data from the request
        company = request.POST.get('company')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        description = request.POST.get('description')

        # Create a new client instance and save it
        client = Clients.objects.create(
            company_id=company,
            f_name=f_name,
            l_name=l_name,
            email=email,
            telephone=telephone,
            description=description
        )

        messages.success(request, 'Client added successfully!')

        return JsonResponse({'success': True, 'message': 'Client added successfully!'})
    else:
        return JsonResponse({'warning': True, 'message': 'Error creating client!'})


def fetch_equipments(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    equipments = Equipment.objects.filter(client=client).values('id', 'name', 'serial_no')
    return JsonResponse(list(equipments), safe=False)
