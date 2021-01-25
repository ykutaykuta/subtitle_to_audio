from django.contrib import admin
from .models import TTSAudio


class TTSAudioAdmin(admin.ModelAdmin):
  list_display = ("uri", "text", "duration", "sample_rate", "sample_fmt", "channel_layout")


# Register your models here.

admin.site.register(TTSAudio, TTSAudioAdmin)
