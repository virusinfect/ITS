import base64
from datetime import timedelta, datetime

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from service.models import Equipment
from technical.models import Signature, Delivery, CallCards, CSignature, FSignature, FormatApproval, UniqueToken, \
    Tickets

from .models import PartsCategory, Parts, Company, Clients, Task, Personal, Notification


def server_error(request):
    return render(request, '500.html', status=500)


def get_clients(request):
    company_id = request.GET.get('company_id')

    if company_id:
        clients = Clients.objects.filter(company_id=company_id)
        clients_data = [{'id': client.id, 'f_name': client.f_name} for client in clients]
        return JsonResponse({'clients': clients_data})

    return JsonResponse({'clients': []})


@login_required
def parts_categories_list(request):
    categories = PartsCategory.objects.all()
    return render(request, 'parts_category.html', {'categories': categories})


@login_required
def parts_list(request):
    parts = Parts.objects.select_related('category').all()
    return render(request, 'parts_list.html', {'parts': parts})


@csrf_exempt
def save_signature_view(request):
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        delivery_id = request.POST.get('delivery_id')

        # Extract the Base64 data after the comma
        base64_data = signature_data.split(',')[1]

        # Decode the Base64 data
        signature_binary = base64.b64decode(base64_data)

        # Create a Signature object and save it to the database
        signature = Signature()

        # Update the corresponding Delivery object with the signature
        try:
            delivery = Delivery.objects.get(pk=delivery_id)
            signature.delivery = delivery  # Associate the delivery with the signature
            signature.signature_image.save('signature.png', ContentFile(signature_binary), save=True)
            return JsonResponse({'success': True})
        except Delivery.DoesNotExist:
            return JsonResponse({'message': 'Delivery not found'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def save_signature_view_format(request):
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        format_id = request.POST.get('format_id')
        approved = request.POST.get('approved')


        # Extract the Base64 data after the comma
        base64_data = signature_data.split(',')[1]

        # Decode the Base64 data
        signature_binary = base64.b64decode(base64_data)

        # Create a Signature object and save it to the database
        signature = FSignature()

        # Update the corresponding Delivery object with the signature
        try:
            formatapp = FormatApproval.objects.get(pk=format_id)
            signature.format = formatapp
            signature.approved = approved  # Associate the delivery with the signature
            signature.signature_image.save('signature.png', ContentFile(signature_binary), save=True)
            return JsonResponse({'success': True})
        except FormatApproval.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Format Approval not found'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def save_signature_view_call(request):
    if request.method == 'POST':
        signature_data = request.POST.get('signature_data')
        cc_id = request.POST.get('cc_id')
        call_card = get_object_or_404(CallCards, pk=cc_id)
        status1 = call_card.status
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


        if signature_data:
            try:
                # Split the base64 data and get the second part
                base64_data = signature_data.split(',')[1]
            except IndexError:
                return JsonResponse({'success': False, 'message': 'Invalid signature data'})
        else:
            # Handle the case where there is no signature
            base64_data = ''

        # Extract the Base64 data after the comma
        #base64_data = signature_data.split(',')[1]

        # Decode the Base64 data
        signature_binary = base64.b64decode(base64_data)

        # Create a Signature object and save it to the database
        signature = CSignature()

        # Update the corresponding Delivery object with the signature
        try:
            signature.callcard = call_card  # Associate the delivery with the signature
            if signature_data:
                signature.signature_image.save('signature.png', ContentFile(signature_binary), save=True)

            if status1 == "Pending" and status2 == "Done":
                management_group = Group.objects.get(name='Helpdesk')

                # Get all users in the "management" group
                management_users = management_group.user_set.all()

                # Extract email addresses
                management_emails = [user.email for user in management_users]

                # Your existing code to create new_sourcing_data objects
                url = "http://146.190.61.23:8500/technical/edit_call_card/" + str(
                    call_card.cc_id) + "/"  # Replace with your actual URL
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
            return JsonResponse({'success': True})

        except CallCards.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Format Approval not found'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(Deliverys, delivery_id=delivery_id)
    return render(request, 'sign2.html', {'delivery': delivery})


def is_member_of_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@login_required
def test_view(request):
    if is_member_of_group(request.user, 'Sales'):
        return redirect('sales_dashboard')
    elif is_member_of_group(request.user, 'Helpdesk'):
        return redirect('helpdesk_dashboard')
    elif is_member_of_group(request.user, 'Technician'):
        return redirect('tech_dashboard')
    elif is_member_of_group(request.user, 'Store'):
        return redirect('store_dashboard')
    elif is_member_of_group(request.user, 'Accounts'):
        return redirect('acc_dashboard')
    else:
        return render(request, 'base.html')


@login_required
def pushjs(request):
    return render(request, 'pushjs.html')


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # You can add validation and error handling here if needed
        if name:
            PartsCategory.objects.create(name=name)
            messages.success(request, 'Category added successfully')
            return redirect('parts-categories-list')  # Redirect to the category list page

    return render(request, 'add_category.html')


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(PartsCategory, id=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        # You can add validation and error handling here if needed
        if name:
            category.name = name
            category.save()
            messages.success(request, 'Category edited successfully')
            return redirect('parts-categories-list')  # Redirect to the category list page

    return render(request, 'edit_category.html', {'category': category})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(PartsCategory, id=category_id)

    if request.method == 'POST':
        # Check if a POST request was made, indicating the user confirmed deletion.
        category.delete()
        messages.warning(request, 'Category deleted successfully')
        return redirect('parts-categories-list')  # Redirect to the category list page after deletion

    return render(request, 'delete_category.html', {'category': category})


@login_required
def add_part(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        code = request.POST.get('code')
        description = request.POST.get('description')
        is_active = 1
        # Assuming is_active, created, and updated are handled automatically.

        # Create the part
        Parts.objects.create(category_id=category_id, code=code, description=description, is_active=is_active)
        messages.success(request, 'Part Added successfully')
        return redirect('parts-list')  # Redirect to the parts list page

    categories = PartsCategory.objects.all()
    return render(request, 'add_part.html', {'categories': categories})


@login_required
def edit_part(request, part_id):
    part = Parts.objects.get(pk=part_id)

    if request.method == 'POST':
        part.category_id = request.POST.get('category')
        part.code = request.POST.get('code')
        part.description = request.POST.get('description')
        part.updated = timezone.now()

        # Assuming is_active is set automatically.
        # No need to update 'created' and 'updated'.

        part.save()
        messages.success(request, 'Part Edited successfully')
        return redirect('parts-list')  # Redirect to the parts list page

    categories = PartsCategory.objects.all()
    return render(request, 'edit_part.html', {'part': part, 'categories': categories})


@login_required
def delete_part(request, part_id):
    part = get_object_or_404(Parts, pk=part_id)

    if request.method == 'POST':
        part.delete()
        messages.warning(request, 'Part deleted successfully')
        return redirect('parts-list')  # Redirect to the parts list page

    return render(request, 'delete_part.html', {'part': part})


@login_required
def company_list(request):
    companies = Company.objects.all().order_by('name')
    return render(request, 'company_list.html', {'companies': companies})


@login_required
def create_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        other_telephone = request.POST.get('other_telephone')
        type = request.POST.get('type')
        description = request.POST.get('description')

        # Assuming is_active, created, and updated are handled automatically.

        Company.objects.create(
            name=name,
            address=address,
            email=email,
            telephone=telephone,
            other_telephone=other_telephone,
            type=type,
            description=description
        )
        messages.success(request, 'Company Created successfully')
        return redirect('company-list')  # Redirect to the company list page

    return render(request, 'create_company.html')

@login_required
def modal_create_company(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        other_telephone = request.POST.get('other_telephone')
        type = request.POST.get('type')
        description = request.POST.get('description')

        # Create a new company instance
        new_company = Company(
            name=name,
            address=address,
            email=email,
            telephone=telephone,
            other_telephone=other_telephone,
            type=type,
            description=description
        )

        # Save the new company
        new_company.save()

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success', 'message': 'Company created successfully'})

    # Handle non-POST requests (e.g., GET requests)
    return render(request, 'create_company.html')

@login_required
def edit_company(request, company_id):
    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        company.name = request.POST.get('name')
        company.address = request.POST.get('address')
        company.email = request.POST.get('email')
        company.telephone = request.POST.get('telephone')
        company.other_telephone = request.POST.get('other_telephone')
        company.type = request.POST.get('type')
        company.description = request.POST.get('description')

        # Assuming is_active, created, and updated are not editable.

        company.save()
        messages.success(request, 'Company Edited successfully')
        return redirect('company-list')  # Redirect to the company list page

    return render(request, 'edit_company.html', {'company': company})


@login_required
def delete_company(request, company_id):
    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        company.delete()
        messages.warning(request, 'Company deleted successfully')
        return redirect('company-list')  # Redirect to the company list page

    return render(request, 'delete_company.html', {'company': company})


@login_required
def client_list(request, company_id):
    clients = Clients.objects.filter(company_id=company_id)
    return render(request, 'client_list.html', {'clients': clients})


@login_required
def delete_client(request, client_id):
    client = Clients.objects.get(pk=client_id)
    company = client.company

    if request.method == 'POST':
        # If the form is submitted, delete the client
        client.delete()
        messages.warning(request, 'Client deleted successfully')
        return redirect('client-list',
                        company_id=company.id)

    return render(request, 'client_confirm_delete.html',
                  {'client': client, 'company': company})  # Redirect to a client list view or another appropriate URL


@login_required
def create_client(request, company_id):
    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        description = request.POST.get('description')

        # Create the client linked to the company
        client = Clients.objects.create(
            company=company,
            f_name=f_name,
            l_name=l_name,
            email=email,
            telephone=telephone,
            description=description
        )
        messages.success(request, 'Client Created successfully')
        return redirect('client-list', company_id=company_id)

    return render(request, 'create_client.html', {'company': company})


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    all_groups = Group.objects.all()

    if request.method == 'POST':
        # Update user's attributes
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        # Handle group changes
        user_groups = request.POST.getlist('user_groups')  # Get selected group IDs
        user.groups.set(user_groups)

        messages.success(request, 'User Edited successfully')
        return redirect('user_list')  # Redirect to the user list view

    return render(request, 'edit_user.html', {'user': user, 'all_groups': all_groups})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated.')
            return redirect('change_password')  # Redirect to the same page after successful change
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


@login_required
def create_user(request):
    if request.method == 'POST':
        # Process the combined form
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']

        # Create the user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Assign user to selected groups
        group_ids = request.POST.getlist('user_groups')
        user.groups.set(group_ids)

        messages.success(request, 'User Created successfully')
        return redirect('user_list')

    all_groups = Group.objects.all()
    return render(request, 'create_user.html', {'all_groups': all_groups})


@login_required
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        # Delete the user
        user.delete()
        return redirect('user_list')  # Redirect to the user list page after deletion

    return render(request, 'delete_user.html', {'user': user})


@login_required
def create_task(request):
    asignees = User.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)
        asignees_ids = request.POST.getlist('asignees')
        creator = request.user
        task = Task(title=title, description=description, status=status, user=user, created_by=creator)
        task.save()
        # Use the 'table' string in the email message
        message = (
            f"Dear {user},<br><br>"
            f"You have been allocated Task : {task.title} . Created By : {creator} . <br><br>"
            "This is an auto-generated email | © 2023 ITS. All rights reserved."
        )
        subject = f"Allocated Task : {task.title}"
        recipient_list = [user.email]
        from_email = 'its-noreply@intellitech.co.ke'

        # Create an EmailMessage instance for HTML content
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        email_message.content_subtype = 'html'  # Set content type to HTML
        email_message.send()
        # Add users to the cc_users many-to-many relationship
        for user_ids in asignees_ids:
            users = User.objects.get(id=user_ids)  # Replace with your actual user lookup logic
            task.cc_users.add(users)


            # Use the 'table' string in the email message
            message = (
                f"Dear {users},<br><br>"
                f"You have been added to  Task : {task.title} . Created By : {creator} . <br><br>"
                "This is an auto-generated email | © 2023 ITS. All rights reserved."
            )
            subject = f"Allocated Task : {task.title}"
            recipient_list = [users.email]
            from_email = 'its-noreply@intellitech.co.ke'

            # Create an EmailMessage instance for HTML content
            email_message = EmailMessage(subject, message, from_email, recipient_list)
            email_message.content_subtype = 'html'  # Set content type to HTML
            email_message.send()


        messages.success(request, 'Task Created successfully')
        return redirect('tasks')  # Redirect to a task list view or another appropriate URL

    return render(request, 'task_create.html', {'asignees': asignees})


@login_required
def Tasks(request):
    current_user = request.user  # Replace 'your_username' with the actual username
    specific_date = timezone.now().date()

    # Filter for pending tasks where you are either the 'cc_user' or 'user'
    pending_tasks = Task.objects.filter(
        Q(status='Pending', is_active=True, cc_users=current_user) |
        Q(status='Pending', is_active=True, user=current_user)|
        Q(status='Pending', is_active=True, created_by=current_user)
    ).annotate(
        comment_count=Count('comment'),
        cc_users_count=Count('cc_users')
    )

    # Filter for in-progress tasks where you are either the 'cc_user' or 'user'
    in_progress_tasks = Task.objects.filter(
        Q(status='In Progress', is_active=True, cc_users=current_user) |
        Q(status='In Progress', is_active=True, user=current_user)|
        Q(status='In Progress', is_active=True, created_by=current_user)
    ).annotate(
        comment_count=Count('comment'),
        cc_users_count=Count('cc_users')
    )

    # Filter for completed tasks where you are either the 'cc_user' or 'user'
    completed_tasks = Task.objects.filter(
        Q(status='Completed', is_active=True, cc_users=current_user) |
        Q(status='Completed', is_active=True, user=current_user)|
        Q(status='Completed', is_active=True, created_by=current_user),
        updated__date=specific_date  # Filter tasks updated on the specific date
    ).annotate(
        comment_count=Count('comment'),
        cc_users_count=Count('cc_users')
    )

    return render(request, 'tasks.html', {
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    })


@login_required
def view_task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    asignees = User.objects.all()
    if request.method == 'POST':
        user_ids = request.POST.get('assignee')
        task.user = User.objects.get(id=user_ids)
        task.status = request.POST.get('status')
        task.save()
        messages.success(request, 'Task Updated successfully')
        return redirect('tasks')

    return render(request, 'task_details.html', {'task': task,'asignees': asignees})



def form_with_uuid(request, token):
    try:
        # Retrieve the UniqueToken associated with the UUID
        unique_token = get_object_or_404(UniqueToken, token=token)

        # Retrieve the associated FormatApproval
        format_approval = unique_token.FormatApproval
        signature = FSignature.objects.filter(format=format_approval).last()
        # Render the form view with the FormatApproval
        return render(request, 'client_format_approval.html',
                      {'format_approval': format_approval, 'signature': signature})
    except UniqueToken.DoesNotExist:
        # Handle the case where the UniqueToken is not found
        return redirect('form_not_found')  # Replace with the name of your "not found" view


@login_required
def form_not_found(request):
    return render(request, 'form_not_found.html')


@login_required
def create_personal_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        from_date = request.POST.get("from_date")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")
        colour = request.POST.get("colour")

        # Get the current logged-in user
        user = request.user

        # Create a new Personal object
        add_personal_task = Personal(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            colour=colour,
            from_date=from_date,
            created_by=user
        )
        add_personal_task.save()
        messages.success(request, 'Personal Schedule Created successfully')
        return redirect('personal_task')  # Redirect to a view that lists personal tasks

    return render(request, 'create_personal_task.html')


@login_required
def edit_personal(request, personal_id):
    # Get the Personal object by its ID or return a 404 if not found
    personal = get_object_or_404(Personal, pk=personal_id)

    if request.method == 'POST':
        # Handle the form submission when the user submits the edited data
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        from_date = request.POST['from_date']
        colour = request.POST['colour']

        # Update the Personal object with the new data
        personal.title = title
        personal.description = description
        personal.due_date = due_date
        personal.from_date = from_date
        personal.colour = colour

        # Save the updated object
        personal.save()
        messages.success(request, 'Personal Schedule Edited successfully')
        # Redirect to a success page or the detail page of the edited object
        return redirect('personal_task')

    # Render the edit form if it's a GET request
    return render(request, 'edit_personal.html', {'personal': personal})


@login_required
def get_personal(request):
    events = Personal.objects.filter(created_by=request.user, is_active=True)

    data = []
    for event in events:
        event_to_date = event.due_date
        new_date = event_to_date + timedelta(days=1)
        data.append({

            'title': event.title,
            'start': event.from_date.isoformat(),
            'end': new_date.isoformat(),
            'color': event.colour,
        })

    return JsonResponse(data, safe=False)


@login_required
def personal_task(request):
    events = Personal.objects.filter(created_by=request.user, is_active=True).order_by('due_date')
    return render(request, 'personal_task.html', {'events': events})


@login_required
def delete_personal_task(request, task_id):
    # Get the task to be deleted, ensuring it exists and is associated with the current user
    task = get_object_or_404(Personal, pk=task_id, created_by=request.user)

    if request.method == "POST":
        # Delete the task
        task.delete()

        # Redirect to a view that lists personal tasks (replace with your task list view URL)
        return redirect('personal_task')

    return render(request, 'delete_personal_task.html', {'task': task})


def search(request):
    query = request.GET.get('query', '')

    # Search Tickets model
    ticket_results = Tickets.objects.filter(serial_no__icontains=query)

    # Search Equipment model
    equipment_results = Equipment.objects.filter(serial_no__icontains=query)

    return render(request, 'search_results.html', {
        'query': query,
        'ticket_results': ticket_results,
        'equipment_results': equipment_results,
    })


def equipment_lookup(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        query = request.GET.get('query', '')

        equipment_results = Equipment.objects.filter(serial_no__icontains=query)

        results = [{'name': equipment.name, 'serial_no': equipment.serial_no} for equipment in equipment_results]

        return JsonResponse({'results': results})

    return JsonResponse({})

class CompanyAutocompleteView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        companies = Company.objects.filter(name__icontains=query)
        company_names = [company.name for company in companies]
        return JsonResponse({'company_names': company_names})

@login_required
def daily_report(request):
    # Filter tasks with "pending" and "in-progress" status for the current day
    today = timezone.now().date()
    pending_tasks = Task.objects.filter(status='pending',user=request.user,is_active=True)
    InProgres = Task.objects.filter(status='in Progress', user=request.user,is_active=True)
    completed_tasks = Task.objects.filter(status='completed', updated__date=today,user=request.user,is_active=True)



    # Prepare data for the template
    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'InProgres':InProgres
    }

    management_group = Group.objects.get(name='Management')

    # Get all users in the "management" group
    management_users = management_group.user_set.all()

    # Extract email addresses
    management_emails = [user.email for user in management_users]

    InProgres_list = "\n".join(
        [f"<li>{Progres.title}: </li>" for Progres in InProgres])
    pending_tasks_list = "\n".join(
        [f"<li>{pending.title}: </li>" for pending in pending_tasks])
    completed_tasks_list = "\n".join(
        [f"<li>{completed.title}: </li>" for completed in completed_tasks])
    message = (
        f"Dear Sir/Madam,<br><br>"
        f"Here is my daily task report . <br><br>"
        f"Completed tasks . <br><br>"
        f"<ol>{completed_tasks_list}</ol><br>"
        f"In-Progress tasks . <br><br>"
        f"<ol>{InProgres_list}</ol><br>"
        f"Pending tasks . <br><br>"
        f"<ol>{pending_tasks_list}</ol><br>"
        "This is an auto-generated email | © 2023 ITS. All rights reserved."
    )
    subject = f"Daily report for {request.user} - {today} "
    recipient_list = management_emails
    from_email = 'its-noreply@intellitech.co.ke'

    # Create an EmailMessage instance for HTML content
    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.content_subtype = 'html'  # Set content type to HTML
    email_message.send()

    messages.success(request,'Daily report sent successfully')
    return redirect('tasks')