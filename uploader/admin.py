from django.contrib import admin
from .models import User, FinancialRecord

admin.site.register(User)
admin.site.register(FinancialRecord)