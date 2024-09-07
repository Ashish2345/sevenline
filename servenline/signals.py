from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LotteryResult
from .image_processing.process_image import ProcessImage
from django.core.files.base import ContentFile
from datetime import timedelta


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
        instance.save()
