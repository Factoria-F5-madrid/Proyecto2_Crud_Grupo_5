from django.db import models
from clients.models import Client

class Shipment(models.Model):
    shipment_code = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="shipments")
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    recipient_name = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=255)
    packages = models.PositiveIntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_invoiced = models.BooleanField(default=False)

    def __str__(self):
        return self.shipment_code