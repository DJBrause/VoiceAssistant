# pip install SpeechRecognition pydub
# pip install pyaudio
import speech_recognition as sr
import pyaudio


def speech_to_text():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        # audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        try:
            # text = r.recognize_google(audio_data)
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            print(e)
