# pip install gTTS

from gtts import gTTS
import pygame
import os
import multiprocessing
from multiprocessing import Process

pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)
# This module is imported so that we can
# play the converted audio


def terminate_process():
    processes = multiprocessing.active_children()
    for p in processes:
        p.terminate()


def load_and_play(sound_file, x):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.load("sound_file_copy.mp3")
    try:
        os.remove(sound_file)
    except Exception as e:
        print(e)


def text_to_speech(text):
    # The text that you want to convert to audio
    mytext = str(text)
    # Language in which you want to convert
    language = 'en'
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, tld='ca', slow=True)
    # Saving the converted audio in a mp3 file named "sound_file.mp3"
    sound_file = "sound_file.mp3"
    try:
        myobj.save(sound_file)
    except Exception as e:
        print(e)
    # Playing the converted file
    # pygame.mixer.music.load(sound_file)
    # pygame.mixer.music.play()

    # while pygame.mixer.music.get_busy():
    #     pass
    processes = multiprocessing.active_children()
    if len(processes) < 1:
        p1 = Process(target=load_and_play, args=(sound_file, None)) # arguments have to be provided separately, and minimum of 2 for some reason... Thus giving None as the second one.
        p1.start()
