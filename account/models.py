from django.db import models
# from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from account.managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin,BaseModel):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(blank=True,null=True, upload_to="profile")

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=CustomUser)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token =str(uuid.uuid4())
            # CustomUser.objects.create(user = instance, email_token=email_token)
            instance.email_token = email_token
            instance.save()
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)