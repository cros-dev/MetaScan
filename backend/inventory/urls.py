from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inventory'

router = DefaultRouter()
router.register(r'slots', views.SlotViewSet, basename='slot')
router.register(r'slot-history', views.SlotHistoryViewSet, basename='slot-history')
router.register(r'cavalete-history', views.CavaleteHistoryViewSet, basename='cavalete-history')

urlpatterns = [
    path('', include(router.urls)),
]
