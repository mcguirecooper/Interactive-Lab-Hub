import time
import board
from vosk import Model, KaldiRecognizer
import subprocess
import os
import sys
import wave
import json
import board
import random

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

user_word = "user.wav"
model = Model("model")

def speak(instruction):
    comm  = """
    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
    say " """ + str(instruction) +  """ "
    """
    subprocess.call(comm, shell=True)

def wrong_mess():
    speak("What was that? I didn't get it!")

def record_user_word():
    subprocess.call("arecord -D hw:2,0 -f cd -c1 -r 44100 -d 5 -t wav " + user_word, shell=True)

def recognize(pattern):
    wf = wave.open(user_word, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
   
    rec = KaldiRecognizer(model, wf.getframerate(), pattern)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print("Result:", res['text'])
            return res['text']
    print("Failed to recognize")
    return ""

speak("Welcome to the Cornell Tech coronavirus information hotline. Are you calling for yourself? Yes or No.")
while True:
    record_user_word()
    ans = recognize('["yes no", "[unk]"]')
    if ans != "":
        speak("Thank you for calling.")
        break
    wrong_mess()
    speak("You still there?")

speak("If you would like information regarding the coronavirus exposure risk level in your area, please state your five digit zip code. Otherwise, respond no.")
while True:
    record_user_word()
    ans = recognize('["oh one two three four five six seven eight nine zero no", "[unk]"]')
    if "no" in ans:
        break
    else: 
        print(ans)
        speak("Is " + ans + " correct?")
        record_user_word()
        ans = recognize('["yes no", "[unk]"]')
        if ans != "":
            response = ["Your area currently has a high risk of infection","Your area currently has a low risk of infection"]
            ran = random.randint(0,len(response)-1)
            line = response[ran]
            speak(line)
            break
    wrong_mess()
    speak("You still there?")

speak("Are you up to date with your coronavirus vaccinations? Yes or no.")
while True:
    record_user_word()
    ans = recognize('["yes no", "[unk]"]')
    if "yes" in ans:
        speak("Very good.")
        break
    elif "no" in ans:
        break
    wrong_mess()
    speak("You still there?")

speak("What is your age?")
while True:
    record_user_word()
    ans = recognize('["teen twenty thirty forty fifty sixty sevety eighty ninety hundred", "[unk]"]')
    if ans != "":
        speak("Thank you.")
        break
    wrong_mess()
    speak("You still there?")

speak("What was your sex assigned at birth?")
while True:
    record_user_word()
    ans = recognize('["male man boy female woman girl other prefer not say", "[unk]"]')
    if ans != "":
        speak("Thank you.")
        break
    wrong_mess()
    speak("You still there?")

speak("Are you currently experiencing any of the following symptoms? Trouble breathing, chest pain, \
new or worsening confusion, inability to wake or stay awake, pale or blue skin. Yes or no.")
while True:
    record_user_word()
    result = recognize('["yes no", "[unk]"]')
    if "yes" in result:
        speak("Please call your local hospital emergency services immediately!")
        speak("Thank you for calling the Cornell Tech coronavirus information hotline. Goodbye")
        sys.exit("Call ended")
    if "no" in result:
        break
    wrong_mess()
    speak("You still there?")

speak("Have you experienced any of the following symptoms in the past five days? After each, please say yes if true.")
symptoms = ['fever',
    'increased difficulty breathing',
    'chest pain',
    'coughing',
    'sore throat',
    'congestion',
    'headache',
    'muscle aches',
    'fatigue',
    'nausea',
    'loss of smell or taste']
count = 0
for sym in symptoms:
    speak(sym)
    while True:
        record_user_word()
        result = recognize('["yes no", "[unk]"]')
        if "yes" in result:
            count += 1
            break
        if "no" in result:
            break
        wrong_mess()
if count > 1:
    speak("Based on your responses, you present symptoms of coronavirus. Please isolate immediately. Your response and phone number have been added to our records. We will contact you if necessary.")        
else:
    speak("Based on your responses, you show no symptoms of coronavirus. Please isolate and call again if there are developments.")

speak("Thank you for calling the Cornell Tech coronavirus information hotline. Goodbye")