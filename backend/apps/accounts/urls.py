"""
URLs para o app accounts.

Endpoints para gerenciamento de usuários e perfis.
"""

from django.urls import path
from .views import UserProfileView, UserDetailView

app_name = "accounts"

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
]
