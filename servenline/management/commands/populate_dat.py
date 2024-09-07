import json
import os
from django.core.management.base import BaseCommand
from servenline.models import LotteryResult
from django.conf import settings
from datetime import datetime


json_data = [
    {"date": "2024-06-22", "first_prize": "653707", "two_down": "90"},
    {"date": "2024-06-29", "first_prize": "246709", "two_down": "85"},
    {"date": "2024-07-06", "first_prize": "691854", "two_down": "74"},
    {"date": "2024-07-13", "first_prize": "546818", "two_down": "67"},
    {"date": "2024-07-20", "first_prize": "320471", "two_down": "26"},
    {"date": "2024-07-27", "first_prize": "981504", "two_down": "62"},
    {"date": "2024-08-03", "first_prize": "371285", "two_down": "74"},
    {"date": "2024-08-10", "first_prize": "410279", "two_down": "21"},
    {"date": "2024-08-17", "first_prize": "913748", "two_down": "48"},
    {"date": "2024-08-24", "first_prize": "359706", "two_down": "98"},
    {"date": "2024-08-31", "first_prize": "268117", "two_down": "78"},
    {"date": "2024-09-07", "first_prize": "734281", "two_down": "36", "three_digits":"530-291-459-690"}
]

class Command(BaseCommand):
    help = 'Upload lottery results from a JSON file'

    def handle(self, *args, **options):
        # Specify the path to the JSON file

        # Load the data from the JSON file

        # Iterate over each record and save it to the database
        for entry in json_data:
            try:
                # Parse the date string into a datetime object
                date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
                first_prize = entry.get('first_prize', '')
                two_down = entry.get('two_down', '')
                three_digits = entry.get('three_digits', '')

                # Create and save the LotteryResult record
                new_data = LotteryResult.objects.create(
                    date=date,
                    first_prize=first_prize,
                    two_down=two_down,
                    three_digit=three_digits
                )
                
                self.stdout.write(self.style.SUCCESS(f"Successfully uploaded record for {date}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error uploading record for {entry['date']}: {e}"))
