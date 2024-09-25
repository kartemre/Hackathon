import os
import django
import random
import string
from django.contrib.auth.hashers import make_password

# Django ortamını ayarlayın
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mert.settings')
django.setup()

from myApp.models import User, WaterUsage

# Kullanıcı verilerini ekleyin
users = [
    {"first_name": "Ali", "last_name": "Veli", "tc": "12345678901", "email": "ali@example.com", "password": make_password("password"), "phone": "05551234567"},
    {"first_name": "Ayşe", "last_name": "Fatma", "tc": "12345678902", "email": "ayse@example.com", "password": make_password("password"), "phone": "05551234568"},
    # Daha fazla kullanıcı ekleyin
]

for user_data in users:
    user, created = User.objects.get_or_create(tc=user_data['tc'], defaults=user_data)
    if created:
        print(f"Kullanıcı eklendi: {user}")

# Fatura verilerini ekleyin
def generate_water_usage_data(num_entries):
    data = []
    for _ in range(num_entries):
        user = random.choice(users)
        barcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        address = f"{random.randint(1, 100)}. Sokak, {random.choice(['İstanbul', 'Ankara', 'İzmir'])}"
        water_used = round(random.uniform(1, 100), 2)
        amount_paid = round(water_used * random.uniform(0.5, 2), 2)
        billing_month = random.randint(1, 12)
        billing_year = random.randint(2020, 2023)
        is_recent = False
        data.append({
            "barcode": barcode,
            "address": address,
            "water_used": water_used,
            "amount_paid": amount_paid,
            "billing_month": billing_month,
            "billing_year": billing_year,
            "is_recent": is_recent,
            "user_tc": user["tc"]
        })
    return data

water_usage_data = generate_water_usage_data(100)

for data in water_usage_data:
    user = User.objects.get(tc=data['user_tc'])
    water_usage = WaterUsage(
        barcode=data['barcode'],
        address=data['address'],
        water_used=data['water_used'],
        amount_paid=data['amount_paid'],
        billing_month=data['billing_month'],
        billing_year=data['billing_year'],
        is_recent=data['is_recent'],
        user=user
    )
    water_usage.save()
    print(f"Fatura eklendi: {water_usage}")

print("Tüm veriler başarıyla eklendi!")