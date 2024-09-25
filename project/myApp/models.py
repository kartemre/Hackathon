from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    tc = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class WaterUsage(models.Model):
    barcode = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=255)
    water_used = models.FloatField()  # m^3 cinsinden
    amount_paid = models.FloatField()  # ödenilen ücret
    billing_month = models.IntegerField()  # 1-12 arası değer
    billing_year = models.IntegerField()
    is_recent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Fatura: {self.barcode}, Kullanıcı: {self.user.tc}'

    def save(self, *args, **kwargs):
        # Bu kullanıcının en ileri tarihli faturasını bul
        latest_fatura = WaterUsage.objects.filter(user=self.user).order_by('-billing_year', '-billing_month').first()
        
        # Eğer yeni fatura mevcut en ileri tarihli faturadan daha yeni bir tarihe sahipse
        if latest_fatura is None or (self.billing_year > latest_fatura.billing_year) or (self.billing_year == latest_fatura.billing_year and self.billing_month > latest_fatura.billing_month):
            # Diğer tüm faturaları güncel olmayan olarak işaretle
            WaterUsage.objects.filter(user=self.user, is_recent=True).update(is_recent=False)
            self.is_recent = True
        else:
            self.is_recent = False

        super(WaterUsage, self).save(*args, **kwargs)

class Award(models.Model):
    CATEGORY_CHOICES = [
        ('incentive', 'Incentive'),
        ('general', 'General'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    position = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    is_recent = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name} ({self.category}) - {self.year}/{self.month}'