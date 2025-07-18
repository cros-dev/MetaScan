from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    LoginView, MeView,
    CavaleteViewSet, SlotViewSet, SlotHistoryViewSet, CavaleteHistoryViewSet, ProdutoConsultaView
)

router = DefaultRouter()
router.register(r'cavaletes', CavaleteViewSet, basename='cavalete')
router.register(r'slots', SlotViewSet, basename='slot')
router.register(r'slot-history', SlotHistoryViewSet, basename='slot-history')
router.register(r'cavalete-history', CavaleteHistoryViewSet, basename='cavalete-history')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('produto/<str:codigo>/', ProdutoConsultaView.as_view(), name='produto-consulta'),
    path('', include(router.urls)),
]
