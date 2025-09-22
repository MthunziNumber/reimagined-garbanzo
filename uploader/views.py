# views.py
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import User, FinancialRecord
import pandas as pd
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from django.shortcuts import render

def dashboard(request):
    return render(request, 'uploader/index.html')

@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({"error": "Token is required"}, status=400)
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request())
        google_user_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name', email)
        user, created = User.objects.get_or_create(
            google_id=google_user_id,
            defaults={'name': name, 'email': email}
        )
        return Response({
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        })
    except Exception:
        return Response({"error": "Invalid token"}, status=401)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_financial_data(request, user_id, year):
    file_obj = request.FILES['file']
    df = pd.read_excel(file_obj)  # assumes columns Month, Amount

    user = User.objects.get(pk=user_id)

    # iterate rows
    for _, row in df.iterrows():
        FinancialRecord.objects.create(
            user=user,
            year=year,
            month=int(row['Month']),
            amount=row['Amount']
        )

    return Response({"message": "Financial data uploaded successfully"})



# views.py (add this)
@api_view(['GET'])
def get_financial_data(request, user_id, year):
    records = FinancialRecord.objects.filter(user_id=user_id, year=year)
    data = [
        {
            "month": r.month,
            "amount": float(r.amount)
        }
        for r in records
    ]
    return Response(data)