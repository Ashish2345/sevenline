import datetime

from django.db import models

# Create your models here.

def profile_directory_path(self, filename):
    time_stamp = datetime.datetime.now().strftime("%Y%M%d%H%M")
    return f'picture/{self.pk}/{time_stamp}/{"picture.jpg"}'


class AuditFields(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PictureUpload1(AuditFields):

    picture = models.FileField(upload_to="tip_picture1",  null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Picture Upload 1'

class PictureUpload2(AuditFields):

    picture = models.FileField(upload_to="tip_picture2",  null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Picture Upload 2'


class PictureUpload3(AuditFields):

    picture = models.FileField(upload_to="tip_picture3",  null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Picture Upload 3'


class XcrossPictureUpload(AuditFields):

    picture = models.FileField(upload_to="x_cross_pic",  null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'X Cross Image'


class VIPPictureUpload(AuditFields):

    picture = models.FileField(upload_to="vip_pic",  null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Vip Picture Image'

class LotteryResult(AuditFields):
    date = models.DateField()
    first_prize = models.CharField(max_length=200, null=True, blank=True)
    three_digit = models.CharField(max_length=200, null=True, blank=True)
    two_down = models.CharField(max_length=200, null=True, blank=True)
    next_drawn_date = models.DateField(null=True, blank=True)
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)


    class Meta:
        verbose_name_plural = 'LotteryResult'
        ordering = ["-date"]


    def get_two_up(self):
        len_first_prize = len(self.first_prize) - 2
        return self.first_prize[len_first_prize:]
    
    def get_three_up(self):
        len_first_prize = len(self.first_prize) - 3
        return self.first_prize[len_first_prize:]
