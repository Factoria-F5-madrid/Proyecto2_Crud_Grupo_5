from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'old_password': ['Contraseña incorrecta.']}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {'message': 'Contraseña actualizada correctamente.'}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListShippingView(APIView):
     permission_classes = [IsAuthenticated]
     
def get(self, request):
        return Response(
            {"message": "Aquí se mostrarían los envíos solo si estás autenticado.", "user": request.user.username})
def post(self, request):
        return Response(
            {"message": "Aquí se crearían envíos solo si estás autenticado.", "data_recibida": request.data})
        
class ShippingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response(
            {"message": f"Detalles del envío {pk} solo si estás autenticado.", "user": request.user.username})

    def put(self, request, pk):
        return Response(
            {"message": f"Envío {pk} actualizado solo si estás autenticado.", "data_recibida": request.data})

    def delete(self, request, pk):
        return Response(
            {"message": f"Envío {pk} eliminado solo si estás autenticado."})
        
        
class ProtectedTestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] # O [AllowAny] si quieres que sea accesible sin token para probar

    def get(self, request):
        return Response({"message": "Acceso concedido a tu recurso protegido real!"})