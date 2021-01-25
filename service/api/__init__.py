import os
from pathlib import Path
import sys
from enum import Enum

class SampleFormat(Enum):
    pass

IS_LINUX = (sys.platform == "linux")

dir_path = os.path.dirname(__file__)
STORAGE_PATH = os.path.join(Path(dir_path).parent, "storage")
VIETTEL_API = os.path.join(Path(STORAGE_PATH), "viettel-api")
FPT_API = os.path.join(Path(STORAGE_PATH), "fpt-api")
PYTTSX3 = os.path.join(Path(STORAGE_PATH), "pyttsx3")
GTTS = os.path.join(Path(STORAGE_PATH), "gtts")

TOOLS_PATH = os.path.join(Path(dir_path).parent, "tools")
FFMPEG = os.path.join(Path(TOOLS_PATH), "ffmpeg")
FFPROBE = os.path.join(Path(TOOLS_PATH), "ffprobe")
