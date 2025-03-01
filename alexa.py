import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys

# Initialize the recognizer and the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get the available voices and set a preferred voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

def engine_talk(text):
    """Converts text to speech and speaks it out."""
    print(f"Alexa is saying: {text}")  
    engine.say(text)
    engine.runAndWait()

def user_commands():
    """Listens to the user's command and processes speech recognition."""
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Listening for command...")
            voice = listener.listen(source, timeout=5)  # Added timeout to avoid indefinite waiting
            command = listener.recognize_google(voice).lower()
            print(f"User said: {command}")  
            return command
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_alexa():
    """Processes the recognized command and responds accordingly."""
    command = user_commands()
    if command:
        if 'play' in command:
            song = command.replace('play', '').strip()
            engine_talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            engine_talk(f'The current time is {current_time}')
        elif 'who is' in command or 'what is' in command:
            query = command.replace('who is', '').replace('what is', '').strip()
            try:
                info = wikipedia.summary(query, sentences=1)
                print(info)
                engine_talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                engine_talk("Too many results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                engine_talk("I couldn't find any information on that.")
        elif 'joke' in command:
            engine_talk(pyjokes.get_joke())
        elif 'stop' in command or 'exit' in command:
            engine_talk("Goodbye!")
            sys.exit()
        else:
            engine_talk("I did not understand that. Can you repeat?")
    else:
        engine_talk("Please try speaking again.")

# Main loop to keep the assistant running
while True:
    run_alexa()
