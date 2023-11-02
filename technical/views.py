import uuid
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotFound, HttpRequest, Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET
from its.models import Company, Clients, Parts, PartsCategory, Task
from django.db import transaction
from django.http import HttpResponse
from .forms import TsourcingForm
from .models import Tickets, ProductDetail, Delivery, Items, Requisition, CallCards, ServiceSchedules, ServiceTickets, \
    Deliverys, Tsourcing, tQuote,FormatApproval, UniqueToken, FSignature
from django.core.mail import send_mail
from django.conf import settings


@login_required
def helpdesk_dash(request):
    return render(request, "technical/helpdesk_dashboard.html")


@login_required
def ticket_list(request):
    tickets = Tickets.objects.filter(is_active=1).order_by('-created')
    return render(request, 'technical/ticket_list.html', {'tickets': tickets})


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
def edit_ticket(request, ticket_id):
    users = User.objects.all()
    companies = Company.objects.all().order_by("name")
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    product_details = ProductDetail.objects.filter(ticket=ticket.ticket_id)
    tsourcing_data = Tsourcing.objects.filter(ticket=ticket)
    tquote_data = tQuote.objects.filter(ticket=ticket)

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
            selected_technician = User.objects.get(pk=selected_technician_id)
            saved_technician = ticket.tech
            # Update the ticket fields based on the POST data
            ticket.type = request.POST.get('type')
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
            # Update other fields similarly

            # Save the changes
            ticket.save()

            if selected_technician != saved_technician:
                if ticket.task:  # Check if a task exists for the ticket
                    ticket.task.user = selected_technician
                    ticket.task.save()

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
                send_mail(subject, message, from_email, recipient_list)

            # Redirect back to the edit view
            return redirect('edit-ticket', ticket_id=ticket_id)

        elif form_type == 'form3':
            form = TsourcingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('edit-ticket', ticket_id=ticket_id)  # Redirect after saving
            else:
                form = TsourcingForm()

        # Render the edit form
    return render(request, 'technical/edit_ticket.html',
                  {'ticket': ticket, 'users': users, 'product_details': product_details, 'companies': companies,
                   'requisitions': requisitions, 'tsourcing_data': tsourcing_data, 'tquote_data': tquote_data,
                   'parts': parts})


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
    signature_path = ''
    ticket_id = ticket_id
    try:
        ticket = Tickets.objects.get(pk=ticket_id)
    except Tickets.DoesNotExist:
        return HttpResponseNotFound("Ticket not found")

        # Check if a delivery already exists for this ticket
    existing_delivery = Delivery.objects.filter(ticket=ticket).first()

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

        )

        new_delivery.save()

        for i in range(1, 11):  # Example: Create up to 10 items
            quantity = request.POST.get(f'quantity_{i}')
            serial_no = request.POST.get(f'serial_no_{i}')
            particulars = request.POST.get(f'particulars_{i}')

            if quantity and serial_no and particulars:
                item = Items(
                    delivery=new_delivery,
                    quantity=quantity,
                    serial_no=serial_no,
                    particulars=particulars
                )
                item.save()

        messages.success(request, 'Delivery Created successfully')
        # Redirect to the ticket details page or a success page
        return redirect('view_delivery', ticket_id=ticket_id)

    return render(request, 'create_delivery.html', {'ticket': ticket})


