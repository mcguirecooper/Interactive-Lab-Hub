# Chatterboxes
**NAMES OF COLLABORATORS HERE**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. 
Now, we need to find out where your webcam's audio device is connected to the Pi. Use `arecord -l` to get the card and device number:
```
pi@ixe00:~/speech2text $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Device [Usb Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
The example above shows a scenario where the audio device is at card 1, device 0. Now, use `nano vosk_demo_mic.sh` and change the `hw` parameter. In the case as shown above, change it to `hw:1,0`, which stands for card 1, device 0.  

Now, look at which camera you have. Do you have the cylinder camera (likely the case if you received it when we first handed out kits), change the `-r 16000` parameter to `-r 44100`. If you have the IMISES camera, check if your rate parameter says `-r 16000`. Save the file using Write Out and press enter.

Then try `./vosk_demo_mic.sh`

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

![Note Sep 25 2022](https://user-images.githubusercontent.com/50084830/192161434-e6668dc4-6694-47e1-829d-2db536b197b3.jpg)

Due to the volume of screenings being faced by health departments and hospital systems, there requires rudimentary diagnosis procedures in the time before patients can be examined by professionals. For those who are not aware of the stereotypical signs and symptoms of infection, a speech synthesis and response chatbot can quickly give feedback as to possible exposure. A health vocab dataset can be used to populate a decsriptive field for professionals to look at in the case of possible exposure to assess severity. 


https://user-images.githubusercontent.com/50084830/192161278-8071cf0a-1b99-4f76-8e5b-1eb619a6b90c.MOV

Based on the relative few symptoms listed, caller might need to be prompted with different categories of symptoms in order for the chatbot to get a more complete picture of the patient's health. On the other hand, callers tend to elaborate more than required in listing their symptoms with stories and experiences. A limited list of target words will need to be used to limit the info collected and passed along to health professionals.

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

Feedback: Instead of asking an open ended question like 'list your symptoms', I decided to ask each COVID symptoms individually and prompted by the chatbot. This way the caller doesn't need to know the terminology for their experience and can also avoid the narrative callers give that chatbots are not designed to handle. Also, more introductory informational questions are asked before the symptoms in order to give a more complete picture to the record produced by the call. Information of COVID in the area was added at the very beginning for callers who onl want info on prevalence in their area. Then, a emergency symptoms question was placed before the standard symptoms to save time and better instruct those extreme cases. Lastly, a printout of the answers in made for internal records and associated with the phone number who called. 

## Prototype your system

The Pi is being used here to mimic a chatbot you would interact with over a phone call. Cell service is significantly better at serving rural areas compared to a reliable internet connection. A caller would call the phone line seeking to either (1) gauge the risk of COVID in their area or (2) asses the severity of their symptoms or possible exposure to COVID. If the caller presents symptoms of COVID, a record of the call is produced that can be forwarded to any private or public healthcare system.   

![Note Sep 25, 2022](https://user-images.githubusercontent.com/50084830/193652617-ad6146ca-d03f-4e14-a0e3-8e5c823ad869.jpg)

Portions of the code structure I used in this were based on work by zw282 in last years's course. I used the helper functions created there as a starting place. 
The questions and symptoms I am asking are taken directly from the CDC's self screening checklist. 

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

https://cornellprod-my.sharepoint.com/:v:/g/personal/cjm424_cornell_edu/EYR5b2xSeENFuW7Skzh8pNIBObpOJGD1RUIQNJwhPjXrVQ?e=8D8Sye

Answer the following:

### What worked well about the system and what didn't?

The edges cases are well handled. Prompting the caller with options instead of deciphering open responses made the interaction more streamlined. I ran into issues with numerical speech-to-text recognition where certain numbers like 'one' and 'oh' were not reliably recognized. The system also has a human component to it with an introduction and conclusion, greeting and farewell. Automating was easier than anticipated but all possible branches of the dialogue had to be mapped out. 

### What worked well about the controller and what didn't?

I did not use a controller for this system. The system is autonomous as seen in the videos. 

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

I did not use a controller for this system. The system is autonomous as seen in the videos. 

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

Since the system is designed to be accessible in rural areas and thus over cellular service, there aren't many other modalities that would make sense here. Possible adding in features and interactions using the number pad would be more helpful in some cases such as your zip code or date of birth. Recording the individual responses would allow me to create a larger dataset of target words for the recognizer. Recognizing more of the vocabulary people use from different backgrounds would expand access to this systems and its value.  

