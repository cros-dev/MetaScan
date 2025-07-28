from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    LoginView, MeView,
    CavaleteViewSet, SlotViewSet, SlotHistoryViewSet, CavaleteHistoryViewSet, ProductConsultView, TokenRefreshView, UserViewSet
)

router = DefaultRouter()
router.register(r'cavaletes', CavaleteViewSet, basename='cavalete')
router.register(r'slots', SlotViewSet, basename='slot')
router.register(r'slot-history', SlotHistoryViewSet, basename='slot-history')
router.register(r'cavalete-history', CavaleteHistoryViewSet, basename='cavalete-history')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('product/<str:code>/', ProductConsultView.as_view(), name='product-consult'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
