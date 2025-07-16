from django.db import models
from django.db.models import Sum, F
from decimal import Decimal
from clients.models import Client
from logistics.models import Shipment

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="invoices")
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    
    # --- CAMPOS AÑADIDOS PARA LA EXENCIÓN ---
    is_vat_exempt = models.BooleanField(default=False, verbose_name="Exenta de IVA")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas Legales")

    def __str__(self):
        return self.invoice_number

    def calculate_totals(self):
        """Calcula el subtotal a partir de sus líneas y luego los totales."""
        # Calcula el subtotal sumando los importes de todas sus líneas
        aggregation = self.lines.aggregate(subtotal=Sum('amount'))
        self.subtotal = aggregation['subtotal'] or Decimal('0.00')

        if self.is_vat_exempt:
            self.vat_total = Decimal('0.00')
        else:
            # Obtiene el porcentaje de IVA del cliente asociado
            vat_percentage = self.client.vat_rate.percentage
            self.vat_total = self.subtotal * (vat_percentage / Decimal('100.00'))
        
        self.total = self.subtotal + self.vat_total

    def save(self, *args, **kwargs):
        # (Opcional pero recomendado) Llama al cálculo antes de guardar
        self.calculate_totals() 
        super().save(*args, **kwargs)

class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    shipment = models.OneToOneField(Shipment, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Line for {self.shipment.shipment_code} on Invoice {self.invoice.invoice_number}"