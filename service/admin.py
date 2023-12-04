from django.contrib import admin
from .models import Service,Equipment,Software,EquipmentSpecs,MonitorChecklist,PrinterChecklist,UpsChecklist,LaptopChecklist,ServerChecklist,CpuChecklist
# Register your models here.
admin.site.register(Service)
admin.site.register(Equipment)
admin.site.register(Software)
admin.site.register(EquipmentSpecs)
admin.site.register(MonitorChecklist)
admin.site.register(PrinterChecklist)
admin.site.register(UpsChecklist)
admin.site.register(LaptopChecklist)
admin.site.register(ServerChecklist)
admin.site.register(CpuChecklist)
