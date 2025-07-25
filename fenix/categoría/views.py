# categoría/views.py - API Only Implementation
# All views have been converted to API endpoints in views_api.py
# This file is maintained for potential future HTML views if needed

import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
import csv
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer

logger = logging.getLogger('categoria')

# This file now redirects to API views for consistency
# All CRUD operations are handled through the REST API endpoints
