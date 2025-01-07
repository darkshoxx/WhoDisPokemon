# I've been forwarded the package pyttsx3 which I want to try
import pyttsx3

engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()
# Wow that's a lot faster
