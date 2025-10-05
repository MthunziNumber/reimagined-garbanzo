# import requests

# url = "http://127.0.0.1:8000/api/financial/upload/1/2024/"
# files = {'file': open('C:\\Users\\SiphiwoMogoere\\Desktop\\2024.xlsx', 'rb')}
# response = requests.post(url, files=files)
# print(response.status_code, response.text)

import pandas as pd
from uploader.models import User, FinancialRecord

df = pd.read_excel('/Users/SiphiwoMogoere/Desktop/2024.xlsx')
user = User.objects.create(name="Test User", email="test@example.com", google_id="dummy-google-id")

for _, row in df.iterrows():
    if 1 <= int(row['Month']) <= 12:
        FinancialRecord.objects.create(
            user=user,
            year=2024,
            month=int(row['Month']),
            amount=row['Amount']
        )