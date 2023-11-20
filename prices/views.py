# views.py
from decimal import Decimal, ROUND_DOWN
from django.contrib import messages
import openpyxl
import pandas as pd
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import PriceListForm
from .models import Brand
from .models import LaptopPriceList
from .models import Supplier, Equipment
def upload_price_list(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    equipment = Equipment.objects.all()

    if request.method == 'POST':

        excel_file = request.FILES['file']

        wb = openpyxl.load_workbook(excel_file, read_only=True)
        ws = wb.active

        # Assuming headers are in the first row
        headers = [cell.value for cell in ws[1]]

        # Check if 'product_name' and 'price' are present in the headers
        required_columns = ['product_name', 'price']
        for column in required_columns:
            if column not in headers:
                raise ValueError(f"Column '{column}' not found in the Excel file.")

        # Retrieve the index of each column
        product_name_index = headers.index('product_name')
        price_index = headers.index('price')
        supplier_index = request.POST.get('supplier')
        series_index = headers.index('series') if 'series' in headers else None
        product_link_index = headers.index('productlink') if 'productlink' in headers else None
        equipment_index = request.POST.get('equipment')
        brand_index = request.POST.get('brand')
        description_index = headers.index('description') if 'description' in headers else None
        processor_index = headers.index('processor') if 'processor' in headers else None
        os_index = headers.index('os') if 'os' in headers else None
        stock_index = headers.index('stock') if 'stock' in headers else None
        currency_index = headers.index('stock') if 'stock' in headers else None

        for row in ws.iter_rows(min_row=2, values_only=True):
            # Create instances of Supplier, Brand, and Equipment if they don't exist
            supplier = Supplier.objects.get(id=supplier_index)
            brand = Brand.objects.get(id=brand_index)
            equipment = Equipment.objects.get(id=equipment_index)

            # Create an instance of PriceList
            price_list_obj = LaptopPriceList(
                product_name=row[product_name_index],
                price=row[price_index],
                description=row[description_index] if description_index is not None else '',
                processor=row[processor_index] if processor_index is not None else '',
                os=row[os_index] if os_index is not None else '',
                stock=row[stock_index] if stock_index is not None else '',
                currency=request.POST.get('currency'),
                supplier=supplier,
                series=row[series_index] if series_index is not None else '',
                ProductLink=row[product_link_index] if product_link_index is not None else '',
                equipment=equipment,
                brand=brand
            )

            price_list_obj.save()
        messages.success(request, 'Products Uploaded successfully')
        return redirect('search_laptops')  # Redirect to a success page

    return render(request, 'prices/upload_price_list.html',
                  {'suppliers': suppliers, 'brands': brands, 'equipment': equipment})


def dupload_price_list(request):
    if request.method == 'POST':
        form = PriceListForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['file']
                # Specify the engine based on the Excel file format
                engine = 'openpyxl' if excel_file.name.endswith('xlsx') else 'xlrd'
                df = pd.read_excel(excel_file, engine=engine)
                # Assuming your PriceList model has fields like 'product_name', 'price', 'currency'
                for index, row in df.iterrows():
                    LaptopPriceList.objects.create(
                        product_name=row['product_name'],
                        price=row['price'],
                        currency=row['currency']
                    )
                return redirect('view_price_list')  # Redirect to a success page
            except Exception as e:
                # Handle exceptions, log them, or display an error message
                print(f"An error occurred: {e}")
                # You might want to redirect to an error page or display an error message
    else:
        form = PriceListForm()
    return render(request, 'prices/upload_price_list.html', {'form': form})


def view_laptop_price_list(request):
    price_list_items = LaptopPriceList.objects.all()
    for item in price_list_items:
        for item in price_list_items:
            if 1 <= item.price <= 350:
                item.price_min = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
                item.price_max = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
            elif 351 <= item.price <= 500:
                item.price_min = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
                item.price_max = (item.price + item.price * Decimal('0.12')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
            elif 501 <= item.price <= 800:
                item.price_min = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
                item.price_max = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
            elif item.price > 800:
                item.price_min = (item.price + item.price * Decimal('0.06')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)
                item.price_max = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                      rounding=ROUND_DOWN)

    return render(request, 'prices/view_price_list.html', {'price_list_items': price_list_items})


def create_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Supplier.objects.create(name=name)
            return redirect('list-suppliers')  # Redirect to a list view or any other page
        else:
            return HttpResponse("Invalid data submitted for creating a supplier.")

    return render(request, 'prices/create_supplier.html')


def create_brand(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            return redirect('list_brands')  # Redirect to a list view or any other page
        else:
            return HttpResponse("Invalid data submitted for creating a supplier.")

    return render(request, 'prices/create_brand.html')


def create_equipment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        suppliers_ids = request.POST.getlist('suppliers')  # Assuming suppliers are selected through checkboxes

        if name:
            equipment = Equipment.objects.create(name=name)

            if suppliers_ids:
                equipment.suppliers.set(suppliers_ids)

            return redirect('list-equipment')  # Redirect to a list view or any other page
        else:
            return HttpResponse("Invalid data submitted for creating an equipment.")

    suppliers = Supplier.objects.all()
    return render(request, 'prices/create_equipment.html', {'suppliers': suppliers})


def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'prices/list_suppliers.html', {'suppliers': suppliers})


def list_equipment(request):
    equipment = Equipment.objects.all()
    return render(request, 'prices/list_equipment.html', {'equipment': equipment})


def list_brands(request):
    brands = Brand.objects.all()
    return render(request, 'prices/list_brands.html', {'brands': brands})


def search_laptops(request):
    query = request.GET.get('q', '')
    selected_fields = request.GET.getlist('fields', [])

    # Define the fields you want to allow searching
    allowed_fields = ['processor', 'brand__name', 'series', 'equipment__name']

    # Create a dictionary to map the field names to their corresponding lookup
    field_lookup = {
        'processor': 'icontains',
        'brand__name': 'icontains',
        'series': 'icontains',
        'equipment__name': 'icontains',
        # Add other fields as needed
    }

    # Build the Q objects for the selected fields
    q_objects = Q()
    for field in selected_fields:
        if field in allowed_fields:
            lookup = field_lookup[field]
            q_objects |= Q(**{f'{field}__{lookup}': query})

    # Check if both query and selected_fields are empty
    if not query and not selected_fields:
        # Return an empty queryset or default products if needed
        laptops = LaptopPriceList.objects.none()
    else:
        # Query the model using the constructed Q objects
        laptops = LaptopPriceList.objects.filter(q_objects)

    for item in laptops:
        if 1 <= item.price <= 350:
            item.price_min = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
            item.price_max = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
        elif 351 <= item.price <= 500:
            item.price_min = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
            item.price_max = (item.price + item.price * Decimal('0.12')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
        elif 501 <= item.price <= 800:
            item.price_min = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
            item.price_max = (item.price + item.price * Decimal('0.10')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
        elif item.price > 800:
            item.price_min = (item.price + item.price * Decimal('0.06')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)
            item.price_max = (item.price + item.price * Decimal('0.08')).quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_DOWN)

    context = {'laptops': laptops, 'query': query, 'selected_fields': selected_fields, 'allowed_fields': allowed_fields}
    return render(request, 'prices/search_laptops.html', context)
