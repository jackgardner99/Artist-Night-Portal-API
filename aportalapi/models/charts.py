from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_chart_file(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = '.' + file.name.rsplit('.', 1)[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only JPG, PNG, and PDF files are allowed.')


class Chart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_chart")
    chart_file = models.FileField(validators=[validate_chart_file], blank=True)