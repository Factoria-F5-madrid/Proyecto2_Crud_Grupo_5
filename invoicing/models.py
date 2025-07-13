from django.db import models
from django.utils import timezone
from clients.models import Client
from services.models import Service
import uuid

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('pending', 'Pendiente'),
        ('paid', 'Pagada'),
        ('cancelled', 'Cancelada'),
        ('overdue', 'Vencida'),
    )
    
    # Información básica de la factura
    client = models.ForeignKey(
        Client, 
        on_delete=models.PROTECT,
        related_name='invoices',
        verbose_name="Cliente"
    )
    invoice_number = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False,
        verbose_name="Número de Factura"
    )
    reference = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Referencia"
    )
    
    # Fechas relevantes
    issue_date = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de Emisión"
    )
    due_date = models.DateField(
        verbose_name="Fecha de Vencimiento"
    )
    
    # Información financiera
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Importe Total"
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Importe de IVA"
    )
    
    # Estado y notas
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name="Estado"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return f"Factura {self.invoice_number} - {self.client.name}"

    def save(self, *args, **kwargs):
        # Generar número de factura único si es nuevo
        if not self.invoice_number:
            year = timezone.now().year
            month = timezone.now().month
            unique_id = str(uuid.uuid4().hex)[:6].upper()
            self.invoice_number = f"F{year}{month:02d}-{unique_id}"
        
        # Si no se especifica fecha de vencimiento, establecer por defecto a 30 días
        if not self.due_date:
            self.due_date = timezone.now().date() + timezone.timedelta(days=30)
            
        super().save(*args, **kwargs)

    def calculate_total(self):
        """Recalcula el total de la factura basado en sus items."""
        items = self.items.all()
        total = sum(item.subtotal for item in items)
        tax = sum(item.tax_amount for item in items)
        
        self.total_amount = total
        self.tax_amount = tax
        self.save()
        
        return total


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, 
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Factura"
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.PROTECT,
        verbose_name="Servicio"
    )
    description = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Descripción"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio Unitario"
    )
    tax_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=21.00,
        verbose_name="Porcentaje de IVA"
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        editable=False,
        verbose_name="Subtotal"
    )

    class Meta:
        verbose_name = "Detalle de Factura"
        verbose_name_plural = "Detalles de Facturas"
        ordering = ['id']

    def __str__(self):
        return f"{self.service.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Si no hay descripción, usar el nombre del servicio
        if not self.description:
            self.description = self.service.name
            
        # Si no se especifica precio, usar el del servicio
        if not self.price:
            self.price = self.service.price
            
        # Si no se especifica porcentaje de IVA, usar el del servicio
        if not self.tax_percentage:
            self.tax_percentage = self.service.tax_percentage
            
        # Calcular subtotal
        self.subtotal = self.quantity * self.price
        
        super().save(*args, **kwargs)
        
        # Actualizar el total de la factura
        self.invoice.calculate_total()
        
    @property
    def tax_amount(self):
        """Calcula el importe de IVA para este item."""
        return self.subtotal * (self.tax_percentage / 100)