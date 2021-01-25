from rest_framework import serializers
from .models import TTSAudio


class TTSAudioSerializer(serializers.ModelSerializer):
  class Meta:
    model = TTSAudio
    fields = ["id", "text", "duration", "sample_rate", "sample_fmt", "channel_layout"]