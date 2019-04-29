from rest_framework import routers

from app_api.api.views import CustomerProfileViewSet, RequestViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customer-profile', CustomerProfileViewSet, basename='customer-profile')
router.register(r'request', RequestViewSet, basename='request')

urlpatterns = router.urls
