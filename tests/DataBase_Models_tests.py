from django.test import TestCase
from finances.models import User, FinancialRecord

class ModelsTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create(name="Alice")
        self.assertEqual(user.name, "Alice")

    def test_create_financial_record(self):
        user = User.objects.create(name="Bob")
        record = FinancialRecord.objects.create(
            user=user, year=2025, month=1, amount=1000.00
        )
        self.assertEqual(record.user.name, "Bob")
        self.assertEqual(record.year, 2025)
        self.assertEqual(record.month, 1)
        self.assertEqual(float(record.amount), 1000.00)

    def test_unique_record_per_month(self):
        user = User.objects.create(name="Charlie")
        FinancialRecord.objects.create(user=user, year=2025, month=1, amount=500)
        with self.assertRaises(Exception):  # IntegrityError if unique_together is set
            FinancialRecord.objects.create(user=user, year=2025, month=1, amount=800)