@login_required
def create_delivery_normal(request):
    if request.method == 'POST':
        # Process the form data and create a new delivery
        client = request.POST.get('client')
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

        )

        new_delivery.save()

        for i in range(1, 11):  # Example: Create up to 10 items
            quantity = request.POST.get(f'quantity_{i}')
            serial_no = request.POST.get(f'serial_no_{i}')
            amount = request.POST.get(f'amount_{i}')
            particulars = request.POST.get(f'particulars_{i}')

            if quantity and serial_no and particulars:
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
        delivery = Delivery.objects.get(ticket=ticket)
        signature = delivery.signatures.last()
        items = delivery.items.all()
    except (Tickets.DoesNotExist, Delivery.DoesNotExist):
        return HttpResponseNotFound("Ticket or Delivery not found")

    return render(request, 'view_delivery.html',
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

        if delivery.vat_status == "inclusive":
            item.amount -= round((item.amount / 1.16) * 0.16)  # Deduct VAT from item.amount
            item.total -= round((item.total / 1.16) * 0.16)
            subtotals += item.total
            vat = round(subtotals * 0.16)
            total_amount = round(subtotals + vat)


        else:
            subtotals += item.total
            vat = round(subtotals * 0.16)
            total_amount = subtotals + vat

    try:
        signature = delivery.signatures.last()
    except (Delivery.DoesNotExist):
        return HttpResponseNotFound("Ticket or Delivery not found")

    return render(request, 'view_delivery_normal.html',
                  {'delivery': delivery, 'signature': signature, 'items': items, 'subtotals': subtotals, 'vat': vat,
                   'total_amount': total_amount, })


@login_required
def list_deliveries(request):
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

    if request.method == 'POST':
        # Process the form submission and update the requisition fields
        if 'serial_no' in request.POST and request.POST['serial_no']:
            requisition.serial_no = request.POST.get('serial_no')
        if 'remarks' in request.POST and request.POST['remarks']:
            requisition.remarks = request.POST.get('remarks')
        if 'req_status' in request.POST and request.POST['req_status']:
            requisition.req_status = request.POST.get('req_status')
        if 'issue_status' in request.POST and request.POST['issue_status']:
            requisition.issue_status = request.POST.get('issue_status')
        if 'return_status' in request.POST and request.POST['return_status']:
            requisition.return_status = request.POST.get('return_status')
            requisition.return_approved_by = request.user

        # Save the updated requisition
        requisition.save()
        messages.success(request, 'Requisition Edited successfully')
        return redirect('list_requisitions')

    return render(request, 'technical/edit_requisition.html', {'requisition': requisition})


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
        new_date = event_to_date + timedelta(days=1)
        data.append({
            'title': company,
            'start': event.from_date.isoformat(),
            'end': new_date.isoformat(),
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
                creator=user,
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

        # Update both ServiceSchedules and ServiceTickets instances within a transaction
        with transaction.atomic():
            # Update ServiceSchedules instance
            service_schedule.company_id = company_instance
            service_schedule.from_date = from_date
            service_schedule.to_date = to_date
            service_schedule.notes = notes
            service_schedule.status = status
            service_schedule.updated = timezone.now()
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

    if request.method == 'POST':
        # Handle form submission and update the call card
        call_card.time_in = request.POST.get('time_in')
        call_card.time_out = request.POST.get('time_out')
        call_card.equipment = request.POST.get('equipment')
        call_card.fault = request.POST.get('fault')
        call_card.remarks = request.POST.get('remarks')
        call_card.status = request.POST.get('status')
        call_card.type = request.POST.get('type')

        call_card.save()

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
            creator=user,

        )

        # Save the new_task instance
        new_task.save()

        ticket.task = new_task
        ticket.save()

        subject = "TICKET ITL/TN/" + str(ticket.ticket_id) + " OPENED - ITS"
        message = "Dear {0},\n\nA ticket ITL/TN/{1} has been raised for your work order, and our team is now reviewing the details to ensure a prompt and effective resolution.\n\nNote: You can reach out to us at support@intellitech.co.ke if you have any questions or concerns.\n\nThank you for your patience and understanding.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.".format(
            company_id, ticket.ticket_id)
        recipient_list = [company_id.email]
        from_email = 'its-noreply@intellitech.co.ke'
        send_mail(subject, message, from_email, recipient_list)
        # Redirect to a success page or any other desired action
        return redirect('edit-ticket', ticket.ticket_id)  # Replace 'success_page' with the actual success page URL

    else:
        # Handle GET request, render the form
        companies = Company.objects.all().order_by('name')
        clients = Clients.objects.all()
        users = User.objects.all()

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
                )
                new_quote_data.append(quote)

        # Delete old tQuote data
        tQuote.objects.filter(ticket=ticket).delete()

        # Insert the new data
        tQuote.objects.bulk_create(new_quote_data)

        messages.success(request, 'Quotation Products Updated.')

    return redirect('edit-ticket', ticket_id=ticket_id)


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
        handler = request.POST.get('handler')
        handler_id = User.objects.get(pk=handler)
        first_handler = ticket.sourcing_parts
        ticket.sourcing_parts = handler_id
        ticket.save()

        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and desc_list[i]):
                sourcing = Tsourcing(
                    part_no=part_no_list[i],
                    desc=desc_list[i],
                    qty=qty_list[i],
                    availability=availability_list[i],
                    supplier=supplier_list[i],
                    currency=currency_list[i],
                    price=price_list[i],
                    ticket=ticket,
                )
                new_sourcing_data.append(sourcing)

        # Delete old Tsourcing data
        Tsourcing.objects.filter(ticket=ticket).delete()

        # Insert the new data
        Tsourcing.objects.bulk_create(new_sourcing_data)

        user = request.user
        # Create a new Task instance without saving it
        if ticket.task is None:
            new_task = Task(
                title="Sourcing Items for " + str(ticket.company) + ", Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                description="Help in sourcing for items in Ticket NO : ITL/TN/" + str(ticket.ticket_id),
                is_active=True,
                status="In Progress",
                user_id=handler_id,  # Correctly set the user_id
                creator=user,
            )
            # Save the new_task instance
            new_task.save()
        elif ticket.task.user_id != handler_id:  # Check if the user_id is different
            ticket.task.user_id = handler_id  # Correctly set the user_id
            ticket.task.save()  # Save the task

        messages.success(request, 'Sourcing Products Updated.')

    return redirect('edit-ticket', ticket_id=ticket_id)


