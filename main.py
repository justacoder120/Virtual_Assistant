import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
from playsound import playsound
from time import sleep


class Assistant:
    def __init__(self):
        self.agree = ["yes","go ahead", "sure", "yup", "yeah","i agree", "ok"]
        self.disagree = ["no", "never","don't", "stop","i disagree"]
        self.stop = ["break", "that's it", "i'm done", "you may stop now", "stop"]
        self.one_or_two = []
        self.repeat = ["sorry i couldn't hear you. can you say that again.", "couldn't hear that.", "i didn't understand."]
        self.repeat_index = 0
        self.name = "the assistant that u have not give a name"
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[0].id)
        self.talk(f"Hey i'm your virtual assistant.")
        self.talk("let's start by setting my perameters.")
        self.change_voice()
        self.talk("cool. now let's set my name")
        self.change_name()
        self.talk(f"Awsome. my name is {self.name} and this is my voice.")
        self.run()
    def talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
    def listen(self):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                try:
                    playsound("waiting_for_input_indicator.wav")
                    voice = listener.listen(source,phrase_time_limit=3)
                    command = listener.recognize_google(voice)
                    break
                except sr.UnknownValueError:
                    self.noanswer()
                    continue
            if command not in self.stop:
                return command
    def change_voice(self):
        self.engine.setProperty("voice", self.voices[0].id)
        self.talk("do you prefer this voice?")
        self.engine.setProperty("voice", self.voices[1].id)
        self.talk("or this voice?")
        self.talk("say 1 or 2 to choose.")
        while True:
            command = self.listen()
            if command == None:
                self.talk(self.repeat[self.repeat_index])
                self.repeat_index = self.repeat_index + 1 if self.repeat_index < len(self.repeat) -1 else 0
                continue
            if "one" in command or "1" in command:
                self.engine.setProperty("voice", self.voices[0].id)
                break
            elif "two" in command or "2" in command:
                self.engine.setProperty("voice", self.voices[1].id)
                break
            else:
                self.talk("u can onlu say 1 or 2.")
    def change_name(self):
        self.talk("what do you want to call me?")
        command = self.listen()
        while True:
            self.talk(f"do you want to call me {command}?")
            yes_no = self.yes_or_no()
            if yes_no:
                self.name = command
                break
            else:
                self.talk("what do you want to call me")
                command = self.listen()       
    def google_search(self,text):
        text = text.lower().replace("on google","").replace("search for ", "")
        self.talk(f"searching for {text} on google")
        pk.search(text)
    def yes_or_no(self):
        while True:
            yes_or_no1 = self.listen()
            if yes_or_no1 in self.agree:
                return True
            elif yes_or_no1 in self.disagree:
                return False
            else:
                self.noanswer()
    def noanswer(self):
        self.talk(self.repeat[self.repeat_index])
        self.repeat_index = self.repeat_index + 1 if self.repeat_index < len(self.repeat) -1 else 0
    def run(self):
        while True:
            self.talk("what can i do for you")
            command = self.listen()
            if not command:
                self.talk(f"{self.name} thanks you alot for using the alpha version of this assistant.")
                break
            
            if "your name" in command and "change" in command:
                self.talk("Do want to change my name?")
                if self.yes_or_no():
                    self.change_name()
                else:
                    self.talk(f"i'm keeping my name which is {self.name}.")
            elif "your voice" in command and "change" in command:
                self.talk("Do want to change my voice?")
                if self.yes_or_no():
                    self.change_voice()
                else:
                    self.talk(f"i'm keeping my voice which is the one that your hearing")
            
            elif "your name" in command:
                self.talk(f"my name is {self.name}")

            elif "google" in command or "search" in command:
                self.google_search(command)
                break

            else:
                print(command)
                self.talk(f"The command {command}is not supported yet.")
    

assistant = Assistant()