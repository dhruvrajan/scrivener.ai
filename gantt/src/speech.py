import speech_recognition as sr
from gantt_parser import gantt_main
r = sr.Recognizer()
with sr.Microphone() as source:                # use the default microphone as the audio source
    print("got mic, getting audio ... Please be patient.")
    audio = r.listen(source, .5)
    print("got audio")
    # listen for the first phrase and extract it into audio data

while True:
    try:
        text = r.recognize_google(audio)
        print("You said: " + r.recognize_google(audio))    # recognize speech using Google Speech Recognition

        with open("in.txt", "w") as f:
            f.write(text)

        gantt_main()
        break
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio, please try a again")
        continue
    except:
        print("Failed to load audio")
        break