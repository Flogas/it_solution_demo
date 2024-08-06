from django.db import models

class Logger(models.Model):
    log_text = models.CharField(max_length = 128)
    datetime = models.DateTimeField()
