from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from technical.models import ServiceTickets, ServiceSchedules
from its.models import Company, Clients
from .models import Equipment, Software, EquipmentSpecs, Service, MonitorChecklist, PrinterChecklist, UpsChecklist


@login_required
def ticket_list(request):
    tickets = ServiceSchedules.objects.filter(is_active=1).order_by('-created')
    return render(request, 'service/tickets.html', {'tickets': tickets})


@login_required
def delete_service_ticket(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    service_schedule.is_active = False
    service_schedule.save()
    messages.warning(request, 'Service Ticket Deleted successfully')
    return redirect('service-tickets')


@login_required
def ticket_view(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    ticket = get_object_or_404(ServiceTickets, ticket_id=service_schedule)
    clients = service_schedule.company.clients_set.all()

    context = {'service_schedule': service_schedule, 'ticket': ticket,
               'clients': clients}  # Include 'ticket' in the context
    return render(request, "service/ticket_view.html", context)


def client_view(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    equipments = Equipment.objects.filter(client=client_id)
    software = Software.objects.filter(client=client_id)
    context = {'client': client, 'equipments': equipments, 'software': software}
    return render(request, "service/client_view.html", context)


def add_equipment(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)

    if request.method == 'POST':
        # Process the form data when it's submitted
        name = request.POST['name']
        details = request.POST['details']
        equipment_type = request.POST['type']
        serial_no = request.POST['serial_no']

        # Create a new equipment instance and associate it with the client
        equipment = Equipment(client=client, name=name, details=details, type=equipment_type, serial_no=serial_no)
        equipment.save()

        # You can add a success message or redirect to another page
        return redirect('client_view', client_id=client_id)

    # Display the form for adding equipment
    return render(request, 'service/add_equipment.html', {'client': client})


def add_software(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)

    if request.method == 'POST':
        os = request.POST['os']
        mo = request.POST['mo']
        backup = request.POST['backup']
        outlook = request.POST['outlook']

        software = Software(client=client, os=os, mo=mo, backup=backup, outlook=outlook)
        software.save()

        return redirect('client_view', client_id=client_id)

    return render(request, 'service/add_software_info.html', {'client': client})


def edit_software(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    software = get_object_or_404(Software, client=client_id)

    if request.method == 'POST':
        # Process the form data when it's submitted
        os = request.POST['os']
        mo = request.POST['mo']
        backup = request.POST['backup']
        outlook = request.POST['outlook']

        # Update the software details
        software.os = os
        software.mo = mo
        software.backup = backup
        software.outlook = outlook

        # Save the updated software instance
        software.save()

        # Redirect to a success page or client detail page
        return redirect('client_view', client_id=software.client.pk)

    # Display the form for editing software
    return render(request, 'service/edit_software.html', {'software': software})


def create_or_edit_equipment_specs(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment_specs, created = EquipmentSpecs.objects.get_or_create(equipment=equipment)

    if request.method == 'POST':
        # Process the form data (POST request)
        equipment_specs.antivirus = request.POST['antivirus']
        equipment_specs.psu = request.POST['psu']
        equipment_specs.comp_name = request.POST['comp_name']
        equipment_specs.ip_address = request.POST['ip_address']
        equipment_specs.ram = request.POST['ram']
        equipment_specs.cd_dvd = request.POST['cd_dvd']
        equipment_specs.processor = request.POST['processor']
        equipment_specs.hdd = request.POST['hdd']
        equipment_specs.hdd_status = request.POST['hdd_status']
        equipment_specs.mainboard = request.POST['mainboard']

        equipment_specs.save()

        return redirect('client_view', client_id=equipment.client.pk)

    # Redirect to the equipment's detail page
    return render(request, 'service/equipment_specs.html', {'equipment': equipment, 'equipment_specs': equipment_specs})


def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        # Process the form data for editing the equipment here
        equipment.name = request.POST.get('name')
        equipment.serial_no = request.POST.get('serial_no')
        equipment.details = request.POST.get('details')
        equipment.type = request.POST.get('type')
        equipment.save()

        # Redirect to the equipment detail page or any other appropriate page
        return redirect('client_view', client_id=equipment.client.pk)

    return render(request, 'service/edit_equipment.html', {'equipment': equipment})


def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        equipment.delete()
        # Redirect to a page after deleting the equipment (e.g., equipment list)
        return redirect('client_view', client_id=equipment.client.pk)

    return render(request, 'service/delete_equipment.html', {'equipment': equipment})


def create_service_form(request, client_id, ticket_id):
    client = get_object_or_404(Clients, pk=client_id)
    ticket = get_object_or_404(ServiceTickets, pk=ticket_id)
    schedule = ticket.ticket_id_id
    # Check if a Service object already exists for the given ticket and client
    service = Service.objects.filter(ticket=ticket, client=client).first()
    if service:
        if request.method == 'POST':
            details = request.POST.get('details')
            observations = request.POST.get('observations')
            recommendation = request.POST.get('recommendation')
            status = request.POST.get('status')

            # If a service object already exists, update it
            service.details = details
            service.observations = observations
            service.recommendation = recommendation
            service.status = status
            service.save()

            # Redirect to a success page or the ticket detail page
            return redirect('service_ticket_view', schedule_id=schedule)
    else:
        service = Service.objects.create(
            ticket=ticket,
            client=client, )

    return render(request, 'service/service_form.html', {'client': client, 'ticket': ticket, 'service': service})


def create_or_edit_monitor_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    # Check if a MonitorChecklist exists for the given equipment and service
    monitor_checklist = MonitorChecklist.objects.filter(equipment=equipment, service=service).first()

    if request.method == 'POST':
        # Process the form data
        phy_damage = request.POST.get('phy_damage') == 'on'
        colour_display = request.POST.get('colour_display') == 'on'
        vertical_lines = request.POST.get('vertical_lines') == 'on'
        vga_cable = request.POST.get('vga_cable') == 'on'
        status = request.POST.get('status')

        if monitor_checklist:
            # If a checklist already exists, update it
            monitor_checklist.phy_damage = phy_damage
            monitor_checklist.colour_display = colour_display
            monitor_checklist.vertical_lines = vertical_lines
            monitor_checklist.vga_cable = vga_cable
            monitor_checklist.status = status
            monitor_checklist.save()
        else:
            # If no checklist exists, create a new one
            monitor_checklist = MonitorChecklist.objects.create(
                equipment=equipment,
                service=service,
                phy_damage=phy_damage,
                colour_display=colour_display,
                vertical_lines=vertical_lines,
                vga_cable=vga_cable,
                status=status
            )

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/monitor_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'monitor_checklist': monitor_checklist})


def create_or_edit_printer_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    printer_checklist, created = PrinterChecklist.objects.get_or_create(equipment=equipment, service=service)

    if request.method == 'POST':
        power = request.POST.get('power') == 'on'
        tone = request.POST.get('tone') == 'on'
        phy_damage = request.POST.get('phy_damage') == 'on'
        service_interior = request.POST.get('service_interior') == 'on'
        service_roller = request.POST.get('service_roller') == 'on'
        static_eliminator = request.POST.get('static_eliminator') == 'on'
        fuser_unit = request.POST.get('fuser_unit') == 'on'
        gears = request.POST.get('gears') == 'on'
        status = request.POST.get('status')

        printer_checklist.power = power
        printer_checklist.tone = tone
        printer_checklist.phy_damage = phy_damage
        printer_checklist.service_interior = service_interior
        printer_checklist.service_roller = service_roller
        printer_checklist.static_eliminator = static_eliminator
        printer_checklist.fuser_unit = fuser_unit
        printer_checklist.gears = gears
        printer_checklist.status = status
        printer_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/printer_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'printer_checklist': printer_checklist})


def create_or_edit_ups_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    ups_checklist, created = UpsChecklist.objects.get_or_create(equipment=equipment, service=service)

    if request.method == 'POST':
        power = request.POST.get('power') == 'on'
        backup = request.POST.get('backup') == 'on'
        ports = request.POST.get('ports') == 'on'
        battery = request.POST.get('battery') == 'on'
        phy_damage = request.POST.get('phy_damage') == 'on'
        status = request.POST.get('status')

        ups_checklist.power = power
        ups_checklist.backup = backup
        ups_checklist.ports = ports
        ups_checklist.battery = battery
        ups_checklist.phy_damage = phy_damage
        ups_checklist.status = status
        ups_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/ups_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'ups_checklist': ups_checklist})


