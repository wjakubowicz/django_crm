from django.db import models

class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    purchase_date = models.DateField(blank=True, null=True)  # Allows blank and NULL
    product_name = models.CharField(max_length=100, blank=True)  # Allows blank
    serial_number = models.CharField(max_length=100, blank=True)  # Allows blank
    revision = models.CharField(max_length=100, blank=True)  # Allows blank

    customer_first_name = models.CharField(max_length=100, blank=True)  # Allows blank
    customer_last_name = models.CharField(max_length=100, blank=True)  # Allows blank

    address_street = models.CharField(max_length=100, blank=True)  # Allows blank
    address_building = models.CharField(max_length=100, blank=True)  # Allows blank
    address_apartment = models.CharField(max_length=100, blank=True)  # Allows blank
    address_city = models.CharField(max_length=100, blank=True)  # Allows blank
    address_postal_code = models.CharField(max_length=100, blank=True)  # Allows blank
    address_country = models.CharField(max_length=100, blank=True)  # Allows blank

    phone_number = models.CharField(max_length=100, blank=True)  # Allows blank
    email = models.EmailField(max_length=100, blank=True)  # Allows blank

    auction_name = models.CharField(max_length=100, blank=True)  # Allows blank

    additional_info = models.TextField(max_length=1000, blank=True)  # Allows blank

    gps_latitude = models.FloatField(null=True, blank=True)  # Allows NULL and blank
    gps_longitude = models.FloatField(null=True, blank=True)  # Allows NULL and blank

    def __str__(self):
        return self.customer_first_name + '   ' + self.customer_last_name
    