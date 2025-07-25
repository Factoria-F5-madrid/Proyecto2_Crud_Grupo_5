from django.contrib import admin
from .models import Usuaria

@admin.register(Usuaria)
class UsuariaAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'full_name', 'email', 'role', 
        'status', 'is_active', 'hire_date', 'created_at'
    ]
    list_filter = ['role', 'status', 'is_active', 'hire_date', 'created_at']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-created_at']
    
    fieldsets = [
        ('Información Personal', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'avatar')
        }),
        ('Información Laboral', {
            'fields': ('role', 'status', 'hire_date', 'salary', 'address')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Nombre Completo'
