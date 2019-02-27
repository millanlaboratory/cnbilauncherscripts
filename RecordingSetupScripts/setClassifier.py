import argparse
from appJar import gui
import getpass
import sys
from os import walk
import xml.etree.ElementTree as ET
import shutil


global app 
global data
global dataDouble
global dataSingle
global fileName


parser = argparse.ArgumentParser()
parser.add_argument("--modality", help="For which modality you are setting classifier path", required = True)
parser.add_argument("--subject",    help="For which subject you are setting classifier path", required = True)
parser.add_argument("--session",    help="For which session you are setting classifier path", required = True)
parser.add_argument("--taskset",    help="For which tasket you are setting threshold values", required = True)


args, unknown = parser.parse_known_args()
modality = args.modality
subject = args.subject
session = args.session
taskset = args.taskset

user = getpass.getuser()
path = "/home/" + user + "/data/" + subject + "/"
pathToSession = "/home/" + user + "/data/" + subject + "/" + session + "/"
xmlFile = pathToSession + "mi_stroke_prot.xml"

def chooseClassifier(button):
    global app
    if button == "Validate":
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        root.find('classifier').find('kmi2').find('filename').text = app.getRadioButton("classifier")
        tree.write(xmlFile)
        shutil.copyfile(path + app.getRadioButton("classifier"), pathToSession + app.getRadioButton("classifier"))
        app.showSubWindow('Threshold')
        app.hide()
    elif button == "Cancel":
        print(str(-1))
        app.stop()

def chooseValues(button):
    global app
    if button == "Set":
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        tasksets = root.find('online').find('mi').findall('taskset')
        movementClass = taskset.replace('_fes','')
        for task in tasksets:
            if task.attrib['ttype'] == taskset:
                task.find('threshold').find(movementClass).text = str(app.getEntry("Threshold Movement")) if app.getEntry("Threshold Movement") is not None else task.find('threshold').find(movementClass).text
                task.find('threshold').find('mi_rest').text = str(app.getEntry("Threshold Rest")) if app.getEntry("Threshold Rest") is not None else task.find('threshold').find('mi_rest').text
        tree.write(xmlFile)
    elif button == "Exit":
        print(str(-1))
    app.stop()

if modality == "online":
    user = getpass.getuser()
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            if ".mat" in filename and ".smr.mat" not in filename:
                f.append(filename)
        break

    # # # app.go
    sys.argv = [sys.argv[0]];
    padding = 10;
    app=gui()
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    app.startSubWindow("Threshold")
    app.setGuiPadding(padding, padding)
    app.addLabelNumericEntry("Threshold Movement")
    app.addLabelNumericEntry("Threshold Rest")
    tasksets = root.find('online').find('mi').findall('taskset')
    movementClass = taskset.replace('_fes','')
    for task in tasksets:
        if task.attrib['ttype'] == taskset:
            app.setEntryDefault("Threshold Movement", task.find('threshold').find(movementClass).text)
            app.setEntryDefault("Threshold Rest", task.find('threshold').find('mi_rest').text)
    app.addButtons(["Set", "Exit"], chooseValues)
    app.setLocation(500, 450)
    app.stopSubWindow()


    app.setGuiPadding(padding, padding)
    for filename in f:
        app.addRadioButton("classifier", filename)
    app.addButtons(["Validate", "Cancel"], chooseClassifier)
    app.setLocation(500, 450)
    app.go()
