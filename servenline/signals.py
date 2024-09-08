from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LotteryResult, XcrossPictureUpload, VIPPictureUpload
from .image_processing.process_image import ProcessImage
from django.core.files.base import ContentFile
from datetime import timedelta
import random

def generate_unique_digit_number(num):
    digits = random.sample(range(1, 10), num) 
    return ''.join(map(str, digits))

@receiver(post_save, sender=LotteryResult)
def generate_result_image(sender, instance, created, **kwargs):
    if created and not instance.result_image:
        # Generate the image
        image_processor = ProcessImage(image_path='result.png')

        next_drawn_date = instance.date + timedelta(days=7)
        image_io = image_processor.result_generate(
            date=str(instance.date),
            first_prize=instance.first_prize,
            three_digits=instance.three_digit,
            two_down=instance.two_down,
            next_drawn_date=str(next_drawn_date)
        )

        # Save the image to the model's ImageField
        instance.result_image.save(f'result_{instance.id}.png', ContentFile(image_io.read()), save=False)
        instance.next_drawn_date = next_drawn_date
        instance.save()


        #Instance XCROSS IMAGE
        XcrossPictureUpload.objects.all().delete()

        x_cross = XcrossPictureUpload()
        random5_generate = generate_unique_digit_number(5)
        x_cross.drawn_number = random5_generate

        x_cross_image_io = image_processor.x_cross_img(
            date=str(next_drawn_date),
            random_generate=random5_generate
        )

        # Save the image to the model's ImageField
        x_cross.picture.save(f'x_cross_{instance.id}.png', ContentFile(x_cross_image_io.read()), save=False)

        x_cross.save()


        #Instance Sasima Image IMAGE
        VIPPictureUpload.objects.all().delete()
        sasima_pic = VIPPictureUpload()
        random5_generate = generate_unique_digit_number(4)
        sasima_pic.drawn_number = random5_generate
        sasima_pic.date = next_drawn_date

        sasima_image_io = image_processor.sasima_img_generate(
            date=str(next_drawn_date),
            random_generate=random5_generate
        )

        # Save the image to the model's ImageField
        sasima_pic.picture.save(f'sasima_pic_{instance.id}.png', ContentFile(sasima_image_io.read()), save=False)

        sasima_pic.save()




        
