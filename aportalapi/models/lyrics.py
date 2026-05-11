from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_lyrics_file(file):
    valid_extensions = ['.txt', '.pdf', '.docx']
    ext = '.' + file.name.rsplit('.', 1)[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only TXT, PDF, and DOCX files are allowed.')


class Lyrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lyrics')
    lyrics_file = models.FileField(validators=[validate_lyrics_file], blank=True)
