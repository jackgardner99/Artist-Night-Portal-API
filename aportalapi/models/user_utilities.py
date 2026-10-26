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
    marketing_opt_in = models.BooleanField(default=False)
    signup_count = models.PositiveIntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_utilities(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:
        UserUtilities.objects.create(user=instance)
