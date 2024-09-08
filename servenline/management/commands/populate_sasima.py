import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
import random
from servenline.models import VIPPictureUpload
from django.core.files.base import ContentFile

from servenline.image_processing.process_image import ProcessImage

def generate_unique_digit_number(num):
    digits = random.sample(range(1, 10), num) 
    return ''.join(map(str, digits))

class Command(BaseCommand):
    help = 'Upload lottery results from a JSON file'

    def handle(self, *args, **options):
        image_processor = ProcessImage(image_path='result.png')
        VIPPictureUpload.objects.all().delete()
        sasima_pic = VIPPictureUpload()
        random5_generate = generate_unique_digit_number(4)
        sasima_pic.drawn_number = random5_generate
        sasima_pic.date = "2024-09-14"

        sasima_image_io = image_processor.sasima_img_generate(
            date=str("2024-09-14"),
            random_generate=random5_generate
        )

        # Save the image to the model's ImageField
        sasima_pic.picture.save(f'sasima_pic.png', ContentFile(sasima_image_io.read()), save=False)

        sasima_pic.save()