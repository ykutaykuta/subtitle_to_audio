from django.db import models

# Create your models here.

class TTSAudio(models.Model):
    uri = models.TextField(default=None, blank=True, null=True)
    text = models.TextField(default=None, blank=True, null=True)
    duration = models.FloatField(default=None, blank=True, null=True)
    sample_rate = models.IntegerField(default=None, blank=True, null=True)
    sample_fmt = models.TextField(default=None, blank=True, null=True)
    channel_layout = models.TextField(default=None, blank=True, null=True)

    def _str_(self):
        return self.uri
