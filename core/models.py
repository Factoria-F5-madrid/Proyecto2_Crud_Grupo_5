from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.postal_code})"
    
class VatRate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
    
class PaymentTerm(models.Model):
    name = models.CharField(max_length=50, unique=True)
    due_days = models.PositiveIntegerField(default=30)
    
    def __str__(self):
        return self.name