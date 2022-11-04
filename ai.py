# pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
# pip install transformers
# documentation
# https://huggingface.co/docs/transformers/model_doc/blenderbot
# available pre-trained models
# https://huggingface.co/models?sort=downloads&search=blender

# import model and tokenizer
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import STT as stt
import TTS as tts
import weather_module as wf
import re
from time import sleep
import spotify_module as sp
import wikipedia_module as wiki
from datetime import datetime
import dice_roller as dr
import random

class Main:
    def __init__(self):
        # Download and setup model and the tokenizer
        # facebook/blenderbot-3B
        # facebook/blenderbot-400M-distill
        self.tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
        self.model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
        self.CLEANR = re.compile('<.*?>')
        self.bots_name = 'Rebecca'
        self.bot_active = False
        self.activation_keyword = "activate"
        self.deactivation_keyword = "deactivate"
        self.play_song_keywords = ["play", "song"]
        self.stop_song_keywords = ["stop", "pause"]
        self.next_song_keywords = ["next", "song"]
        self.previous_song_keywords = ["previous", "song"]
        self.current_time_keywords = ["current", "now", "present", "what", "what's"]
        self.playlist_selection_keywords = ["select", "playlist"]
        self.stop_thread_keywords = ["stop", "shut"]
        self.weather_forecast_keywords = ["weather", "forecast"]
        self.resume_keyword = "resume"
        self.search_keyword = "search"
        self.quit = False
        self.play_song_enabled = False
        self.empty_input_counter = 0
        self.utterance = "None"
        self.keyword_detected = False
        self.song_paused = False
        self.search_keyword_mentioned = False
        self.spotify_playlists = None
        self.kill_thread = False
        self.city_name = None
        self.forcast_for_today = False
        self.full_forecast = False

    def cleantags(self, text):
        cleantext = re.sub(self.CLEANR, '', text)
        return cleantext

    def playlist_selection(self, playlist_name):
        # List of playlist names
        try:
            self.spotify_playlists = sp.get_playlists()
            uri = self.spotify_playlists[playlist_name]
            sp.select_playlist(uri)
        except Exception as e:
            print(e)

    def play_playlist_called(self, utterance):
        playlist_found = False
        playlist_name = None
        split_utternace = utterance.split()
        # List of playlist names
        playlist_names = list(sp.get_playlists().keys())
        print(split_utternace)
        for title in playlist_names:
            for word in split_utternace:
                lower_title = title.lower()
                if lower_title.find(word.lower()) > -1 and playlist_found is False:
                    print(f"The title is {title}")
                    playlist_name = title
                    playlist_found = True

        self.playlist_selection(playlist_name)

    def ask_for_location(self):
        print("Please specify city:")
        tts.text_to_speech("Please specify a city")
        utterance = stt.speech_to_text()
        self.city_name = utterance

    def keyword_detection(self, text):
        name_mentioned = False
        play_keyword_mentioned = False
        song_keyword_mentioned = False
        volume_mentioned = False

        split_text = text.split()
        for i in split_text:
            stripped_i = i.strip()
            if stripped_i == self.bots_name or stripped_i == self.bots_name.lower():
                name_mentioned = True

            ################################# Activates the bot ############################
            if name_mentioned and stripped_i == self.activation_keyword:

                self.bot_active = True
                self.empty_input_counter = 0
                tts.text_to_speech("Hello, I am now active")
                self.keyword_detected = True

            ############################### Deactivates the bot ############################
            if name_mentioned and stripped_i == self.deactivation_keyword:
                self.bot_active = False
                self.empty_input_counter = 5
                tts.text_to_speech("Sleep mode on")
                self.keyword_detected = True

            ##########################Playlist functions test###############################

            if stripped_i == 'playlist':
                self.keyword_detected = True
                print("Say a playlist title:")
                tts.text_to_speech("Say a playlist title:")
                utternance = stt.speech_to_text()
                self.play_playlist_called(utternance)

            ################ Activates song selection in the main loop #####################
            if stripped_i == self.play_song_keywords[0]:
                play_keyword_mentioned = True

            if stripped_i == self.play_song_keywords[1]:
                song_keyword_mentioned = True

            ################ Pause the song or stops AI from talking #######################
            if stripped_i == self.stop_song_keywords[0] or stripped_i == self.stop_song_keywords[1]:
                if self.song_paused is False:
                    try:
                        self.keyword_detected = True
                        tts.terminate_process()
                        sp.pause_song()
                        self.song_paused = True
                        self.keyword_detected = True
                        break
                    except Exception as e:
                        print(e)

                else:
                    try:
                        self.keyword_detected = True
                        tts.terminate_process()
                    except Exception as e:
                        print(e)

            ################################################################################

            if play_keyword_mentioned and song_keyword_mentioned:
                self.play_song_enabled = True
                self.song_paused = False
                tts.text_to_speech("What song do you want me to play?")
                break
            ################################################################################

            # Song pause/resume
            if stripped_i == self.resume_keyword:
                if self.song_paused is True:
                    sp.resume_song()
                    self.song_paused = False
                    self.keyword_detected = True
                    break

            if stripped_i == "song":
                for s in split_text:
                    stripped_s = s.strip()
                    if stripped_s == self.next_song_keywords[0]:
                        sp.next_song()
                        self.keyword_detected = True
                    if stripped_s == self.previous_song_keywords[0]:
                        sp.previous_song()
                        self.keyword_detected = True

            ############################## Weather Forecast ################################

            if stripped_i == self.weather_forecast_keywords[0] or stripped_i == self.weather_forecast_keywords[1]:
                self.keyword_detected = True
                for t in split_text:
                    if t == "today":
                        if self.city_name is None:
                            self.forcast_for_today = True
                            self.ask_for_location()
                if self.city_name is None and self.forcast_for_today is False:
                    self.ask_for_location()
                elif self.city_name == "error":
                    print("I didn't quite get that. Please try again.")
                    tts.text_to_speech("I didn't quite get that. Please try again.")
                elif self.city_name is not None and self.forcast_for_today is True:
                    try:
                        print(f"Forecast for city: {self.city_name}")
                        forecast_list = wf.three_day_forecast(self.city_name)
                        forcast_for_today = forecast_list[0]
                        forcast_for_today_joined = '. '.join(forcast_for_today)
                        print(forcast_for_today_joined)
                        tts.text_to_speech(str(forcast_for_today_joined))
                        self.city_name = None
                        break
                    except Exception as e:
                        tts.text_to_speech("Sorry, I didn't quite get that.")
                        self.city_name = None
                        print(e)
                        break

                elif self.city_name is not None:
                    try:
                        final_list = []
                        print(f"Forecast for city: {self.city_name}")
                        forecast_list = wf.three_day_forecast(self.city_name)
                        for f in forecast_list:
                            joint_inner_list = '. '.join(f)
                            final_list.append(joint_inner_list)
                        joint_final_list = '. '.join(final_list)
                        print(joint_final_list)
                        tts.text_to_speech(str(joint_final_list))
                        self.city_name = None
                        break
                    except Exception as e:
                        tts.text_to_speech("Sorry, I didn't quite get that.")
                        self.city_name = None
                        print(e)

            ############################# Wikipedia search ###############################

            if stripped_i == self.search_keyword:
                self.search_keyword_mentioned = True
                tts.text_to_speech("What term would you like me to search for?")
                self.keyword_detected = True
                break

            ############################# Dice roller ####################################

            if stripped_i == "roll":
                dice = None
                for y in split_text:
                    if y == "die":
                        self.keyword_detected = True
                        roll = random.randint(1, 6)
                        tts.text_to_speech(f"The result is {roll}")
                        break

                    if y == "dice" or y == "dices":
                        self.keyword_detected = True
                        for z in split_text:
                            if z == "two":
                                dice = 2
                                break
                            elif z == "three":
                                dice = 3
                                break
                            elif z == "four":
                                dice = 4
                                break
                            elif z == "five":
                                dice = 5
                                break
                            elif z == "six":
                                dice = 6
                                break
                            elif z == "seven":
                                dice = 7
                                break
                            elif z == "eight":
                                dice = 8
                                break
                            elif z == "nine":
                                dice = 9
                                break
                            else:
                                try:
                                    dice = int(z)
                                except ValueError:
                                    message = "I'm sorry, if you wanted me to roll dice I didn't quite get how many."
                                    print(message)
                                    tts.text_to_speech(message)

                    if dice is not None:
                        results = dr.roll_dice(dice)
                        end_result = {}
                        message = "Roll results are: "
                        for r in results:
                            if results[r] != 0:
                                end_result[r] = results[r]
                        for m in end_result:
                            message = message + m + " " + str(end_result[m]) + ". "

                        tts.text_to_speech(message)


            # Gives the current time
            if stripped_i == "time":
                answer_already_given = False
                for y in split_text:
                    for z in self.current_time_keywords:
                        if y == z and answer_already_given is False:
                            now = datetime.now()
                            current_time = now.strftime("%H:%M")
                            response = f"It is {current_time}"
                            print(response)
                            tts.text_to_speech(response)
                            self.keyword_detected = True
                            answer_already_given = True
                            break

            # Gives the current date
            if stripped_i == "day" or stripped_i == "date":
                answer_already_given = False
                for y in split_text:
                    for z in self.current_time_keywords:
                        if y == z and answer_already_given is False:
                            now = datetime.now()
                            current_time = now.strftime("%A %B %d")
                            response = f"It is {current_time}"
                            print(response)
                            tts.text_to_speech(response)
                            self.keyword_detected = True
                            answer_already_given = True
                            break

            # Spotify volume control
            if stripped_i == "volume":
                volume_mentioned = True
                self.keyword_detected = True

            if volume_mentioned:
                for y in split_text:
                    stripped_y = y.strip()
                    if stripped_y == "increase":
                        sp.change_volume(20)
                        break
                    if stripped_y == "decrease":
                        sp.change_volume(-20)
                        break

    def main_loop(self):
        print("Say 'quit' to end the program. \n")
        while self.quit is not True:
            print("Speak:")
            utternance = stt.speech_to_text()
            print(utternance)

            if self.play_song_enabled and utternance is not None:
                self.empty_input_counter = 0
                sp.play_song(utternance)
                self.play_song_enabled = False
                utternance = "None"

            if self.search_keyword_mentioned and utternance is not None:
                self.empty_input_counter = 0
                try:
                    tts.text_to_speech(wiki.search_in_wikipedia(utternance))
                    utternance = "None"
                    self.search_keyword_mentioned = False
                except Exception as e:
                    tts.text_to_speech("There was an error.")
                    print(e)
                    self.search_keyword_mentioned = False

            if utternance is not None:
                self.keyword_detection(utternance)

                if utternance.strip() == 'quit':
                    self.quit = True
                    print("Goodbye!")
                    tts.text_to_speech("goodbye")
                    break

            else:

                self.empty_input_counter += 1
                if self.empty_input_counter == 10:
                    self.bot_active = False
                    tts.text_to_speech("No input detected. Sleep mode on.")

            # Blenderbot
            if utternance != "None" and self.bot_active and self.keyword_detected is False and self.play_song_enabled is False:
                # tokenize the utterance
                self.empty_input_counter = 0
                try:
                    inputs = self.tokenizer(utternance, max_length=128, truncation=True, return_tensors="pt")
                    res = self.model.generate(**inputs)
                    answer = self.tokenizer.decode(res[0])
                    #  Passing throught the utternances to the Blenderbot model
                    clean_answer = self.cleantags(answer)
                    print(f"Reply: {clean_answer}")
                    tts.text_to_speech(clean_answer)
                except Exception as e:
                    print(e)

                # Decoding the inputs
                # print(tokenizer.decode(inputs['input_ids'][0]))

            else:
                sleep(.3)
                self.keyword_detected = False
                self.kill_thread = False


if __name__ == "__main__":
    program = Main()
    program.main_loop()
