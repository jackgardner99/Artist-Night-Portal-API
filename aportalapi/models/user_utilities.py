from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserUtilities(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_utilities")
    spotify_link = models.URLField(blank=True)
    apple_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    user_image = models.FileField(blank=True)


@receiver(post_save, sender=User)
def create_user_utilities(_sender, instance, created, **kwargs):
    if created:
        UserUtilities.objects.create(user=instance)
