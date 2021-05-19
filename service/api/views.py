import base64
import socket

from django.shortcuts import render
from rest_framework import viewsets
from api import function
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from .models import TTSAudio
from .serializers import TTSAudioSerializer
import os
import time
import json
from PIL import Image

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


@api_view(["POST"])
def ocr(request):
    texts = list()
    data = json.loads(request.body)
    rects = data["rects"]

    # process image
    x_min = 1000
    x_max = 0
    y_min = 1000
    y_max = 0
    for rect in rects:
        x_min = min(x_min, rect["x"])
        y_min = min(y_min, rect["y"])
        x_max = max(x_max, rect["x"] + rect["w"])
        y_max = max(y_max, rect["y"] + rect["h"])
    image_size = (x_max - x_min, y_max - y_min)

    gray_alpha = Image.new("L", image_size)
    for rect in rects:
        x = rect["x"] - x_min
        y = rect["y"] - y_min
        w = x + rect["w"]
        h = y + rect["h"]
        nb_color = rect["nb_color"]
        image = base64.b64decode(rect["b64"])
        if nb_color <= 4:
            image = [x * 64 for x in image]
        elif nb_color <= 16:
            image = [x * 16 for x in image]
        count = 0
        for tmp_y in range(y, h):
            for tmp_x in range(x, w):
                gray_alpha.putpixel((tmp_x, tmp_y), (image[count]))
                count += 1
    image_path = os.path.abspath("tmp.png")
    gray_alpha.save(fp=image_path, format="PNG")
    # with open("tmp.png", "rb") as f:
    #     d = f.read()
    #     print("ykuta", len(image), len(d), type(d))
    d = image_path.encode()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(1.0)
    client.sendto(d, ("127.0.0.1", 5000))
    text, server = client.recvfrom(1024)
    texts.append(text.decode())
    print(texts)
    return JsonResponse({"text": texts}, json_dumps_params={'ensure_ascii': False})


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
