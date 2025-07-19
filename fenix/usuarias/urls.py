from rest_framework.routers import DefaultRouter
from .views import UsuariaViewSet

router = DefaultRouter()
router.register(r'usuarias', UsuariaViewSet, basename='usuarias')

urlpatterns = router.urls