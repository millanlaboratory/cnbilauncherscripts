import argparse
from appJar import gui
from screeninfo import get_monitors
import json
import getpass
import sys

global app 
global data
global dataDouble
global dataSingle
global fileName

parser = argparse.ArgumentParser()
parser.add_argument("--task", help="For which task you are setting FES values", required = True)
parser.add_argument("--subject", 	help="For which subject you are setting FES values", required = True)

args, unknown = parser.parse_known_args()
task = args.task.split("_") #split string into a list
task = task[len(task)-1]
subject = args.subject

def chooseValues(button):
 	global app
 	if button == "Validate":
 		valid = True
 		if app.getEntry("Max stim biceps") < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if app.getEntry("Max stim forearm") < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if valid:
 			data["sequence"][0]["currentIncrementerParameters"][1] = app.getEntry("Max stim biceps") if app.getEntry("Max stim biceps") != 0 else data["sequence"][0]["currentIncrementerParameters"][1]
	 		data["sequence"][1]["currentIncrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") != 0 else data["sequence"][1]["currentIncrementerParameters"][1]
	 		data["sequence"][0]["currentDecrementerParameters"][1] = app.getEntry("Max stim biceps") if app.getEntry("Max stim biceps") != 0 else data["sequence"][0]["currentDecrementerParameters"][1]
	 		data["sequence"][1]["currentDecrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") != 0 else data["sequence"][1]["currentDecrementerParameters"][1]
	 		dataDouble["sequence"][1]["current"] = app.getEntry("Sensory stim biceps") if app.getEntry("Sensory stim biceps") != 0 else dataDouble["sequence"][1]["current"]
	 		dataDouble["sequence"][0]["current"] = app.getEntry("Sensory stim forearm") if app.getEntry("Sensory stim forearm") != 0 else dataDouble["sequence"][0]["current"]
	 		dataSingle["sequence"][0]["current"] = app.getEntry("Sensory stim forearm") if app.getEntry("Sensory stim forearm") != 0 else dataDouble["sequence"][0]["current"]
	 		with open(fileName, 'w') as outfile:
	 			json.dump(data, outfile, indent=4)
	 		with open(path + "/lowStimDouble.json", 'w') as f:
	 			json.dump(dataDouble, f, indent=4)
	 		with open(path + "/lowStimSingle.json", 'w') as f:
	 			json.dump(dataSingle, f, indent=4)
 	elif button == "Cancel":
 		print(str(-1))
 		
 	app.stop()

user = getpass.getuser()
path = "/home/" + user + "/data/" + subject + "/resources"
fileName = path + "/" + task + ".json"
with open(fileName, 'r') as f:
 	data = json.load(f)
with open(path + "/lowStimDouble.json", 'r') as f:
 	dataDouble = json.load(f)
with open(path + "/lowStimSingle.json", 'r') as f:
	dataSingle = json.load(f)

# # app.go
sys.argv = [sys.argv[0]];
app=gui()
padding = 10;
app.setGuiPadding(padding, padding)
app.addLabelNumericEntry("Max stim biceps")
app.addLabelNumericEntry("Max stim forearm")
app.addLabelNumericEntry("Sensory stim biceps")
app.addLabelNumericEntry("Sensory stim forearm")
app.setEntryDefault("Max stim biceps", data["sequence"][0]["currentIncrementerParameters"][1])
app.setEntryDefault("Max stim forearm", data["sequence"][1]["currentIncrementerParameters"][1])
app.setEntryDefault("Sensory stim biceps", dataDouble["sequence"][0]["current"])
app.setEntryDefault("Sensory stim forearm", dataDouble["sequence"][1]["current"])

app.addButtons(["Validate", "Cancel"], chooseValues)
app.setLocation(get_monitors()[0].width/2, get_monitors()[0].height/2)

app.go()
