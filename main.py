import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import wolframalpha


# speech recognition initialization

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voice[0].id')  # 0 = male, 1 = female
activationWord = 'computer'


def parseCommand() :
    listener = sr.Recognizer()
    print("listening for command")

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_us')
        print(f'the input speech was: {query}')
    except Exception as exception:
        print('i did not quite catch that')

        print(exception)
        return 'None'
    return query
