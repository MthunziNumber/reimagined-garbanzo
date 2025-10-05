print("Loaded uploader/urls.py!")
from django.urls import path
from .views import (
    DashboardView,
    GoogleLoginView,
    UploadFinancialDataView,
    GetFinancialDataView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/google-login/', GoogleLoginView.as_view(), name='google_login'),
    path('api/financial/upload/<int:user_id>/<int:year>/', UploadFinancialDataView.as_view(), name='upload-financial-data'),
    path('api/finances/<int:user_id>/<int:year>/', GetFinancialDataView.as_view(), name='get_financial_data'),
]
