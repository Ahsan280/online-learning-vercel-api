from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    email=models.EmailField(max_length=100, unique=True)
    username=models.CharField(max_length=100)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS =['username']
    
    def profile(self):
        return Profile.objects.get(user=self)


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    profile_picture=models.ImageField(upload_to="profile_pictures", null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)