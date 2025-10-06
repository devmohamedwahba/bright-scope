from rest_framework.routers import SimpleRouter
from .views import FeatureViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'features', FeatureViewSet, basename='feature')

urlpatterns = router.urls
