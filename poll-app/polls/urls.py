from rest_framework.routers import DefaultRouter
from .views import PollViewSet

router = DefaultRouter()
router.register(r'', PollViewSet, basename='poll')

urlpatterns = router.urls
