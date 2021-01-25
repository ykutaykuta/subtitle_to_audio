import json
import requests
import os.path
from pathlib import Path
import sys
from time import sleep
import pyttsx3
from gtts import gTTS
import io
from api import GTTS, FFMPEG, FFPROBE
from subprocess import Popen
import subprocess


dirname = os.path.dirname(__file__)
ffprobe_get_duration = '{} -i {} -show_entries format=duration -v quiet -of csv="p=0"'
ffmpeg_filter = '{} -i {} -filter_complex "[0:a]atempo={}[p0];[p0]aresample={}:osf={}:ocl={}[p1]" -map "[p1]" {}'

def pyttsx3_packet(text: str):
    engine = pyttsx3.init(driverName="sapi5")  # object creation

    """ RATE"""
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    print(rate)  # printing current voice rate
    # engine.setProperty('rate', 125)  # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    print(volume)  # printing current volume level
    # engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')  # getting details of current voice
    for voice in voices:
        print("voice: ", voice.id, voice.age, voice.name, voice.gender, voice.languages)
        if voice.id == "vietnam_sgn":
            engine.setProperty('voice', voice.id)  # changing index, changes voices. 1 for female
            break

    engine.say(text.encode())
    engine.runAndWait()
    engine.stop()

    """Saving Voice to a file"""
    # On linux make sure that 'espeak' and 'ffmpeg' are installed
    engine.save_to_file('Hello World', 'test.mp3')
    engine.runAndWait()


def gtts_packet(text: str, audio: str, duration: float, sr: int, sf: str, cl: str):
    tts = gTTS(text, lang="vi", slow=False, lang_check=False)
    uri_tmp = os.path.join(Path(GTTS), "tmp")
    uri = os.path.join(Path(GTTS), audio + ".aac")
    # if not os.path.exists(uri_tmp):
    #     tts.save(uri_tmp)
    tts.save(uri_tmp)
    cmd = ffprobe_get_duration.format(FFPROBE, uri_tmp)
    p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
    output, errors = p.communicate(timeout=1.0)
    if None == errors:
        rate = float(output)/duration
        if rate < 0.50:
            rate = 0.50
        if rate > 100.00:
            rate = 100.00
        cmd = ffmpeg_filter.format(FFMPEG, uri_tmp, rate, sr, sf, cl, uri)
        p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
        output, errors = p.communicate(timeout=1.0)
        print(output)
        if not os.path.exists(uri):
            os.rename(uri_tmp, uri)
    return uri


def viettel_api(text: str):
    # Viettel tts api
    # cert_path = os.path.join(Path(dirname), 'tts.crt')
    # # url = "https://viettelgroup.ai/voice/api/asr/v1/rest/decode_file"
    # url = "https://vtcc.ai/voice/api/tts/v1/rest/syn"
    # data = {
    #     "text": "Đây là chương trình demo tổng hợp tiếng nói của trung tâm không gian mạng",
    #     "voice": "doanngocle",
    #     "id": "2",
    #     "without_filter": False,
    #     "speed": 1.0,
    #     "tts_return_option": 2
    # }
    # headers = {
    #     'Content-type': 'application/json',
    #     'token': 'hnl6vnxBy57wk8dfm7CgcSa64WYqMJJ1H3eATJP39kfvMhcqUnRJIkU2t5-DuTQ5'
    #     # 'sample_rate': 16000,
    #     # 'format':'S16LE',
    #     # 'num_of_channels':1,
    #     # 'asr_model': 'model code'
    # }
    # s = requests.Session()
    # response = requests.post(url, data=json.dumps(data), headers=headers, verify=cert_path)
    #
    # print(response.headers)
    # # Get status_code
    # print(response.status_code)
    # with open(audio_path, "wb+") as f:
    #     f.write(response.content)
    return 0;


def fpt_api(text: str):
    # FPT tts api
    # url = 'https://api.fpt.ai/hmi/tts/v5'
    # payload = 'Phần lớn thời gian'
    # headers = {
    #     'api-key': 'u5avLwV5HbS8RHxC2JbtYjmruinhYR3m',
    #     'speed': '',
    #     'voice': 'banmai'
    # }
    # response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
    # res_json = json.loads(response.text)
    # print(res_json)
    # response = requests.get(res_json["async"], allow_redirects=True)
    # retry = 3
    # while response.status_code == 404 and retry > 0:
    #     response = requests.get(res_json["async"], allow_redirects=True)
    #     retry = retry - 1
    #     sleep(0.3)
    # if response.status_code == 404:
    #     return -1
    # with open(audio_path, "wb+") as f:
    #     f.write(response.content)
    return 0


# def main(argv):
#     audio_path = os.path.join(Path(dirname), str(argv[1]) + ".wav")
#     text = "Đây là chương trình demo tổng hợp tiếng nói của trung tâm không gian mạng"
#
#     gTTS_Packet(text)
#     # Pyttsx3_Packet(text)
#     return 0

