from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'cavaletes'

router = DefaultRouter()
router.register(r'cavaletes', views.CavaleteViewSet, basename='cavalete')

urlpatterns = [
    path('', include(router.urls)),
]
