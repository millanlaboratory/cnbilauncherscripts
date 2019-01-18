from appJar import gui
import argparse
import getpass
import os
from shutil import copyfile
import xml.etree.ElementTree as ET
import datetime
import json
global app 
global dataPath
import sys



parser = argparse.ArgumentParser()
parser.add_argument("--subject",    help="For which subject you are setting classifier path", required = True)

args, unknown = parser.parse_known_args()
subject = args.subject

def whichSession(button):
    if button == "Exit":
        print(str(-1))
        exit()
    else:
        app.showSubWindow(button)
        app.hide()
def validateSession(button):
    global app
    if button == "Validate":
        session = app.getEntry("Session")
        createPath(session)
        dataPath = "/home/" + user + "/data"
        subjectPath = dataPath + "/" + subject
        copyfile(subjectPath + "/mi_stroke_prot.xml", subjectPath + "/" + session + "/mi_stroke_prot.xml")
        app.stop()
        print(session)
    elif button == "Cancel":
        app.setEntry("Session","")
        app.hideSubWindow("New Session")
        app.show()

def chooseSession(button):
    global app
    if button == "Choose":
        user = getpass.getuser()
        session = app.getRadioButton("sessions")
        
        createPath(session)
        print(session)
        app.stop()
    elif button == "Back":
        app.hideSubWindow("Existing Session")
        app.show()

def createPath(session="calibration"):
    user = getpass.getuser()
    sessionPath = dataPath + "/" + session
    if not os.path.isdir(sessionPath):
        os.makedirs(sessionPath)

    
sys.argv = [sys.argv[0]];
user = getpass.getuser()
dataPath = "/home/" + user + "/data/" + subject
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)
onlydir = [f for f in os.listdir(dataPath) if os.path.isdir(os.path.join(dataPath, f)) and f != "resources" and f != "eegc3"]
# app.go
app=gui()
padding = 10;

# this is a pop-up
app.startSubWindow("New Session")
app.setGuiPadding(padding, padding)
app.addLabelEntry("Session")
app.getEntry("Session")
app.addButtons(["Validate", "Cancel"], validateSession)
app.setLocation(500, 450)
app.stopSubWindow()

# this is another pop-up
if len(onlydir) != 0:
    app.startSubWindow("Existing Session")
    for directory in onlydir:
        app.addRadioButton("sessions", directory)
    app.addButtons(["Choose", "Back"], chooseSession)
    app.setLocation(500, 450)
    app.stopSubWindow()
    app.addButtons(["New Session", "Existing Session", "Exit"], whichSession)
else:
    app.addButtons(["New Session", "Exit"], whichSession)
app.setLocation(500, 450)
app.go()
