import requests
from bs4 import BeautifulSoup
import os
import keys

# Voices for speech kit
voices = {"male": "zahar",
          "female": "oksana"}

class Assistant:

    def __init__(self, voice): # initialize assistant with voice from dict voices
        self.voice = voice

    def weather(self, city): # Yandex can't give Weather Api for you if you're not an organization. So, we can scrap the weather page.
        page = requests.get("https://yandex.ru/pogoda/search?request={}".format(city.lower())) # Download this page

        try: # This is for search field (Just pass this, but don't delete)
            soup = BeautifulSoup(page.content, "html.parser")

            page = requests.get("https://yandex.ru" + soup.find_all("a", class_="link place-list__item-name")[0]['href'])
        except Exception:
            pass
        try: # Trying to scrap page with weather
            soup = BeautifulSoup(page.content, "html.parser")

            info = [soup.find(class_="title title_level_1").text, soup.find(class_="temp__value").text,
                    soup.find(class_="fact__condition day-anchor i-bem").text]
            print(info)
            return ", ".join(info)
        except Exception: # If we can't scrap, return sorry phrase. 
            return "Простите, но я не могу посмотреть погоду для этого региона..." # "Sorry, but I can't show the weather for this region"

    def speak(self, speech, emotion="good"): # Speak function for Speech Kit. Takes two arguments with text to speak and emotion.
        file = open("response.mp3", "wb")
        file.write(requests.get("https://tts.voicetech.yandex.net/generate?text={}&format=mp3&lang=ru-RU&speaker={}&emotion={}&key={}".format(speech, self.voice, emotion, keys.speechKey)).content) # Downloading content with voice
        file.close()

        os.system("mpg321 response.mp3") # Playing this file

    def change_voice(self): # Change voice function for quick change from one voice to another
        self.voice = "oksana" if self.voice == "zahar" else "zahar"
        

