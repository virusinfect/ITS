from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from technical.models import ServiceTickets, ServiceSchedules
from its.models import Company, Clients
from .models import Equipment, Software, EquipmentSpecs, Service, MonitorChecklist, PrinterChecklist, UpsChecklist, \
    ServiceQuote, ServerChecklist, LaptopChecklist, CpuChecklist


@login_required
def ticket_list(request):
    tickets = ServiceSchedules.objects.all().order_by('-created')
    return render(request, 'service/tickets.html', {'tickets': tickets})


@login_required
def delete_service_ticket(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    service_schedule.delete()
    messages.warning(request, 'Service Ticket Deleted successfully')
    return redirect('service-tickets')


@login_required
def ticket_view(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    ticket = get_object_or_404(ServiceTickets, ticket_id=service_schedule)
    clients = service_schedule.company.clients_set.all()
    service_count = Service.objects.filter(ticket=ticket).count()
    service = Service.objects.filter(ticket=ticket)

    context = {'service_schedule': service_schedule, 'ticket': ticket,
               'clients': clients, 'service_count': service_count,
               'service': service}  # Include 'ticket' in the context
    return render(request, "service/ticket_view.html", context)


@login_required
def client_view(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    equipments = Equipment.objects.filter(client=client_id)
    software = Software.objects.filter(client=client_id)
    if request.method == 'POST':
        # If the form is submitted, update the client's information
        client.f_name = request.POST.get('f_name')
        client.l_name = request.POST.get('l_name')
        client.email = request.POST.get('email')
        client.telephone = request.POST.get('telephone')
        client.mobile = request.POST.get('mobile')
        client.description = request.POST.get('description')
        client.save()
        messages.success(request, 'Client Details Edited successfully.')

    context = {'client': client, 'equipments': equipments, 'software': software}
    return render(request, "service/client_view.html", context)


@login_required
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
        messages.success(request, 'Equipment Created successfully.')
        # You can add a success message or redirect to another page
        return redirect('client_view', client_id=client_id)

    # Display the form for adding equipment
    return render(request, 'service/add_equipment.html', {'client': client})


@login_required
def add_software(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)

    if request.method == 'POST':
        os = request.POST['os']
        mo = request.POST['mo']
        backup = request.POST['backup']
        outlook = request.POST['outlook']

        software = Software(client=client, os=os, mo=mo, backup=backup, outlook=outlook)
        software.save()
        messages.success(request, 'Software Added successfully.')
        return redirect('client_view', client_id=client_id)

    return render(request, 'service/add_software_info.html', {'client': client})


@login_required
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
        messages.success(request, 'Software Edited successfully.')
        # Redirect to a success page or client detail page
        return redirect('client_view', client_id=software.client.pk)

    # Display the form for editing software
    return render(request, 'service/edit_software.html', {'software': software})


@login_required
def create_or_edit_equipment_specs(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment_specs, created = EquipmentSpecs.objects.get_or_create(equipment=equipment)

    if request.method == 'POST':
        # Process the form data (POST request)
        equipment_specs.antivirus = request.POST['antivirus']
        equipment_specs.psu = request.POST['psu']
        equipment_specs.domain = request.POST['domain']
        equipment_specs.comp_name = request.POST['comp_name']
        equipment_specs.ip_address = request.POST['ip_address']
        equipment_specs.ram = request.POST['ram']
        equipment_specs.cd_dvd = request.POST['cd_dvd']
        equipment_specs.processor = request.POST['processor']
        equipment_specs.hdd = request.POST['hdd']
        equipment_specs.gen = request.POST['gen']
        equipment_specs.hdd_status = request.POST['hdd_status']
        equipment_specs.mainboard = request.POST['mainboard']

        equipment_specs.save()
        messages.success(request, 'Specifications Edited successfully.')
        return redirect('client_view', client_id=equipment.client.pk)

    # Redirect to the equipment's detail page
    return render(request, 'service/equipment_specs.html', {'equipment': equipment, 'equipment_specs': equipment_specs})


@login_required
def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        # Process the form data for editing the equipment here
        equipment.name = request.POST.get('name')
        equipment.serial_no = request.POST.get('serial_no')
        equipment.details = request.POST.get('details')
        equipment.type = request.POST.get('type')
        equipment.save()
        messages.success(request, 'Equipment Edited successfully.')
        # Redirect to the equipment detail page or any other appropriate page
        return redirect('client_view', client_id=equipment.client.pk)

    return render(request, 'service/edit_equipment.html', {'equipment': equipment})


@login_required
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        equipment.delete()
        messages.warning(request, 'Equipment Deleted successfully.')
        # Redirect to a page after deleting the equipment (e.g., equipment list)
        return redirect('client_view', client_id=equipment.client.pk)

    return render(request, 'service/delete_equipment.html', {'equipment': equipment})


@login_required
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
            messages.success(request, 'Service Form Edited successfully.')
            # Redirect to a success page or the ticket detail page
            return redirect('service_ticket_view', schedule_id=schedule)
    else:
        service = Service.objects.create(
            ticket=ticket,
            client=client, )

    return render(request, 'service/service_form.html', {'client': client, 'ticket': ticket, 'service': service})


@login_required
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
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        if monitor_checklist:
            # If a checklist already exists, update it
            monitor_checklist.phy_damage = phy_damage
            monitor_checklist.colour_display = colour_display
            monitor_checklist.vertical_lines = vertical_lines
            monitor_checklist.vga_cable = vga_cable
            monitor_checklist.status = status
            monitor_checklist.observations = observations
            monitor_checklist.recommendation = recommendation
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
        messages.success(request, 'Monitor Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/monitor_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'monitor_checklist': monitor_checklist})


@login_required
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
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        printer_checklist.power = power
        printer_checklist.tone = tone
        printer_checklist.phy_damage = phy_damage
        printer_checklist.service_interior = service_interior
        printer_checklist.service_roller = service_roller
        printer_checklist.static_eliminator = static_eliminator
        printer_checklist.fuser_unit = fuser_unit
        printer_checklist.gears = gears
        printer_checklist.status = status
        printer_checklist.observations = observations
        printer_checklist.recommendation = recommendation
        printer_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        messages.success(request, 'Printer Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/printer_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'printer_checklist': printer_checklist})

@login_required
def create_or_edit_server_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    server_checklist, created = ServerChecklist.objects.get_or_create(equipment=equipment, service=service)

    if request.method == 'POST':
        antiv = request.POST.get('antiv') == 'on'
        pwr = request.POST.get('pwr') == 'on'
        memory = request.POST.get('memory') == 'on'
        fan = request.POST.get('fan') == 'on'
        dvd = request.POST.get('dvd') == 'on'
        processor = request.POST.get('processor') == 'on'
        hdd = request.POST.get('hdd') == 'on'
        board = request.POST.get('board') == 'on'
        status = request.POST.get('status')
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        server_checklist.antiv = antiv
        server_checklist.pwr = pwr
        server_checklist.memory = memory
        server_checklist.fan = fan
        server_checklist.dvd = dvd
        server_checklist.processor = processor
        server_checklist.hdd = hdd
        server_checklist.board = board
        server_checklist.status = status
        server_checklist.observations = observations
        server_checklist.recommendation = recommendation
        server_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        messages.success(request, 'Server Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/server_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'server_checklist': server_checklist})

@login_required
def create_or_edit_laptop_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    laptop_checklist, created = LaptopChecklist.objects.get_or_create(equipment=equipment, service=service)

    if request.method == 'POST':
        antiv = request.POST.get('antiv') == 'on'
        pwr = request.POST.get('pwr') == 'on'
        memory = request.POST.get('memory') == 'on'
        fan = request.POST.get('fan') == 'on'
        dvd = request.POST.get('dvd') == 'on'
        processor = request.POST.get('processor') == 'on'
        hdd = request.POST.get('hdd') == 'on'
        board = request.POST.get('board') == 'on'
        status = request.POST.get('status')
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        laptop_checklist.antiv = antiv
        laptop_checklist.pwr = pwr
        laptop_checklist.memory = memory
        laptop_checklist.fan = fan
        laptop_checklist.dvd = dvd
        laptop_checklist.processor = processor
        laptop_checklist.hdd = hdd
        laptop_checklist.board = board
        laptop_checklist.status = status
        laptop_checklist.observations = observations
        laptop_checklist.recommendation = recommendation
        laptop_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        messages.success(request, 'Laptop Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/laptop_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'laptop_checklist': laptop_checklist})

@login_required
def create_or_edit_cpu_checklist(request, equipment_id, service_id, client_id, ticket_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    service = get_object_or_404(Service, pk=service_id)

    cpu_checklist, created = CpuChecklist.objects.get_or_create(equipment=equipment, service=service)

    if request.method == 'POST':
        antiv = request.POST.get('antiv') == 'on'
        pwr = request.POST.get('pwr') == 'on'
        memory = request.POST.get('memory') == 'on'
        fan = request.POST.get('fan') == 'on'
        dvd = request.POST.get('dvd') == 'on'
        processor = request.POST.get('processor') == 'on'
        hdd = request.POST.get('hdd') == 'on'
        board = request.POST.get('board') == 'on'
        status = request.POST.get('status')
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        cpu_checklist.antiv = antiv
        cpu_checklist.pwr = pwr
        cpu_checklist.memory = memory
        cpu_checklist.fan = fan
        cpu_checklist.dvd = dvd
        cpu_checklist.processor = processor
        cpu_checklist.hdd = hdd
        cpu_checklist.board = board
        cpu_checklist.status = status
        cpu_checklist.observations = observations
        cpu_checklist.recommendation = recommendation
        cpu_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        messages.success(request, 'Cpu Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/cpu_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'cpu_checklist': cpu_checklist})

@login_required
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
        observations = request.POST.get('observations')
        recommendation = request.POST.get('recommendation')

        ups_checklist.power = power
        ups_checklist.backup = backup
        ups_checklist.ports = ports
        ups_checklist.battery = battery
        ups_checklist.phy_damage = phy_damage
        ups_checklist.status = status
        ups_checklist.observations = observations
        ups_checklist.recommendation = recommendation
        ups_checklist.save()

        # Redirect to a success page or the equipment or service detail page
        # Adjust this based on your project's requirements
        messages.success(request, 'UPS Checklist Edited successfully.')
        return redirect('create_service_form', client_id=client_id, ticket_id=ticket_id)

    return render(request, 'service/ups_checklist_form.html',
                  {'equipment': equipment, 'service': service, 'ups_checklist': ups_checklist})


@login_required
def service_report(request, schedule_id):
    service_schedule = get_object_or_404(ServiceSchedules, pk=schedule_id)
    ticket = get_object_or_404(ServiceTickets, ticket_id=service_schedule)
    service_tickets = service_schedule.servicetickets_set.all()
    services = Service.objects.filter(ticket=ticket)
    checklists = []

    for service in services:
        client = service.client
        equipment = Equipment.objects.filter(client=client)

        monitor_checklists = MonitorChecklist.objects.filter(equipment__in=equipment, service=service)
        printer_checklists = PrinterChecklist.objects.filter(equipment__in=equipment, service=service)
        laptop_checklists = LaptopChecklist.objects.filter(equipment__in=equipment, service=service)
        cpu_checklists = CpuChecklist.objects.filter(equipment__in=equipment, service=service)
        server_checklists = ServerChecklist.objects.filter(equipment__in=equipment, service=service)
        ups_checklists = UpsChecklist.objects.filter(equipment__in=equipment, service=service)

        checklists.append({
            'service': service,
            'client': client,
            'equipment': equipment,
            'monitor_checklists': monitor_checklists,
            'printer_checklists': printer_checklists,
            'ups_checklists': ups_checklists,
            'laptop_checklists':laptop_checklists,
            'cpu_checklists':cpu_checklists,
            'server_checklists':server_checklists,

        })

    return render(request, 'service/service_report.html',
                  {'checklists': checklists, 'ticket': ticket, 'service_schedule': service_schedule,
                   'service_tickets': service_tickets})

@login_required
def quote_tickets(request, ticket_id):
    if request.method == 'POST':
        ticket = ServiceTickets.objects.get(ticket_id=ticket_id)

        part_no_list = request.POST.getlist('part_no[]')
        description_list = request.POST.getlist('description[]')
        quantity_list = request.POST.getlist('quantity[]')
        currency_list = request.POST.getlist('currency[]')
        price_list = request.POST.getlist('price[]')

        # Create a list to hold the new tQuote objects
        new_quote_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and description_list[i]):
                quote = ServiceQuote(
                    part_no=part_no_list[i],
                    description=description_list[i],
                    quantity=quantity_list[i],
                    currency=currency_list[i],
                    price=price_list[i],
                    ticket=ticket,
                )
                new_quote_data.append(quote)

        # Delete old tQuote data
        ServiceQuote.objects.filter(ticket=ticket).delete()

        # Insert the new data
        ServiceQuote.objects.bulk_create(new_quote_data)

        messages.success(request, 'Quotation Products Updated.')

    return redirect('edit-ticket', ticket_id=ticket_id)
