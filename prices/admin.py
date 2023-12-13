from django.contrib import admin
from .models import Brand,LaptopPriceList,ColoursoftPriceList,FellowesPricelist,PriceRule,Equipment
# Register your models here.
admin.site.register(Brand)
admin.site.register(LaptopPriceList)
admin.site.register(ColoursoftPriceList)
admin.site.register(FellowesPricelist)
admin.site.register(PriceRule)
admin.site.register(Equipment)
