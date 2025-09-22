from django.urls import path
from . import views

urlpatterns = [
    path('api/financial/upload/<int:user_id>/<int:year>/', views.upload_financial_data),
    path('api/finances/<int:user_id>/<int:year>/', views.get_financial_data),
    path('api/google-login/', views.google_login),
    path('', views.dashboard, name='dashboard'),
]
