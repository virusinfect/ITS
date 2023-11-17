from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from its.models import Company, Task

from .models import SalesTickets, SalesQuotes, Orders, ProformaInvoice, OurBanks, SalesQuoteProducts, OrderProducts, \
    SalesTicketProducts, ProformaInvoiceProducts


@login_required
def sales_tickets_list(request):
    # Filter sales tickets that are active (assuming "is_active" is a boolean field)
    active_sales_tickets = SalesTickets.objects.filter(is_active=1).order_by("-ticket_id")
    return render(request, 'sales/sales_tickets.html', {'active_sales_tickets': active_sales_tickets})

@login_required
def filtered_sales_tickets_list(request):
    # Filter sales tickets that are active and get the 50 latest ones
    active_sales_tickets = SalesTickets.objects.filter(is_active=1).order_by("-ticket_id")[:50]
    return render(request, 'sales/sales_tickets.html', {'active_sales_tickets': active_sales_tickets})

@login_required
def open_tickets_list(request):
    # Filter sales tickets that are active (assuming "is_active" is a boolean field)
    active_sales_tickets = SalesTickets.objects.filter(is_active=1, status__in=["Quote", "Sourcing"]).order_by("-ticket_id")
    return render(request, 'sales/sales_tickets.html', {'active_sales_tickets': active_sales_tickets})


@login_required
def tickets_in_status(request, status):
    active_sales_tickets = SalesTickets.objects.filter(status=status, is_active=1)
    return render(request, 'sales/sales_tickets.html',
                  {'active_sales_tickets': active_sales_tickets, 'status': status, })


@login_required
def edit_sales_ticket(request, ticket_id):
    # Get the SalesTickets instance to edit
    ticket = get_object_or_404(SalesTickets, ticket_id=ticket_id)
    companies = Company.objects.all()
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    handler1 = ticket.handler
    try:
        sales_quote = SalesQuotes.objects.filter(ticket=ticket, is_active=True)
    except SalesQuotes.DoesNotExist:
        sales_quote = None

    try:
        sales_order = Orders.objects.filter(ticket=ticket, is_active=True)
    except Orders.DoesNotExist:
        sales_order = None

    try:
        sales_invoice = ProformaInvoice.objects.filter(ticket=ticket, is_active=True)
    except ProformaInvoice.DoesNotExist:
        sales_invoice = None

    if request.method == 'POST':
        # Handle the form submission (update the instance)
        ticket.status = request.POST['status']
        ticket.contact = request.POST['contact']
        ticket.issue_summary = request.POST['issue_summary']
        ticket.via = request.POST['via']
        handler_id = request.POST.get('handler_id')
        handler = User.objects.get(id=handler_id)
        ticket.handler = handler
        ticket.more = request.POST['more']
        ticket.company = get_object_or_404(Company, id=request.POST['company_id'])
        ticket.save()

        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('description[]')
        qty_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')
        supplier_list = request.POST.getlist('supplier[]')
        currency_list = request.POST.getlist('currency[]')
        price_list = request.POST.getlist('price[]')

        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and desc_list[i]):
                products = SalesTicketProducts(
                    part_no=part_no_list[i],
                    description=desc_list[i],
                    quantity=qty_list[i],
                    price=price_list[i],
                    availability=availability_list[i],
                    supplier=supplier_list[i],
                    currency=currency_list[i],
                    ticket=ticket,
                )
                new_sourcing_data.append(products)

        # Delete old Tsourcing data
        SalesTicketProducts.objects.filter(ticket=ticket).delete()

        # Insert the new data
        SalesTicketProducts.objects.bulk_create(new_sourcing_data)
        if handler1.id != handler.id:
            table = (
                "<table style='border-collapse: collapse; width: 100%;'>"
                "<tr style='border-bottom: 3px solid #ddd;'>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Part No</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Description</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Price</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Availability</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
                "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Currency</th>"
                "</tr>"
            )

            for i in range(len(part_no_list)):
                if part_no_list[i] and desc_list[i]:
                    row = (
                        "<tr>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{part_no_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{desc_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{qty_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{price_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{availability_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                        f"<td style='border: 3px solid #ddd; padding: 8px;'>{currency_list[i]}</td>"
                        "</tr>"
                    )
                    table += row

            table += "</table>"
            if ticket.status == "Sourcing":
                status = "Source"
                status2 = "sourcing"
            elif ticket.status == "Quote":
                status = "Quote"
                status2 = "quoting"
            elif ticket.status == "Closed":
                status = "Close"
                status2 = "Closed"

            # Your existing code to create new_sourcing_data objects
            url = "http://146.190.61.23:8500/sales/edit/" + str(ticket.ticket_id) + "/"  # Replace with your actual URL
            clickable_url = f"<a href='{url}'>#" + str(ticket.ticket_id) + "</a>"
            # Use the 'table' string in the email message
            message = (
                f"Dear {handler},<br><br>"
                f"Our sales team has reassigned a ticket, {clickable_url} on your behalf, for {status2} of the following details and summary:<br><br>"
                f"Topic: <strong>GENERAL ENQUIRY</strong><br><br>"
                f"Subject: <strong>{ticket.status}</strong> : <strong>{ticket.company.name}</strong> : <strong>{ticket.issue_summary}</strong><br><br>"
                f"Kindly {status} for below:<br><br>{table}<br><br>"
                "This is an auto-generated email | © 2023 ITS. All rights reserved."
            )

            subject = f"{status} : {ticket.company.name} : {ticket.issue_summary} : #{ticket.ticket_id}"
            recipient_list = [handler.email, ticket.company]
            from_email = 'its-noreply@intellitech.co.ke'

            # Create an EmailMessage instance for HTML content
            email_message = EmailMessage(subject, message, from_email, recipient_list)
            email_message.content_subtype = 'html'  # Set content type to HTML
            email_message.send()

        messages.success(request, 'Ticket Edited successfully.')

        # Redirect to a success page or the edited ticket's detail page
        return redirect('edit_sales_ticket', ticket_id=ticket.ticket_id)

    return render(request, 'sales/edit_ticket.html',
                  {'ticket': ticket, 'companies': companies, 'users': users, 'sales_quote': sales_quote,
                   'sales_order': sales_order, 'sales_invoice': sales_invoice})


