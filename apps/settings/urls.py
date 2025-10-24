from rest_framework.routers import SimpleRouter
from .views import (
    ContactInfoViewSet
)

router = SimpleRouter(trailing_slash=False)
router.register(r'contact-info', ContactInfoViewSet, basename='settings')

urlpatterns = router.urls
