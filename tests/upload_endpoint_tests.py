from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from finances.models import User, FinancialRecord
import pandas as pd
import io

class UploadAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="Diana")

    def create_excel_file(self):
        df = pd.DataFrame({
            "Month": [1, 2, 3],
            "Amount": [1000, 1500, 2000]
        })
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        return excel_buffer

    def test_upload_valid_excel(self):
        url = reverse("upload_financial_data", args=[self.user.id, 2025])
        excel_file = self.create_excel_file()
        response = self.client.post(url, {"file": excel_file}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FinancialRecord.objects.count(), 3)

    def test_upload_no_file(self):
        url = reverse("upload_financial_data", args=[self.user.id, 2025])
        response = self.client.post(url, {}, format="multipart")
        self.assertEqual(response.status_code, 400)
