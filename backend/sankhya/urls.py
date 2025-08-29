from django.urls import path
from . import views

app_name = 'sankhya'

urlpatterns = [
    path('product/<str:code>/', views.ProductConsultView.as_view(), name='product-consult'),
]
