# load_provinces_and_districts.py within your Django app's management/commands directory
#python manage.py loaddata zimbabwe_provinces.json


from django.core.management.base import BaseCommand, CommandError
from smeapp.models import Province, District  # Replace 'yourapp' with your actual app name
import json

class Command(BaseCommand):
    help = 'Load provinces and districts from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        try:
            with open(options['json_file'], 'r', encoding='utf-8') as file:
                data = json.load(file)

            for entry in data:
                province, created = Province.objects.get_or_create(province_name=entry['province'])
                for district_name in entry['districts']:
                    District.objects.get_or_create(name=district_name, province=province)

            self.stdout.write(self.style.SUCCESS('Successfully loaded provinces and districts'))
        except FileNotFoundError:
            raise CommandError('JSON file not found')
        except Exception as e:
            raise CommandError(f'Error loading data: {e}')
