import apiai
import json
import assistant
import keys
import requests

app = apiai.ApiAI(keys.apiaiKey) # Initialize Dialogflow api (ApiAi is the old name of the service)
Assistant = assistant.Assistant(assistant.voices["female"]) # Initialize our assistant


def translate(word, lang="en"): # This function probably shoud be in assistant class, but I didn't transfered this for now. Args: Text to translete, destination language code
    response = requests.post("https://translate.yandex.net/api/v1.5/tr.json/translate",
                             {"key": keys.translatorKey, "text": word, "lang": lang}) # Requesting json from Yandex Translator
    return json.loads(response.content.decode("utf-8")) # Return response


def get_response(text): # Get response from Dialogflow. Takes text for request.
    request = app.text_request() # Init the text request
    request.lang = 'ru' # Lang of request
    request.session_id = "oosdif87g1" # Session ID should be different in different devices.
    request.query = text # Our request
    response = json.loads(request.getresponse().read().decode('utf-8')) # Reading response
    try:
        return response['result']['fulfillment']['speech'] # Returns just text!
    except Exception:
        return "Произошла ошибка, попробуйте позднее." # If we haven't got response, return sorry message. "An error has occured, try again later."


while True: # Infinite loop for texting
    speech = input("Введите запрос >>  ") # "Enter your request >> "
    response = get_response(speech) # Getting response with "speech" variable request
    print(response) # Print text for debug.
    if response.split(";")[0] == "command": # Response command;weather;Moscow. "command;..." says assistant, that it's command for him, not just talk.
        if response.split(";")[1] == "weather": # weather command
            word = translate(response.split(";")[2].replace(" ", "-"))['text'][0].replace(" ", "-")
            print("Погода", word, response.split(";")[2].replace(" ", "-"))
            Assistant.speak(Assistant.weather(word), "good")
        elif response.split(";")[1] == "translate": # translate command
            word = translate(response.split(";")[2], response.split(";")[3])['text'][0]
            print("Перевод:", word)
            Assistant.speak("Это будет. " + word)
        elif response.split(";")[1] == "change_voice": # change voice command
            Assistant.change_voice()
            Assistant.speak(response.split(";")[2], "good")
        elif response.split(";")[1] == "say": # Say command is just repeating word or phrase after you. "Say hello" and It says "Hello"
            Assistant.speak(response.split(";")[2])
        else: # If command, but It's new command and not supported by this version of assistent, speaking "This function is unavailable yet."
            Assistant.speak("Эта функция временно недоступна!")
        continue # Let the loop go forward.
    Assistant.speak(response) # If it isn't command, just speak response from Dialogflow. It's chat.

