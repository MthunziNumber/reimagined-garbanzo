from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render, get_object_or_404
from .models import User, FinancialRecord
from .serializers import UserSerializer, FinancialRecordSerializer, FinancialRecordUploadSerializer

from google.oauth2 import id_token
from google.auth.transport import requests as grequests

import pandas as pd


class DashboardView(APIView):
    def get(self, request):
        return render(request, 'uploader/index.html')


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            idinfo = id_token.verify_oauth2_token(token, grequests.Request())
            google_user_id = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name', email)

            user, created = User.objects.get_or_create(
                google_id=google_user_id,
                defaults={'name': name, 'email': email}
            )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


class UploadFinancialDataView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, user_id, year):
        serializer = FinancialRecordUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_obj = serializer.validated_data['file']

        user = get_object_or_404(User, pk=user_id)

        # Read the Excel file
        df = pd.read_excel(file_obj)

        # Validate month and amount values
        invalid_months = df[~df['Month'].between(1, 12)]
        if not invalid_months.empty:
            return Response({"error": "Months must be between 1 and 12"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare FinancialRecord instances for bulk creation
        records = [
            FinancialRecord(
                user=user,
                year=year,
                month=int(row['Month']),
                amount=row['Amount']
            ) for _, row in df.iterrows()
        ]

        FinancialRecord.objects.bulk_create(records)

        return Response({"message": "Financial data uploaded successfully"}, status=status.HTTP_201_CREATED)


class GetFinancialDataView(APIView):
    def get(self, request, user_id, year):
        user = get_object_or_404(User, pk=user_id)
        records = FinancialRecord.objects.filter(user=user, year=year)
        serializer = FinancialRecordSerializer(records, many=True)
        return Response(serializer.data)
