# views.py
import re
from decimal import Decimal, ROUND_DOWN

import openpyxl
import pandas as pd
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .forms import PriceListForm
from .models import Brand, Exchange
from .models import LaptopPriceList
from .models import Supplier, Equipment


def upload_price_list(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    equipment = Equipment.objects.all()

    if request.method == 'POST':
        equipment_index = request.POST.get('equipment')
        excel_file = request.FILES['file']

        wb = openpyxl.load_workbook(excel_file, read_only=True)
        ws = wb.active

        # Assuming headers are in the first row
        headers = [cell.value for cell in ws[1]]

        # Check if 'product_name' and 'price' are present in the headers
        required_columns = ['part no', 'price']
        for column in required_columns:
            if column not in headers:
                raise ValueError(f"Column '{column}' not found in the Excel file.")

        supplier_index = request.POST.get('supplier')
        brand_index = request.POST.get('brand')

        # Assume headers is a list containing the column headers
        headers_lower = [header.lower() for header in headers]

        # Function to get index if header is present, otherwise None
        def get_index(header_name):
            return headers_lower.index(header_name) if header_name in headers_lower else None

        # Mapping headers to their indices
        index_mapping = {
            'product_name': get_index('part no'),
            'availability': get_index('availability'),
            'price': get_index('price'),
            'series': get_index('series'),
            'product_link': get_index('productlink'),
            'description': get_index('description'),
            'processor': get_index('processor'),
            'os': get_index('os'),
            'stock': get_index('stock'),
        }

        # Now you can access the indices using the keys
        product_name_index = index_mapping['product_name']
        price_index = index_mapping['price']
        series_index = index_mapping['series']
        product_link_index = index_mapping['product_link']
        description_index = index_mapping['description']
        processor_index = index_mapping['processor']
        os_index = index_mapping['os']
        stock_index = index_mapping['stock']
        availability_index = index_mapping['availability']

        for row in ws.iter_rows(min_row=2, values_only=True):
            # Create instances of Supplier, Brand, and Equipment if they don't exist
            supplier = Supplier.objects.get(id=supplier_index)
            brand = Brand.objects.get(id=brand_index)
            equipment = Equipment.objects.get(id=equipment_index)

            # Create an instance of PriceList
            price_list_obj = LaptopPriceList(
                product_name=row[product_name_index],
                price=row[price_index] if price_index is not None else '0',
                description=row[description_index] if description_index is not None else '',
                availability=row[availability_index] if availability_index is not None else '',
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
    query = request.GET.get('q', '').lower().strip()
    selected_fields = request.GET.getlist('fields', [])

    # Define the fields you want to allow searching
    allowed_fields = ['processor', 'brand__name', 'series', 'equipment__name', 'description']

    # Create a dictionary to map the field names to their corresponding lookup
    field_lookup = {
        'processor': 'icontains',
        'brand__name': 'icontains',
        'series': 'icontains',
        'equipment__name': 'icontains',
        'description': 'icontains',  # Use icontains for case-insensitive search
        # Add other fields as needed
    }
    equipment_id = request.GET.get('equipment')
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
    # Additional filter for the description field
    elif 'description' in selected_fields and query:
            # Split the query into keywords using both semicolons and spaces
            keywords = [kw.strip().lower() for kw in re.split(r'[;\s]+', query)]

            # Construct a list of Q objects for each keyword
            keyword_queries = [Q(description__icontains=keyword) for keyword in keywords]
            laptops = LaptopPriceList.objects.all()
            # Combine the Q objects using the | operator
            laptops = laptops.filter(*keyword_queries)
            if equipment_id:
                laptops = laptops.filter(equipment=equipment_id)

    else:
        # Query the model using the constructed Q objects
        laptops = LaptopPriceList.objects.filter(q_objects)
        if equipment_id:
            laptops = laptops.filter(equipment=equipment_id)



        # Filter by equipment if selected

        if equipment_id:
            laptops = laptops.filter(equipment=equipment_id)

    # Retrieve all equipment for the dropdown
    all_equipment = Equipment.objects.all()
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

    context = {'laptops': laptops, 'query': query, 'selected_fields': selected_fields, 'allowed_fields': allowed_fields,'all_equipment': all_equipment,}
    return render(request, 'prices/search_laptops.html', context)


def edit_exchange(request):
    exchange, created = Exchange.objects.get_or_create(pk=1)  # Adjust the condition based on your requirements

    if request.method == 'POST':
        rate = request.POST.get('rate')
        try:
            rate = Decimal(rate)
            exchange.rate = rate
            exchange.save()
        except ValueError:
            # Handle invalid input (non-numeric)
            pass


    return render(request, 'prices/edit_exchange.html', {'exchange': exchange})