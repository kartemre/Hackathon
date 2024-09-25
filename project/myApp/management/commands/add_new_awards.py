from django.core.management.base import BaseCommand
from myApp.models import Award, User, WaterUsage
import random

class Command(BaseCommand):
    help = 'Add new awards for the new month and update last month\'s awards with random winners'

    def handle(self, *args, **kwargs):
        # Eski ayın ödüllerini güncelle
        last_month_awards = Award.objects.filter(is_recent=True)
        for award in last_month_awards:
            award.is_recent = False
            if award.category == 'incentive':
                eligible_users = User.objects.filter(waterusage__water_used__lte=25).distinct()
            else:
                eligible_users = User.objects.all()

            if eligible_users.exists():
                random_user = random.choice(list(eligible_users))
                if random_user:  # Ensure the selected user is valid
                    award.winner = random_user
                    award.save()
            else:
                self.stdout.write(self.style.WARNING(f'No eligible users found for award {award.name}'))

        # Yeni ay ödüllerini ekle
        new_month = 7
        new_year = 2024
        awards = [
            {'name': 'kol 5', 'category': 'incentive', 'position': 1},
            {'name': 'Bilgisayar', 'category': 'incentive', 'position': 2},
            {'name': 'AirPods', 'category': 'incentive', 'position': 3},
            {'name': '5000 TL', 'category': 'general', 'position': 1},
            {'name': '4000 TL', 'category': 'general', 'position': 2},
            {'name': '300 TL', 'category': 'general', 'position': 3},
        ]

        for award_data in awards:
            Award.objects.create(
                name=award_data['name'],
                category=award_data['category'],
                position=award_data['position'],
                month=new_month,
                year=new_year,
                is_recent=True
            )

        self.stdout.write(self.style.SUCCESS('Successfully added new awards and updated last month\'s awards'))