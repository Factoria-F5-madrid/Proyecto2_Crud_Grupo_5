from django.urls import path
from .views import (
    DashboardSummaryView,
    MonthlySalesView,
    TopClientsView,
    TopServicesView
)

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('monthly-sales/', MonthlySalesView.as_view(), name='monthly-sales'),
    path('top-clients/', TopClientsView.as_view(), name='top-clients'),
    path('top-services/', TopServicesView.as_view(), name='top-services'),
]