def schedule_detail(request, schedule_id):
    # Retrieve the service schedule for the given schedule_id
    schedule = ServiceSchedules.objects.get(ss_id=schedule_id)
    ticket = get_object_or_404(ServiceTickets, ticket_id=schedule)
    service = Service.object.get(ticket=ticket)

    # Retrieve associated clients and equipment for the schedule
    clients_and_equipment = Equipment.objects.filter(client__company=schedule.company)

    # Create an empty list to store equipment data
    equipment_data = []

    for equipment in clients_and_equipment:
        # Depending on the type of equipment, retrieve the relevant checklist
        if equipment.type == 'Monitor':
            checklist = MonitorChecklist.objects.get(equipment=equipment, service=service)
        elif equipment.type == 'Printer':
            checklist = PrinterChecklist.objects.get(equipment=equipment, service=service)
        elif equipment.type == 'UPS':
            checklist = UpsChecklist.objects.get(equipment=equipment, service=service)
        else:
            # Handle other equipment types as needed
            checklist = None

        # Append the equipment data to the list
        equipment_data.append({
            'client_name': equipment.client.f_name,
            'equipment_name': equipment.name,
            'observations': checklist.observations if checklist else '',
            'recommendation': checklist.recommendation if checklist else '',
            'status': checklist.status if checklist else '',
        })

    return render(request, 'service/schedule_detail.html', {
        'schedule': schedule,
        'equipment_data': equipment_data,
    })

