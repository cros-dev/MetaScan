"""URLs do app accounts (perfil e detalhe de usuário)."""

from django.urls import path
from .views import UserListView, UserProfileView, UserDetailView

app_name = "accounts"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
]