@login_required
def duplicate_sales_ticket(request, ticket_id):
    # Get the SalesTicket to duplicate
    original_ticket = get_object_or_404(SalesTickets, ticket_id=ticket_id)

    # Create a new SalesTicket with the same data, excluding the ID
    new_ticket = SalesTickets(
        contact=original_ticket.contact,
        issue_summary=original_ticket.issue_summary,
        description=original_ticket.description,
        via=original_ticket.via,
        handler=original_ticket.handler,
        more=original_ticket.more,
        is_active=original_ticket.is_active,
        created=original_ticket.created,
        updated=original_ticket.updated,
        company=original_ticket.company,
    )

    new_ticket.save()

    # Duplicate associated SalesTicketProducts
    for product in original_ticket.salesticketproducts_set.all():
        new_product = SalesTicketProducts(
            part_no=product.part_no,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            currency=product.currency,
            availability=product.availability,
            supplier=product.supplier,
            attachment=product.attachment,
            is_active=product.is_active,
            created=product.created,
            updated=product.updated,
            ticket=new_ticket,
            ticket_handler=product.ticket_handler,
        )
        new_product.save()

    return redirect('edit_sales_ticket', ticket_id=new_ticket.ticket_id)


@login_required
def bank_list(request):
    banks = OurBanks.objects.all()
    return render(request, 'sales/bank_list.html', {'banks': banks})


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Orders, o_id=order_id)
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    companies = Company.objects.all().order_by('name')

    if request.method == 'POST':
        # Update the order fields based on user input
        order.lpo_no = request.POST.get('lpo_no')
        assignee_id = request.POST.get('assignee')
        order.assignee = User.objects.get(id=assignee_id)
        order.status = request.POST.get('status')
        order.save()

        # Create OrderProducts from the form data
        product_list = request.POST.getlist('product[]')
        quantity_list = request.POST.getlist('quantity[]')
        date_ordered_list = request.POST.getlist('date_ordered[]')
        supplier_list = request.POST.getlist('supplier[]')
        date_received_list = request.POST.getlist('date_received[]')

        new_sourcing_data = []

        for i in range(len(product_list)):
            if (product_list[i]):
                order_product = OrderProducts(
                    product=product_list[i],
                    quantity=quantity_list[i],
                    supplier=supplier_list[i],
                    is_active=True,
                    orders=order,
                )
                if date_received_list[i]:
                    order_product.date_received = date_received_list[i]
                if date_ordered_list[i]:
                    order_product.date_ordered = date_ordered_list[i]
                new_sourcing_data.append(order_product)

            # Delete old order data
        OrderProducts.objects.filter(orders=order).delete()

        # Insert the new data
        OrderProducts.objects.bulk_create(new_sourcing_data)

        messages.success(request, 'Order Edited successfully')

        return redirect('edit-order', order.o_id)  # Redirect to the order list page or a success page

    # Render the edit form with the existing order details
    return render(request, 'sales/edit_order.html', {'order': order, 'users': users, 'companies': companies})


@login_required
def duplicate_order(request, order_id):
    # Get the Order to duplicate
    original_order = get_object_or_404(Orders, o_id=order_id)

    # Create a new Order with the same data, excluding the ID
    new_order = Orders(
        client=original_order.client,
        lpo_no=original_order.lpo_no,
        assignee=original_order.assignee,
        status=original_order.status,
        is_active=original_order.is_active,
        created=original_order.created,
        updated=original_order.updated,
        ticket=original_order.ticket,  # Assuming you want to duplicate the ticket reference
    )

    new_order.save()

    # Duplicate associated OrderProducts
    for product in original_order.orderproducts_set.all():
        new_product = OrderProducts(
            product=product.product,
            quantity=product.quantity,
            date_ordered=product.date_ordered,
            supplier=product.supplier,
            date_received=product.date_received,
            is_active=product.is_active,
            created=product.created,
            updated=product.updated,
            orders=new_order,
        )
        new_product.save()

    return redirect('edit-order', new_order.o_id)  # Redirect to the order list page or a success page


@login_required
def deactivate_order_product(request, op_id, order_id):
    order_product = get_object_or_404(OrderProducts, op_id=op_id)
    order_product.is_active = False
    order_product.save()
    messages.success(request, 'Product Received successfully')
    return redirect('edit-order', order_id)


@login_required
def active_orders(request):
    orders = Orders.objects.filter(is_active=True).prefetch_related('orderproducts_set').order_by('-o_id')
    return render(request, 'sales/orders.html', {'orders': orders})


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Orders, o_id=order_id)
    order.is_active = False
    order.save()
    messages.warning(request, 'Order Succefully Deleted.')
    return redirect('active-orders')


