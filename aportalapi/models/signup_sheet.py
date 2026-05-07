from django.db import models
from django.contrib.auth.models import User
from .charts import Chart

class SignupSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="signup")
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name="signup_chart")
    completed = models.BooleanField(default=False)