from django.db import models
from django.contrib.auth.models import User
from .charts import Chart

class UserUtilities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    spotify_link = models.URLField()
    apple_link = models.URLField()
    youtube_link = models.URLField()
    user_image = models.ImageField()