@login_required
def active_quotes(request):
    quotes = SalesQuotes.objects.filter(is_active=True).prefetch_related('salesquoteproducts_set').order_by('-sq_id')
    return render(request, 'sales/active_quotes.html', {'quotes': quotes})


@login_required
def quotes_in_status(request, status):
    quotes = SalesQuotes.objects.filter(status=status, is_active=True)

    return render(request, 'sales/active_quotes.html', {'quotes': quotes, 'status': status, })


@login_required
def active_invoice(request):
    invoices = ProformaInvoice.objects.filter(is_active=True).prefetch_related('proformainvoiceproducts_set').order_by(
        '-pfq_id')
    return render(request, 'sales/active_invoices.html', {'invoices': invoices})


@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(SalesQuotes, sq_id=quote_id)
    sales_group = Group.objects.get(name='sales')
    users = sales_group.user_set.all()
    products = SalesQuoteProducts.objects.filter(quote=quote)

    if request.method == 'POST':
        # Update the fields with values from the POST request
        quote.mail_text = request.POST.get('mail_text')
        quote.footer_note = request.POST.get('footer_note')
        quote.currency = request.POST.get('currency')
        quote.status = request.POST.get('status')
        quote.layout = request.POST.get('layout')
        quote.vat_stats = request.POST.get('vat_stats')
        quote.remark = request.POST.get('remark')
        quote.notes = request.POST.get('notes')
        # Assuming you have a 'quote_handler' field as well:
        quote.quote_handler = User.objects.get(id=request.POST.get('quote_handler'))

        quote.save()  # Save the changes to the database

        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('description[]')
        qty_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')
        price_list = request.POST.getlist('price[]')
        uploaded_images = request.FILES.getlist('image[]')
        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (desc_list[i]):
                products = SalesQuoteProducts(
                    part_no=part_no_list[i],
                    description=desc_list[i],
                    quantity=qty_list[i],
                    price=price_list[i],
                    availability=availability_list[i],
                    quote=quote,
                )
                # Check if there is an uploaded image for the current index
                if i < len(uploaded_images):
                    image_file = uploaded_images[i]

                    # Handle file upload for each product
                    if image_file:
                        # Generate a unique file name or use the original name
                        file_name = f"sales_image_{part_no_list[i]}_{image_file.name}"

                        # Save the image file to your desired storage location
                        file_path = default_storage.save(file_name, ContentFile(image_file.read()))
                        print("image")
                        print(file_path)
                        # Update your model instance with the file path
                        products.attachment = file_path

                new_sourcing_data.append(products)

        # Delete old quote data
        SalesQuoteProducts.objects.filter(quote=quote).delete()

        # Insert the new data
        SalesQuoteProducts.objects.bulk_create(new_sourcing_data)

        messages.success(request, 'Quotation Edited successfully')

        return redirect('edit-quote', quote_id)  # Redirect to the list of active quotes

    return render(request, 'sales/edit_quote.html', {'quote': quote, 'users': users, 'products': products})


@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(SalesQuotes, pk=quote_id)

    # Set is_active to False (0) to "delete" the quote
    quote.is_active = False
    quote.save()
    messages.warning(request, 'Quotation Deleted successfully')
    # Assuming you want to redirect back to the same page it was deleted from
    # You may need to dynamically determine the URL based on your app's structure
    return redirect('active-quotes')


@login_required
def delete_quote_ticket(request, quote_id, ticket_id):
    quote = get_object_or_404(SalesQuotes, pk=quote_id)

    # Set is_active to False (0) to "delete" the quote
    quote.is_active = False
    quote.save()
    messages.warning(request, 'Quotation Deleted successfully')
    # Assuming you want to redirect back to the same page it was deleted from
    # You may need to dynamically determine the URL based on your app's structure
    return redirect('edit_sales_ticket', ticket_id)


@login_required
def convert_to_quote(request, ticket_id):
    ticket = get_object_or_404(SalesTickets, ticket_id=ticket_id)
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    if request.method == 'POST':
        handler_id = request.POST.get('handler')
        handler = User.objects.get(id=handler_id)
        # Create a new SalesQuotes object
        quote = SalesQuotes(
            mail_text=request.POST.get('mail_text'),
            footer_note=request.POST.get('footer_note'),
            currency=request.POST.get('currency'),
            status=request.POST.get('status'),
            layout=request.POST.get('layout'),
            vat_stats=request.POST.get('vat_stats'),
            remark=request.POST.get('remark'),
            notes=request.POST.get('notes'),
            is_active=True,  # You can set this based on your logic
            ticket=ticket,
            company=ticket.company,  # Assuming you want to keep the same company
            sent_stats=0,  # Adjust this as needed
            quote_handler=handler,  # Set the quote handler to the current user
        )
        quote.save()

        # Copy ticket products to quote products
        part_no_list = request.POST.getlist('part_no[]')
        description_list = request.POST.getlist('description[]')
        price_list = request.POST.getlist('price[]')
        quantity_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')

        for i in range(len(part_no_list)):
            quote_product = SalesQuoteProducts(
                part_no=part_no_list[i],
                description=description_list[i],
                price=price_list[i],
                quantity=quantity_list[i],
                currency='KES',
                availability=availability_list[i],
                is_active=True,  # You can set this based on your logic
                quote=quote,
            )
            quote_product.save()

        messages.success(request, 'Ticket successfully converted to a quote.')
        return redirect('edit-quote', quote.sq_id)  # Redirect to the list of active quotes or the desired page

    return render(request, 'sales/convert_to_quote.html', {'ticket': ticket, 'users': users})


