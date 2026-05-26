import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[1].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.setProperty('rate', 174)
    engine.runAndWait()
    eel.receiverText(text)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 20)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)

        speak(query)

    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input

        if not query:
            return  # Exit if no query is received

        print(query)
        eel.senderText(query)

    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)

    try:
        if query:

            if "open" in query:
                from backend.feature import openCommand  # type: ignore
                openCommand(query)

            elif "send message" in query or "call" in query or "video call" in query:

                from backend.feature import findContact, whatsApp

                flag = ""
                Phone, name = findContact(query)

                if(Phone != 0):

                    if "send message" in query:
                        flag = 'message'
                        speak("what message to send")
                        query = takecommand()

                    elif "call" in query:
                        flag = 'call'

                    else:
                        flag = 'video call'

                    whatsApp(Phone, query, flag, name)

            elif "on youtube" in query:
                from backend.feature import PlayYoutube  # type: ignore
                PlayYoutube(query)

            else:
                from backend.feature import chatBot
                chatBot(query)

        else:
            speak("No command was given.")

    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")

    eel.ShowHood()