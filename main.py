import speech_recognition as sr
from logging.config import listen
import pyttsx3
from datetime import datetime
import wikipedia
import webbrowser
import wolframalpha

# speech recognition initialization

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voice[0].id')  # 0 = male, 1 = female
activationWord = 'computer'

# browser configuration
# setting the path
chrome_path = "/Applications/Google Chrome.app"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# wolfram alpha client
appId = 'K9HG67-HRKL6ELGH7'
wolframClient = wolframalpha.Client(appId)

def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
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
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia results')
        return 'No results received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)

    if response['@success'] == 'false':
        return 'could not compute'

    # query resolved
    else:
        result = ''
        # question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        # may contain the answer, has the highest confidence value
        # if it's primary, or has the title of result or definition, then it's the official result
        if ('result' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listOrDict(pod1['sub-pod'])
            # remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['sub-pod'])
            return question.split('(')[0]
            # search wikipedia instead
            speak('computation failed, querying universal databank')
            return search_wikipedia(question)


# main loop

if __name__ == '__main__':
    speak('All systems nominal.', 120)

    while True:
        # parsing as list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # list commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all! ')
                else:
                    query.pop(0)  # remove say
                    speech = ' '.join(query)
                    speak(speech)

            # web navigation
            if query[0] == 'go' and query[1] == 'to' :
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank.')
                speak(search_wikipedia(query))

            # wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')

                try:
                    search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('unable to compute')


            # recording notes
            if query[0] == 'log':
                speak('ready to record your notes')
                newNote = parseCommand().lower()
                now datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

                with open('note_%s.txt' % now, w) as newFile:
                    newFile.write(newNote)
                    speak('note written')

            if query[0] == 'exit':
                speak('Good bye')
                break
