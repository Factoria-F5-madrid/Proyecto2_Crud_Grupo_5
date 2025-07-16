from django.contrib import admin
from .models import Location, VatRate, PaymentTerm

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin view for Location model.
    """
    list_display = ('name', 'postal_code', 'province')
    search_fields = ('name', 'postal_code', 'province')
    ordering = ('name',)

@admin.register(VatRate)
class VatRateAdmin(admin.ModelAdmin):
    """
    Admin view for VatRate model.
    """
    list_display = ('name', 'percentage')
    ordering = ('percentage',)

@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    """
    Admin view for PaymentTerm model.
    """
    list_display = ('name', 'due_days')
    ordering = ('due_days',)