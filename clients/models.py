from django.db import models
from core.models import Location, VatRate, PaymentTerm

class Client(models.Model):
    client_code = models.CharField(max_length=20, unique=True)
    legal_name = models.CharField(max_length=150)
    tax_id = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    vat_rate = models.ForeignKey(VatRate, on_delete=models.PROTECT)
    payment_term = models.ForeignKey(PaymentTerm, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.legal_name