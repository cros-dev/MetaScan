from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CavaleteViewSet, SlotViewSet

app_name = "cavaletes"

router = DefaultRouter()
router.register(r"cavaletes", CavaleteViewSet, basename="cavalete")
router.register(r"slots", SlotViewSet, basename="slot")

urlpatterns = [
    path("", include(router.urls)),
]
