from django.db import models

from django.db import models

class WordBank(models.Model):
    word = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)