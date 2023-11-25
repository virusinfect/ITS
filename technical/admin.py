from django.contrib import admin
from .models import ServiceSchedules,InhouseTsourcing,InhouseTickets, Delivery,FormatApproval,TechSignature, Signature, Deliverys, Items, Tickets,Tsourcing,tQuote ,ServiceTickets, CSignature,UniqueToken,FSignature,TechnicalReport,TSignature,TicketImage,Requisition
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
admin.site.register(TSignature)
admin.site.register(TicketImage)
admin.site.register(tQuote)
admin.site.register(TechSignature)
admin.site.register(InhouseTickets)
admin.site.register(Requisition)
admin.site.register(InhouseTsourcing)






