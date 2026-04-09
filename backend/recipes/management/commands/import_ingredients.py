import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт ингредиентов из data/ingredients.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default=os.path.join(
                settings.BASE_DIR,
                # '..', для локального тестирования
                'data',
                'ingredients.csv'
            ),
            help='Путь до файла ingredients.csv'
        )

    def handle(self, *args, **options):
        path = options['path']
        if not os.path.exists(path):
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {path}')
            )
            return

        with open(path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            ingredients = []
            for row in reader:
                try:
                    name, measurement_unit = row
                    ingredients.append(Ingredient(
                        name=name.strip(),
                        measurement_unit=measurement_unit.strip()
                    ))
                except ValueError:
                    self.stdout.write(
                        self.style.WARNING(f'Пропущена строка: {row}')
                    )

        Ingredient.objects.bulk_create(
            ingredients,
            ignore_conflicts=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Импортировано {len(ingredients)} ингредиентов'
            )
        )
