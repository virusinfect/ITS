from django.db import models

class Exchange(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

class LaptopPriceList(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    series = models.CharField(max_length=255,null=True)
    processor = models.CharField(max_length=255, null=True)
    os = models.CharField(max_length=255, null=True)
    stock = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255, null=True)
    ProductLink = models.CharField(max_length=255,null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_name = models.CharField(max_length=255)
    availability = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.product_name
    # Add other fields as needed
