from django.db import models
from django.core.exceptions import ValidationError
from .charts import Chart


def validate_lyrics_file(file):
    valid_extensions = ['.txt', '.pdf', '.docx']
    ext = '.' + file.name.rsplit('.', 1)[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only TXT, PDF, and DOCX files are allowed.')


class Lyrics(models.Model):
    chart = models.OneToOneField(Chart, on_delete=models.CASCADE, related_name='lyrics')
    lyrics_file = models.FileField(validators=[validate_lyrics_file])
