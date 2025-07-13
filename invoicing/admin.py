from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ('service', 'description', 'quantity', 'price', 'tax_percentage', 'subtotal')
    readonly_fields = ('subtotal',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'issue_date', 'due_date', 'total_amount', 'status')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'client__name', 'reference')
    readonly_fields = ('invoice_number', 'total_amount', 'tax_amount', 'created_at', 'updated_at')
    inlines = [InvoiceItemInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('client', 'invoice_number', 'reference', 'status')
        }),
        ('Fechas', {
            'fields': ('issue_date', 'due_date')
        }),
        ('Importes', {
            'fields': ('total_amount', 'tax_amount')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )