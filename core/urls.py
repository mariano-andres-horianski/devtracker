from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_tenant_view, name='test_tenant'),
]