from rest_framework import serializers
from .models import User, FinancialRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'google_id']

class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['id', 'user', 'year', 'month', 'amount']

class FinancialRecordUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        import pandas as pd

        try:
            df = pd.read_excel(value)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid Excel file: {str(e)}")

        if not {'Month', 'Amount'}.issubset(df.columns):
            raise serializers.ValidationError("Excel file must contain 'Month' and 'Amount' columns")

        # Reset file pointer after reading
        value.seek(0)
        return value
