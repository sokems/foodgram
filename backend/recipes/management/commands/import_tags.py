import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Load Tags from CSV file'

    def handle(self, *args, **kwargs):
        counter = 0
        csv_path = os.path.join(
            settings.BASE_DIR, 'data', 'tags.csv'
        )

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) >= 2:
                    name, slug = row[0], row[1]
                    Tag.objects.get_or_create(
                        name=name, slug=slug
                    )
                    counter += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Add «{name}»')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {counter} tags')
        )
