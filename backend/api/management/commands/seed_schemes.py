from django.core.management.base import BaseCommand
from api.db import init_mongo
from api.seed_data import seed_schemes_in_db

class Command(BaseCommand):
    help = 'Seeds authentic Indian Government schemes into MongoDB'

    def handle(self, *args, **options):
        init_mongo()
        self.stdout.write("Seeding Government Schemes into MongoDB...")
        count = seed_schemes_in_db()
        self.stdout.write(self.style.SUCCESS(f"Successfully processed seed data ({count} newly inserted or updated)."))
