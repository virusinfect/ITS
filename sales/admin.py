from django.contrib import admin
from .models import SalesTickets,SalesTicketProducts,Orders,OrderProducts
# Register your models here.

admin.site.register(SalesTickets)
admin.site.register(SalesTicketProducts)
admin.site.register(Orders)
admin.site.register(OrderProducts)