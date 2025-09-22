from django.db import models

class User(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'year', 'month')
        ordering = ['user', 'year', 'month'] 

    def __str__(self):
        return f"{self.user.name} - {self.month} {self.year}: {self.amount}"