@login_required
def convert_to_order(request, ticket_id):
    ticket = get_object_or_404(SalesTickets, pk=ticket_id)
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    if request.method == 'POST':
        handler_id = request.POST.get('handler')
        handler = User.objects.get(id=handler_id)
        # Create a new Orders record
        order = Orders(
            client=ticket.contact,
            lpo_no=request.POST.get('lpo_no'),
            assignee=handler,  # Set assignee to the current user
            status=request.POST.get('status'),
            is_active=True,
            ticket=ticket,  # Attach the ticket
        )
        order.save()

        # Create OrderProducts from the form data
        product_list = request.POST.getlist('product[]')
        quantity_list = request.POST.getlist('quantity[]')
        date_ordered_list = request.POST.getlist('date_ordered[]')
        supplier_list = request.POST.getlist('supplier[]')
        date_received_list = request.POST.getlist('date_received[]')

        for i in range(len(product_list)):
            if product_list[i]:
                order_product = OrderProducts(
                    product=product_list[i],
                    quantity=quantity_list[i],
                    supplier=supplier_list[i],
                    is_active=True,
                    orders=order,
                )
                order_product.save()
                if date_received_list[i]:
                    order_product.date_received = date_received_list[i]
                    order_product.save()

                if date_ordered_list[i]:
                    order_product.date_ordered = date_ordered_list[i]
                    order_product.save()

        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Product</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Ordered</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Received</th>"
            "</tr>"
        )

        for i in range(len(product_list)):
            if product_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{product_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{quantity_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_ordered_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_received_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/sales/orders/edit/" + str(order.o_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(order.o_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler},<br><br>"
            f"Our sales team has created an order, {clickable_url} on your behalf. Here are the details and summary of the order:<br><br>"
            f"Client: {order.client};<br><br>"
            f"Kindly order for below::<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"ORDER: SO-{order.o_id}"
        recipient_list = [handler.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        messages.success(request, 'Ticket successfully converted to an order.')
        return redirect('edit-order', order.o_id)  # Redirect to the list of active orders or the desired page

    return render(request, 'sales/convert_to_order.html', {'ticket': ticket, 'users': users})


@login_required
def convert_quote_to_order(request, quote_id):
    quote = get_object_or_404(SalesQuotes, sq_id=quote_id)
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    if request.method == 'POST':
        handler_id = request.POST.get('handler')
        handler = User.objects.get(id=handler_id)
        # Create a new Orders record
        order = Orders(
            ticket=quote.ticket,
            client=request.POST.get('client'),
            lpo_no=request.POST.get('lpo_no'),
            assignee=handler,  # Set assignee to the current user
            status=request.POST.get('status'),
            is_active=True,
        )
        order.save()

        # Create OrderProducts from the form data
        product_list = request.POST.getlist('product[]')
        quantity_list = request.POST.getlist('quantity[]')
        date_ordered_list = request.POST.getlist('date_ordered[]')
        supplier_list = request.POST.getlist('supplier[]')
        date_received_list = request.POST.getlist('date_received[]')

        for i in range(len(product_list)):
            if product_list[i]:
                order_product = OrderProducts(
                    product=product_list[i],
                    quantity=quantity_list[i],
                    supplier=supplier_list[i],
                    is_active=True,
                    orders=order,
                )
                order_product.save()
                if date_received_list[i]:
                    order_product.date_received = date_received_list[i]
                    order_product.save()

                if date_ordered_list[i]:
                    order_product.date_ordered = date_ordered_list[i]
                    order_product.save()

        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Product</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Ordered</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Received</th>"
            "</tr>"
        )

        for i in range(len(product_list)):
            if product_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{product_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{quantity_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_ordered_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_received_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/sales/orders/edit/" + str(order.o_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(order.o_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler},<br><br>"
            f"Our sales team has created an order, {clickable_url} on your behalf. Here are the details and summary of the order:<br><br>"
            f"Client: {order.client};<br><br>"
            f"Kindly order for below::<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"ORDER: SO-{order.o_id}"
        recipient_list = [handler.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        messages.success(request, 'Quote successfully converted to an order.')
        return redirect('edit-order', order.o_id)  # Redirect to the list of active orders or the desired page

    return render(request, 'sales/convert_quote_to_order.html', {'quote': quote, 'users': users})


@login_required
def create_order(request):
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    if request.method == 'POST':
        handler_id = request.POST.get('handler')
        handler = User.objects.get(id=handler_id)
        client_name = request.POST.get('client')
        # Create a new Orders record
        order = Orders(
            client=client_name,
            lpo_no=request.POST.get('lpo_no'),
            assignee=handler,  # Set assignee to the current user
            status=request.POST.get('status'),
            is_active=True,
        )
        order.save()
        print(client_name)

        # Create OrderProducts from the form data
        product_list = request.POST.getlist('product[]')
        quantity_list = request.POST.getlist('quantity[]')
        date_ordered_list = request.POST.getlist('date_ordered[]')
        supplier_list = request.POST.getlist('supplier[]')
        date_received_list = request.POST.getlist('date_received[]')
        for i in range(len(product_list)):
            if (product_list[i]):
                order_product = OrderProducts(
                    product=product_list[i],
                    quantity=quantity_list[i],
                    supplier=supplier_list[i],
                    is_active=True,
                    orders=order,

                )
                order_product.save()
                if date_received_list[i]:
                    order_product.date_received = date_received_list[i]
                    order_product.save()

                if date_ordered_list[i]:
                    order_product.date_ordered = date_ordered_list[i]
                    order_product.save()

        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Product</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Ordered</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Date Received</th>"
            "</tr>"
        )

        for i in range(len(product_list)):
            if product_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{product_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{quantity_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_ordered_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{date_received_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/sales/orders/edit/" + str(order.o_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(order.o_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler},<br><br>"
            f"Our sales team has created an order, {clickable_url} on your behalf. Here are the details and summary of the order:<br><br>"
            f"Client: {order.client};<br><br>"
            f"Kindly order for below::<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"ORDER: SO-{order.o_id}"
        recipient_list = [handler.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        messages.success(request, 'Order Created successfully.')
        return redirect('edit-order', order.o_id)  # Redirect to the list of active orders or the desired page

    return render(request, 'sales/convert_to_order.html', {'users': users})


@login_required
def create_ticket(request):
    companies = Company.objects.all().order_by('name')
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        issue = request.POST.get('issue_summary')
        more = request.POST.get('more')
        handler_id = request.POST.get('handler_id')
        via = request.POST.get('via')
        handler = User.objects.get(id=handler_id)
        company = Company.objects.get(id=company_id)
        # Create a new Ticket record
        ticket = SalesTickets(
            # Populate the fields based on your form data
            # For example:
            handler=handler,
            contact=request.POST.get('contact'),
            status=request.POST.get('status'),
            issue_summary=issue,
            company=company,
            more=more,
            via=via,

        )
        ticket.save()

        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('description[]')
        qty_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')
        supplier_list = request.POST.getlist('supplier[]')
        currency_list = request.POST.getlist('currency[]')
        price_list_strings = request.POST.getlist('price[]')


        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i]):
                products = SalesTicketProducts(
                    part_no=part_no_list[i],
                    description=desc_list[i],
                    quantity=qty_list[i],
                    price=price_list_strings[i],
                    availability=availability_list[i],
                    supplier=supplier_list[i],
                    currency=currency_list[i],
                    ticket=ticket,
                )
                new_sourcing_data.append(products)

        # Delete old Tsourcing data
        SalesTicketProducts.objects.filter(ticket=ticket).delete()

        # Insert the new data
        SalesTicketProducts.objects.bulk_create(new_sourcing_data)



        table = (
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 3px solid #ddd;'>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Part No</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Description</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Quantity</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Price</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Availability</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Supplier</th>"
            "<th style='border: 3px solid #ddd; padding: 8px; text-align: left;'>Currency</th>"
            "</tr>"
        )

        for i in range(len(part_no_list)):
            if part_no_list[i] and desc_list[i]:
                row = (
                    "<tr>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{part_no_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{desc_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{qty_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{price_list_strings[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{availability_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{supplier_list[i]}</td>"
                    f"<td style='border: 3px solid #ddd; padding: 8px;'>{currency_list[i]}</td>"
                    "</tr>"
                )
                table += row

        table += "</table>"
        if ticket.status == "Sourcing":
            status = "Source"
        elif ticket.status == "Quote":
            status = "Quote"

        # Your existing code to create new_sourcing_data objects
        url = "http://146.190.61.23:8500/sales/edit/" + str(ticket.ticket_id) + "/"  # Replace with your actual URL
        clickable_url = f"<a href='{url}'>#" + str(ticket.ticket_id) + "</a>"
        # Use the 'table' string in the email message
        message = (
            f"Dear {handler},<br><br>"
            f"Our sales team has created a ticket, {clickable_url} on your behalf, with the following details and summary:<br><br>"
            f"Topic: <strong>GENERAL ENQUIRY</strong><br><br>"
            f"Subject: <strong>{ticket.status}</strong> : <strong>{ticket.company.name}</strong> : <strong>{ticket.issue_summary}</strong><br><br>"
            f"Kindly {status} for below:<br><br>{table}<br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )

        subject = f"{status} : {ticket.company.name} : {ticket.issue_summary} : #{ticket.ticket_id}"
        recipient_list = [handler.email, ticket.company]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()

        messages.success(request, 'Ticket Created Succesfully.')

        # Redirect to a success page or any other desired action
        return redirect('edit_sales_ticket', ticket.ticket_id)

    # If the request method is not POST, render the form for creating a ticket
    return render(request, 'sales/create_ticket.html', {'companies': companies, 'users': users})


@login_required
def view_invoice(request, invoice_id):
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    banks = OurBanks.objects.all()
    invoice = ProformaInvoice.objects.get(pfq_id=invoice_id)
    products = ProformaInvoiceProducts.objects.filter(pfi=invoice)

    if request.method == 'POST':
        handler_id = request.POST.get('invoice_handler')
        handler = User.objects.get(id=handler_id)
        bank_id = request.POST.get('bank')
        try:
            banks = OurBanks.objects.get(bank_id=bank_id)
        except OurBanks.DoesNotExist:
            banks = None

        invoice.bank = banks
        invoice.currency = request.POST.get('currency')
        invoice.status = request.POST.get('status')
        invoice.layout = request.POST.get('layout')
        invoice.vat_stats = request.POST.get('vat_stats')
        invoice.remark = request.POST.get('remark')
        invoice.notes = request.POST.get('notes')
        invoice.invoice_handler = handler  # Assuming you have a 'quote_handler' field as well:

        invoice.save()  # Save the changes to the database

        part_no_list = request.POST.getlist('part_no[]')
        desc_list = request.POST.getlist('description[]')
        qty_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')
        price_list = request.POST.getlist('price[]')

        # Create a list to hold the new sourcing objects
        new_sourcing_data = []

        for i in range(len(part_no_list)):
            if (part_no_list[i] and desc_list[i]):
                products = ProformaInvoiceProducts(
                    part_no=part_no_list[i],
                    description=desc_list[i],
                    quantity=qty_list[i],
                    price=price_list[i],
                    availability=availability_list[i],
                    pfi=invoice,
                )
                new_sourcing_data.append(products)

                # Delete old Invoice data
                ProformaInvoiceProducts.objects.filter(pfi=invoice).delete()

                # Insert the new data
                ProformaInvoiceProducts.objects.bulk_create(new_sourcing_data)

        messages.success(request, 'ProForma Succefully Edited.')
        return redirect('view_invoice', invoice_id)  # Redirect to the list of active quotes

    return render(request, 'sales/invoice_detail.html',
                  {'invoice': invoice, 'products': products, 'users': users, 'banks': banks})


@login_required
def delete_sales_ticket(request, ticket_id):
    try:
        ticket = SalesTickets.objects.get(ticket_id=ticket_id)
        ticket.is_active = 0  # Set is_active to 0 to mark it as deleted
        ticket.save()
    except SalesTickets.DoesNotExist:
        # Handle the case where the ticket does not exist
        pass
    messages.warning(request, 'Ticket Succefully Deleted.')
    return redirect('sales_tickets')


@login_required
def delete_sales_invoice(request, invoice_id):
    try:
        invoice = ProformaInvoice.objects.get(pfq_id=invoice_id)
        invoice.is_active = 0  # Set is_active to 0 to mark it as deleted
        invoice.save()
    except ProformaInvoice.DoesNotExist:
        # Handle the case where the ticket does not exist
        pass
    messages.warning(request, 'Invoice Succefully Deleted.')
    return redirect('active-invoice')


@login_required
def delete_sales_invoice_ticket(request, invoice_id, ticket_id):
    try:
        invoice = ProformaInvoice.objects.get(pfq_id=invoice_id)
        invoice.is_active = 0  # Set is_active to 0 to mark it as deleted
        invoice.save()
    except ProformaInvoice.DoesNotExist:
        # Handle the case where the ticket does not exist
        pass
    messages.warning(request, 'Invoice Succefully Deleted.')
    return redirect('edit_sales_ticket', ticket_id)


@login_required
def delete_order_ticket(request, order_id, ticket_id):
    order = get_object_or_404(Orders, o_id=order_id)
    order.is_active = False
    order.save()
    messages.warning(request, 'Order Succefully Deleted.')
    return redirect('edit_sales_ticket', ticket_id)


@login_required
def convert_to_invoice(request, ticket_id):
    ticket = get_object_or_404(SalesTickets, pk=ticket_id)
    sales_group = Group.objects.get(name='Sales')
    users = sales_group.user_set.all()
    if request.method == 'POST':
        handler_id = request.POST.get('handler')
        handler = User.objects.get(id=handler_id)
        # Create a new Invoice record
        invoice = ProformaInvoice(
            company=ticket.company,
            vat_stats=request.POST.get('vat_stats'),
            layout=request.POST.get('layout'),
            currency=request.POST.get('currency'),
            is_active=True,
            invoice_handler=handler,
            ticket=ticket,
        )
        invoice.save()

        # Create InvoiceProducts from the form data
        part_no_list = request.POST.getlist('part_no[]')
        description_list = request.POST.getlist('description[]')
        quantity_list = request.POST.getlist('quantity[]')
        availability_list = request.POST.getlist('availability[]')
        price_list = request.POST.getlist('price[]')

        for i in range(len(part_no_list)):
            order_product = ProformaInvoiceProducts(
                part_no=part_no_list[i],
                quantity=quantity_list[i],
                availability=availability_list[i],
                price=price_list[i],
                is_active=True,
                pfi=invoice,
                description=description_list[i],
            )
            order_product.save()

        messages.success(request, 'Ticket successfully converted to an invoice.')
        return redirect('view_invoice', invoice.pfq_id)  # Redirect to the list of active orders or the desired page

    return render(request, 'sales/convert_to_invoice.html', {'ticket': ticket, 'users': users})


@login_required
def delete_row(request, product_id, ticket_id):
    # Fetch the product from the database using the product_id

    product = SalesTicketProducts.objects.get(product_id=product_id)

    product.delete()
    messages.warning(request, 'Product Deleted Succesfully.')
    # Redirect back to the original page
    return redirect('edit_sales_ticket', ticket_id)


@login_required
def delete_row_quote(request, product_id, quote_id):
    # Fetch the product from the database using the product_id

    product = SalesQuoteProducts.objects.get(product_id=product_id)

    product.delete()
    messages.warning(request, 'Product Deleted Succesfully.')
    # Redirect back to the original page
    return redirect('edit-quote', quote_id)


@login_required
def delete_row_order(request, product_id, order_id):
    # Fetch the product from the database using the product_id

    product = OrderProducts.objects.get(op_id=product_id)

    product.delete()
    messages.warning(request, 'Product Deleted Succesfully.')
    # Redirect back to the original page
    return redirect('edit-order', order_id)


@login_required
def delete_row_invoice(request, product_id, invoice_id):
    # Fetch the product from the database using the product_id

    product = ProformaInvoiceProducts.objects.get(product_id=product_id)

    product.delete()
    messages.warning(request, 'Product Deleted Succesfully.')
    # Redirect back to the original page
    return redirect('view_invoice', invoice_id)


@login_required
def quote(request, quote_id):
    quote = get_object_or_404(SalesQuotes, sq_id=quote_id)

    items = SalesQuoteProducts.objects.filter(quote=quote)

    subtotals = Decimal(0)
    vat = Decimal(0)
    total_amount = Decimal(0)
    d_vat = Decimal(0)

    if quote.layout == "Grouped":
        for item in items:
            item.total = Decimal(item.price) * Decimal(item.quantity)  # Ensure price is a Decimal

            if quote.vat_stats == "Inclusive":
                item.price -= Decimal(round((Decimal(item.price) / Decimal(1.16)) * Decimal(0.16)))  # Deduct VAT from item.amount
                item.total -= Decimal(round((Decimal(item.total) / Decimal(1.16)) * Decimal(0.16)))
                subtotals += Decimal(item.total)
                vat = Decimal(round(subtotals * Decimal(0.16)))
                total_amount = Decimal(round(subtotals + vat))

            elif quote.vat_stats == "Exclusive":
                subtotals += Decimal(item.total)
                vat = Decimal(round(subtotals * Decimal(0.16)))
                total_amount = Decimal(subtotals + vat)

            elif quote.vat_stats == "Exempted":
                subtotals += Decimal(item.total)
                vat += Decimal(0)
                total_amount = Decimal(subtotals + vat)

    elif quote.layout == "Separated":
        for item in items:
            item.total = Decimal(item.price) * Decimal(item.quantity)  # Ensure price is a Decimal

            if quote.vat_stats == "Inclusive":
                item.price -= Decimal(round((Decimal(item.price) / Decimal(1.16)) * Decimal(0.16)))  # Deduct VAT from item.amount
                item.total -= Decimal(round((Decimal(item.total) / Decimal(1.16)) * Decimal(0.16)))
                item.subtotals = Decimal(item.total)
                item.vat = Decimal(round(item.total * Decimal(0.16)))
                item.total_amount = Decimal(round(item.total + item.vat))

            elif quote.vat_stats == "Exclusive":
                subtotals = Decimal(item.total)
                item.vat = Decimal(round(subtotals * Decimal(0.16)))
                item.total_amount = Decimal(round(item.total + item.vat))

            elif quote.vat_stats == "Exempted":
                subtotals = Decimal(item.total)
                item.vat = Decimal(0)
                item.total_amount = Decimal(round(item.total + item.vat))

    elif quote.layout == "Classified":
        for item in items:
            item.total = Decimal(item.price) * Decimal(item.quantity)  # Ensure price is a Decimal

            if quote.vat_stats == "Inclusive":
                item.price -= Decimal(round((Decimal(item.price) / Decimal(1.16)) * Decimal(0.16)))  # Deduct VAT from item.amount
                item.total -= Decimal(round((Decimal(item.total) / Decimal(1.16)) * Decimal(0.16)))
                item.subtotals = Decimal(item.total)
                item.vat = Decimal(round(item.total * Decimal(0.16)))
                item.total_amount = Decimal(round(item.total + item.vat))

            elif quote.vat_stats == "Exclusive":
                subtotals = Decimal(item.total)
                item.vat = Decimal(round(subtotals * Decimal(0.16)))
                item.total_amount = Decimal(round(item.total + item.vat))

            elif quote.vat_stats == "Exempted":
                subtotals = Decimal(item.total)
                item.vat = Decimal(0)
                item.total_amount = Decimal(round(item.total + item.vat))

    return render(request, 'sales/quote.html', {'quote': quote, 'items': items, 'subtotals': subtotals, 'vat': vat,
                                                'total_amount': total_amount})



@login_required
def invoice(request, invoice_id):
    invoice = get_object_or_404(ProformaInvoice, pfq_id=invoice_id)

    items = ProformaInvoiceProducts.objects.filter(pfi=invoice)

    subtotals = 0
    vat = 0

    for item in items:
        item.total = item.price * item.quantity

        if invoice.vat_stats == "Inclusive":
            item.price -= round((item.price / 1.16) * 0.16)  # Deduct VAT from item.amount
            item.total -= round((item.total / 1.16) * 0.16)
            subtotals += item.total
            vat = round(subtotals * 0.16)
            total_amount = round(subtotals + vat)


        elif invoice.vat_stats == "Exclusive":
            subtotals += item.total
            vat = round(subtotals * 0.16)
            total_amount = subtotals + vat

        else:
            subtotals += item.total
            vat = round(subtotals * 0.16)
            total_amount = subtotals + vat

    return render(request, 'sales/invoice.html',
                  {'invoice': invoice, 'items': items, 'subtotals': subtotals, 'vat': vat,
                   'total_amount': total_amount})


@login_required
def sales_dashboard(request):
    # Count tickets in 'Sourcing' status that are also 'is_active'
    sourcing_count = SalesTickets.objects.filter(status='Sourcing', is_active=1).count()
    # Count tickets in 'Quote' status that are also 'is_active'
    quote_count = SalesTickets.objects.filter(status='Quote', is_active=1).count()
    # Count tickets in 'Closed' status that are also 'is_active'
    closed_count = SalesTickets.objects.filter(status='Closed', is_active=1).count()

    open_count = sourcing_count + quote_count

    # Count quotes in 'Follow up' status that are also 'is_active'
    follow_up_count = SalesQuotes.objects.filter(status='Follow up', is_active=True).count()

    # Count quotes in 'Awaiting LPO' status that are also 'is_active'
    awaiting_lpo_count = SalesQuotes.objects.filter(status='Awaiting LPO', is_active=True).count()

    # Count quotes in 'On hold' status that are also 'is_active'
    on_hold_count = SalesQuotes.objects.filter(status='On hold', is_active=True).count()

    # Count quotes in 'Not interested' status that are also 'is_active'
    not_interested_count = SalesQuotes.objects.filter(status='Not interested', is_active=True).count()

    # Count quotes in 'Done' status that are also 'is_active'
    done_count = SalesQuotes.objects.filter(status='Done', is_active=True).count()

    # Count orders in 'Pending' status that are also 'is_active'
    pending_count = Orders.objects.filter(status='Pending', is_active=True).count()

    # Count orders in 'Awaiting LPO' status that are also 'is_active'
    order_awaiting_lpo_count = Orders.objects.filter(status='Awaiting LPO', is_active=True).count()

    # Count orders in 'Expected' status that are also 'is_active'
    expected_count = Orders.objects.filter(status='Expected', is_active=True).count()

    # Count orders in 'Ordered' status that are also 'is_active'
    ordered_count = Orders.objects.filter(status='Ordered', is_active=True).count()

    # Count orders in 'Completed' status that are also 'is_active'
    completed_count = Orders.objects.filter(status='Completed', is_active=True).count()

    # Count orders in 'Cancelled' status that are also 'is_active'
    cancelled_count = Orders.objects.filter(status='Cancelled', is_active=True).count()
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of tickets created each month this year
    monthly_ticket_counts = SalesTickets.objects.filter(
        created__year=current_year
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('ticket_id')
    ).order_by('month')

    return render(request, 'sales/sales_dashboard.html', {
        'sourcing_count': sourcing_count,
        'quote_count': quote_count,
        'closed_count': closed_count,
        'open_count': open_count,
        'follow_up_count': follow_up_count,
        'awaiting_lpo_count': awaiting_lpo_count,
        'on_hold_count': on_hold_count,
        'not_interested_count': not_interested_count,
        'done_count': done_count,
        'pending_count': pending_count,
        'order_awaiting_lpo_count': order_awaiting_lpo_count,
        'expected_count': expected_count,
        'ordered_count': ordered_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'monthly_ticket_counts': monthly_ticket_counts,

    })


@login_required
def tickets_created_this_year(request):
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of tickets created each month this year
    monthly_ticket_counts = SalesTickets.objects.filter(
        created__year=current_year, is_active=True
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('ticket_id')
    ).order_by('month')

    # Serialize the QuerySet to JSON
    data = list(monthly_ticket_counts)

    return JsonResponse(data, safe=False)


@login_required
def quotes_created_this_year(request):
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of quotes created each month this year
    monthly_quote_counts = SalesQuotes.objects.filter(
        created__year=current_year, is_active=True
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('sq_id')
    ).order_by('month')

    # Serialize the QuerySet to JSON
    data = list(monthly_quote_counts)

    return JsonResponse(data, safe=False)


@login_required
def orders_created_this_year(request):
    # Get the current year
    current_year = timezone.now().year

    # Query the database to get the count of orders created each month this year
    monthly_order_counts = Orders.objects.filter(
        created__year=current_year, is_active=True
    ).annotate(
        month=ExtractMonth('created')
    ).values(
        'month'
    ).annotate(
        count=Count('o_id')
    ).order_by('month')

    # Serialize the QuerySet to JSON
    data = list(monthly_order_counts)

    return JsonResponse(data, safe=False)


@login_required
def donut_chart_data(request):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Count the number of tickets with each status for the current month
    sourcing_count = SalesTickets.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Sourcing', is_active=True
    ).count()

    quote_count = SalesTickets.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Quote', is_active=True
    ).count()

    closed_count = SalesTickets.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Closed', is_active=True
    ).count()

    data = [sourcing_count, quote_count, closed_count]

    return JsonResponse(data, safe=False)


@login_required
def donut_chart_quotes_data(request):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Count the number of quotes with each status for the current month
    follow_up_count = SalesQuotes.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Follow up'
    ).count()

    awaiting_lpo_count = SalesQuotes.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Awaiting LPO'
    ).count()

    on_hold_count = SalesQuotes.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='On hold'
    ).count()

    not_interested_count = SalesQuotes.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Not interested'
    ).count()

    done_count = SalesQuotes.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Done'
    ).count()

    data = [follow_up_count, awaiting_lpo_count, on_hold_count, not_interested_count, done_count]

    return JsonResponse(data, safe=False)


@login_required
def donut_chart_orders_data(request):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Count the number of orders with each status for the current month
    pending_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Pending'
    ).count()

    awaiting_lpo_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Awaiting LPO'
    ).count()

    expected_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Expected'
    ).count()

    ordered_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Ordered'
    ).count()

    completed_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Completed'
    ).count()

    cancelled_count = Orders.objects.filter(
        created__month=current_month,
        created__year=current_year,
        status='Cancelled'
    ).count()

    data = [pending_count, awaiting_lpo_count, expected_count, ordered_count, completed_count, cancelled_count]

    return JsonResponse(data, safe=False)


@login_required
def orders_in_status(request, status):
    # Retrieve orders for the specified status and filter for active orders
    orders = Orders.objects.filter(status=status, is_active=True)
    return render(request, 'sales/orders.html', {'orders': orders, 'status': status, })
