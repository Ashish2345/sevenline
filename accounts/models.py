import datetime

from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator

from dateutil.relativedelta import relativedelta

from random import randint


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class AuditFields(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        else:
            super().delete()

        
def profile_directory_path(self, filename):
    time_stamp = datetime.datetime.now().strftime("%Y%M%d%H%M")
    return f'account/{self.pk}/{time_stamp}/{"profile_image.jpg"}'


class UserManager(BaseUserManager):
    def create_user(self, email,username,  is_active,is_verified_email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        if not is_active:
            raise ValueError("User must have an active status")
        if not first_name:
            raise ValueError("User must have an first name")
        if not last_name:
            raise ValueError("User must have an last name")

        user_obj = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_verified_email=is_verified_email,
            first_name=first_name,
            last_name=last_name)

        user_obj.set_password(password)
        user_obj.save(using=self._db)

        return user_obj

    def create_superuser(self, email,username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
            is_verified_email=True,
            first_name=first_name,
            last_name=last_name,
            password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    
    first_name = models.CharField(verbose_name='first name', max_length=20, null=True, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=30, null=True, blank=True)
    username = models.CharField(verbose_name='Username', max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_verified_email = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name_plural = 'Users'

    @property
    def get_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_avatar(self):
        url="https://ui-avatars.com/api/?background=0D8ABC&color=fff&name={0}+{1}&size=256&format=png".format(self.first_name,self.last_name)
        return url
    
    def __str__(self):
        return str(self.username)


class Profile(models.Model):

    
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True, related_name="user_profile")
    photo = models.FileField(upload_to=profile_directory_path, 
        validators=[FileExtensionValidator(allowed_extensions=settings.VALID_IMAGE_FORMAT)], null=True)
    contact_no = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=250, null=True,blank=True)
    is_verified_contact = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Profiles'



class Otp(AuditFields):
    email = models.EmailField()
    phone_number = models.CharField(("phone number"), max_length=50, null=True, blank=True)
    otp = models.CharField(max_length=150)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return self.email

    

    @property
    def is_otp_valid(self):
        self.attempts += 1
        self.save()
        if self.created_date + relativedelta(seconds=settings.OTP_VALID_TILL) > timezone.now() and self.attempts < 6:
            return True
        return False


class AuditTrail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    model_type = models.CharField('Model Type', max_length=255)
    object_id = models.IntegerField('Model Id')
    object_str = models.CharField('Model Str', max_length=255)
    action = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True)
    instance = models.TextField(null=True)
    previous_instance = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.model_type) 