def delete_entry(request, entry_id):
    try:
        entry = Tsourcing.objects.get(id=entry_id)  # Replace YourModel with the appropriate model name
        entry.delete()
        return JsonResponse({'message': 'Entry deleted successfully'})
    except Tsourcing.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)


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


def report(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    quote_subtotals = 0
    quote_vat = 0
    quote_total_amount = 0

    try:
        tquote_data = tQuote.objects.filter(ticket=ticket)
        for item in tquote_data:
            item.total = item.quantity * item.price
            quote_subtotals += item.total
            quote_vat = round(quote_subtotals * 0.16)
            quote_total_amount = quote_subtotals + quote_vat

    except tQuote.DoesNotExist:
        tquote_data = None

    subtotals = ticket.labour
    vat = 0

    try:
        parts = Requisition.objects.filter(ticket=ticket, is_active=True, issue_status="Issue")
        for requisition in parts:
            requisition.total = requisition.quantity * requisition.price
            subtotals += requisition.total
    except Requisition.DoesNotExist:
        parts = None

    vat = round(subtotals * 0.16)
    total_amount = subtotals + vat
    return render(request, 'technical/report.html',
                  {'ticket': ticket, 'tquote_data': tquote_data, 'parts': parts, 'vat': vat,
                   'total_amount': total_amount, 'subtotals': subtotals, 'quote_subtotals': quote_subtotals,
                   'quote_total_amount': quote_total_amount, 'quote_vat': quote_vat})


def fill_checklist(request, client_id):
    if request.method == 'POST':
        client = Clients.objects.get(pk=client_id)
        service = ServiceDetails.objects.filter(client=client).first()  # You need to specify the correct service here.
        if service:
            checklist_items = ChecklistItem.objects.filter(checklist=service.equipment.checklist)
            with transaction.atomic():
                for item in checklist_items:
                    item_id = str(item.id)
                    checked = item_id in request.POST  # Check if the item is checked in the POST data.
                    comments = request.POST.get(f'comments_{item_id}')
                    # Update the ServiceDetails instance with the checked status and comments.
                    service_detail, created = ServiceDetails.objects.get_or_create(service=service, checklist_item=item)
                    service_detail.checked = checked
                    service_detail.comments = comments
                    service_detail.save()
            return redirect('client_page')  # Replace 'client_page' with the actual URL you want to redirect to.
        else:
            return HttpResponse('Service not found')  # Handle the case where the service is not found.
    else:
        # Retrieve the client and the associated checklist for the view.
        client = Clients.objects.get(pk=client_id)
        service = ServiceDetails.objects.filter(client=client).first()  # You need to specify the correct service here.
        if service:
            checklist_items = ChecklistItem.objects.filter(checklist=service.equipment.checklist)
            checklist_data = {}
            for item in checklist_items:
                service_detail = service.servicedetails_set.filter(checklist_item=item).first()
                checklist_data[item.id] = {
                    'checked': service_detail.checked if service_detail else False,
                    'comments': service_detail.comments if service_detail else ""
                }
            return render(request, 'technical/fill_checklist.html',
                          {'checklist_items': checklist_items, 'service': service})
        else:
            return HttpResponse('Service not found')  # Handle the case where the service is not found.


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


def send_format_email(request, format_approval_id):
    # Retrieve the FormatApproval object
    format_approval = get_object_or_404(FormatApproval, pk=format_approval_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')  # Get the recipient's email from the form
        # Ensure recipient_email is valid and not empty before proceeding

        # Generate a unique UUID for this email
        token = uuid.uuid4()

        # Create a UniqueToken and associate it with the FormatApproval
        unique_token = UniqueToken.objects.create(token=token, FormatApproval=format_approval)

        # Construct the URL using reverse with the UUID as a parameter
        url = request.build_absolute_uri(reverse('form_with_uuid', args=[str(token)]))

        subject = 'Format Approval Request'
        message = 'Dear ' + str(
            format_approval.ticket.company) + '\n\nPlease click the following link to approve the request for :' + str(
            format_approval.ticket.equipment) + ', Serial Number : ' + str(
            format_approval.ticket.serial_no) + ' \n\n'+str(url)+'\n\nNote: You can reach out to us at support@intellitech.co.ke if you have any questions or concerns.\n\nThank you for your patience and understanding.\n\nRegards,\nIntellitech Limited.\n\nThis is an auto-generated email | © 2023 ITS. All rights reserved.'
        recipient_list = [recipient_email]  # Use the recipient's email from the form input
        from_email = 'its-noreply@intellitech.co.ke'

        try:
            send_mail(subject, message, from_email, recipient_list)

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
