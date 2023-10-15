from gtts import gTTS
from os import system
from time import sleep
from mutagen.mp3 import MP3


def durationOfAudioFileFromPath(path):
    audio = MP3(path)
    return audio.info.length


def generateIntruderAlertSound():
    text = "Intruder Alert!"
    language = 'en'

    myObj = gTTS(text=text, lang=language, slow=False)
    myObj.save("intruder.mp3")


def playCustomSound(text):
    language = 'en'

    myObj = gTTS(text=text, lang=language, slow=False)
    myObj.save("custom.mp3")
    system("custom.mp3")
    sleep(durationOfAudioFileFromPath("custom.mp3"))
