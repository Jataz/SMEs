# load_provinces_and_districts.py within your Django app's management/commands directory
#python manage.py loaddata django_fixture.json

from django.core.management.base import BaseCommand, CommandError
from smeapp.models import Province, District, Ward
import json

class Command(BaseCommand):
    help = 'Load provinces, districts, and wards from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for entry in data:
                province_name = entry['province']
                districts_data = entry['districts']

                # Get or create the province
                province, created = Province.objects.get_or_create(province_name=province_name)

                for district_data in districts_data:
                    district_name = district_data['district']
                    wards = district_data['wards']

                    # Get or create the district
                    district, created = District.objects.get_or_create(district_name=district_name, province=province)

                    for ward_name in wards:
                        # Get or create the ward
                        Ward.objects.get_or_create(ward_name=ward_name, district=district)

            self.stdout.write(self.style.SUCCESS('Successfully loaded provinces, districts, and wards'))

        except FileNotFoundError:
            raise CommandError(f'JSON file "{json_file}" not found')
        except json.JSONDecodeError:
            raise CommandError(f'Error decoding JSON from file "{json_file}"')
        except Exception as e:
            raise CommandError(f'Error loading data: {e}')


