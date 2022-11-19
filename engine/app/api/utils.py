import random
from gtts import gTTS
from settings import settings
import uuid
from pathlib import Path


def get_random_words(list_id):
    l = random.sample(list_id, len(list_id))
    return l


def text_to_audio(text, lang):
    listen = gTTS(str(text), lang=str(lang))
    hashik = str(uuid.uuid4())
    audio_name = f'{hashik[:2]}/{hashik[2:4]}/{hashik}.ogg'
    full_path = f'{settings["file_path"]}/{audio_name}'
    Path(f'{settings["file_path"]}/{hashik[:2]}/{hashik[2:4]}').mkdir(parents=True, exist_ok=True)
    listen.save(full_path)
    return audio_name