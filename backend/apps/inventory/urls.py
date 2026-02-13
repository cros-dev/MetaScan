from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CavaleteHistoryViewSet, SlotHistoryViewSet

app_name = "inventory"

router = DefaultRouter()
router.register(
    r"history/cavaletes", CavaleteHistoryViewSet, basename="cavalete-history"
)
router.register(r"history/slots", SlotHistoryViewSet, basename="slot-history")

urlpatterns = [
    path("", include(router.urls)),
]
