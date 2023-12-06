from decimal import Decimal, ROUND_DOWN

from django.db import models


class Exchange(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.rate


class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    # Add other fields as needed


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    # Add other fields as needed


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    suppliers = models.ManyToManyField(Supplier)

    def __str__(self):
        return self.name
    # Add other fields as needed

class Type(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class LaptopPriceList(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    series = models.CharField(max_length=255, null=True)
    processor = models.CharField(max_length=255, null=True)
    os = models.CharField(max_length=255, null=True)
    stock = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255, null=True)
    ProductLink = models.CharField(max_length=255, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_name = models.CharField(max_length=100)
    availability = models.CharField(max_length=255, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    data = models.IntegerField(null=True)

    def __str__(self):
        return self.product_name





class ColoursoftPriceList(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, unique=True)
    hp_code = models.CharField(max_length=255, null=True)
    yield_no = models.CharField(max_length=255, null=True)
    cost = models.CharField(max_length=255, null=True)
    level_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    level_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    brand = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    level_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    end_user = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # Check if there is an existing entry with the same code
        existing_entry = ColoursoftPriceList.objects.filter(code=self.code).first()

        # If there is an existing entry, delete it before saving the new one
        if existing_entry:
            existing_entry.delete()

        # Save the new entry
        super().save(*args, **kwargs)


class FellowesPricelist(models.Model):
    code = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(null=True)
    specification = models.TextField(null=True)
    stock = models.CharField(max_length=255, null=True)
    discount = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.code

class PriceRule(models.Model):
    product_type = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    price_range_start = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage2 = models.DecimalField(max_digits=10, decimal_places=2)
    constant = models.BooleanField(default=False)

    def apply_discount(self, price):
        if self.constant is True:
            return price + self.discount_percentage
        else:
            return (price + price * Decimal(self.discount_percentage)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    def apply_discount2(self, price):
        if self.constant  is True:
            return price + self.discount_percentage2
        else:
            return (price + price * Decimal(self.discount_percentage2)).quantize(Decimal('0.00'),rounding=ROUND_DOWN)
    def __str__(self):
        return f"{self.product_type} - {self.price_range_start} to {self.price_range_end}"

