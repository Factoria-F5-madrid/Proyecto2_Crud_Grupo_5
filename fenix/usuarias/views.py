from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuaria
from .forms import Usuaria
from rest_framework.response import Response
from rest_framework import status
from .serializers import DatosUsuariaSerializer

class UsuariaViewSet(viewsets.ViewSet):
    """
    Un ViewSet para ver y editar los datos de la única usuaria.
    """
    def list(self, request):
        usuaria = Usuaria.objects.first()
        if not usuaria:
            return Response({"detail": "No existe registro de datos de la usuaria."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DatosUsuariaSerializer(usuaria)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        usuaria = Usuaria.objects.first()
        if not usuaria:
            return Response({"detail": "No existe registro de datos de la usuaria."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DatosUsuariaSerializer(usuaria)
        return Response(serializer.data)

    def update(self, request, pk=None):
        usuaria = Usuaria.objects.first()
        if not usuaria:
            return Response({"detail": "No existe registro de datos de la usuaria."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DatosUsuariaSerializer(usuaria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
