from rest_framework.routers import DefaultRouter
from .views import PrendaViewSet

router = DefaultRouter()
router.register(r'prendas', PrendaViewSet, basename='prendas')
urlpatterns = router.urls