from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('test/', views.test_tenant_view, name='test_tenant'),
]