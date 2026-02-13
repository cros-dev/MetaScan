from django.urls import path
from .views import ProductDetailView

app_name = "sankhya"

urlpatterns = [
    path("products/<str:code>/", ProductDetailView.as_view(), name="product-detail"),
]
