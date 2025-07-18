from django.contrib import admin
from django.urls import path
from core.views import LoginView, MeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
]
