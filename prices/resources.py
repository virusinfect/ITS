from import_export import resources
from .models import PriceList

class PriceListResource(resources.ModelResource):
    class Meta:
        model = PriceList
