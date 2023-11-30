import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Model
import datetime
from decimal import Decimal
from django.db.models.fields import DateField, DateTimeField

class Command(BaseCommand):
    help = 'Converts SQLite database to JSON for all models in the project'

    def handle(self, *args, **options):
        def convert_to_serializable(obj):
            if isinstance(obj, Model):
                # Exclude the _state attribute
                model_dict = obj.__dict__.copy()
                model_dict.pop('_state', None)
                return model_dict
            elif isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(obj, datetime.datetime) else obj.strftime(
                    '%Y-%m-%d')
            elif isinstance(obj, Decimal):
                return float(obj)  # Convert Decimal to float for serialization
            else:
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        # Get all models in the project
        all_models = apps.get_models()

        # Fetch all objects for each model
        data_list = []
        for model in all_models:
            model_name = model.__name__
            self.stdout.write(self.style.SUCCESS(f"Processing {model_name}..."))
            data_objects = model.objects.all()
            model_data = [obj for obj in data_objects]
            data_list.append({model_name: model_data})

        # Write the data to a JSON file
        output_file = 'cryptoApp/management/commands/database.json'  # Adjust the path as needed
        with open(output_file, 'w') as json_file:
            json.dump(data_list, json_file, default=convert_to_serializable, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Conversion completed. Check '{output_file}' for the JSON data."))
