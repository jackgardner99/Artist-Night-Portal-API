from django.db import models
from django.contrib.auth.models import User
from .charts import Chart
from .lyrics import Lyrics


class SignupSheet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="signup")
    chart = models.ForeignKey(Chart, on_delete=models.SET_NULL, related_name="signup_chart", null=True, blank=True)
    lyrics = models.ForeignKey(Lyrics, on_delete=models.SET_NULL, related_name="signup_lyrics", null=True, blank=True)
    completed = models.BooleanField(default=False)
