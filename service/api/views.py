from django.shortcuts import render
from rest_framework import viewsets
from api import function
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from .models import TTSAudio
from .serializers import TTSAudioSerializer
import os, time


# Create your views here.

class TTSAudioView(viewsets.ModelViewSet):
    serializer_class = TTSAudioSerializer
    queryset = TTSAudio.objects.all()


@api_view(["POST"])
def gen_audio(request):
    print(str(request.data))
    serializer = TTSAudioSerializer(data=request.data)
    if serializer.is_valid():
        text = serializer.data.get("text")
        duration = float(serializer.data.get("duration"))
        sr = int(serializer.data.get("sample_rate"))
        sf = serializer.data.get("sample_fmt")
        cl = serializer.data.get("channel_layout")
        file_name = time.strftime("%Y-%m-%d_%H:%M:%S")
        uri = function.gtts_packet(text=text, audio=file_name, duration=duration, sr=sr, sf=sf, cl=cl)
        return JsonResponse({"uri": uri})
    return HttpResponseBadRequest()


@api_view(["GET"])
def list_audio(request):
    tts_audio = TTSAudio.objects.all()
    serializer = TTSAudioSerializer(tts_audio, many=True)
    return HttpResponse(serializer.data)


@api_view(["GET"])
def get_audio(request, uri):
    # tts_audio = TTSAudio.objects.get(pk=pk)
    with open(uri, "rb") as f:
        response = HttpResponse()
        response.write(f.read())
        response["Content-Type"] = "audio/aac"
        response["Content-Length"] = os.path.getsize(uri)
        return response


