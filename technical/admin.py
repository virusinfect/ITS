from django.contrib import admin
from .models import ServiceSchedules, Delivery,FormatApproval, Signature, Deliverys, Items, Tickets,Tsourcing ,ServiceTickets, CSignature,UniqueToken,FSignature,TechnicalReport
# Register your models here.

admin.site.register(ServiceSchedules)
admin.site.register(ServiceTickets)
admin.site.register(Delivery)
admin.site.register(Deliverys)
admin.site.register(Signature)
admin.site.register(CSignature)
admin.site.register(FSignature)
admin.site.register(Items)
admin.site.register(Tickets)
admin.site.register(Tsourcing)
admin.site.register(UniqueToken)
admin.site.register(FormatApproval)
admin.site.register(TechnicalReport)






