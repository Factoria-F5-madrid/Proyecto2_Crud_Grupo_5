from django.urls import path
from .views import PrendaListCreateView

urlpatterns = [
    path('prendas/', PrendaListCreateView.as_view(), name='prenda-list-create'),
]