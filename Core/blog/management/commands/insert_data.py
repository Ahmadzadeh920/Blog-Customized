from django.core.management.base import BaseCommand
from faker import Faker

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        fake = Faker()
        print(fake.name())