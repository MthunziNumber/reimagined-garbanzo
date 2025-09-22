from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from finances.models import User, FinancialRecord

class RetrieveAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="Eve")
        FinancialRecord.objects.create(user=self.user, year=2025, month=1, amount=1000)
        FinancialRecord.objects.create(user=self.user, year=2025, month=2, amount=1500)

    def test_get_financial_data(self):
        url = reverse("get_financial_data", args=[self.user.id, 2025])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["month"], 1)
        self.assertEqual(data[0]["amount"], 1000.0)

    def test_get_no_records(self):
        new_user = User.objects.create(name="Frank")
        url = reverse("get_financial_data", args=[new_user.id, 2025])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
