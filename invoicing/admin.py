from django.contrib import admin
from .models import Invoice, InvoiceLine

class InvoiceLineInline(admin.TabularInline):
    """
    Permite editar las líneas de factura directamente desde la vista de la factura.
    """
    model = InvoiceLine
    extra = 0  # No mostrar líneas vacías por defecto, se añaden según se necesite
    
    # --- CAMPOS CORREGIDOS ---
    # Usamos los campos del modelo InvoiceLine: shipment, description, amount
    fields = ('shipment', 'description', 'amount')
    readonly_fields = ('description', 'amount') # Estos campos se deberían copiar del envío

    # Para evitar que se pueda añadir un envío ya facturado
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shipment":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_invoiced=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Invoice.
    """
    inlines = [InvoiceLineInline] # <-- Inline corregido

    # --- CAMPOS CORREGIDOS ---
    list_display = ('invoice_number', 'client', 'issue_date', 'due_date', 'total', 'is_paid', 'is_vat_exempt')
    list_filter = ('is_paid', 'is_vat_exempt', 'issue_date')
    search_fields = ('invoice_number', 'client__legal_name') # Buscar por el nombre legal del cliente
    readonly_fields = ('subtotal', 'vat_total', 'total') # Los totales se calculan, no se editan
    ordering = ('-issue_date',)
    
    # --- FIELDSETS CORREGIDOS ---
    fieldsets = (
        ('Información Principal', {
            'fields': ('invoice_number', 'client', 'issue_date', 'due_date')
        }),
        ('Estado y Notas', {
            'fields': ('is_paid', 'is_vat_exempt', 'notes')
        }),
        ('Importes Calculados', {
            'fields': ('subtotal', 'vat_total', 'total'),
            'classes': ('collapse',) # Ocultar por defecto
        }),
    )