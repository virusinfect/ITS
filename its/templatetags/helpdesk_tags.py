# myapp/templatetags/helpdesk_tags.py
from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def can_access_view_bank(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_bank')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def can_access_view_deliveries(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_deliveries')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def can_access_view_users(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_users')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_companies(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_companies')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_parts(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_parts')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_invoice(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_invoice')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_helpdesk_dashboard(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_helpdesk_dashboard')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_sales_dashboard(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_sales_dashboard')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_tech_tickets(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_tech_tickets')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_sales_tickets(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_sales_tickets')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_service(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_service')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_quotes(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_quotes')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_orders(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_orders')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@register.filter
def can_access_view_invoice(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_invoice')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def can_access_store_dashboard(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_store_dashboard')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def can_access_view_invoice(user):
    try:
        helpdesk_group = Group.objects.get(name='R_view_invoice')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def is_sales(user):
    try:
        helpdesk_group = Group.objects.get(name='Sales')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False
@register.filter
def is_tech(user):
    try:
        helpdesk_group = Group.objects.get(name='Technician')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def is_helpdesk(user):
    try:
        helpdesk_group = Group.objects.get(name='Helpdesk')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def is_management(user):
    try:
        helpdesk_group = Group.objects.get(name='Management')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def is_store(user):
    try:
        helpdesk_group = Group.objects.get(name='Store')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False

@register.filter
def is_accounts(user):
    try:
        helpdesk_group = Group.objects.get(name='Accounts')
        return helpdesk_group in user.groups.all()
    except Group.DoesNotExist:
        return False
